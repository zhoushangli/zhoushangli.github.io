import type { DesignRecord } from '../design-types';

// Slot D axes come from fnv1a hashing plus one recorded re-draw that separates it from slot C.
// e.g. axes.accent was re-drawn from 同色系渐层 to 冷暖双色对照 because C already used it.
const design: DesignRecord = {
  id: 'design-d',
  label: 'D',
  seed: 'fQztxsMTC',
  name: '待设计',
  english: 'PENDING',
  idea: '待设计',
  intro: '待设计',
  device: '待设计',
  axes: {
    imagery: '图书馆索书号与卡片目录',
    layout: '宽屏左右对峙分栏',
    typography: '无衬线正文+等宽元数据',
    accent: '冷暖双色对照',
    mechanism: '大图裁切主导',
    rhythm: '均匀如表格',
  },
  axesNote: '重抽 A4 强调色：原派生值与 design-c 重合，改用 fnv1a(seed:4:alt3) 的冷暖双色对照。',
};

export default design;
