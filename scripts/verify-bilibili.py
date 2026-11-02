"""Check imported articles, source text, local images and built series navigation.

e.g. python scripts/verify-bilibili.py (after npm run build)
"""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bilibili_import", ROOT / "scripts/import-bilibili.py")
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)
manifest = json.loads((ROOT / "docs/bilibili-import.json").read_text(encoding="utf-8"))
assert len(manifest) == 15
assert sum(item["sourceImageCount"] for item in manifest) == 349
assert sum(item["platformDividers"] for item in manifest) == 88
counts = {"ori2-level-analysis": 7, "celeste-level-analysis": 8}
references = 0
unique_images = set()
for series, count in counts.items():
    articles = [item for item in manifest if item["slug"].startswith(series + "-")]
    assert len(articles) == count
    overview = BeautifulSoup((ROOT / f"dist/articles/{series}/index.html").read_text(encoding="utf-8"), "html.parser")
    chapters = overview.select_one(".series-chapters")
    assert len(chapters.select("li a")) == count
    assert [link["href"] for link in chapters.select("li a")] == [f"/articles/{item['slug']}/" for item in articles]
    for index, item in enumerate(articles):
        markdown = (ROOT / f"src/content/published/articles/{item['slug']}.zh.md").read_text(encoding="utf-8")
        body = markdown.split("---", 2)[2]
        assert importer.text_hash(body) == item["textSha256"], (item["slug"], "body text")
        page = BeautifulSoup((ROOT / f"dist/articles/{item['slug']}/index.html").read_text(encoding="utf-8"), "html.parser")
        prose = page.select_one("[data-chinese-only] .prose")
        assert prose and not prose.find_parent(attrs={"data-language-block": True})
        assert page.select_one(".content-language-note")["data-en"].startswith("This article")
        assert not prose.select("[style], [contenteditable], script, iframe")
        assert [image["src"] for image in prose.select("img")] == [image["local"] for image in item["images"]]
        assert len(prose.select("hr")) == item["platformDividers"]
        previous, following = page.select_one('a[rel="prev"]'), page.select_one('a[rel="next"]')
        assert (previous["href"] if previous else None) == (f"/articles/{articles[index - 1]['slug']}/" if index else None)
        assert (following["href"] if following else None) == (f"/articles/{articles[index + 1]['slug']}/" if index + 1 < count else None)
        for image, node in zip(item["images"], prose.select("img")):
            path = ROOT / "public" / image["local"].lstrip("/")
            assert hashlib.sha256(path.read_bytes()).hexdigest() == image["sha256"]
            with Image.open(path) as decoded:
                assert decoded.size == (int(node["width"]), int(node["height"]))
                decoded.verify()
            assert node["alt"] and node["loading"] == "lazy"
            assert node.parent.name == "a" and node.parent["href"] == image["local"]
            references += 1
            unique_images.add(image["local"])
home = BeautifulSoup((ROOT / "dist/index.html").read_text(encoding="utf-8"), "html.parser")
index_page = BeautifulSoup((ROOT / "dist/articles/index.html").read_text(encoding="utf-8"), "html.parser")
for series in counts:
    assert home.select_one(f'#articles a[href="/articles/{series}"]')
    assert index_page.select_one(f'.reading-grid a[href="/articles/{series}"]')
assert len(index_page.select(".reading-card")) == 4
print(json.dumps({"articles": len(manifest), "series": len(counts), "imageReferences": references, "uniqueImages": len(unique_images), "textAndNavigation": "pass"}, indent=2))
