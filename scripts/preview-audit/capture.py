"""Capture browser evidence and interactions for the six dark blog prototypes.

e.g. python scripts/preview-audit/capture.py --design design-a --round 1 --base http://127.0.0.1:4322
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
VIEWS = ("home", "articles", "article")
VIEWPORTS = (("desktop", 1440, 900), ("laptop", 1024, 768), ("mobile", 390, 844))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

METRICS = r"""() => {
  const rgb = (value) => (value.match(/[\d.]+/g) || []).map(Number);
  const blend = (front, back) => {
    const alpha = front.length > 3 ? front[3] : 1;
    return [0,1,2].map((i) => front[i] * alpha + back[i] * (1 - alpha));
  };
  const background = (element) => {
    const stack = [];
    for (let node = element; node; node = node.parentElement) {
      stack.unshift(rgb(getComputedStyle(node).backgroundColor));
    }
    return stack.reduce((color, layer) => layer.length >= 3 ? blend(layer, color) : color, [0,0,0]);
  };
  const luminance = (color) => {
    const linear = color.map((v) => v / 255).map((v) => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
    return linear[0] * .2126 + linear[1] * .7152 + linear[2] * .0722;
  };
  const contrast = (element) => {
    const bg = background(element);
    const fg = blend(rgb(getComputedStyle(element).color), bg);
    const a = luminance(fg), b = luminance(bg);
    return Math.round((Math.max(a,b) + .05) / (Math.min(a,b) + .05) * 100) / 100;
  };
  const visible = (el) => el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden';
  const label = (el) => el.tagName.toLowerCase() + '.' + String(el.className).slice(0,55);
  const controls = [...document.querySelectorAll('a[href],button,summary')].filter(visible).filter((el) => !el.closest('astro-dev-toolbar') && !el.classList.contains('skip-link'));
  const short = controls.map((el) => ({selector:label(el),text:el.textContent.trim().slice(0,30),height:Math.round(el.getBoundingClientRect().height)})).filter((el) => el.height < 44);
  const small = [...document.querySelectorAll('.micro,.destination,.lede,.article-deck,.entry-copy p,.toc a,.reading-prose p:has(> em:only-child),nav a,button')].filter(visible).filter((el) => el.textContent.trim()).map((el) => ({selector:label(el),text:el.textContent.trim().slice(0,24),contrast:contrast(el)}));
  const prose = document.querySelector('.reading-prose');
  const paragraph = prose?.querySelector('p');
  const cs = paragraph ? getComputedStyle(paragraph) : null;
  const bg = rgb(getComputedStyle(document.body).backgroundColor);
  const lightness = (Math.max(...bg.slice(0,3)) + Math.min(...bg.slice(0,3))) / 510 * 100;
  return {
    title:document.title, mainCount:document.querySelectorAll('main').length,
    overflow:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth,
    brokenImages:[...document.images].filter((img) => !img.complete || !img.naturalWidth).map((img) => img.getAttribute('src')),
    shortTargets:short,
    smallContrastFailures:small.filter((el) => el.contrast < 4.5),
    minimumSmallContrast:small.length ? Math.min(...small.map((el) => el.contrast)) : null,
    backgroundLightness:Math.round(lightness*10)/10,
    robots:document.querySelector('meta[name=robots]')?.content,
    headingCount:document.querySelectorAll('main h1').length,
    prose:paragraph ? {
      fontSize:parseFloat(cs.fontSize),lineHeight:parseFloat(cs.lineHeight)/parseFloat(cs.fontSize),
      contrast:contrast(paragraph),width:prose.getBoundingClientRect().width,
      charsPerLine:prose.getBoundingClientRect().width/parseFloat(cs.fontSize),
      left:prose.getBoundingClientRect().left,right:innerWidth-prose.getBoundingClientRect().right,
      images:prose.querySelectorAll('img').length,codeBlocks:prose.querySelectorAll('pre').length,
      headings:[...prose.querySelectorAll('h2')].map((h) => h.id),
    } : null
  };
}"""

def ready(page):
    page.evaluate("""async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map((img) => {
        img.loading = 'eager';
        return img.complete ? Promise.resolve() : new Promise((resolve) => {img.onload=resolve; img.onerror=resolve;});
      }));
    }""")

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def sheet(images, target, width=480):
    tiles = []
    for title, path in images:
        with Image.open(path) as source:
            tile = source.convert("RGB")
            tile.thumbnail((width, 1200))
            canvas = Image.new("RGB", (width, tile.height + 30), "#111318")
            ImageDraw.Draw(canvas).text((10,8), title, fill="#eeeeee")
            canvas.paste(tile, (0,30))
            tiles.append(canvas)
    canvas = Image.new("RGB", (width * len(tiles), max(t.height for t in tiles)), "#111318")
    for index, tile in enumerate(tiles):
        canvas.paste(tile, (width * index, 0))
    canvas.save(target, quality=86)

def state_shot(page, folder, name, evidence):
    path = folder / (name + ".jpg")
    page.screenshot(path=str(path), type="jpeg", quality=85, animations="disabled")
    evidence["screenshot"] = str(path.relative_to(REPO))
    return evidence

def run_interactions(page, design, view, size, folder):
    result = {}
    if view == "articles":
        buttons = page.locator('[data-filter]')
        result["filters"] = []
        for index in range(buttons.count()):
            button = buttons.nth(index)
            category = button.get_attribute("data-filter")
            button.click()
            state = page.evaluate("""(category) => {
              const entries = [...document.querySelectorAll('[data-entry]')];
              const visible = entries.filter((el) => !el.hidden && el.getClientRects().length);
              return {category, expected:entries.filter((el) => category === 'all' || el.dataset.category === category).length,
                count:visible.length,correct:visible.every((el) => category === 'all' || el.dataset.category === category),
                selected:document.querySelector('[data-filter][aria-pressed=true]')?.dataset.filter};
            }""", category)
            state["pass"] = state["correct"] and state["count"] == state["expected"] and state["selected"] == category
            result["filters"].append(state)
        if buttons.count() > 1:
            buttons.nth(1).click()
            result["filterState"] = state_shot(page, folder, view + "-" + size + "-filter", {"category":buttons.nth(1).get_attribute("data-filter")})
        buttons.first.click()
        if design == "design-d":
            choices = page.locator('[data-select-entry]')
            choice = choices.last
            expected = choice.get_attribute("data-title")
            choice.click()
            page.wait_for_timeout(350)
            link_box = page.locator('[data-selected-link]').bounding_box()
            preview_box = page.locator('.specimen-preview').bounding_box()
            visible = bool(link_box) and 0 <= link_box['y'] and link_box['y'] + link_box['height'] <= page.viewport_size['height']
            result["selection"] = state_shot(page, folder, size + "-selection", {
                "pass":page.locator('[data-selected-title]').inner_text() == expected and visible,
                "readingLinkVisible":visible,"readingLinkBox":link_box,"previewBox":preview_box,
                "title":expected,"href":page.locator('[data-selected-link]').get_attribute("href")
            })
            choices.first.click()
        if design == "design-e":
            group = page.locator('.theatre-index details').first
            group.locator('summary').click()
            closed = group.get_attribute("open") is None
            group.locator('summary').click()
            result["programme"] = state_shot(page, folder, size + "-programme", {"pass":closed and group.get_attribute("open") is not None})
        if design == "design-f":
            page.locator('[data-view-mode=compact]').click()
            compact = page.locator('.folio-entries').evaluate("(el) => el.classList.contains('is-compact')")
            result["viewSwitch"] = state_shot(page, folder, size + "-compact", {"pass":compact})
            page.locator('[data-view-mode=illustrated]').click()
            result["viewSwitch"]["restored"] = page.locator('.folio-entries').evaluate("(el) => !el.classList.contains('is-compact')")

    if view == "home":
        if design == "design-a":
            menu = page.locator('.library-menu')
            if size == "mobile":
                initial = menu.get_attribute("open") is None
                menu.locator('summary').click()
                opened = menu.get_attribute("open") is not None
                result["mobileMenu"] = state_shot(page, folder, "mobile-menu", {"pass":initial and opened})
            page.locator('[data-section-link][href="#projects"]').click()
            page.wait_for_timeout(650)
            active = page.locator('[data-section-link][href="#projects"]').get_attribute("aria-current")
            result["chapters"] = state_shot(page, folder, size + "-chapter", {"pass":active == "location","active":active})
        if design == "design-e":
            acts = page.locator('.theatre-programme details')
            acts.nth(1).locator('summary').click()
            opened = acts.nth(1).get_attribute("open") is not None
            result["acts"] = state_shot(page, folder, size + "-act", {"pass":opened})
            acts.nth(1).locator('summary').click()
            result["acts"]["closed"] = acts.nth(1).get_attribute("open") is None
        if design == "design-f":
            gallery = page.locator('.folio-gallery')
            before = gallery.evaluate("(el) => el.scrollLeft")
            page.locator('[data-gallery-next]').click()
            page.wait_for_timeout(200)
            after = gallery.evaluate("(el) => el.scrollLeft")
            page.locator('[data-gallery-prev]').click()
            page.wait_for_timeout(200)
            previous = gallery.evaluate("(el) => el.scrollLeft")
            gallery.focus()
            page.keyboard.press('ArrowRight')
            page.wait_for_timeout(250)
            keyboard = gallery.evaluate("(el) => el.scrollLeft")
            result["gallery"] = state_shot(page, folder, size + "-gallery", {"pass":after > before and previous < after and keyboard > previous,"before":before,"next":after,"previous":previous,"keyboard":keyboard})
            if size == "mobile":
                gallery.scroll_into_view_if_needed()
                box = gallery.bounding_box()
                touch_before = gallery.evaluate("(el) => el.scrollLeft")
                session = page.context.new_cdp_session(page)
                y = max(80, min(650, box["y"] + 100))
                session.send("Input.dispatchTouchEvent", {"type":"touchStart","touchPoints":[{"x":320,"y":y}]})
                for x in range(300, 69, -20):
                    session.send("Input.dispatchTouchEvent", {"type":"touchMove","touchPoints":[{"x":x,"y":y}]})
                    page.wait_for_timeout(16)
                session.send("Input.dispatchTouchEvent", {"type":"touchEnd","touchPoints":[]})
                page.wait_for_timeout(450)
                touch_after = gallery.evaluate("(el) => el.scrollLeft")
                result["touchSwipe"] = state_shot(page, folder, "mobile-touch-swipe", {"pass":touch_after > touch_before,"before":touch_before,"after":touch_after})
                session.detach()

    if view == "article":
        if design == "design-b":
            toc = page.locator('.stone-toc')
            initial = toc.get_attribute("open") is None
            toc.locator('summary').click()
            result["toc"] = state_shot(page, folder, size + "-toc", {"pass":initial and toc.get_attribute("open") is not None})
        if design == "design-c":
            note = page.locator('.ink-margins details').nth(1)
            note.locator('summary').click()
            opened = note.get_attribute("open") is not None
            result["marginalia"] = state_shot(page, folder, size + "-marginalia", {"pass":opened})
            note.locator('summary').click()
            result["marginalia"]["closed"] = note.get_attribute("open") is None
        if design == "design-d":
            zoom = page.locator('.image-zoom').first
            zoom.click()
            dialog = page.locator('.image-inspector')
            opened = dialog.evaluate("(el) => el.open")
            focused = page.evaluate("Boolean(document.activeElement.closest('dialog'))")
            result["imageInspector"] = state_shot(page, folder, size + "-zoom", {"pass":opened and focused,"focusInside":focused})
            page.keyboard.press('Escape')
            result["imageInspector"]["escapeCloses"] = not dialog.evaluate("(el) => el.open")
            result["imageInspector"]["focusRestored"] = zoom.evaluate("(el) => el === document.activeElement")
            zoom.click()
            page.locator('[data-close-inspector]').click()
            result["imageInspector"]["buttonCloses"] = not dialog.evaluate("(el) => el.open")
        links = page.locator('nav.toc a, .toc a')
        if links.count():
            link = links.nth(min(2, links.count()-1))
            closed_details = link.locator('xpath=ancestor::details[not(@open)]')
            if closed_details.count():
                closed_details.locator('summary').click()
            href = link.get_attribute("href")
            link.click()
            page.wait_for_timeout(650)
            target = page.locator('[id="' + href[1:] + '"]')
            top = target.evaluate("(el) => el.getBoundingClientRect().top") if target.count() else None
            result["anchor"] = {"pass":top is not None and 0 <= top <= 170,"href":href,"targetTop":top}
            if design == "design-b":
                value = int(page.locator('.stone-progress').get_attribute('aria-valuenow'))
                result["progress"] = {"pass":value > 0,"value":value}
    return result

def all_pass(value):
    if isinstance(value, dict):
        if "pass" in value and not value["pass"]:
            return False
        for key in ("closed","restored","escapeCloses","focusRestored","buttonCloses"):
            if key in value and not value[key]:
                return False
        return all(all_pass(v) for v in value.values())
    if isinstance(value, list):
        return all(all_pass(v) for v in value)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", required=True, choices=["design-" + c for c in "abcdef"])
    parser.add_argument("--round", type=int, default=1)
    parser.add_argument("--base", default="http://127.0.0.1:4323")
    parser.add_argument("--out", type=Path, default=REPO / "artifacts" / "preview-audit")
    args = parser.parse_args()
    folder = args.out.resolve() / args.design / ("round-" + str(args.round))
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / "gates.json").exists():
        raise SystemExit("This round is already archived. Use a new --round number.")
    report = {"design":args.design,"round":args.round,"base":args.base,"capturedAt":datetime.now(timezone.utc).isoformat(),"views":{},"gates":{},"screenshots":{}}
    errors, external = [], []
    links = set()
    folds = {size:[] for size,_,_ in VIEWPORTS}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(reduced_motion="reduce", has_touch=True)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("response", lambda response: errors.append(str(response.status) + " " + response.url) if response.status >= 400 else None)
        page.on("request", lambda request: external.append(request.url) if request.url.startswith("http") and not request.url.startswith(args.base) else None)
        for size, width, height in VIEWPORTS:
            page.set_viewport_size({"width":width,"height":height})
            for view in VIEWS:
                url = args.base + "/previews/" + args.design + "/" + view
                response = page.goto(url, wait_until="networkidle")
                ready(page)
                metrics = page.evaluate(METRICS)
                metrics["httpStatus"] = response.status
                metrics["screenshots"] = {}
                for full in (False, True):
                    suffix = "full" if full else "fold"
                    path = folder / (view + "-" + size + "-" + suffix + ".jpg")
                    page.screenshot(path=str(path), type="jpeg", quality=84, full_page=full, animations="disabled")
                    metrics["screenshots"][suffix] = str(path.relative_to(REPO))
                    if not full:
                        folds[size].append((view + " / " + str(width), path))
                        if view == "home" and size in ("desktop","mobile"):
                            public = REPO / "public" / "previews-audit" / (args.design + "-" + size + ".webp")
                            public.parent.mkdir(parents=True, exist_ok=True)
                            with Image.open(path) as source:
                                source.save(public, "WEBP", quality=84)
                if view == "article":
                    page.locator('.reading-prose pre').first.scroll_into_view_if_needed()
                    path = folder / (view + "-" + size + "-detail.jpg")
                    page.screenshot(path=str(path), type="jpeg", quality=88, animations="disabled")
                    metrics["screenshots"]["detail"] = str(path.relative_to(REPO))
                links.update(page.locator('a[href]').evaluate_all("(els) => els.map((el) => el.getAttribute('href')).filter((href) => href.startsWith('/'))"))
                metrics["interactions"] = run_interactions(page, args.design, view, size, folder)
                page.goto(url, wait_until="networkidle")
                ready(page)
                focus = []
                for _ in range(8):
                    page.keyboard.press("Tab")
                    focus.append(page.evaluate("""() => {
                      const el = document.activeElement;
                      const cs = getComputedStyle(el);
                      return {text:el.textContent.trim().slice(0,24),visible:cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2};
                    }"""))
                metrics["focus"] = focus
                metrics["focusPass"] = all(item["visible"] for item in focus)
                if view == "articles":
                    metrics["growthStress"] = page.evaluate("""() => {
                      const entries = [...document.querySelectorAll('[data-entry]')];
                      for (let i=entries.length; i<21; i++) {
                        entries[0].parentElement.append(entries[i % entries.length].cloneNode(true));
                      }
                      const title = document.querySelector('[data-entry] h3');
                      title.textContent = '一个用于检验长标题折行与内容增长的排版样例'.repeat(5);
                      const overflow = Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth;
                      return {count:document.querySelectorAll('[data-entry]').length,overflow,pass:overflow <= 1};
                    }""")
                    state_shot(page, folder, size + "-growth", metrics["growthStress"])
                if view == "article":
                    metrics["wideContent"] = page.evaluate("""() => {
                      const prose = document.querySelector('.reading-prose');
                      const wrapper = document.createElement('div');
                      wrapper.className='table-scroll'; wrapper.tabIndex=0;
                      const table = document.createElement('table'); table.style.minWidth='1100px';
                      table.innerHTML='<tr><th>临时宽表格</th><th>布局验证</th></tr><tr><td>仅测试中注入</td><td>不修改文章源文件</td></tr>';
                      wrapper.append(table); prose.prepend(wrapper);
                      const pre=document.createElement('pre');pre.textContent='wide_content_'.repeat(120);prose.prepend(pre);
                      const overflow=Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth;
                      return {overflow,tableScrollable:wrapper.scrollWidth> wrapper.clientWidth,codeScrollable:pre.scrollWidth>pre.clientWidth,pass:overflow<=1 && wrapper.scrollWidth> wrapper.clientWidth && pre.scrollWidth>pre.clientWidth};
                    }""")
                    page.locator('[data-reading]').scroll_into_view_if_needed()
                    state_shot(page, folder, size + "-wide-content", metrics["wideContent"])
                report["views"].setdefault(view, {})[size] = metrics
        link_statuses = {href:context.request.get(urljoin(args.base,href)).status for href in sorted(links)}
        redirect = page.goto(args.base + "/previews/" + args.design + "/category", wait_until="networkidle")
        page.wait_for_url("**/articles/**", timeout=10000)
        report["categoryRedirect"] = {"status":redirect.status,"url":page.url}
        report["reducedMotion"] = page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
        browser.close()
    report["errors"] = sorted(set(errors))
    report["externalRequests"] = sorted(set(external))
    report["links"] = link_statuses
    entries = [report["views"][v][s] for v in VIEWS for s,_,_ in VIEWPORTS]
    articles = [report["views"]["article"][s]["prose"] for s,_,_ in VIEWPORTS]
    desktop = report["views"]["article"]["desktop"]["prose"]
    report["gates"] = {
        "routesLoaded":all(e["httpStatus"] == 200 and e["mainCount"] == 1 and e["headingCount"] == 1 for e in entries),
        "noErrors":not report["errors"],
        "localAssets":not report["externalRequests"],
        "noBrokenImages":all(not e["brokenImages"] for e in entries),
        "linksValid":all(status == 200 for status in link_statuses.values()),
        "noHorizontalOverflow":all(e["overflow"] <= 1 for e in entries),
        "darkSurface":all(e["backgroundLightness"] <= 15 for e in entries),
        "bodyContrast":all(p["contrast"] >= 7 for p in articles),
        "smallTextContrast":all(not e["smallContrastFailures"] for e in entries),
        "readingMetrics":all(17 <= p["fontSize"] <= 19 and p["lineHeight"] >= 1.75 for p in articles) and 32 <= desktop["charsPerLine"] <= 40,
        "mobileGutters":min(report["views"]["article"]["mobile"]["prose"][side] for side in ("left","right")) >= 16,
        "touchTargets":all(not e["shortTargets"] for e in entries),
        "focusVisible":all(e["focusPass"] for e in entries),
        "interactions":all(all_pass(e["interactions"]) for e in entries),
        "growthStress":all(report["views"]["articles"][s]["growthStress"]["pass"] for s,_,_ in VIEWPORTS),
        "wideContent":all(report["views"]["article"][s]["wideContent"]["pass"] for s,_,_ in VIEWPORTS),
        "noindex":all(e["robots"] == "noindex,nofollow" for e in entries),
        "reducedMotion":report["reducedMotion"],
        "categoryRedirect":report["categoryRedirect"]["status"] == 200 and report["categoryRedirect"]["url"].rstrip("/").endswith("/articles"),
    }
    for size,_,_ in VIEWPORTS:
        target = folder / ("contact-" + size + ".jpg")
        sheet(folds[size], target, 390 if size == "mobile" else 480)
        report["screenshots"][size] = str(target.relative_to(REPO))
    report["allGatesPass"] = all(report["gates"].values())
    save_json(folder / "gates.json", report)
    save_json(REPO / "src" / "data" / "preview-audit" / (args.design + ".gates.json"), report)
    print(args.design + " round " + str(args.round) + ": " + ("PASS" if report["allGatesPass"] else "FAIL"))
    print("failed=" + ", ".join(k for k,v in report["gates"].items() if not v))
    print("evidence=" + str(folder))
    if report["errors"]:
        print("errors=" + json.dumps(report["errors"], ensure_ascii=False))
    return 0 if report["allGatesPass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
