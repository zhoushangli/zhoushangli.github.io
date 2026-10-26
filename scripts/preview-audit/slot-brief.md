# 暗色博客候选设计 · 槽位任务书

## 1. 你的角色与边界

你是六套候选设计中的一名设计者，负责分配给自己的槽位。最终目标是一名中文博客读者能长期阅读的暗色设计，四个视图共用同一套视觉语法。

- 只允许修改属于自己的文件：`src/data/designs/design-<x>.ts` 与 `src/styles/designs/design-<x>.css`。
- 其他文件一律不动，包括 `src/data/preview.ts`、`src/pages/previews/**`、`src/styles/previews.css`、正式站点页面。需要共享改动时向 `/root` 提出。
- 另一位设计者正在并行编辑其他槽位，不要查看或改动对方的文件。
- 每个 CSS 文件必须一次写完整，不要留下语法半成品：另一个设计者的页面也会打包你的样式表，写坏会导致双方都渲染失败。
- 全部选择器以 `html.theme-design-<x>` 开头，例如 `html.theme-design-a .article-row`。共享基础样式在 `previews.css` 里，你靠更高的选择器优先级覆盖它，不要依赖导入顺序。

## 2. 记录字段（design-<x>.ts）

保留 `id`、`label`、`seed`、`axes` 与可选的 `axesNote` 原样不变（它们由种子哈希派生，是多样性与评审的依据）。需要填写的字段：

- `name`：中文概念名，4–7 字，来自你的意象域。
- `english`：2–3 个英文单词，全大写，用于页面上的小标签。
- `idea`：一句话说明「种子 → 意象 → 设计语言」，必须能在布局里被指认。
- `intro`：首页 hero 的一句话，≤ 20 字，出现在 `.hero-intro`。
- `device`：记忆点装置，一句话，必须能在截图里被指出来（例如「每个栏目用一条从左侧延伸到边缘的刻度带分隔」）。

如果你判断派生轴组合不自洽，可以做一次重抽：改一个轴的值，并在 `axesNote` 写明原因。除此之外不要改轴。

## 3. DOM 契约（不可修改）

四个视图由 `src/pages/previews/[design]/[view].astro` 统一渲染，HTML 固定，你只能通过 CSS 重塑。所有页面共用外壳：

```html
<html class="preview-site theme-design-x">
  <header class="site-header">
    <a class="brand"><span class="brand-symbol">✳</span><span>周尚礼<span class="brand-en"> / ShangLi Zhou</span></span></a>
    <nav> 首页 / 文章 / 分类 / 作品 （当前项带 class="active"） </nav>
    <span class="header-number">NO. 04 / 09</span>
  </header>
  <main>…视图内容…</main>
  <footer class="site-footer">
    <div><span class="footer-symbol">✳</span><p>代码、文字与尚未完成的世界。<br>© 2026 周尚礼</p></div>
    <div class="footer-links">首页 / 文章 / 分类 / 正式网站</div>
    <span class="footer-seed">SEED / <seed></span>
  </footer>
</html>
```

**首页 `home`**

```html
<section class="home-hero">
  <div class="hero-copy">
    <p class="eyebrow">{english} <span>— 游戏开发者的个人现场</span></p>
    <h1>把好奇心<br><em>做成</em><span class="keep-word">可游玩的世界<span class="title-period">。</span></span></h1>
    <p class="hero-intro">{intro}</p>
    <div class="hero-actions">
      <a class="button-primary">阅读文章 <span>↗</span></a>
      <a class="button-text">探索作品 <span>↓</span></a>
    </div>
  </div>
  <div class="hero-art" aria-hidden="true">
    <div class="art-orbit orbit-one"></div><div class="art-orbit orbit-two"></div>
    <div class="art-core">S<span>/</span>Z</div>
    <div class="art-note note-one">CODE → WORLD</div><div class="art-note note-two">36° 52′ N</div>
  </div>
  <div class="hero-bottom"><span>ENGINEERING · GAME DESIGN · WRITING</span><span>SCROLL TO EXPLORE ↓</span></div>
</section>
<section class="home-about section-frame">
  <p class="section-index">01 / 关于</p>
  <div><h2>写代码，也写下<br>代码之外的事情。</h2><p>我是周尚礼，…</p></div>
</section>
<section class="home-projects section-frame" id="projects">
  <div class="section-heading"><div><p class="section-index">02 / 选定作品</p><h2>正在建造的世界</h2></div><span class="side-caption">…</span></div>
  <div class="project-grid">
    4 × <a class="project-card"><div class="project-image"><img><span class="project-number">01</span></div>
        <div class="project-meta"><span>个人作品</span><span>↗</span></div><h3>{title}</h3><p>{summary}</p></a>
  </div>
</section>
<section class="home-writing section-frame">
  <div class="section-heading"><div><p class="section-index">03 / 近期文字</p><h2>制作中的旁白</h2></div><a class="all-link">全部文章 ↗</a></div>
  <div class="article-list compact">3 × <a class="article-row">…</a></div>
</section>
```

