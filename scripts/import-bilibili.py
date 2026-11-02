"""Import the two public level-analysis series without rewriting their content.

e.g. python scripts/import-bilibili.py (requires requests, beautifulsoup4 and Pillow)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "artifacts/bilibili"
CONTENT = ROOT / "src/content/published/articles"
MEDIA = ROOT / "public/media/level-analysis"
SERIES = {
    762254: ("ori2-level-analysis", "《奥日2》关卡拆解", "水墨沼泽、夸洛克地穴与泉源，共 7 篇关卡分析。"),
    735828: ("celeste-level-analysis", "《蔚蓝》关卡拆解", "序章、城市与黄金山脊，共 8 篇关卡分析。"),
}
CORRECTIONS = {
    25290185: {"只要目的为": "主要目的为"},
    25299665: {"散发这荧光": "散发着荧光"},
    25305622: {"我们进度第1章": "我们进入第1章", "放在了与支线上": "放在了支线上", "会想做继续深入": "会想继续深入", "又用过边缘": "又通过边缘", "耐性观察": "耐心观察", "三次考研": "三次考验"},
    25323054: {"操作点的分布时": "操作点的分布是", "难度的考研": "难度的考验"},
    25688079: {"气泡八项突进": "气泡八向突进", "可见一般": "可见一斑", "向右挂起": "向右刮起", "向上走的行": "向上走就行", "利用风素": "利用风速", "这种考研": "这种考验"},
    25704874: {"显眼的哪一个": "显眼的那一个", "继续考研按钮": "继续考验按钮", "摄像机的那个部分": "摄像机的哪个部分"},
    25713294: {"机关来考研玩家": "机关来考验玩家", "考研移动砖块": "考验移动砖块", "风向的考研": "风向的考验"},
    25728966: {"那一面近": "哪一面近", "多个机关服用": "多个机关复用", "可见一般": "可见一斑", "所没的": "所没有的"},
    26985538: {"上来后一直莫基": "上来后一只莫基", "合适的事件给我们": "合适的时间给我们"},
    27006998: {"就可以会到原位置": "就可以回到原位置"},
    27028136: {"这也设计上的继承关系": "这也是设计上的继承关系", "哪里是一个可选的区域": "那里是一个可选的区域"},
    27051563: {"制作这在这里": "制作者在这里", "渐进时的设计": "渐进式的设计"},
    27106383: {"抓勾能力": "抓钩能力"},
}
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", "Referer": "https://www.bilibili.com/"})


# Cache successful public API responses so interrupted imports can resume.
# e.g. fetch("article", 25290185) reads the archived response on a second run.
def fetch(kind, ident):
    cache = ARCHIVE / f"{kind}-{ident}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    endpoint = "list/web/articles" if kind == "list" else "view"
    for attempt in range(5):
        params = {"id": ident, "jsonp": "jsonp", "from": "readlist"}
        if attempt:
            params["_ts"] = int(time.time())
        response = SESSION.get(f"https://api.bilibili.com/x/article/{endpoint}", params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        if result.get("code") == 0 and result.get("data"):
            cache.write_text(json.dumps(result["data"], ensure_ascii=False, indent=2), encoding="utf-8")
            time.sleep(3)
            return result["data"]
        print(f"Retry {kind} {ident}: {result.get('code')} {result.get('message')}", flush=True)
        time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"Could not read {kind} {ident}; cached successes were retained")


# Archive original images and publish full-resolution, pixel-identical WebP copies.
# e.g. download("//i0.hdslb.com/bfs/article/example.png") returns a local URL.
def download(url):
    url = "https:" + url if url.startswith("//") else url
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or not parsed.hostname.endswith(".hdslb.com"):
        raise ValueError(f"Unexpected image host: {url}")
    filename = Path(parsed.path).name
    if not re.fullmatch(r"[A-Za-z0-9_-]+\.(png|jpg|jpeg|webp|gif)", filename, re.I):
        raise ValueError(f"Unexpected image path: {url}")
    path = ARCHIVE / "images" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    legacy = MEDIA / filename
    if legacy.exists() and not path.exists():
        if not legacy.resolve().is_relative_to(MEDIA.resolve()) or not path.resolve().is_relative_to(ARCHIVE.resolve()):
            raise ValueError("Image migration escaped the import directories")
        legacy.replace(path)
    if not path.exists():
        for attempt in range(3):
            response = SESSION.get(url, timeout=45)
            if response.ok:
                path.write_bytes(response.content)
                break
            time.sleep(2 * (attempt + 1))
        else:
            response.raise_for_status()
    with Image.open(path) as image:
        width, height = image.size
        output = MEDIA / (path.stem + ".webp")
        if not output.exists():
            temporary = output.with_suffix(".webp.part")
            image.save(temporary, format="WEBP", lossless=True, exact=True, method=6)
            temporary.replace(output)
        with Image.open(output) as served:
            if image.convert("RGBA").tobytes() != served.convert("RGBA").tobytes():
                raise ValueError(f"Image pixels changed: {filename}")
    return f"/media/level-analysis/{output.name}", width, height, hashlib.sha256(output.read_bytes()).hexdigest()


# Keep source text and image order while replacing platform styling with site markup.
# e.g. a room number paragraph becomes a Markdown heading and screenshots link to originals.
def convert(article):
    soup = BeautifulSoup(article["content"], "html.parser")
    images = []
    allowed = {"p", "div", "figure", "figcaption", "img", "span", "strong", "b", "em", "i", "u", "s", "br", "h1", "h2", "h3", "h4", "blockquote", "ul", "ol", "li", "a", "table", "thead", "tbody", "tr", "th", "td", "hr", "sub", "sup"}
    for element in soup.find_all(True):
        if element.name not in allowed:
            raise ValueError(f"Unreviewed source element: {element.name}")
        element.attrs = {key: value for key, value in element.attrs.items() if key in ("src", "data-src", "href", "width", "height", "colspan", "rowspan")}
    for image in soup.find_all("img"):
        original = image.get("data-src") or image.get("src")
        if Path(urlsplit(original).path).name == "4adb9255ada5b97061e610b682b8636764fe50ed.png":
            figure = image.find_parent("figure")
            if not figure or figure.get_text(strip=True):
                raise ValueError("Platform divider unexpectedly contains text")
            figure.replace_with(soup.new_tag("hr"))
    sources = list(dict.fromkeys(image.get("data-src") or image.get("src") for image in soup.find_all("img")))
    with ThreadPoolExecutor(max_workers=4) as workers:
        downloaded = dict(zip(sources, workers.map(download, sources)))
    for index, image in enumerate(soup.find_all("img"), 1):
        original = image.get("data-src") or image.get("src")
        local, width, height, digest = downloaded[original]
        figure = image.find_parent("figure")
        if figure is None:
            figure = soup.new_tag("figure")
            image.wrap(figure)
        caption = figure.find("figcaption")
        label = caption.get_text(" ", strip=True) if caption else ""
        image.attrs = {"src": local, "alt": label or f"{article['title']} · 图 {index}", "width": width, "height": height, "loading": "lazy", "decoding": "async"}
        link = soup.new_tag("a", href=local, target="_blank", rel="noreferrer")
        link["aria-label"] = f"查看原图：{image['alt']}"
        image.wrap(link)
        if caption and not label:
            caption.decompose()
        images.append({"source": original, "local": local, "sha256": digest, "caption": label})
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if href.startswith("//"):
            link["href"] = "https:" + href
        elif href and not href.startswith(("https://", "http://", "/", "#")):
            raise ValueError(f"Unreviewed link: {href}")
    blocks = []
    for node in soup.contents:
        if getattr(node, "name", None) == "p":
            text = node.get_text(strip=True)
            if re.fullmatch(r"\d+(?:\.\d+)+", text):
                prefix = "##" if text.count(".") == 1 else "###"
                blocks.append(f"{prefix} {text}")
                continue
            if not text and not node.find("img"):
                continue
        blocks.append(str(node))
    body = "\n\n".join(blocks)
    if not any(block.startswith("## ") for block in blocks):
        body = "## 路线分析\n\n" + body
    return body, images


# Write schema-compatible Chinese entries with source and series metadata.
# e.g. write_entry(...) creates a .zh.md file without inventing an English translation.
def write_entry(slug, title, description, series, order, url, published, body):
    fields = {"contentId": slug, "lang": "zh", "section": "articles", "title": title, "description": description, "category": "gameplay", "tags": ["关卡设计", "游戏分析"], "chineseOnly": True, "seriesId": series, "seriesOrder": order, "sourceUrl": url, "publishedAt": published, "draft": False}
    frontmatter = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in fields.items())
    (CONTENT / f"{slug}.zh.md").write_text(f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8")


# Hash visible text independently of whitespace and HTML styling.
# e.g. text_hash("<p>0.1</p>") also matches the Markdown heading "## 0.1".
def text_hash(content):
    content = re.sub(r"(?m)^## (?:路线分析)\n", "", content)
    content = re.sub(r"(?m)^#{2,3} ", "", content)
    text = BeautifulSoup(content, "html.parser").get_text()
    return hashlib.sha256(re.sub(r"\s+", "", text).encode()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)
    manifest = []
    listings = {rid: fetch("list", rid) for rid in SERIES}
    for listing in listings.values():
        for item in listing["articles"]:
            fetch("article", item["id"])
            print(f"Source ready: cv{item['id']}", flush=True)
    for rid, (series, title, description) in SERIES.items():
        listing = listings[rid]
        for order, item in enumerate(listing["articles"], 1):
            article = fetch("article", item["id"])
            if not article.get("content"):
                raise ValueError(f"Empty body: {item['id']}")
            print(f"Importing cv{item['id']}: {article['title']}", flush=True)
            corrected = dict(article)
            corrections = []
            for before, after in CORRECTIONS.get(item["id"], {}).items():
                if before not in corrected["content"]:
                    raise ValueError(f"Typo correction no longer matches: {before}")
                corrected["content"] = corrected["content"].replace(before, after)
                corrections.append({"before": before, "after": after})
            body, images = convert(corrected)
            slug = f"{series}-{order:02}"
            published = datetime.fromtimestamp(article["publish_time"], timezone.utc).astimezone(ZoneInfo("Asia/Shanghai")).date().isoformat()
            source = f"https://www.bilibili.com/read/cv{item['id']}"
            write_entry(slug, article["title"], f"{title}系列 · 第 {order} 篇，共 {len(listing['articles'])} 篇。", series, order, source, published, body)
            if text_hash(corrected["content"]) != text_hash(body):
                raise ValueError(f"Visible source text changed: {slug}")
            source_image_count = len(BeautifulSoup(article["content"], "html.parser").find_all("img"))
            manifest.append({"id": item["id"], "slug": slug, "title": article["title"], "source": source, "publishedAt": published, "sourceHtmlSha256": hashlib.sha256(article["content"].encode()).hexdigest(), "textSha256": text_hash(body), "corrections": corrections, "sourceImageCount": source_image_count, "platformDividers": source_image_count - len(images), "images": images})
            print(f"Saved {slug}: {len(images)} images", flush=True)
        overview = "## 阅读范围\n\n" + ("这个系列按探索顺序拆解水墨沼泽、夸洛克地穴与泉源，保留各篇中的路线说明、截图和结构分析。" if rid == 762254 else "这个系列选取序章、第一章城市和第四章黄金山脊，按各篇中的房间编号阅读。第二、三章及其他章节不在本系列的分析范围内。")
        write_entry(series, title, description, series, 0, f"https://www.bilibili.com/read/readlist/rl{rid}", manifest[-len(listing['articles'])]["publishedAt"], overview)
    (ROOT / "docs/bilibili-import.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(manifest)} articles; {sum(len(a['images']) for a in manifest)} image references", flush=True)


if __name__ == "__main__":
    main()
