# 周尚礼 · 个人博客与作品集

使用 Astro 构建的中英双语个人网站：首页、作品、笔记、教学四个栏目，另提供独立的个人经历页。采用午夜藏书室的深蓝、象牙白与旧铜色设计，仅提供深色主题。首次访问默认中文，语言选择会保存在浏览器本地，刷新与跨页面访问时保持。项目列表在悬停或键盘选中时显示该行的图片背景；手机点击直接进入详情。

正式站点地址：<https://zhoushangli.github.io>

## 页面结构

| 路由 | 内容 |
| --- | --- |
| `/` | 简介、完整教育与实习经历、作品、笔记、教学及个人兴趣 |
| `/experience/` | 个人介绍、完整教育与实习经历、技能 |
| `/projects/` | 项目作品总览（个人 / 团队分类） |
| `/projects/<slug>/` | 项目详情：平台、状态、开发时间、项目介绍、团队职责、功能、实现和开发进展 |
| `/articles/` | 笔记总览（按分类筛选） |
| `/articles/<contentId>/` | 笔记详情：双语正文、左侧目录、图注、代码、表格与视频 |
| `/teaching/` | 教学总览 |
| `/teaching/<contentId>/` | 课程、作业、案例与 Game Jam 作品展详情 |

`/previews/` 提供六套暗色古典博客方向对比，每套包含首页、文章索引与阅读示例，并展示独立评审结果。历史三案仍保留。所有预览已设置 `noindex` 且不进入 sitemap；浏览与评审流程见 [`docs/design-previews.md`](docs/design-previews.md)。

## 双语内容维护

正式内容位于 `src/content/published/`，由 `src/content.config.ts` 在构建时加载：

```
src/content/published/
├─ articles/<contentId>.zh.md   # 中文
├─ articles/<contentId>.en.md   # 英文
└─ teaching/<contentId>.zh.md / .en.md
```

- 同一篇内容用相同的 `contentId` 维护中文、英文两个文件，图片与附件共享（放在 `public/media/`）。
- frontmatter 字段：`contentId`、`lang`、`section`、`title`、`description`、`category`、`tags`、`relatedProject`（可选）、`draft`。
- 生成页面时会校验：同一 `contentId` 缺少任一语言、或中英文 `category` / `relatedProject` 不一致，构建直接失败。
- `draft: true` 的内容不生成页面，也不进入公开列表与 sitemap（成对内容任一语言为草稿即整体不发布）。MingEngine 三组、SpectreX 两组文章已设为草稿，源文件保留。
- 标题锚点按语言加前缀（`zh-` / `en-`），保证同一页面两种语言的目录锚点不重名。
- `src/content/articles/` 下是早期随笔与 Obsidian 提示词，不在集合加载范围内，不会发布。

## 项目与教学数据

- `src/data/projects.ts`：项目条目。技术栈最多三项；`media.alt` 描述画面，`media.caption` 是可选双语图注。
- `src/components/ExperienceTimeline.astro`：首页与独立经历页共用的教育、实习记录。
- 左上主导航固定，左下按页面显示项目、内容列表或本文目录；正文目录通过布局的 `sidebar` 插槽传入。
- `src/data/gamejam.ts`：PICO-8 卡带提交清单，含原件文件名与 SHA-256；卡带文件位于 `public/downloads/gamejam-2026/`。
- `src/data/content.ts`：内容分类与中英文配对读取逻辑。

## 本地开发

```sh
npm install
npm run dev      # http://127.0.0.1:4321
npm run build    # 输出到 dist/
npm run preview  # 预览构建结果
```

要求 Node.js >= 22.12.0。

正式页面改动后，先运行 `npm run build`，再在另一个终端用 `npm run preview -- --host 127.0.0.1 --port 4323` 启动构建产物，执行 `python scripts/verify-portfolio.py`。检查覆盖 21 个正式路由、中英文及 1440/1024/390px，验证深色主题、语言记忆、项目行背景、目录、筛选和下载。结果与截图位于 `artifacts/preview-audit/site-migration/`；该目录仅保留在本机。

无浏览器时运行 `python scripts/verify-portfolio.py --static-only`，检查构建页面、链接与锚点、草稿隔离、共享经历、技术栈数量、媒体配置及下载文件哈希。静态检查不代表浏览器视觉或视频播放验收。

## 部署

推送到 `main` 分支后由 `.github/workflows/deploy.yml` 通过 `withastro/action` 构建并发布到 GitHub Pages。本轮不涉及远程推送与正式发布。

## 维护清单

素材来源、内容清单、已确认的措辞决策与仍待核实的事实见 [`docs/content-manifest.md`](docs/content-manifest.md)。
