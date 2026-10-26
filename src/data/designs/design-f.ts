import type { DesignRecord } from '../design-types';

// Slot F axes come from fnv1a hashing plus one recorded re-draw that separates it from slot B.
// e.g. axes.imagery was re-drawn from 夜行列车时刻表 because B already shared three axes with F.
const design: DesignRecord = {
  id: 'design-f',
  label: 'F',
  seed: '6Nmfinhq',
  name: '待设计',
  english: 'PENDING',
  idea: '待设计',
  intro: '待设计',
  device: '待设计',
  axes: {
    imagery: '考古地层剖面与标尺',
    layout: '单栏叙事流',
    typography: '衬线标题+无衬线正文',
    accent: '材质色',
    mechanism: '网格与刻度系统',
    rhythm: '极端尺度对比',
  },
  axesNote: '重抽 A1 意象域：原派生值夜行列车与 design-b 在 A1/A2/A6 三轴重合，改用 fnv1a(seed:1:alt2) 的考古地层剖面。',
};

export default design;
