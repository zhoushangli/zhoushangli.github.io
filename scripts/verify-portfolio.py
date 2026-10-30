"""Check the dark portfolio migration against real pages in Chromium.

e.g. python scripts/verify-portfolio.py --base http://127.0.0.1:4323
"""
from __future__ import annotations

import argparse
import json
import sys
import re
import hashlib
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote


REPO = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class MainContent(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.pairs, self.links, self.ids, self.image_alts = [], [], [], []
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.nodes.append((tag, data))
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


RETIRED_TEACHING = ("pico8-intro", "pico8-l01", "pico8-l02", "pico8-l03", "pico8-a01", "pico8-a02", "pico8-object-organization")

RETIRED = ("ming-scene-resources", "ming-csharp-bridge", "ming-gui-input", "spectrex-light-gameplay", "spectrex-rendering")


def verify_static():
    pages = {
        "/" if path.parent == REPO / "dist" else "/" + path.parent.relative_to(REPO / "dist").as_posix() + "/": path
        for path in (REPO / "dist").rglob("index.html")
        if not path.relative_to(REPO / "dist").as_posix().startswith("previews/")
    }
    assert len(pages) == 13 and "/experience/" not in pages, sorted(pages)
    parsed = {}
    local_links = assets = anchors = captions = 0
    for route, path in pages.items():
        source = path.read_text(encoding="utf-8")
        parser = MainContent()
        parser.feed(source)
        parsed[route] = parser
        assert len(parser.ids) == len(set(parser.ids)), (route, "duplicate main IDs")
        all_ids = [attrs["id"] for _, attrs in parser.nodes if "id" in attrs]
        assert len(all_ids) == len(set(all_ids)), (route, "duplicate document IDs")
        assert "???" not in source and "\ufffd" not in source, (route, "encoding")
        assert not any("/articles/" + slug in source for slug in RETIRED), (route, "retired reference")
        assert not any("/teaching/" + slug + "/" in source for slug in RETIRED_TEACHING), (route, "retired teaching reference")
        main_navigation = re.search(r'<nav class="site-navigation"[^>]*>(.*?)</nav>', source, re.S).group(1)
        assert re.findall(r'href="([^"]+)"', main_navigation) == ["/", "/projects/", "/articles/", "/teaching/"]
        assert "secondary-navigation" in source
        assert '/experience/' not in source, (route, "retired experience link")
        for tag, attrs in parser.nodes:
            if "showcase-tech" in attrs.get("class", "").split():
                for language in ("zh", "en"):
                    assert 1 <= len(attrs["data-" + language].split("|")) <= 3, (route, "technology count")
            if tag == "iframe":
                assert attrs.get("loading") == "lazy"
                if "bilibili" in attrs.get("src", ""):
                    assert "autoplay=0" in attrs["src"]
            if tag == "video":
                assert attrs.get("preload") == "none" and "autoplay" not in attrs
            if tag == "figcaption":
                captions += 1
            for attribute in ("href", "src"):
                value = attrs.get(attribute, "")
                if not value or urlsplit(value).scheme or value.startswith("//"):
                    continue
                url = urlsplit(urljoin("https://local.test" + route, value))
                target = unquote(url.path)
                candidate = REPO / "dist" / target.lstrip("/")
                if target.endswith("/") or not candidate.suffix:
                    candidate = candidate / "index.html"
                assert candidate.is_file(), (route, value, "missing local target")
                if attribute == "src":
                    assets += 1
                else:
                    local_links += 1
                    if url.fragment:
                        target_parser = MainContent()
                        target_parser.feed(candidate.read_text(encoding="utf-8"))
                        assert unquote(url.fragment) in target_parser.ids, (route, value, "missing anchor")
                        anchors += 1
    home = pages["/"].read_text(encoding="utf-8")
    chapters = ("intro", "about", "education", "experience", "skills", "personal-projects", "team-projects", "articles", "teaching", "interests")
    order = [home.index('id="' + section + '"') for section in chapters]
    assert order == sorted(order), "home order"
    chapter_links = [attrs["href"] for tag, attrs in parsed["/"].nodes if "data-chapter-link" in attrs]
    assert chapter_links == ["#" + section for section in chapters], "home contents order"
    for section in chapters[1:]:
        block = re.search(r'<section[^>]*id="' + section + r'"[\s\S]*?</section>', home).group()
        assert "section-major" in block and "<h2 " in block, (section, "peer section")
        if section == "about":
            assert block.count('<p ') == 3, "three biography paragraphs"
    for slug in RETIRED:
        assert "/articles/" + slug + "/" not in pages
        for lang in ("zh", "en"):
            assert "draft: true" in (REPO / "src/content/published/articles" / (slug + "." + lang + ".md")).read_text(encoding="utf-8")
    for slug in RETIRED_TEACHING:
        assert "/teaching/" + slug + "/" not in pages
        for lang in ("zh", "en"):
            assert "draft: true" in (REPO / "src/content/published/teaching" / (slug + "." + lang + ".md")).read_text(encoding="utf-8")
    for route, parser in parsed.items():
        if route.startswith("/projects/") and route != "/projects/":
            current = [a["href"] for tag, a in parser.nodes if a.get("aria-current") == "page"]
            assert route in current, (route, "current project")
        if route.startswith(("/articles/", "/teaching/")) and route.count("/") == 3:
            assert any("reading-toc" in a.get("class", "") for _, a in parser.nodes), (route, "sidebar contents")
    sitemap = (REPO / "dist/sitemap-0.xml").read_text(encoding="utf-8")
    assert sitemap.count("<loc>") == 13 and "/previews/" not in sitemap and "/experience/" not in sitemap
    assert not any("/articles/" + slug in sitemap for slug in RETIRED)
    for slug in ("animal-well-rendering", "sifu-combat-analysis"):
        source_text = pages["/articles/" + slug + "/"].read_text(encoding="utf-8").lower()
        editorial_phrases = ("原笔记", "原稿", "原分析", "原记录", "原始笔记", "original notes", "initial draft", "the draft", "for this edit")
        assert not any(phrase in source_text for phrase in editorial_phrases), (slug, "editorial voice")
    rendering = pages["/projects/spectrex/"].read_text(encoding="utf-8")
    assert 'class="project-rendering"' in rendering and "RenderService" in rendering and "RenderPipeline" in rendering
    source = (REPO / "src/data/gamejam.ts").read_text(encoding="utf-8")
    hashes = re.findall(r'"sha256":\s*"([0-9a-f]{64})"', source)
    assert len(hashes) == 15
    actual = [hashlib.sha256(path.read_bytes()).hexdigest() for path in (REPO / "public/downloads/gamejam-2026").iterdir() if path.is_file()]
    assert Counter(hashes) == Counter(actual), "cartridge integrity"
    assert all(path.suffix == ".png" for path in (REPO / "public/downloads/gamejam-2026").iterdir() if path.is_file())
    gallery = parsed["/teaching/pico8-game-jam/"]
    assert sum("gamejam-card" in attrs.get("class", "").split() for _, attrs in gallery.nodes) == 15
    assert not any("download" in attrs for _, attrs in gallery.nodes)
    training_links = {attrs.get("href") for tag, attrs in parsed["/teaching/pico8-2026/"].nodes if tag == "a"}
    assert {"https://meeting.tencent.com/crm/237OkeqV26", "https://meeting.tencent.com/crm/KErQqqpObc", "https://meeting.tencent.com/crm/NARXvk9a12"} <= training_links
    assert "NARXvk9acd" not in pages["/teaching/pico8-2026/"].read_text(encoding="utf-8")
    assert "\u60a8\u597d\uff0c\u6211\u662f\u5468\u5c1a\u793c" in home and "hero-subtitle" in home
    logs = [attrs.get("href") for tag, attrs in parsed["/projects/spectrex/"].nodes if tag == "a" and "www.taptap.cn/moment/" in attrs.get("href", "")]
    assert len(logs) == 6 and len(set(logs)) == 6
    assert "spectrex-cover.jpg" in pages["/projects/spectrex/"].read_text(encoding="utf-8")
    assert "BV1gEny6hEAC" in pages["/projects/spectrex/"].read_text(encoding="utf-8")
    return {"routes": len(pages), "localLinks": local_links, "assets": assets, "anchors": anchors, "captions": captions, "retiredArticlePairs": len(RETIRED), "retiredTeachingPairs": len(RETIRED_TEACHING), "pngSubmissions": len(hashes), "pass": True}


METRICS = r"""() => {
  const visible = (el) => el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden';
  const blocks = [...document.querySelectorAll('main [data-language-block]')];
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
    technologies:[...document.querySelectorAll('main .showcase-tech')].map(el=>({size:parseFloat(getComputedStyle(el).fontSize),detail:!!el.closest('.page-intro'),color:getComputedStyle(el).color,count:el.textContent.split('|').length})),
    captions:[...document.querySelectorAll('main figcaption')].map(el=>({size:parseFloat(getComputedStyle(el).fontSize),align:getComputedStyle(el).textAlign})),
    sidebar:{primaryBottom:document.querySelector('.site-navigation').getBoundingClientRect().bottom,secondaryTop:document.querySelector('.secondary-navigation').getBoundingClientRect().top,secondaryBottom:document.querySelector('.secondary-navigation').getBoundingClientRect().bottom,footerTop:document.querySelector('.sidebar-bottom').getBoundingClientRect().top},
    detailImage:image ? {filter:getComputedStyle(image).filter,fit:getComputedStyle(image).objectFit,opacity:getComputedStyle(image).opacity} : null,
    shortControls:[...document.querySelectorAll('.site-navigation a,.secondary-navigation a,.language-toggle,.category-filters button,.site-menu summary')].filter(visible).filter(el => el.getBoundingClientRect().height < 44).map(el=>el.textContent.trim()),
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


def verify_language_detection(browser, base):
    endpoint = "https://ipwho.is/**"
    cases = [
        (country, {"success": True, "country_code": country}, 200, "zh-CN" if country == "CN" else "en")
        for country in ("CN", "US", "HK", "MO", "TW")
    ] + [
        ("api-error", {"success": False, "country_code": "CN"}, 200, "en"),
        ("http-error", {"success": True, "country_code": "CN"}, 429, "en"),
        ("missing-country", {}, 200, "en"),
        ("invalid-json", None, 200, "en"),
    ]
    for name, payload, status, expected in cases:
        context = browser.new_context()
        requests, errors = [], []
        def respond(route):
            requests.append(route.request.url)
            route.fulfill(status=status, content_type="application/json", body=json.dumps(payload) if payload is not None else "invalid json")
        context.route(endpoint, respond)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(base + "/articles/animal-well-rendering/", wait_until="domcontentloaded")
        page.evaluate("window.portfolioLanguageReady")
        assert page.locator("html").get_attribute("lang") == expected, name
        language = "zh" if expected == "zh-CN" else "en"
        assert page.title() == page.locator("html").get_attribute("data-title-" + language), name
        assert page.locator('[data-language-block]:not([hidden])').count() > 0, name
        assert page.locator('[data-language-block="' + ("en" if language == "zh" else "zh") + '"]:not([hidden])').count() == 0, name
        assert page.evaluate("localStorage.getItem('portfolio-language')") is None, name
        if name == "CN":
            page.reload(wait_until="domcontentloaded")
            assert page.locator("html").get_attribute("lang") == "zh-CN"
            page.goto(base + "/projects/", wait_until="domcontentloaded")
            assert page.locator("html").get_attribute("lang") == "zh-CN"
            assert len(requests) == 1, "reuse automatic language across pages"
        assert not errors, (name, errors)
        context.close()

    for preferred in ("zh", "en"):
        context = browser.new_context()
        context.add_init_script("localStorage.setItem('portfolio-language', " + json.dumps(preferred) + ")")
        requests = []
        context.route(endpoint, lambda route: (requests.append(route.request.url), route.abort()))
        page = context.new_page()
        page.goto(base + "/", wait_until="domcontentloaded")
        assert page.locator("html").get_attribute("lang") == ("zh-CN" if preferred == "zh" else "en")
        assert not requests, "manual preference skips IP lookup"
        context.close()

    for storage_blocked in (False, True):
        context = browser.new_context()
        if storage_blocked:
            context.add_init_script("for(const key of ['localStorage','sessionStorage']) { Object.defineProperty(window,key,{get(){throw new Error('Storage blocked');}}); }")
        pending = []
        context.route(endpoint, lambda route: pending.append(route))
        page = context.new_page()
        page.goto(base + "/", wait_until="domcontentloaded")
        assert page.locator("body").get_attribute("data-language-ready") is not None
        assert page.locator("html").get_attribute("lang") == "en", "visible English while lookup is pending"
        page.locator('[data-language-toggle]').click()
        page.locator('[data-language-toggle]').click()
        assert pending, "IP lookup started"
        pending[0].fulfill(json={"success": True, "country_code": "CN"})
        page.evaluate("window.portfolioLanguageReady")
        assert page.locator("html").get_attribute("lang") == "en", "late lookup must preserve manual choice"
        if not storage_blocked:
            page.reload(wait_until="domcontentloaded")
            assert page.locator("html").get_attribute("lang") == "en", "manual choice survives reload"
            assert len(pending) == 1, "manual choice avoids another lookup"
        context.close()

    context = browser.new_context()
    context.add_init_script("""const originalFetch = window.fetch;
        window.fetch = (url, options) => String(url).startsWith('https://ipwho.is/')
            ? new Promise((resolve, reject) => options.signal.addEventListener('abort',
                () => reject(new DOMException('Lookup timed out', 'AbortError')), {once: true}))
            : originalFetch(url, options);
    """)
    page = context.new_page()
    page.goto(base + "/", wait_until="domcontentloaded")
    assert page.evaluate("window.portfolioLanguageReady") == "en", "timeout fallback"
    assert page.locator("html").get_attribute("lang") == "en"
    assert page.locator("body").get_attribute("data-language-ready") is not None
    context.close()
    return {"countryAndErrorCases": len(cases), "manualPriority": True, "sessionCache": True, "lateResponse": True, "blockedStorage": True, "timeout": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:4323")
    parser.add_argument("--static-only", action="store_true", help="Check built pages without a browser")
    args = parser.parse_args()
    static = verify_static()
    if args.static_only:
        print(json.dumps(static, ensure_ascii=False, indent=2))
        return 0
    from playwright.sync_api import sync_playwright
    folder = REPO / "artifacts" / "preview-audit" / "site-migration"
    folder.mkdir(parents=True, exist_ok=True)
    routes = sorted(
        "/" + str(path.parent.relative_to(REPO / "dist")).replace("\\", "/") + "/"
        for path in (REPO / "dist").rglob("index.html")
        if not path.relative_to(REPO / "dist").as_posix().startswith("previews/")
    )
    routes = ["/" if route == "/./" else route for route in routes]
    report = {"content": static, "pages": {}, "interactions": {}}
    shots = {"/projects/spectrex/":"spectrex","/":"home","/projects/":"projects","/articles/":"articles","/teaching/":"teaching","/projects/ming-engine/":"project-detail","/articles/animal-well-rendering/":"reading","/teaching/pico8-game-jam/":"gamejam"}
    links, local_errors, page_errors = set(), set(), []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        report["interactions"]["ipLanguageDetection"] = verify_language_detection(browser, args.base)
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
                    assert all(item["count"] <= 3 and item["size"] == (18 if item["detail"] else 14) and item["color"] == "rgb(210, 179, 135)" for item in data["technologies"]), (key,"technology style")
                    assert all(13 <= item["size"] <= 14 and item["align"] == "center" for item in data["captions"]), (key,"caption style")
                    if width > 900:
                        sidebar = data["sidebar"]
                        assert sidebar["secondaryTop"] >= sidebar["primaryBottom"] and abs(sidebar["secondaryBottom"] - sidebar["footerTop"]) <= 4, (key,"sidebar layout")
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
        context.route("https://ipwho.is/**", lambda route: route.fulfill(json={"success": True, "country_code": "CN"}))
        page = context.new_page()
        page.goto(args.base + "/",wait_until="domcontentloaded")
        page.evaluate("localStorage.setItem('portfolio-theme','light')")
        page.reload(wait_until="domcontentloaded")
        page.evaluate("window.portfolioLanguageReady")
        assert page.locator('html').get_attribute('data-theme') == "dark"
        assert page.locator('.hero-portrait img').count() == 1
        order = page.evaluate("['intro','about','education','experience','skills','personal-projects','team-projects','articles','teaching','interests'].map(id=>document.getElementById(id).getBoundingClientRect().top)")
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
        toc = page.locator('.secondary-navigation .reading-toc[data-language-block="zh"]')
        page.locator('.site-menu summary').click()
        target = toc.locator('a').nth(2).get_attribute('href')[1:]
        toc.locator('a').nth(2).click()
        assert page.locator('.site-menu').get_attribute('open') is None
        top = page.locator('[id="'+target+'"]').bounding_box()["y"]
        assert 0 <= top <= 100, top
        report["interactions"]["mobileToc"] = {"pass":True,"targetTop":top}
        page.locator('[data-language-toggle]').click()
        english_toc = page.locator('.secondary-navigation .reading-toc[data-language-block="en"]')
        page.locator('.site-menu summary').click()
        target = english_toc.locator('a').nth(2).get_attribute('href')[1:]
        english_toc.locator('a').nth(2).click()
        assert page.locator('.site-menu').get_attribute('open') is None
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
        assert page.locator('a[download]').count() == 0
        assert page.locator('.gamejam-card img').count() == 15
        report["pngGallery"] = {"covers": 15, "downloads": 0}
        for width in (1440, 1024):
            for lang in ("zh", "en"):
                tops = [data["sidebar"]["secondaryTop"] for key, data in report["pages"].items() if key.startswith(lang + "/" + str(width) + "/")]
                assert max(tops) - min(tops) <= 1, (width, lang, "secondary navigation start moved")
        report["interactions"]["fixedSecondaryStart"] = True
        context.close()
        blocked = browser.new_context()
        blocked.route("https://ipwho.is/**", lambda route: route.abort())
        blocked.add_init_script("if(location.origin === " + json.dumps(args.base) + "){Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage blocked for verification');}});}")
        fallback = blocked.new_page()
        fallback.goto(args.base + "/",wait_until="domcontentloaded")
        fallback.evaluate("window.portfolioLanguageReady")
        assert fallback.locator('html').get_attribute('lang') == "en"
        assert fallback.locator('body').get_attribute('data-language-ready') is not None
        fallback.locator('[data-language-toggle]').click()
        assert fallback.locator('html').get_attribute('lang') == "zh-CN"
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
