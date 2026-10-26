"""Check the dark portfolio migration against real pages in Chromium.

e.g. python scripts/verify-portfolio.py --base http://127.0.0.1:4323
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class MainContent(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.pairs, self.links, self.ids, self.image_alts = [], [], [], []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "main":
            self.inside = True
        if not self.inside:
            return
        if "data-zh" in data and "data-en" in data:
            pair = (data["data-zh"], data["data-en"])
            self.pairs.append(pair)
            if "data-i18n-inline-alt" in data:
                self.image_alts.append(pair)
        if tag == "a" and "href" in data:
            self.links.append(data["href"])
        if "id" in data:
            self.ids.append(data["id"])

    def handle_endtag(self, tag):
        if tag == "main":
            self.inside = False


def preserve_content(folder):
    baseline_path = folder / "baseline.json"
    if not baseline_path.exists():
        return {"available": False}
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    current = {}
    for relative in baseline:
        parser = MainContent()
        parser.feed((REPO / "dist" / relative).read_text(encoding="utf-8"))
        current[relative] = parser
    project_alts = Counter(
        pair for path, parser in current.items()
        if path.startswith("projects/") and path != "projects/index.html"
        for pair in parser.image_alts
    )
    changes = []
    for relative, old in baseline.items():
        parser = current[relative]
        missing = Counter(map(tuple, old["pairs"])) - Counter(parser.pairs)
        # List pictures became decorative backgrounds; detail pictures retain their alt text.
        # e.g. a project row now describes the work through its title, summary and technologies.
        allowed = missing & project_alts if relative in ("index.html", "projects/index.html") else Counter()
        unexpected = missing - allowed
        assert not unexpected, (relative, "missing text", unexpected)
        assert not set(old["links"]) - set(parser.links), (relative, "missing links")
        assert not set(old["ids"]) - set(parser.ids), (relative, "missing anchors")
        changes.extend({"page": relative, "decorativeAlt": pair} for pair in allowed)
    return {"available": True, "pagesPreserved": len(baseline), "intentionalDecorativeAltChanges": changes}


METRICS = r"""() => {
  const visible = (el) => el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden';
  const blocks = [...document.querySelectorAll('[data-language-block]')];
  const active = blocks.filter((el) => !el.hidden);
  const prose = active[0]?.querySelector('.prose');
  const paragraph = prose?.querySelector('p');
  const style = paragraph ? getComputedStyle(paragraph) : null;
  const badAnchors = [...document.querySelectorAll('main a[href^="#"]')].map((a) => a.getAttribute('href').slice(1)).filter((id) => !document.getElementById(id));
  const ids = [...document.querySelectorAll('[id]')].map((el) => el.id);
  const image = document.querySelector('.project-detail-media img');
  return {
    overflow:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth,
    mainCount:document.querySelectorAll('main').length,
    headingCount:document.querySelectorAll('main h1').length,
    theme:document.documentElement.dataset.theme,
    background:getComputedStyle(document.body).backgroundColor,
    themeControls:document.querySelectorAll('[data-theme-toggle]').length,
    language:document.documentElement.lang,
    title:document.title,
    visible:document.body.getAttribute('data-language-ready') !== null && getComputedStyle(document.body).visibility === 'visible',
    brokenImages:[...document.images].filter((img) => !img.complete || !img.naturalWidth).map((img) => img.getAttribute('src')),
    badAnchors,duplicateIds:ids.filter((id,index) => ids.indexOf(id) !== index),
    activeVersions:active.length,versionCount:blocks.length,
    inactiveInert:blocks.filter((el) => el.hidden).every((el) => el.inert),
    prose:prose ? {fontSize:parseFloat(style.fontSize),lineHeight:parseFloat(style.lineHeight)/parseFloat(style.fontSize),width:prose.getBoundingClientRect().width,left:prose.getBoundingClientRect().left,right:innerWidth-prose.getBoundingClientRect().right,color:style.color} : null,
    detailImage:image ? {filter:getComputedStyle(image).filter,fit:getComputedStyle(image).objectFit,opacity:getComputedStyle(image).opacity} : null,
    shortControls:[...document.querySelectorAll('.site-navigation a,.language-toggle,.category-filters button,.site-menu summary')].filter(visible).filter(el => el.getBoundingClientRect().height < 44).map(el=>el.textContent.trim()),
    damagedLabels:[...document.querySelectorAll('[data-zh],[data-en]')].filter(el=>['data-zh','data-en'].some(key=>(el.getAttribute(key)||'').includes('???'))).map(el=>el.tagName),
  };
}"""


def ready(page):
    page.evaluate("""async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map((img) => {
        img.loading='eager';
        return img.complete ? Promise.resolve() : new Promise((resolve) => {img.onload=resolve; img.onerror=resolve;});
      }));
    }""")


def contrast(first, second):
    def luminance(color):
        channels = [float(n) / 255 for n in color.removeprefix("rgb(").removesuffix(")").split(",")]
        linear = [v / 12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in channels]
        return sum(a*b for a,b in zip(linear, (.2126,.7152,.0722)))
    a, b = luminance(first), luminance(second)
    return (max(a,b)+.05)/(min(a,b)+.05)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:4323")
    args = parser.parse_args()
    folder = REPO / "artifacts" / "preview-audit" / "site-migration"
    folder.mkdir(parents=True, exist_ok=True)
    routes = sorted(
        "/" + str(path.parent.relative_to(REPO / "dist")).replace("\\", "/") + "/"
        for path in (REPO / "dist").rglob("index.html")
        if not path.relative_to(REPO / "dist").as_posix().startswith("previews/")
    )
    routes = ["/" if route == "/./" else route for route in routes]
    report = {"content": preserve_content(folder), "pages": {}, "interactions": {}}
    shots = {"/":"home","/projects/":"projects","/articles/":"articles","/teaching/":"teaching","/projects/ming-engine/":"project-detail","/articles/animal-well-rendering/":"reading","/teaching/pico8-game-jam/":"gamejam"}
    links, local_errors, page_errors = set(), set(), []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for lang in ("zh","en"):
            context = browser.new_context(reduced_motion="reduce")
            context.add_init_script("if(location.origin === " + json.dumps(args.base) + "){localStorage.setItem('portfolio-language'," + json.dumps(lang) + "); localStorage.setItem('portfolio-theme','light');}")
            page = context.new_page()
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.on("response", lambda response: local_errors.add(str(response.status)+" "+response.url) if response.status >= 400 and response.url.startswith(args.base) else None)
            for width,height in ((1440,1000),(1024,768),(390,844)):
                page.set_viewport_size({"width":width,"height":height})
                for route in routes:
                    page.mouse.move(5,5)
                    response = page.goto(args.base + route, wait_until="domcontentloaded")
                    assert response.status == 200, route
                    ready(page)
                    data = page.evaluate(METRICS)
                    key = lang + "/" + str(width) + route
                    assert data["overflow"] <= 1, (key,"overflow",data["overflow"])
                    assert data["mainCount"] == 1 and data["headingCount"] == 1, (key,"structure")
                    assert data["theme"] == "dark" and data["background"] == "rgb(16, 23, 34)" and data["themeControls"] == 0, (key,"dark theme")
                    assert data["language"] == ("zh-CN" if lang == "zh" else "en") and data["visible"], (key,"language")
                    assert not data["brokenImages"], (key,"images",data["brokenImages"])
                    assert not data["badAnchors"] and not data["duplicateIds"], (key,"anchors")
                    assert not data["shortControls"], (key,"touch",data["shortControls"])
                    assert not data["damagedLabels"], (key,"label encoding")
                    if data["versionCount"]:
                        assert data["activeVersions"] == 1 and data["inactiveInert"], (key,"language blocks")
                    if data["prose"]:
                        prose = data["prose"]
                        assert 17 <= prose["fontSize"] <= 19 and prose["lineHeight"] >= 1.75, (key,"reading")
                        assert contrast(prose["color"],data["background"]) >= 7, (key,"contrast")
                        if width == 1440 and lang == "zh":
                            assert 32 <= prose["width"]/prose["fontSize"] <= 40, (key,"line width")
                        if width == 390:
                            assert min(prose["left"],prose["right"]) >= 16, (key,"gutters")
                    if data["detailImage"]:
                        assert data["detailImage"] == {"filter":"none","fit":"contain","opacity":"1"}, (key,"clear complete image")
                    report["pages"][key] = data
                    links.update(page.locator('a[href^="/"]').evaluate_all("(els)=>els.map(el=>el.getAttribute('href').split('#')[0])"))
                    if route in shots and width in (1440,390):
                        page.screenshot(path=str(folder/(shots[route]+"-"+lang+"-"+str(width)+".jpg")),type="jpeg",quality=88,animations="disabled")
            context.close()

        context = browser.new_context(reduced_motion="reduce",viewport={"width":1440,"height":1000})
        page = context.new_page()
        page.goto(args.base + "/",wait_until="domcontentloaded")
        page.evaluate("localStorage.setItem('portfolio-theme','light')")
        page.reload(wait_until="domcontentloaded")
        assert page.locator('html').get_attribute('data-theme') == "dark"
        assert page.locator('.hero-portrait img').count() == 1
        order = page.evaluate("['projects','articles','teaching','about','interests'].map(id=>document.getElementById(id).getBoundingClientRect().top)")
        assert order == sorted(order), order
        report["interactions"]["homeOrder"] = order
        page.locator('[data-language-toggle]').click()
        assert page.locator('html').get_attribute('lang') == "en"
        english_title = page.title()
        page.goto(args.base + "/articles/",wait_until="domcontentloaded")
        assert page.locator('html').get_attribute('lang') == "en"
        page.reload(wait_until="domcontentloaded")
        assert page.locator('html').get_attribute('lang') == "en"
        report["interactions"]["languagePersistence"] = {"pass":True,"homeTitle":english_title,"articleTitle":page.title()}
        for button in page.locator('[data-filter]').all():
            key = button.get_attribute('data-filter')
            button.click()
            visible = page.locator('.reading-card:visible')
            expected = page.locator('.reading-card').count() if key == "all" else page.locator('.reading-card[data-category="'+key+'"]').count()
            assert visible.count() == expected
        report["interactions"]["filters"] = True
        page.locator('[data-language-toggle]').click()
        page.goto(args.base + "/projects/",wait_until="domcontentloaded")
        ready(page)
        rows = page.locator('[data-project-row]')
        for row in rows.all():
            row.hover()
            assert row.locator('.project-row-backdrop img').evaluate("(el)=>getComputedStyle(el).opacity") == "1"
            assert row.evaluate("""el=>{const a=el.getBoundingClientRect(),b=el.querySelector('.project-row-backdrop').getBoundingClientRect();return b.left>=a.left && b.right<=a.right && b.top>=a.top && b.bottom<=a.bottom;}""")
        spectrex = page.locator('[data-project-row][href="/projects/spectrex"]')
        spectrex.scroll_into_view_if_needed()
        spectrex.hover()
        page.screenshot(path=str(folder/"project-row-hover.jpg"),type="jpeg",quality=91)
        page.mouse.move(5,5)
        assert rows.locator('.project-row-backdrop img').evaluate_all("(els)=>els.every(el=>getComputedStyle(el).opacity==='0')")
        rows.first.focus()
        assert rows.first.locator('img').evaluate("(el)=>getComputedStyle(el).opacity") == "1"
        assert rows.first.evaluate("(el)=>parseFloat(getComputedStyle(el).outlineWidth)") >= 2
        page.keyboard.press('Tab')
        assert rows.nth(1).evaluate("(el)=>el===document.activeElement")
        report["interactions"]["rowHoverAndKeyboard"] = True
        page.set_viewport_size({"width":390,"height":844})
        page.wait_for_function("!document.querySelector('.site-menu').open")
        assert page.locator('.site-menu').get_attribute('open') is None
        page.locator('.site-menu summary').click()
        assert page.locator('.site-menu').get_attribute('open') is not None
        page.locator('.site-navigation a[href="/articles/"]').click()
        page.wait_for_url("**/articles/")
        assert page.locator('.site-menu').get_attribute('open') is None
        page.set_viewport_size({"width":1440,"height":1000})
        page.wait_for_function("document.querySelector('.site-menu').open")
        assert page.locator('.site-menu').get_attribute('open') is not None
        report["interactions"]["responsiveMenu"] = True
        page.goto(args.base + "/articles/animal-well-rendering/",wait_until="domcontentloaded")
        page.set_viewport_size({"width":390,"height":844})
        toc = page.locator('[data-language-block="zh"] .reading-toc')
        page.wait_for_function("!document.querySelector('[data-language-block=zh] .reading-toc').open")
        assert toc.get_attribute('open') is None
        toc.locator('summary').click()
        target = toc.locator('a').nth(2).get_attribute('href')[1:]
        toc.locator('a').nth(2).click()
        assert toc.get_attribute('open') is None
        top = page.locator('[id="'+target+'"]').bounding_box()["y"]
        assert 0 <= top <= 100, top
        report["interactions"]["mobileToc"] = {"pass":True,"targetTop":top}
        page.locator('[data-language-toggle]').click()
        english_toc = page.locator('[data-language-block="en"] .reading-toc')
        english_toc.locator('summary').click()
        target = english_toc.locator('a').nth(2).get_attribute('href')[1:]
        english_toc.locator('a').nth(2).click()
        assert 0 <= page.locator('[id="'+target+'"]').bounding_box()["y"] <= 100
        report["interactions"]["englishToc"] = True
        result = page.evaluate("""() => {
          const prose=document.querySelector('[data-language-block="en"] .prose');
          const table=document.createElement('table');table.innerHTML='<tr><th>Temporary wide table</th><td>Layout check</td></tr>';table.style.minWidth='0';
          for(let i=0;i<16;i++) table.querySelector('tr').append(document.createElement('td'));
          prose.prepend(table);
          const pre=document.createElement('pre');pre.textContent='wide_content_'.repeat(150);prose.prepend(pre);
          return {table:table.scrollWidth>table.clientWidth,code:pre.scrollWidth>pre.clientWidth,overflow:document.documentElement.scrollWidth-innerWidth};
        }""")
        assert result["table"] and result["code"] and result["overflow"] <= 1, result
        report["interactions"]["wideContent"] = result
        for href in sorted(links):
            response = context.request.get(urljoin(args.base,href),timeout=15000)
            assert response.status == 200, (href,response.status)
        report["internalLinksChecked"] = len(links)
        page.goto(args.base + "/teaching/pico8-game-jam/",wait_until="domcontentloaded")
        downloads = page.locator('a[download]').count()
        assert downloads > 0
        report["cartridgeDownloads"] = downloads
        context.close()
        blocked = browser.new_context()
        blocked.add_init_script("if(location.origin === " + json.dumps(args.base) + "){Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage blocked for verification');}});}")
        fallback = blocked.new_page()
        fallback.goto(args.base + "/",wait_until="domcontentloaded")
        assert fallback.locator('html').get_attribute('lang') == "zh-CN"
        assert fallback.locator('body').get_attribute('data-language-ready') is not None
        fallback.locator('[data-language-toggle]').click()
        assert fallback.locator('html').get_attribute('lang') == "en"
        report["interactions"]["storageFallback"] = True
        blocked.close()
        browser.close()
    assert not page_errors and not local_errors, (page_errors,local_errors)
    report["pageErrors"], report["localErrors"] = page_errors, sorted(local_errors)
    report["pass"] = True
    (folder / "verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("PASS: " + str(len(routes)) + " routes × 3 widths × 2 languages; content, hover, menu, theme, TOC, links and downloads.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