**文章列表 `articles`**

```html
<section class="page-hero">
  <p class="eyebrow">THE WRITING INDEX / 文章索引</p>
  <h1>写下来，<br><em>才能继续</em>往前走。</h1><p>关于游戏、技术与创作过程中的偶然发现。…</p>
  <div class="page-count">05 <small>篇文章 / 持续更新</small></div>
</section>
<section class="content-section">
  <div class="section-heading"><p class="section-index">全部记录 / 2025—2026</p><a class="all-link">浏览分类 ↗</a></div>
  <div class="article-list">
    5 × <a class="article-row">
      <span class="row-number">01</span>
      <div><span class="category-tag">创作笔记</span><h2>{title}</h2><p>{excerpt}</p>
           <span class="placeholder-label">排版示例 / 待发布</span>（仅第 2 条起）</div>
      <span class="article-date">2026.09<small>8 分钟</small><b>↗</b></span>
    </a>
  </div>
</section>
```

**分类 `category`**

```html
<section class="page-hero">…A MAP OF IDEAS / 主题地图…<div class="page-count">03 <small>个主题 / 05 篇文章</small></div></section>
<section class="content-section">
  <div class="category-grid">
    3 × <a class="category-card" data-topic="创作笔记" href="?topic=…">
      <span class="category-number">01 / TOPIC</span><h2>创作笔记<span>↗</span></h2>
      <p>{desc}</p><span class="category-count">2 篇文章</span></a>
  </div>
  <div class="section-heading category-results" id="category-articles">
    <p class="section-index" id="selected-category">01 / 创作笔记</p><h2>从制作现场出发</h2><a class="all-link">查看全部 ↗</a>
  </div>
  <div class="article-list">5 × <a class="article-row" data-article-topic="创作笔记">…<h3>{title}</h3>…</a></div>
</section>
```

分类页有一个内联脚本：点击分类卡后给命中项加 `.selected`，给不命中的 `.article-row` 设置 `[hidden]`，并改写 `#selected-category` 文本。基础样式里已有 `[hidden] { display: none !important }`，所以**不要在 `.article-row` 上用 `display: … !important`**，否则过滤会失效。你可以给 `[hidden]` 状态另做视觉处理（例如 `display:none` 之外不再额外写规则）。

**文章详情 `article`**

```html
<article class="essay-page">
  <header class="essay-header">
    <a class="back-link">← 返回文章索引</a>
    <div class="essay-heading">
      <p class="eyebrow">创作笔记 / 2026.09 / 8 分钟阅读</p>
      <h1>在自己的引擎里，<br><em>重新认识</em>一棵树</h1>
      <p class="essay-deck">从场景节点到屏幕上的一个像素，…</p>
    </div>
    <div class="essay-byline"><span>文 / 周尚礼</span><span>WRITING NOTE 01</span></div>
  </header>
  <div class="essay-body-wrap">
    <aside class="essay-aside"><span>目录 / CONTENTS</span>3 × <a href="#section-N">01　从一个节点开始</a><span class="aside-rule">✳</span></aside>
    <div class="essay-body">
      <p class="lead">一棵树，可以是一组顶点、…</p>
      3 × <section id="section-N"><span class="body-index">01 / 03</span><h2>{title}</h2><p>…</p>
        <figure class="essay-figure"><div class="diagram">
          <span class="diagram-node">资源</span><span>→</span><span class="diagram-node">场景</span>
          <span>→</span><span class="diagram-node">视口</span><span>→</span><span class="diagram-node">画面</span>
        </div><figcaption>图 01 / 从文件到画面的一条简化路径</figcaption></figure>（仅第 1 节）
      </section>
      <div class="essay-end">✳<span>写于持续制作之中</span></div>
      <a class="next-article">继续阅读其他文章 <span>↗</span></a>
    </div>
  </div>
</article>
```

