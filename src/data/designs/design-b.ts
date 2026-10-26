import type { DesignRecord } from '../design-types';

// Slot B axes were derived from the seed by fnv1a hashing and are shared with the review script.
// e.g. axes.imagery decides the metaphor, axes.layout decides the four-view structure.
const design: DesignRecord = {
  id: 'design-b',
  label: 'B',
  seed: 'PZquZyReER',
  name: '待设计',
  english: 'PENDING',
  idea: '待设计',
  intro: '待设计',
  device: '待设计',
  axes: {
    imagery: '夜行列车时刻表与站台编号',
    layout: '单栏叙事流',
    typography: '全无衬线',
    accent: '纯无彩靠明度',
    mechanism: '大面积色块分割',
    rhythm: '极端尺度对比',
  },
};

export default design;
