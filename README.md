# 周尚礼 · 个人博客与作品集

使用 Astro 构建的中英双语个人网站：个人介绍与经历、项目作品、技术研究与开发笔记、教学与社群实践四个栏目。首次访问默认中文，语言与明暗主题的选择会保存在浏览器本地，刷新与跨页面访问时保持。

正式站点地址：<https://zhoushangli.github.io>

## 页面结构

| 路由 | 内容 |
| --- | --- |
| `/` | 个人介绍、教育、实习经历、技能、联系方式、各栏目精选入口与个人兴趣 |
| `/projects/` | 项目作品总览（个人 / 团队分类） |
| `/projects/<slug>/` | 项目详情：平台、状态、开发时间、职责、关键实现、取舍与反思、关联文章 |
| `/articles/` | 技术研究与开发笔记总览（按分类筛选） |
| `/articles/<contentId>/` | 文章详情：双语正文、目录、图注、代码、表格与视频 |
| `/teaching/` | 教学与社群实践总览 |
| `/teaching/<contentId>/` | 课程、作业、案例与 Game Jam 作品展详情 |

`/previews/` 下是历史设计稿对比页，保留用于回顾，已设置 `noindex` 且不进入 sitemap。

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
- `draft: true` 的内容不进入公开列表与 sitemap（成对内容任一语言为草稿即整体不发布）。
- 标题锚点按语言加前缀（`zh-` / `en-`），保证同一页面两种语言的目录锚点不重名。
- `src/content/articles/` 下是早期随笔与 Obsidian 提示词，不在集合加载范围内，不会发布。

## 项目与教学数据

- `src/data/projects.ts`：项目条目（分类、摘要、职责、技术、取舍、局限、关联文章、媒体）。
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

## 部署

推送到 `main` 分支后由 `.github/workflows/deploy.yml` 通过 `withastro/action` 构建并发布到 GitHub Pages。本轮不涉及远程推送与正式发布。

## 维护清单

素材来源、内容清单、已确认的措辞决策与仍待核实的事实见 [`docs/content-manifest.md`](docs/content-manifest.md)。
