# B 站关卡分析导入

本次范围为两个系列入口和 15 篇中文正文：

| 系列 | 博客入口 | 原文集 | 篇数 |
| --- | --- | --- | --- |
| 《奥日2》关卡拆解 | `/articles/ori2-level-analysis/` | <https://www.bilibili.com/read/readlist/rl762254> | 7 |
| 《蔚蓝》关卡拆解 | `/articles/celeste-level-analysis/` | <https://www.bilibili.com/read/readlist/rl735828> | 8 |

正文位于 `src/content/published/articles/*-level-analysis-*.zh.md`。系列入口使用相同前缀、不带章节序号。首页和笔记列表展示入口，正文提供系列目录、上一篇和下一篇。沿用现有游戏机制与设计分类、深色主题、阅读宽度和手机导航。

## 内容与语言

- 保留原来的分篇、段落、图片顺序、图注、房间编号和分析判断，只修正明确的错字。
- 房间编号提升为二级标题；没有房间编号的文章使用“路线分析”作为正文目录入口。
- 原图注有内容时保留，空图注不生成空白区域。缺少图注的图片使用文章名与图号作为替代文本。
- 88 处重复的 B 站图标分隔线改为博客细线，全部 261 张实际截图与顺序保留；分隔线替换数量逐篇记入清单。
- 首次发布日期按北京时间记录，每篇保留 B 站原文链接。
- `chineseOnly: true` 表示尚无英文译文；英文界面保留中文正文与目录，并明确提示，不生成占位英文文章。
- 每项错字修正和文章正文的文本哈希记录在 `bilibili-import.json`，便于检查是否出现额外改写。

## 图片和原始记录

网页图片位于 `public/media/level-analysis/`，使用原始分辨率的无损 WebP。导入时逐张对比 RGBA 像素，保证截图和标注不因压缩改变；点击图片在新标签页查看完整分辨率。页面采用懒加载，不依赖 B 站图片外链。

原始 API JSON 与原始图片保存在本机 `artifacts/bilibili/`，该目录被 Git 忽略。可追踪的来源、图片路径及文件哈希记录在 `bilibili-import.json`。

## 导入与验证

`python scripts/import-bilibili.py` 使用公开接口并缓存成功结果，遇到限频等待后重试。需要 Python 的 requests、beautifulsoup4、Pillow 和时区数据。再次运行会根据缓存重新生成这 17 篇内容，人工编辑后应先比对变更。

```sh
npm run build
python scripts/verify-portfolio.py --static-only
python scripts/verify-bilibili.py
```

最后一项检查 15 篇正文的文本哈希、截图完整性、原图链接、两个系列目录与章节前后顺序。浏览器验证使用既有 `scripts/verify-portfolio.py --base <本机预览地址>`。

2026-11-02 验证结果：

- `npm run build` 通过，生成 68 个页面，其中正式页面 30 个。
- 静态检查通过：1,129 个本地链接、214 个锚点及既有草稿隔离检查。
- 导入专项检查通过：15 篇正文、2 个系列、261 张截图的文件哈希与尺寸、章节顺序与前后导航。
- 浏览器检查通过：30 个正式路由 × 1440/1024/390px × 中文/英文界面，共 180 组页面。
- 单独确认：英文界面下中文正文持续可见，语言选择跨章节保留，原图弹窗显示完整分辨率，手机目录点击定位与收起正常。
- 桌面与手机代表页面截图已检查，保存在本机 `artifacts/bilibili/`；全站浏览器结果位于 `artifacts/preview-audit/site-migration/verification.json`。

本次仅修改本地项目，未推送或发布。
