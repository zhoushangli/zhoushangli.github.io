"""Capture screenshots and hard-gate evidence for one preview design slot.

e.g. python scripts/preview-audit/capture.py --design design-a --round 1
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = Path(
    r"C:\Users\Shangli Zhou\.codex\visualizations\2026\09\28\01a0e9ca-2d3d-73f2-a597-9a367465fd22\blog-designs"
)
DEFAULT_BASE = "http://127.0.0.1:4321"
VIEWS = ("home", "articles", "category", "article")
VIEWPORTS = (("desktop", 1440, 900), ("laptop", 1024, 768), ("mobile", 390, 844))
REMOTE_FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CSS_PRELUDE = """
const parseColor = (value) => {
  const match = value && value.match(/rgba?\\(([^)]+)\\)/);
  if (!match) return null;
  const parts = match[1].split(/[,\\s/]+/).filter(Boolean).map(Number);
  if (parts.length < 3) return null;
  return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
};
const relLum = (c) => {
  const f = (v) => { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
};
const describe = (el) => {
  const cls = typeof el.className === 'string' && el.className.trim()
    ? '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.')
    : '';
  return el.tagName.toLowerCase() + cls;
};
"""

METRICS_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const de = document.documentElement;
  const vw = de.clientWidth;
  const offenders = [];
  for (const el of document.querySelectorAll('body *')) {
    const rect = el.getBoundingClientRect();
    if (rect.width < 2 || rect.height < 2) continue;
    if (rect.right > vw + 1 || rect.left < -1) {
      offenders.push({ sel: describe(el), left: Math.round(rect.left), right: Math.round(rect.right) });
    }
  }
  const broken = [...document.images].filter((i) => i.complete && i.naturalWidth === 0);
  return {
    viewportWidth: vw,
    scrollWidth: de.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    overflow: Math.max(de.scrollWidth, document.body.scrollWidth) - vw,
    offenders: offenders.slice(0, 12),
    offenderCount: offenders.length,
    imageCount: document.images.length,
    brokenImages: broken.map((i) => i.currentSrc || i.src),
    pendingImages: [...document.images].filter((i) => !i.complete).length,
    title: document.title,
    robots: (document.querySelector('meta[name=robots]') || {}).content || null,
    dmSansLoaded: document.fonts ? document.fonts.check('16px "DM Sans"') : null,
  };
}"""
)

BACKGROUND_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const read = (el) => {
    const cs = getComputedStyle(el);
    return {
      tag: el.tagName.toLowerCase(),
      color: cs.backgroundColor,
      image: cs.backgroundImage === 'none' ? null : cs.backgroundImage.slice(0, 80),
    };
  };
  return { body: read(document.body), html: read(document.documentElement) };
}"""
)

TEXT_BOXES_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const pick = (key, sel) => {
    const el = document.querySelector(sel);
    if (!el) return { key, sel, found: false };
    const rect = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return {
      key, sel, found: true,
      x: Math.round(rect.x), y: Math.round(rect.y),
      w: Math.round(rect.width), h: Math.round(rect.height),
      color: cs.color,
      fontSize: parseFloat(cs.fontSize),
      lineHeight: parseFloat(cs.lineHeight) || null,
      letterSpacing: cs.letterSpacing,
      text: (el.textContent || '').trim().slice(0, 20),
    };
  };
  return [
    pick('heroIntro', '.hero-intro'),
    pick('aboutBody', '.home-about p:last-child'),
    pick('essayLead', '.essay-body .lead'),
    pick('essayBody', '.essay-body section p'),
    pick('essaySectionTitle', '.essay-body h2'),
    pick('metaSmall', '.article-date'),
  ];
}"""
)

