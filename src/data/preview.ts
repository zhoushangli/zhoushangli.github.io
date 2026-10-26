import { projects } from './projects';
import type { DesignRecord } from './design-types';

// Collect every slot file under ./designs so a new design only needs its own file.
// e.g. src/data/designs/design-a.ts creates the /previews/design-a/* routes automatically.
const designModules = import.meta.glob('./designs/design-*.ts', { eager: true }) as Record<string, { default: DesignRecord }>;

export type Concept = {
  seed: string;
  name: string;
  english: string;
  idea: string;
  intro: string;
  label?: string;
  device?: string;
  axes?: DesignRecord['axes'];
  axesNote?: string;
};

const legacyConcepts = {
  observatory: {
    seed: 'HhojBDEx',
    name: '天文台手稿',
    english: 'OBSERVATORY',
    idea: '将随机种子的圆形字母与断续节奏转译为轨道、星图刻度与手稿边注。',
    intro: '记录游戏、工具与世界之间的引力。',
  },
  arcade: {
    seed: 'Dg-JGkJ2',
    name: '游戏杂志剪贴',
    english: 'SIDE QUEST',
    idea: '将种子中的连字符视为裁切线，字母与数字的跳跃转译为杂志拼贴和醒目的栏目色块。',
    intro: '把制作游戏的过程，做成值得翻阅的一本杂志。',
  },
  atlas: {
    seed: 'saov3tBL',
    name: '系统终端图谱',
    english: 'FIELD ATLAS',
    idea: '把种子的大小写和数字变化转译为坐标、索引与节点连线，形成一张可阅读的工作图谱。',
    intro: '从代码、场景到文字，绘制个人创作的坐标。',
  },
} as const;

export const concepts: Record<string, Concept> = {
  ...legacyConcepts,
  ...Object.fromEntries(
    Object.entries(designModules)
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([, module]) => [module.default.id, module.default as Concept]),
  ),
};

export type ConceptId = string;
export const conceptIds = Object.keys(concepts);
export const views = ['home', 'articles', 'category', 'article'] as const;
export type PreviewView = (typeof views)[number];

export const featuredProjects = projects.slice(0, 4);

export const articles = [
  {
    category: '创作笔记',
    number: '01',
    date: '2026.09',
    title: '在自己的引擎里，重新认识一棵树',
    excerpt: '从场景节点到屏幕上的一个像素，开发引擎让我重新理解“看见”这件事。',
    reading: '8 分钟',
  },
  {
    category: '关卡设计',
    number: '02',
    date: '2026.07',
    title: '让玩家先于提示发现道路',
    excerpt: '一道光、一处遮挡和一次回望，如何在没有箭头的情况下组成引导。',
    reading: '6 分钟',
  },
  {
    category: '创作笔记',
    number: '03',
    date: '2026.05',
    title: '独立制作的慢节奏',
    excerpt: '工具、原型和作品之间的距离，比一张任务列表所显示的更长。',
    reading: '5 分钟',
  },
  {
    category: '技术拆解',
    number: '04',
    date: '2026.03',
    title: '从一个 RID 到一帧画面',
    excerpt: '用一个最小渲染链路解释资源、实例与视口如何协作。',
    reading: '11 分钟',
  },
  {
    category: '关卡设计',
    number: '05',
    date: '2025.12',
    title: '在狭窄空间里制造选择',
    excerpt: '以路线、节奏与视线的变化，让短小的空间保有探索感。',
    reading: '7 分钟',
  },
];

export const categories = [
  { title: '创作笔记', count: 2, desc: '制作过程、个人观察，以及那些值得留下的岔路。' },
  { title: '关卡设计', count: 2, desc: '空间如何说话，玩家如何在其中找到自己的路线。' },
  { title: '技术拆解', count: 1, desc: '将底层系统拆开，找到可以复用的思考方式。' },
];

export const essay = [
  {
    title: '从一个节点开始',
    paragraphs: [
      '第一次在自己的引擎里放下一棵树，它只是场景树上的一个名字。没有阴影，没有风，也没有记忆。我给它加上网格和材质，调整位置，再从摄像机看过去，屏幕上终于出现一片绿色。那一刻的快乐并不来自画面有多精致，而是我知道这片绿色经过了哪些地方。',
      '它从文件进入资源系统，被解析成顶点和纹理；场景节点保存它的位置，渲染实例取得自己的标识；视口决定从哪里看，绘制命令最后抵达显卡。平时使用成熟引擎时，这些步骤像地底的根。自己重新走一遍之后，树的轮廓和根都变得清晰。',
    ],
  },
  {
    title: '让工具留下思考的痕迹',
    paragraphs: [
      '编辑器不是为了把所有按钮摆在眼前。好的工具应该让重要的关系被看见：一个对象属于哪棵场景树，素材从哪里来，修改会影响哪些地方。为此，我不断删去过早出现的选项，尽量让每个面板只回答一个问题。',
      '有时问题来自一个小小的空白。拖入资源后没有反馈，使用者就不知道操作是否成功；层级列表缺少缩进，父子关系就难以辨认。它们看似只是界面细节，却决定了制作时思路能否连续。写程序时我关心数据是否正确，设计工具时还必须关心人是否确信数据正确。',
      '做自己的引擎，让我同时站在开发者和使用者两边。一个接口能运行，不代表它易于理解；一个功能能展示，不代表它能陪伴长期的创作。每一次把操作缩短一步，我都会想：这里节省下来的注意力，是否能还给真正想做的游戏？',
    ],
  },
  {
    title: '屏幕以外的风',
    paragraphs: [
      '后来我又给那棵树加上光。方向光从左侧扫过树冠，地面收到一片简单的阴影。我知道距离自然还很远，但画面终于开始有时间感：像某个下午，人在走近树林前停了一下。',
      '技术并不会自动生成情感。它只是提供条件，让观察得到更准确的表达。树的网格、材质、空间关系和光照逻辑都是条件；真正决定它是否值得被记住的，是玩家为何在这里遇见它。我希望作品中的系统最后都能退到这种体验的背后。',
      '下一次打开编辑器，我还会看见许多不完善的地方。它们不再只是一张待办清单，而是一张地图：每个缺口都指向一种尚未建立的联系。沿着它们往前走，我也许会更明白自己想做怎样的游戏，以及为什么还想继续写下去。',
    ],
  },
];
