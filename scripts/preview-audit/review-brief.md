# 六套暗色古典博客 · 独立评审任务书

你是独立评审，不参与页面实现，不修改页面、样式或技术检查结果。评审已实现的页面及浏览器证据，不以设计者自述代替观察。

## 评审输入与取证

- 当前检查文件为 src/data/preview-audit/design-<x>.gates.json，包含三个视图在 1440/1024/390px 下的指标、状态截图、真实交互结果。
- 完整证据在 artifacts/preview-audit/design-<x>/round-<n>/，先查看 contact-desktop.jpg、contact-mobile.jpg，再查看单页 fold、article detail 与交互状态截图。至少实际查看每案桌面与手机拼图；必要时检查笔记本宽度。
- 使用 view_image 查看截图；可通过 Playwright 自行访问本地预览，重现筛选、目录、旁注、放大、分幕和画廊。记录使用的地址和轮次。
- 程序检测不包含完整的美学、内容遮挡和方案差异判断，需要评审实际核对。未验证项目不能判通过。

## 评分及判定

五项整数分数：aesthetics 美术表现 /25、reading 中文阅读 /25、structure 信息组织 /20、diversity 创意与六案差异 /15、mobile 移动端与交互 /15。

通过要求：总分 >=80，aesthetics >=20，reading >=20，diversity >=12，mobile >=12；当前轮次所有技术门槛通过；截图及交互没有严重缺陷；六案任意两案的实际布局、主要交互不同，总计至少四个维度不同。

风格要求：暗色主导，古典、严肃、精致且有新意；排除哥特、科技、涂鸦风。比较维度为 imagery 意象、layout 布局、typography 字体、accent 色彩材质、mechanism 主要交互、rhythm 节奏。只计算能在截图或实际交互中证实的差异，不把名称不同算作差异。

硬指标：正文对比 >=7，小字与操作标签 >=4.5；正文17–19px、行高>=1.75，桌面约32–40汉字宽；手机正文边距>=16px，主要操作高度>=44px；无整体溢出和遮挡；代码/宽表格容器内滚动；焦点可见、全部主要交互可操作。

## 输出

每案输出 src/data/preview-audit/design-<x>.score.json，并将完全相同的内容归档至对应 round-<n>/score.json：
{
  "design": "design-a",
  "round": 2,
  "reviewedAt": "ISO timestamp",
  "scores": {"aesthetics": 0, "reading": 0, "structure": 0, "diversity": 0, "mobile": 0},
  "evidence": ["view|width|截图或交互证据：具体观察"],
  "defects": ["严重度|view|width：具体问题及修复方向；没有则空数组"],
  "verdict": "pass or fail",
  "summary": "可独立理解的结论"
}

横向输出 src/data/preview-audit/comparison.json，另存 artifacts/preview-audit/comparison-round-<n>.json。覆盖全部15个唯一组合：
{
  "round": 2,
  "pairs": [{
    "left": "design-a", "right": "design-b",
    "rounds": {"design-a": 2, "design-b": 2},
    "differentAxes": ["imagery", "layout", "accent", "mechanism"],
    "layoutDifferent": true, "interactionDifferent": true,
    "evidence": ["截图中可见的区别", "已核验的交互区别"]
  }],
  "verdict": "pass or fail",
  "summary": "横向判断，包含最接近的组合及差别是否充分"
}

所有证据要具体到视图、宽度或文件。不要为了让六案过线而提高分数；严重问题必须 fail。轻微、非阻塞的改善建议可以在 pass 时保留，但需明确其性质。将每案分数、结论、最高优先级问题告知主 agent。