TOUCH_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const groups = [
    ['nav', '.site-header nav a'],
    ['brand', '.site-header .brand'],
    ['action', '.button-primary'],
    ['action-text', '.button-text'],
    ['all-link', '.all-link'],
    ['category-card', '.category-card'],
    ['footer-link', '.site-footer a'],
  ];
  const targets = [];
  for (const [group, sel] of groups) {
    for (const el of document.querySelectorAll(sel)) {
      const rect = el.getBoundingClientRect();
      if (rect.width < 1 || rect.height < 1) continue;
      targets.push({ group, sel: describe(el), w: Math.round(rect.width), h: Math.round(rect.height) });
    }
  }
  const gated = targets.filter((t) => t.group === 'nav' || t.group === 'brand' || t.group === 'action');
  return {
    targets,
    gatedCount: gated.length,
    failing: gated.filter((t) => t.h < 44),
    smallest: gated.length ? Math.min(...gated.map((t) => t.h)) : null,
  };
}"""
)

FOCUS_BASELINE_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const snap = (el) => {
    const cs = getComputedStyle(el);
    return [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow, cs.backgroundColor, cs.color, cs.textDecorationLine].join('|');
  };
  const list = [...document.querySelectorAll('a[href], button')].slice(0, 16);
  window.__focusList = list;
  window.__focusBaseline = list.map(snap);
  return { focusable: list.length };
}"""
)

FOCUS_STEP_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const list = window.__focusList || [];
  const active = document.activeElement;
  const idx = list.indexOf(active);
  if (idx < 0) return { idx: -1, changed: false, tag: active ? active.tagName.toLowerCase() : null };
  const cs = getComputedStyle(active);
  const now = [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow, cs.backgroundColor, cs.color, cs.textDecorationLine].join('|');
  return {
    idx, changed: now !== window.__focusBaseline[idx], tag: active.tagName.toLowerCase(),
    text: (active.textContent || '').trim().slice(0, 12),
  };
}"""
)

CATEGORY_ROWS_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const rows = [...document.querySelectorAll('[data-article-topic]')];
  const expected = {};
  for (const row of rows) {
    const key = row.dataset.articleTopic;
    expected[key] = (expected[key] || 0) + 1;
  }
  const visible = rows.filter((row) => {
    const cs = getComputedStyle(row);
    return cs.display !== 'none' && cs.visibility !== 'hidden' && !row.hidden && row.offsetHeight > 0;
  });
  return {
    rowCount: rows.length,
    topics: [...document.querySelectorAll('[data-topic]')].map((c) => c.dataset.topic),
    expected,
    visibleCount: visible.length,
    visibleTopics: [...new Set(visible.map((r) => r.dataset.articleTopic))],
    selectedLabel: (document.querySelector('#selected-category') || {}).textContent || null,
  };
}"""
)

STRESS_JS = (
    "() => {"
    + CSS_PRELUDE
    + """
  const rows = [...document.querySelectorAll('.article-row')];
  if (!rows.length) return { ok: false, reason: 'no .article-row found' };
  const parent = rows[0].parentElement;
  const before = rows.length;
  let guard = 0;
  while (document.querySelectorAll('.article-row').length < 15 && guard < 60) {
    const src = rows[guard % rows.length];
    const clone = src.cloneNode(true);
    clone.removeAttribute('id');
    parent.appendChild(clone);
    guard += 1;
  }
  const after = document.querySelectorAll('.article-row').length;
  const heights = [...document.querySelectorAll('.article-row')].map((r) => Math.round(r.getBoundingClientRect().height));
  const de = document.documentElement;
  return {
    ok: true, before, after,
    overflow: Math.max(de.scrollWidth, document.body.scrollWidth) - de.clientWidth,
    minRowHeight: Math.min(...heights),
    squashedRows: heights.filter((h) => h < 24).length,
  };
}"""
)


