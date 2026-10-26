# 内容、素材与验证清单

本文件记录正式站点的内容清单、素材来源与校验结果、已确认的措辞决策、仍待核实的事实，以及本轮验证结论。最后更新：2026-10-26。

## 1. 站点结构与正式路由

正式路由 25 条（`npm run build` 共 62 页，其中 37 页为 `/previews/` 设计稿，已 `noindex` 且不进入 sitemap）：

```
/                                  个人介绍与经历（含教育、实习、技能、联系方式、兴趣、精选入口）
/projects/                         项目作品总览（个人 / 团队）
/projects/ming-engine/             项目详情
/projects/spectrex/
/projects/doomenstein/
/projects/the-primary-colors/
/projects/hamsterballin/
/articles/                         技术研究与开发笔记（分类筛选）
/articles/animal-well-rendering/
/articles/ming-csharp-bridge/
/articles/ming-gui-input/
/articles/ming-scene-resources/
/articles/sifu-combat-analysis/
/articles/spectrex-light-gameplay/
/articles/spectrex-rendering/
/teaching/                         教学与社群实践
/teaching/pico8-2026/
/teaching/pico8-intro/
/teaching/pico8-l01/
/teaching/pico8-l02/
/teaching/pico8-l03/
/teaching/pico8-a01/
/teaching/pico8-a02/
/teaching/pico8-object-organization/
/teaching/pico8-game-jam/
```

双语内容位于 `src/content/published/<section>/<contentId>.{zh,en}.md`，由 `src/content.config.ts` 加载；同一 `contentId` 必须有中英两份，缺一份或 `category`/`relatedProject` 不一致时构建失败。`src/content/articles/` 下是早期随笔与 Obsidian 提示词，不在集合范围内，确认不发布。

## 2. 文章清单（7 对）

| contentId | 中文标题 | 分类 | 关联项目 |
| --- | --- | --- | --- |
| animal-well-rendering | 《动物井》：从帧捕获理解分层渲染与光照合成 | graphics | — |
| ming-csharp-bridge | Ming：连接 C++ 对象与 C# 脚本 | engine | ming-engine |
| ming-gui-input | Ming：一次输入如何到达按钮 | engine | ming-engine |
| ming-scene-resources | Ming：节点、场景与资源如何连接起来 | engine | ming-engine |
| sifu-combat-analysis | 《师父》：攻守交替、硬直与反击窗口 | gameplay | — |
| spectrex-light-gameplay | SpectreX：让光路成为可交互的游戏规则 | gameplay | spectrex |
| spectrex-rendering | SpectreX：分层采集、光照与场景合成 | graphics | spectrex |

分类说明：「开发实践」当前没有匹配文章，因此筛选条只显示有内容的分类，不显示空分类按钮。

## 3. 教学清单（9 对）

| contentId | 中文标题 |
| --- | --- |
| pico8-2026 | 从 PICO-8 入门到 Game Jam：游戏社开发培训（培训总览） |
| pico8-intro | PICO-8 Intro：从共同兴趣到第一个制作目标 |
| pico8-l01 | PICO-8 L01：让输入产生可见反馈 |
| pico8-l02 | PICO-8 L02：从调试移动到整理对象 |
| pico8-l03 | PICO-8 L03：对象生命周期、关卡数据与创作衔接 |
| pico8-a01 | PICO-8 A01：用打砖块练习移动与碰撞 |
| pico8-a02 | PICO-8 A02：继续完善打砖块并解释实现 |
| pico8-object-organization | 教学案例：从分散变量到 Lua 对象组织 |
| pico8-game-jam | 课程之后的一周 Game Jam：从原型到作品提交（含 17 个卡带提交） |

## 4. 项目清单（5 个）

| 项目 | 分类 | 开发时间 | 技术 | 关联文章 |
| --- | --- | --- | --- | --- |
| MingEngine | personal | 2026.5 - Present | C++ / DirectX 11 / C# .NET / Editor UI | ming-scene-resources、ming-csharp-bridge、ming-gui-input |
| SpectreX | team | 未提供（见第 8 节） | Godot / C# / 光学交互 / Shader / 制作工具 | spectrex-light-gameplay、spectrex-rendering |
| Doomenstein | personal | 2026.1 - 2026.5 | 节点系统 / 地狱风格化场景 / IK 蜘蛛 | — |
| The Primary Colors | personal | 2023.6 - 2023.8 | Unity / C# / QFramework / MVC | — |
| Hamsterballin' | team | 2026.1 - 2026.5 | Unreal Engine 5 / PCG / 技术美术 / UI | — |