装饰内容（`.hero-art` 及其子元素、`.art-note` 的文字、`.diagram`）属于既有结构，你只能重绘它们的外观：可以改尺寸、颜色、描边、伪元素内容、隐藏或替换为图形，但不能新增或改写 HTML 结构与文字。

## 4. 暗色与可读性硬指标

- 主背景 HSL 亮度 ≤ 15%（例如 `#101114`、`#14161a`、`#0f1412` 都在范围内）；卡片/浮层可以更亮，但整体必须以暗色为主。
- 文章正文段落（`.essay-body section p`）与背景对比 ≥ 7:1；正文 17–19px，行高 ≥ 1.75；行宽 32–40 字（约 560–720px）。
- 强调色面积克制：视觉占比 ≤ 10%，不要变成大面积亮色块。
- 390px 宽度下整页无横向滚动；正文区左右留白 ≥ 16px。
- 移动端导航、品牌链接、主按钮的点击高度 ≥ 44px（共享的 `.brand` 默认只有 31px 高，需要你补内边距）。
- 必须提供 `:hover`、`:focus-visible`、`.active` 与选中态；`outline` 不能裸奔为 `none`，可用自绘描边或色块代替。
- 不要新引入远程字体：本环境无法访问 Google Fonts。使用系统字体栈，例如正文 `'Microsoft YaHei','PingFang SC','Hiragino Sans GB',sans-serif`，衬线可用 `'Songti SC','SimSun',Georgia,serif`，等宽可用 `Consolas,'DM Mono',monospace`。

## 5. 评分表（评审按此打分，100 分）

| 维度 | 分值 | 满分锚点 | 低分锚点 |
| --- | --- | --- | --- |
| 中文长文阅读 | 25 | 行宽 32–40 字、行高 ≥1.75、正文 17–19px、引用/代码/图注/目录层级分明 | 正文 <16px、行宽 >50 字或对比不足 |
| 信息结构与可扩展性 | 25 | 四视图共享同一套视觉语法，编号/日期/分类系统一致，新增文章不破坏版式 | 首页与内页像两套设计 |
| 视觉创意与记忆点 | 20 | 记忆点装置可一句话说清且在截图里可指认，与种子意象的关联可解释 | 装置可替换、看不出与意象的关联 |
| 暗色体系完成度 | 15 | 底色/卡片/浮层层次清楚，正文对比 ≥7:1，强调色克制，图片不发灰 | 主背景亮度 >15% 或正文对比 <4.5:1 |
| 移动端与状态 | 15 | 390px 无溢出、触摸目标 ≥44px、断行合理、状态齐备 | 横向滚动、遮挡或不可读 |

合格线：总分 ≥ 80，中文长文阅读 ≥ 20，移动端 ≥ 12，且硬门槛全过。

反俗套黑名单，命中两项即「视觉创意」判低分且当轮不通过：紫蓝渐变 + 玻璃拟态 + 霓虹描边三件套；全屏居中大标题 Hero + 滚动淡入作为唯一叙事；无叙事的等宽三栏卡片墙首页；全站伪终端 cosplay；无意义漂浮粒子/星空/矩阵雨；emoji 当图标体系。

## 6. 自检流程

预览服务已在 `http://127.0.0.1:4321` 运行（不要重启它）。每完成一个槽位后运行：

```powershell
python scripts/preview-audit/capture.py --design design-<x> --round <n>
```

它会输出 12 张截图（四视图 × 1440/1024/390）、门禁结果与可读性数据，并写出 `src/data/preview-audit/design-<x>.gates.json`。**必须把自己槽位的所有门禁修到 PASS 再汇报**，然后看一眼 `fold-desktop.jpg`（四个视图的首屏拼图）确认没有明显的排版事故。截图目录会打印在命令输出里。

汇报给 `/root` 时给出：槽位、中文名、seed、门禁是否全过、`capture.py` 输出的关键数字（surfaceL / bodyContrast / charsPerLine / lineHeight）、以及你的记忆点装置一句话。

## 7. 评审轮次

`/root` 会把独立评审的缺陷清单发回给你。每条缺陷必须逐条处理（含视图与断点、截图位置），修完重跑自检再汇报，不要只让整体观感变好而不处理具体条目。每套最多 3 轮，3 轮未过线则该槽位换种子重做。