def srgb_channel(value: float) -> float:
    value = value / 255.0
    return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (srgb_channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    high, low = max(relative_luminance(fg), relative_luminance(bg)), min(
        relative_luminance(fg), relative_luminance(bg)
    )
    return (high + 0.05) / (low + 0.05)


def hsl_lightness(rgb: tuple[int, int, int]) -> float:
    r, g, b = (v / 255.0 for v in rgb)
    return (max(r, g, b) + min(r, g, b)) / 2 * 100


def parse_css_color(value: str | None) -> tuple[int, int, int] | None:
    if not value:
        return None
    value = value.strip()
    if value.startswith("rgb"):
        parts = value[value.find("(") + 1 : value.find(")")].replace("/", " ").replace(",", " ").split()
        if len(parts) < 3:
            return None
        if len(parts) > 3 and float(parts[3]) < 0.9:
            return None
        return tuple(int(float(parts[i])) for i in range(3))  # type: ignore[return-value]
    return None


def dominant_color(image: Image.Image, box: tuple[int, int, int, int] | None = None) -> tuple[int, int, int]:
    region = image.convert("RGB")
    if box:
        region = region.crop(box)
    region = region.resize((min(region.width, 320), max(1, min(region.height, 320))))
    quantized = region.quantize(colors=8, method=Image.Quantize.MEDIANCUT).convert("RGB")
    return Counter(quantized.getdata()).most_common(1)[0][0]


def sample_background(image: Image.Image, box: dict) -> tuple[int, int, int] | None:
    width, height = image.size
    x0 = max(0, min(box["x"], width - 2))
    y0 = max(0, min(box["y"], height - 2))
    x1 = min(width, max(x0 + 2, box["x"] + box["w"]))
    y1 = min(height, max(y0 + 2, box["y"] + min(box["h"], 260)))
    if x1 - x0 < 4 or y1 - y0 < 4:
        return None
    return dominant_color(image, (x0, y0, x1, y1))


def text_metrics(box: dict, image: Image.Image, checks: list[dict]) -> None:
    if not box.get("found") or box["w"] < 40 or box["h"] < 8:
        return
    fg = parse_css_color(box["color"])
    bg = sample_background(image, box)
    entry = {
        "key": box["key"],
        "sel": box["sel"],
        "fontSize": box["fontSize"],
        "lineHeight": box["lineHeight"],
        "lineHeightRatio": round(box["lineHeight"] / box["fontSize"], 2) if box["lineHeight"] else None,
        "width": box["w"],
        "charsPerLine": round(box["w"] / box["fontSize"], 1) if box["fontSize"] else None,
        "sample": box["text"],
    }
    if fg and bg:
        entry["fg"] = "#%02x%02x%02x" % fg
        entry["bgSampled"] = "#%02x%02x%02x" % bg
        entry["contrast"] = round(contrast_ratio(fg, bg), 2)
    checks.append(entry)


def label_strip(draw: ImageDraw.ImageDraw, size: tuple[int, int], text: str) -> None:
    draw.rectangle([0, 0, size[0], 22], fill=(18, 18, 20))
    draw.text((8, 6), text, fill=(235, 235, 240))


def stack_images(images: list[tuple[str, Image.Image]], width: int, gap: int = 10) -> Image.Image:
    scaled = []
    for label, image in images:
        ratio = width / image.width
        scaled.append((label, image.resize((width, max(1, int(image.height * ratio))), Image.LANCZOS)))
    height = sum(img.height + 24 + gap for _, img in scaled)
    sheet = Image.new("RGB", (width, height), (10, 10, 12))
    draw = ImageDraw.Draw(sheet)
    y = 0
    for label, img in scaled:
        label_strip(draw, (width, 22), label)
        y += 24
        sheet.paste(img, (0, y))
        y += img.height + gap
    return sheet


def grid_images(images: list[tuple[str, Image.Image]], cell_width: int, columns: int = 2) -> Image.Image:
    scaled = []
    for label, image in images:
        ratio = cell_width / image.width
        scaled.append((label, image.resize((cell_width, max(1, int(image.height * ratio))), Image.LANCZOS)))
    rows = (len(scaled) + columns - 1) // columns
    cell_height = max(img.height for _, img in scaled) + 26
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), (10, 10, 12))
    draw = ImageDraw.Draw(sheet)
    for index, (label, img) in enumerate(scaled):
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        label_strip(draw, (cell_width, 22), label)
        sheet.paste(img, (x, y + 24))
    return sheet


