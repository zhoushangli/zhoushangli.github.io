# 内容、素材与验证清单

本文件记录正式站点的内容清单、素材来源与校验结果、已确认的措辞决策、仍待核实的事实，以及本轮验证结论。最后更新：2026-10-26。

## 1. 站点结构与正式路由

正式路由 13 条（构建共 51 页，其中 38 页为 `/previews/` 设计稿，已 `noindex` 且不进入 sitemap）：

```
/                                  简介、个人经历、教育、实习、技能、个人项目、团队项目、笔记、教学、个人兴趣
/projects/                         项目作品总览（个人 / 团队）
/projects/ming-engine/             项目详情
/projects/spectrex/
/projects/doomenstein/
/projects/the-primary-colors/
/projects/hamsterballin/
/articles/                         笔记（分类筛选）
/articles/animal-well-rendering/
/articles/sifu-combat-analysis/
/teaching/                         教学
/teaching/pico8-2026/
/teaching/pico8-game-jam/
```

双语内容位于 `src/content/published/<section>/<contentId>.{zh,en}.md`，由 `src/content.config.ts` 加载；同一 `contentId` 必须有中英两份，缺一份或 `category`/`relatedProject` 不一致时构建失败。`src/content/articles/` 下是早期随笔与 Obsidian 提示词，不在集合范围内，确认不发布。

## 2. 公开笔记（2 对）

| contentId | 中文标题 |
| --- | --- |
| animal-well-rendering | 《动物井》渲染分析 |
| sifu-combat-analysis | 《师父》战斗分析 |

MingEngine 的 `ming-scene-resources`、`ming-csharp-bridge`、`ming-gui-input`，以及 SpectreX 的 `spectrex-light-gameplay`、`spectrex-rendering` 共五组双语源稿设为 `draft: true`。不生成页面，不进入公开列表与 sitemap，项目页不再关联这些文章。

## 3. 教学（2 对）

| contentId | 中文标题 |
| --- | --- |
| pico8-2026 | Pico8 入社培训 |
| pico8-game-jam | Gamejam 作品展 |

原来的 Intro、L01/L02/L03、A01/A02 和对象管理案例共七组双语页面设为草稿，不再生成路由。培训页保留简要课程大纲及三份用户提供的腾讯会议录制链接；录制日期按所附记录显示，不推定为授课日期。L03 使用新地址 `NARXvk9a12`。

## 4. 项目（5 个）

| 项目 | 分类 | 技术栈（最多三项） |
| --- | --- | --- |
| MingEngine | personal | 自研引擎 / C++ / DirectX 11 |
| SpectreX | team | Godot / C# |
| Doomenstein | personal | 自研引擎 / C++ / DirectX 11 |
| The Primary Colors | personal | Unity / C# / QFramework |
| Hamsterballin' | team | Unreal Engine 5 / PCG |

团队项目单列“我的工作”，个人项目将职责并入介绍和功能。实现与开发进展仅在有内容时显示。图片替代文本与图注分开维护。Doomenstein 的 C++ 与 DirectX 11 技术依据本地 `C:\p4\Personal\SD\Doomenstein` 与其 Engine 渲染源码确认。

## 5. 素材来源与校验

