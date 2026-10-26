import type { DesignRecord } from '../design-types';

// Slot E axes were derived from the seed by fnv1a hashing and are shared with the review script.
// e.g. axes.imagery decides the metaphor, axes.layout decides the four-view structure.
const design: DesignRecord = {
  id: 'design-e',
  label: 'E',
  seed: 'CdHbk3LRNV',
  name: '待设计',
  english: 'PENDING',
  idea: '待设计',
  intro: '待设计',
  device: '待设计',
  axes: {
    imagery: '地下档案库索引抽屉',
    layout: '编号推进的序列式',
    typography: '全等宽',
    accent: '材质色',
    mechanism: '大面积色块分割',
    rhythm: '紧凑密集',
  },
};

export default design;