def save_thumbnail(image: Image.Image, target: Path, width: int = 900) -> int:
    ratio = width / image.width
    resized = image.resize((width, max(1, int(image.height * ratio))), Image.LANCZOS)
    target.parent.mkdir(parents=True, exist_ok=True)
    quality = 72
    while quality >= 40:
        resized.save(target, "WEBP", quality=quality, method=5)
        if target.stat().st_size <= 150 * 1024:
            break
        quality -= 8
    return target.stat().st_size


def run(args: argparse.Namespace) -> int:
    design: str = args.design
    round_no: int = args.round
    base: str = args.base.rstrip("/")
    out_root: Path = args.out
    round_dir = out_root / design / f"round-{round_no}"
    shots_dir = round_dir / "shots"
    shots_dir.mkdir(parents=True, exist_ok=True)
    audit_dir = REPO / "src" / "data" / "preview-audit"
    audit_dir.mkdir(parents=True, exist_ok=True)

    screenshots: dict[str, dict[str, Image.Image]] = {view: {} for view in VIEWS}
    console_errors: list[str] = []
    network_errors: list[str] = []
    report: dict = {
        "design": design,
        "round": round_no,
        "base": base,
        "capturedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "views": {},
        "gates": {},
        "notes": [],
    }

    def on_console(message) -> None:
        if message.type != "error":
            return
        text = message.text
        try:
            url = (message.location or {}).get("url") or ""
        except Exception:
            url = ""
        if any(host in text or host in url for host in REMOTE_FONT_HOSTS):
            network_errors.append(f"{text} ({url})")
        elif url and not url.startswith(base) and "ERR_" in text:
            network_errors.append(f"{text} ({url})")
        else:
            console_errors.append(f"{text} ({url})" if url else text)

    def on_response(response) -> None:
        if response.status < 400:
            return
        url = response.url
        if any(host in url for host in REMOTE_FONT_HOSTS):
            network_errors.append(f"{response.status} {url}")
        else:
            console_errors.append(f"{response.status} {url}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(device_scale_factor=1)
        for name, width, height in VIEWPORTS:
            page = context.new_page()
            page.set_viewport_size({"width": width, "height": height})
            page.on("console", on_console)
            page.on("response", on_response)
            for view in VIEWS:
                url = f"{base}/previews/{design}/{view}"
                view_report = report["views"].setdefault(view, {})
                page.goto(url, wait_until="load", timeout=45000)
                page.wait_for_timeout(450)
                path = shots_dir / f"{view}-{width}.png"
                page.screenshot(path=str(path), full_page=True)
                image = Image.open(path).convert("RGB")
                screenshots[view][name] = image

                metrics = page.evaluate(METRICS_JS)
                entry = {
                    "url": url,
                    "overflow": metrics["overflow"],
                    "offenderCount": metrics["offenderCount"],
                    "offenders": metrics["offenders"][:6],
                    "brokenImages": metrics["brokenImages"],
                    "imageCount": metrics["imageCount"],
                    "pendingImages": metrics["pendingImages"],
                    "title": metrics["title"],
                    "robots": metrics["robots"],
                    "dmSansLoaded": metrics["dmSansLoaded"],
                }

                if name == "desktop":
                    backgrounds = page.evaluate(BACKGROUND_JS)
                    dominant = dominant_color(image)
                    surface = (
                        parse_css_color(backgrounds["body"]["color"])
                        or parse_css_color(backgrounds["html"]["color"])
                        or dominant
                    )
                    entry["background"] = {
                        "body": backgrounds["body"],
                        "html": backgrounds["html"],
                        "dominantColor": "#%02x%02x%02x" % dominant,
                        "surfaceColor": "#%02x%02x%02x" % surface,
                        "surfaceLightness": round(hsl_lightness(surface), 1),
                    }
                    text_checks: list[dict] = []
                    for box in page.evaluate(TEXT_BOXES_JS):
                        text_metrics(box, image, text_checks)
                    entry["text"] = text_checks
                    focus_baseline = page.evaluate(FOCUS_BASELINE_JS)
                    stops = []
                    for _ in range(10):
                        page.keyboard.press("Tab")
                        stops.append(page.evaluate(FOCUS_STEP_JS))
                    visible_stops = [s for s in stops if s.get("changed")]
                    entry["focus"] = {
                        "focusable": focus_baseline["focusable"],
                        "stops": len(stops),
                        "distinctTargets": len({s.get("idx") for s in stops if s.get("idx", -1) >= 0}),
                        "visibleStops": len(visible_stops),
                        "sample": stops[:6],
                    }

                if name in ("desktop", "mobile"):
                    entry["touch"] = page.evaluate(TOUCH_JS)

                if view == "category" and name == "desktop":
                    baseline = page.evaluate(CATEGORY_ROWS_JS)
                    filters = []
                    for topic in baseline["topics"]:
                        page.goto(f"{url}?topic={topic}", wait_until="load", timeout=45000)
                        page.wait_for_timeout(250)
                        state = page.evaluate(CATEGORY_ROWS_JS)
                        filters.append(
                            {
                                "topic": topic,
                                "visibleCount": state["visibleCount"],
                                "expected": baseline["expected"].get(topic),
                                "visibleTopics": state["visibleTopics"],
                                "selectedLabel": state["selectedLabel"],
                                "ok": state["visibleCount"] == baseline["expected"].get(topic)
                                and state["visibleTopics"] == [topic],
                            }
                        )
                    entry["categoryFilter"] = {"baseline": baseline, "filters": filters}
                    page.goto(url, wait_until="load", timeout=45000)
                    page.wait_for_timeout(250)

                if view == "articles" and name in ("desktop", "mobile"):
                    entry["growthStress"] = page.evaluate(STRESS_JS)
                    page.goto(url, wait_until="load", timeout=45000)
                    page.wait_for_timeout(200)

                view_report[name] = entry
            page.close()
        context.close()
        browser.close()

    fold_sheet = grid_images(
        [(f"{view} 1440", screenshots[view]["desktop"].crop((0, 0, 1440, min(1150, screenshots[view]["desktop"].height))))
         for view in VIEWS],
        cell_width=800,
    )
    fold_sheet.save(round_dir / "fold-desktop.jpg", "JPEG", quality=80)
    stack_images([(f"{view} 1440 full", screenshots[view]["desktop"]) for view in VIEWS], width=620).save(
        round_dir / "contact-desktop.jpg", "JPEG", quality=78
    )
    stack_images([(f"{view} 390 full", screenshots[view]["mobile"]) for view in VIEWS], width=300).save(
        round_dir / "contact-mobile.jpg", "JPEG", quality=78
    )

    thumbnails = {}
    for view in VIEWS:
        target = REPO / "public" / "previews-audit" / f"{design}-{view}.webp"
        thumbnails[view] = {
            "path": f"/previews-audit/{design}-{view}.webp",
            "bytes": save_thumbnail(screenshots[view]["desktop"], target),
        }

    # 1) Apply the hard gates from the collected evidence.
    # 2) Record every failing gate with the view it came from.
    def all_views(predicate) -> bool:
        return all(predicate(report["views"][view][name]) for view in VIEWS for name in ("desktop", "laptop", "mobile"))

    category_ok = False
    category_entry = report["views"].get("category", {}).get("desktop", {})
    filters = category_entry.get("categoryFilter", {}).get("filters", [])
    if filters:
        category_ok = all(item["ok"] for item in filters)

    stress_entries = [
        report["views"]["articles"][name].get("growthStress", {}) for name in ("desktop", "mobile")
    ]
    stress_ok = all(
        entry.get("ok") and entry.get("overflow", 1) <= 0 and entry.get("squashedRows", 1) == 0
        for entry in stress_entries
    )

    desktop = report["views"]["article"]["desktop"]
    essay_contrast = next((t for t in desktop.get("text", []) if t["key"] == "essayBody"), {})
    essay_metrics = essay_contrast
    surface_lightness = desktop.get("background", {}).get("surfaceLightness", 100)
    focus = desktop.get("focus", {})
    mobile_touch_failures = {
        view: report["views"][view].get("mobile", {}).get("touch", {}).get("failing", []) for view in VIEWS
    }
    mobile_touch_smallest = {
        view: report["views"][view].get("mobile", {}).get("touch", {}).get("smallest") for view in VIEWS
    }
    touch_ok = bool(desktop.get("touch")) and all(not failures for failures in mobile_touch_failures.values())

    gates = {
        "routesLoaded": all_views(lambda entry: entry["title"] is not None),
        "noConsoleErrors": not console_errors,
        "noBrokenImages": all_views(lambda entry: not entry["brokenImages"]),
        "noHorizontalOverflow": all_views(lambda entry: entry["overflow"] <= 1),
        "darkSurface": surface_lightness <= 15,
        "bodyContrast": bool(essay_contrast) and essay_contrast.get("contrast", 0) >= 7,
        "touchTargets": touch_ok,
        "focusVisible": bool(focus) and focus.get("visibleStops", 0) >= 6 and focus.get("distinctTargets", 0) >= 3,
        "categoryFilter": category_ok,
        "growthStress": stress_ok,
    }
    report["gates"] = gates
    report["gateEvidence"] = {
        "consoleErrors": console_errors[:10],
        "networkErrors": network_errors[:10],
        "surfaceLightnessPercent": surface_lightness,
        "essayBodyContrast": essay_contrast.get("contrast"),
        "essayBodyCharsPerLine": essay_metrics.get("charsPerLine"),
        "essayBodyLineHeightRatio": essay_contrast.get("lineHeightRatio"),
        "essayBodyFontSize": essay_contrast.get("fontSize"),
        "touchSmallestHeightMobile": mobile_touch_smallest,
        "touchFailingMobile": {view: failures[:6] for view, failures in mobile_touch_failures.items() if failures},
        "touchSmallestHeightDesktop": desktop.get("touch", {}).get("smallest"),
        "touchFailingDesktop": desktop.get("touch", {}).get("failing", [])[:6],
        "focusVisibleStops": focus.get("visibleStops"),
        "focusDistinctTargets": focus.get("distinctTargets"),
        "categoryFilters": filters,
        "growthStress": stress_entries,
        "overflowByView": {
            f"{view}/{name}": report["views"][view][name]["overflow"] for view in VIEWS for name in ("desktop", "mobile")
        },
    }
    report["screenshots"] = {
        "round": str(round_dir),
        "foldDesktop": str(round_dir / "fold-desktop.jpg"),
        "contactDesktop": str(round_dir / "contact-desktop.jpg"),
        "contactMobile": str(round_dir / "contact-mobile.jpg"),
    }
    report["thumbnails"] = thumbnails
    report["allGatesPass"] = all(gates.values())

    target = audit_dir / f"{design}.gates.json"
    target.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    print(f"design={design} round={round_no} gates={'PASS' if report['allGatesPass'] else 'FAIL'}")
    for key, value in gates.items():
        print(f"  {'ok  ' if value else 'FAIL'} {key}")
    if console_errors:
        print(f"  console errors: {console_errors[:3]}")
    print(
        f"  surfaceL={surface_lightness}% bodyContrast={essay_contrast.get('contrast')} "
        f"charsPerLine={essay_metrics.get('charsPerLine')} lineHeight={essay_contrast.get('lineHeightRatio')}"
    )
    print(f"  report -> {target}")
    print(f"  sheets -> {round_dir}")
    return 0 if report["allGatesPass"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture preview screenshots and hard-gate evidence.")
    parser.add_argument("--design", required=True, help="design slot id, for example design-a")
    parser.add_argument("--round", type=int, default=1, help="review round number")
    parser.add_argument("--base", default=DEFAULT_BASE, help="preview server origin")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="screenshot output root")
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