| 内容 | 来源（只读） | 仓库位置 | 校验 |
| --- | --- | --- | --- |
| Gamejam PNG 封面 15 份 | 原有 `GameJam2026` 提交中的 PNG 文件 | `public/downloads/gamejam-2026/` | 原始 PNG 未改写；15/15 与清单 SHA-256 一致；两个纯 `.p8` 提交按用户要求删除 |
| 《动物井》帧捕获截图 17 张 | `C:\Users\Shangli Zhou\Desktop\NoteBook\Semester 4\聚光灯\分析\动物井\截图\`（18 个文件） | `public/media/animal-well/` | 已复制的 17 张全部哈希一致；未复制的 `texture.png` 在正文中未使用 |
| 《师父》分析图 2 张 + 录屏 8 段 | `C:\Users\Shangli Zhou\Downloads\《师父SIFU》简要分析\图片和附件\` | `public/media/sifu/`（重命名为语义化英文名） | 10/10 哈希一致 |
| SpectreX 宣传封面 | 用户提供的 [B 站宣传视频](https://www.bilibili.com/video/BV1gEny6hEAC/) 封面（1920×1080） | `public/media/projects/spectrex-cover.jpg` | 从视频元数据取得原始封面，画面与用户提供图片一致；旧图标保留但不再展示 |
| SpectreX 宣传视频 | 用户提供的 B 站视频 `BV1gEny6hEAC` | 外部播放器与原站链接 | 懒加载，不自动播放；不下载视频文件 |
| MingEngine 编辑器截图 | 仓库既有 `src/content/images/ming_engine.png` | 同左 | 截图为较早编辑器阶段（页面已注明） |
| Doomenstein / 三原色 / Hamsterballin 封面 | 仓库既有 `src/content/images/` | 同左 | 标题图 / 封面图 |

未入库（按计划排除）：RenderDoc `.rdc` 捕获、完整课程录像、安装包、原始长录像、第三方视频文件。仓库媒体总量约 37 MB，其中《师父》短视频约 35.8 MB；短视频随仓库管理，页面使用 `<video controls preload="none">` 按需加载，不自动播放。

## 6. 事实与措辞决策

- **未核实数字不写入成稿**：Hamsterballin 原稿中的「40 人 / 50 人」团队人数在本轮统一移除（中英文均为「团队」/「a team」）；不写未经记录的玩家测试或性能提升数据。
- **Ming**：当前源码使用 C#/.NET 脚本集成，早期 AngelScript 描述只作为历史说明出现；页面截图标注为较早开发阶段。
- **SpectreX**：个人职责限定为技术美术、程序与策划的交叉工作，页面明确不把团队全部设计与资产归为个人成果；使用用户提供的宣传封面与视频，不添加推测性实机截图。
- **《动物井》**：区分观察与推断；EID 仅指原文所用捕获中的事件编号；本轮未重放捕获、没有源码，因此不把通道语义与设计意图写成已验证事实。
- **《师父》**：以可见行为描述「窗口 / 短硬直 / 长硬直」，不声称恢复内部状态机或数值公式；设计实验部分明确为尚未测试的原型方向。
- **PICO-8 教学**：公开内容缩减为大纲、录制链接和 PNG 作品展。录制时间使用用户给出的原始记录。详细教案源稿留存为草稿，PNG 提交数量不作为参与人数。
- **双语完整性**：每对内容的结构（二级标题、图片、视频、表格数量）保持一致；图注、图片替代文本、项目元数据均提供中英文。

## 7. 首次内容整理的历史验证（2026-10-26，非本轮验收）

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
2. **SpectreX 实机截图**：当前展示用户提供的宣传封面与视频；独立实机截图尚未提供。
3. **Hamsterballin 团队人数**：若确需公开，请提供可核实口径（总人数 / 小组人数），再补入中英文。
4. **简历与求职信 PDF**：本轮未制作，占位 PDF 已删除，页面不提供占位下载链接。
5. **下载包 Releases 能力**：`Project.downloads` 字段已保留，本轮不上传附件、不新建存储服务。
6. **完整课程录像与字幕**：仅保留外部链接；本轮不制作中文配音或完整字幕。
7. **第三方教程视频**：A01/A02 引用外部作者的教程，章节范围按原作业要求保留，未逐集审阅。
8. **未采用的素材**：`动物井\截图\texture.png` 未复制到仓库，正文未引用。

## 9. 维护约定

- 新增内容：在 `src/content/published/<articles|teaching>/` 下同时新增 `<contentId>.zh.md` 与 `<contentId>.en.md`，保持 `category`、`relatedProject` 一致；`draft: true` 可让成对内容暂不发布。
- 新增项目：在 `src/data/projects.ts` 增加条目（含 `summary/detail/contribution/tech/features/decisions/limitations/media`），可选 `platform/status/duration/role/relatedArticles/externalLink/embedVideo/downloads`。
- 新增卡带：放入 `public/downloads/gamejam-2026/` 并在 `src/data/gamejam.ts` 记录 `originalName` 与 SHA-256。
- 修改内容后运行 `npm run build`；构建会校验双语配对与元数据一致性。
- `/previews/` 仅作设计留档：`noindex`、不进入 sitemap，不参与正式内容校对。

## 10. 午夜藏书室正式页面迁移的历史记录（2026-10-26）

- 用户确认保留全部内容，首页依次展示序言与个人照片、个人与团队项目、文章、教学、个人介绍与经历、兴趣。
- 全站采用深蓝、象牙白与旧铜色，中文标题使用宋体风格，英文标题使用 Georgia；仅保留深色主题，旧的浅色偏好不再影响显示。中英切换与语言记忆保留。
- 桌面采用左侧目录，手机采用折叠菜单；语言切换位于导航区。文章目录在窄屏折叠，点击章节后收起并定位正文。
- 首页与项目总览使用文字项目行，悬停或键盘选中时只在该行出现左深右浅的图片背景；手机点击直接进入项目详情。详情图保持完整、清晰。
- 原有 25 个正式路由、正文、双语元数据、下载与页内地址保留；列表图片变为装饰性背景，详情图继续保留双语图片说明。
- `npm run build` 通过；`scripts/verify-portfolio.py` 完成 25 路由 × 中英文 × 1440/1024/390px 共 150 组页面检查，以及语言记忆、旧浅色偏好隔离、项目行悬停与键盘、响应式菜单、双语目录、宽表格与代码、61 个不同内部链接和 17 个卡带下载的检查。
- 构建日志、截图和验收数据位于 `artifacts/preview-audit/site-migration/`，该目录仅保留在本机。第 7 节是迁移前的历史验收记录，其中的浅色主题测试不代表当前功能。
- 本轮仅修改和验证本地代码，未进行远程推送或部署。

## 11. 上轮结构与文案调整的历史记录（2026-10-26）

- 首页顺序：简介 → 完整教育、实习 → 作品 → 笔记 → 教学 → 个人兴趣。独立经历页与首页复用 `ExperienceTimeline`。
- 主导航为首页、作品、笔记、教学；左下按页面显示项目、内容列表或双语正文目录。
- 文案采用平实表述；公开内容共 11 对，五组项目文章保留为草稿。
- 技术栈最多三项，详情页 18px、列表 14px，使用铜色。图注居中、淡色，正文图片与视频使用 `figure/figcaption`。
- `npm run build`：通过，59 页（21 正式 + 38 预览）。
- `python scripts/verify-portfolio.py --static-only`：通过，567 条本地链接、94 个资源引用、178 条锚点、61 个图注、17 个卡带哈希；首页和独立页经历内容一致，五组撤下文章无页面与 sitemap 记录。
- 本地 HTTP 检查：21 个正式页面返回 200，五个撤下文章地址返回 404。22 份公开中英文正文的代码块、媒体引用、外部来源链接和二级章节数量均与修改前一致。
- 浏览器工具未连接（无可用 apps/browsers，native pipe 不存在）：本轮未完成 1440/1024/390px 视觉、交互和实际视频播放验收。此前历史验收不代表本轮通过。
- 本地修改，未推送或部署。

## 12. 展示精简与项目补充（2026-10-26）

- 首页使用“您好，我是周尚礼”“我开发游戏！”和用户提供的简介，副标题缩小并使用铜色。移除重复的身份说明。
- 桌面侧栏上下目录之间的间距由窗口高度确定，次级目录使用固定起点和内部滚动，不受条目数量影响。
- 教学只保留入社培训与 Gamejam 作品展，七组详细教学源稿设为草稿。作品展只显示 15 份 PNG 与名称，桌面三列、手机两列，无文件名和下载按钮。
- 删除 `the-director.p8`、`reverse.p8`，保留 `.p8.png` 等 PNG 原件；清单哈希对应 15 份保留图片。
- MingEngine 与 Doomenstein 强调自研 C++ 引擎，技术栈仍最多三项。MingEngine 的 C#/.NET 功能保留在项目说明中。
- SpectreX 按用户确认写明类银河恶魔城定位、全部三章关卡设计与约 10 小时全程观察的深度试玩；策划内容先于程序、技术美术。项目页末尾加入六个 TapTap 开发日志和总结链接，正文不摘录 AI 使用反思。
- 构建通过：52 页（14 正式 + 38 预览）。静态检查通过：326 条本地链接、94 个资源引用、86 条锚点、61 个图注、15 份 PNG 哈希、五组文章与七组教学草稿隔离。
- 浏览器工具仍未连接，本轮屏幕布局、滚动交互及外部视频播放未作视觉或实际播放验收。
- 未推送或发布。

## 13. 分隔线、图标与笔记文风（2026-10-26）

- 取消普通区块、笔记列表、经历条目、技能和开发日志的重复横线；首页三个主要栏目用 2px 铜色短线，项目间保留低对比度 1px 细线。表格保留较厚表头线与细行分隔，移除竖向网格。
- 学校和企业图片均有透明通道，经历图标容器改为深蓝底并去掉外框，原图片未修改。
- SpectreX 新增独立“自定义渲染管线”章节，介绍分层采集与 Composite A/B/C、颜色与材质数据、分层自发光和后处理、RenderService/RenderPipeline/配置资源的分工。原先的简略渲染功能项由该章节取代，光学解算和反馈方面的内容保留在其他程序工作中。
- 渲染描述依据 `C:\Work\Godot\Project\Spectrum\Spectrum` 下当前的 `Scripts/Core/RenderService.cs`、`Scripts/Core/RenderPipeline.cs`、`Prefabs/Runtime/Core/SCN_RenderPipeline.tscn` 和对应 Shader 核对。没有修改 Spectrum 文件、运行其构建或执行新的 GPU/性能验证。平台说明简化为“桌面端 · Godot”。
- 两篇笔记的中英文正文改为作者直接描述观察、推测和问题；删除“原笔记”“原稿”等审阅措辞，图注直接说明画面内容，保留数值假设与局部不确定性。
- 四份正文的代码块和媒体引用与修改前一致。构建与静态检查通过，14 个正式页面、326 条本地链接、94 个资源引用、86 条锚点和 15 份 PNG 哈希有效；新增检查防止编辑腔措辞再次进入公开笔记。
- 浏览器工具无可用连接，实际排版、滚动和视频播放未作本轮视觉验收。没有推送或发布。

## 14. 个人经历并入首页（2026-10-26）

- 首页顺序为：简介、个人经历、教育经历、实习经历、技能、个人项目、团队项目、笔记、教学、个人兴趣。个人经历保留学习背景、职业方向、教学、关卡设计四段正文，使用 800px 最大正文宽度、16px 字号和 2 倍行高。
- 个人经历与教育、实习为同级栏目；正文栏目统一使用 h2 标题和内容区全宽的 2px 铜色渐隐线。个人兴趣使用大标题，“游戏开发之外”使用小号铜色副标题。
- 技能保留在实习经历之后。左上仍为首页、作品、笔记、教学四个入口，首页次级目录按正文顺序列出个人经历、技能及个人／团队项目。
- 取消独立经历页与“查看独立页面”链接；检查脚本改为验证首页栏目和目录顺序、四段个人经历、独立经历页与链接已移除。
- `npm run build` 通过：51 页（13 正式 + 38 预览）。`python scripts/verify-portfolio.py --static-only` 通过：310 条本地链接、90 个资源引用、82 条锚点、61 个图注和 15 份 PNG 哈希。`git diff --check` 通过。
- 浏览器工具返回无可用浏览器，原生连接亦不可用，因此未执行本轮浏览器排版与滚动交互验收。没有推送或发布。