每个项目页展示：平台、项目状态、开发时间（有则显示）、我的职责、项目介绍、我的贡献、主要功能、实现与设计取舍、范围与反思、演示视频/外链、相关专题。团队项目明确区分个人贡献与团队成果。

## 5. 素材来源与校验

| 内容 | 来源（只读） | 仓库位置 | 校验 |
| --- | --- | --- | --- |
| Game Jam 卡带提交 17 个 | `C:\Users\Shangli Zhou\Desktop\GameJam2026`（17 个文件，含 `.p8` 与带封面 `.p8.png`） | `public/downloads/gamejam-2026/` | SHA-256 与原件逐一比对 17/17 一致；哈希同时记录在 `src/data/gamejam.ts`；副本与声明哈希 17/17 一致 |
| 《动物井》帧捕获截图 17 张 | `C:\Users\Shangli Zhou\Desktop\NoteBook\Semester 4\聚光灯\分析\动物井\截图\`（18 个文件） | `public/media/animal-well/` | 已复制的 17 张全部哈希一致；未复制的 `texture.png` 在正文中未使用 |
| 《师父》分析图 2 张 + 录屏 8 段 | `C:\Users\Shangli Zhou\Downloads\《师父SIFU》简要分析\图片和附件\` | `public/media/sifu/`（重命名为语义化英文名） | 10/10 哈希一致 |
| SpectreX 项目图标 | `C:\Work\Godot\Project\Spectrum\Spectrum\Art\Icon\TEX_Icon.png` | `public/media/projects/spectrex-icon.png` | 只读复制，未修改外部项目 |
| MingEngine 编辑器截图 | 仓库既有 `src/content/images/ming_engine.png` | 同左 | 截图为较早编辑器阶段（页面已注明） |
| Doomenstein / 三原色 / Hamsterballin 封面 | 仓库既有 `src/content/images/` | 同左 | 标题图 / 封面图 |

未入库（按计划排除）：RenderDoc `.rdc` 捕获、完整课程录像、安装包、原始长录像、第三方视频文件。仓库媒体总量约 37 MB，其中《师父》短视频约 35.8 MB；短视频随仓库管理，页面使用 `<video controls preload="none">` 按需加载，不自动播放。

## 6. 事实与措辞决策

- **未核实数字不写入成稿**：Hamsterballin 原稿中的「40 人 / 50 人」团队人数在本轮统一移除（中英文均为「团队」/「a team」）；不写未经记录的玩家测试或性能提升数据。
- **Ming**：当前源码使用 C#/.NET 脚本集成，早期 AngelScript 描述只作为历史说明出现；页面截图标注为较早开发阶段。
- **SpectreX**：个人职责限定为技术美术、程序与策划的交叉工作，页面明确不把团队全部设计与资产归为个人成果；只使用仓库内可用的原始图标，不添加推测性实机截图。
- **《动物井》**：区分观察与推断；EID 仅指原文所用捕获中的事件编号；本轮未重放捕获、没有源码，因此不把通道语义与设计意图写成已验证事实。
- **《师父》**：以可见行为描述「窗口 / 短硬直 / 长硬直」，不声称恢复内部状态机或数值公式；设计实验部分明确为尚未测试的原型方向。
- **PICO-8 教学**：明确区分保存的教案安排与实际授课记录；课程编号与教案/口述不一致处已说明；L03 录像仅作为外部中文材料链接，并声明未逐分钟审阅；Game Jam 的文件数不等同于独立作品、学生或团队数量；A01/A02 引用外部 YouTube 教程并保留出处与作者归属。
- **双语完整性**：每对内容的结构（二级标题、图片、视频、表格数量）保持一致；图注、图片替代文本、项目元数据均提供中英文。

## 7. 本轮验证结果（2026-10-26）

| 项目 | 结果 |
| --- | --- |
| `npm run build` | 成功，62 页（25 正式 + 37 预览），0 构建警告 |
| 编码损坏检测（78 个源文件 + 25 个正式页面） | 0 命中（此前 6 个文件、约 1,900 个字符被写成 `?`，已从会话记录恢复） |
| 内部链接（正式页） | 237 条，0 断链 |
| 页内锚点（含 16 个文章/教学页的 174 条目录链接） | 199 条全部命中，0 断裂；同页 id 无重复 |
| 内容配对 | 16 对完整，分类/关联项目一致，无草稿 |
| 关联项目引用 | 5 个项目 slug 全部存在，5 个项目页均已生成 |
| 本地资源引用 | 44 条（图片/视频/卡带/下载），0 缺失 |
| 占位文案与内部路径泄漏 | 正式页面 0 命中 |
| sitemap | 25 条正式 URL，0 条 `/previews/` |
| 草稿隔离 | 临时 `draft: true` 内容不生成页面、不进入列表与 sitemap（测试后已删除并重建） |
| 浏览器验收（Playwright + Chromium） | 62 项检查全部通过：中文默认、切换/刷新/跨页保持、禁用 localStorage 回退中文、明暗主题持久、1440/1024/390 无横向溢出、目录锚点点击与滚动、隐藏语言块 `inert` 且键盘不可进入、视频 `preload=none` 无自动播放、iframe 懒加载、图注呈块级弱化样式、项目开发时间中英分别显示 |
| 卡带哈希 | 17/17 与桌面原件一致 |
| 截图 | `%TEMP%\blog-acceptance\`（7 条路由 × 3 档宽度 + 明暗主题 + 语言切换状态） |

修复说明：上一轮通过 PowerShell 管道把含中文的脚本交给 Python，导致 Header、Footer、PortfolioLayout、首页、项目详情与 `projects.ts` 的中文变成 `?`；本轮从上一轮 Codex 会话日志中提取原始写入内容并以 UTF-8 重放，未重写文案。目录锚点未生效的原因是 rehype 插件注册在已弃用的 `markdown.rehypePlugins` 且运行在 Astro 生成标题 id 之前，现改为 `markdown.processor: unified({ rehypePlugins: [rehypeHeadingIds, languageHeadings] })`。

## 8. 待确认与后续

1. **SpectreX 开发时间**：未提供，项目页不显示该行，不推测填写。
2. **SpectreX 实机截图**：源仓库只有图标、标题/主菜单美术与分层素材，没有实机截图；当前使用原始图标。
3. **Hamsterballin 团队人数**：若确需公开，请提供可核实口径（总人数 / 小组人数），再补入中英文。
4. **简历与求职信 PDF**：本轮未制作，占位 PDF 已删除，页面不提供占位下载链接。
5. **下载包 Releases 能力**：`Project.downloads` 字段已保留，本轮不上传附件、不新建存储服务。
6. **完整课程录像与字幕**：仅保留外部链接；本轮不制作中文配音或完整字幕。
7. **第三方教程视频**：A01/A02 仅引用外部播放列表，未逐集审阅，正文已声明。
8. **未采用的素材**：`动物井\截图\texture.png` 未复制到仓库，正文未引用。

## 9. 维护约定

- 新增内容：在 `src/content/published/<articles|teaching>/` 下同时新增 `<contentId>.zh.md` 与 `<contentId>.en.md`，保持 `category`、`relatedProject` 一致；`draft: true` 可让成对内容暂不发布。
- 新增项目：在 `src/data/projects.ts` 增加条目（含 `summary/detail/contribution/tech/features/decisions/limitations/media`），可选 `platform/status/duration/role/relatedArticles/externalLink/embedVideo/downloads`。
- 新增卡带：放入 `public/downloads/gamejam-2026/` 并在 `src/data/gamejam.ts` 记录 `originalName` 与 SHA-256。
- 修改内容后运行 `npm run build`；构建会校验双语配对与元数据一致性。
- `/previews/` 仅作设计留档：`noindex`、不进入 sitemap，不参与正式内容校对。
