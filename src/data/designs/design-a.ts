import type { DesignRecord } from '../design-types';

// Slot A axes were derived from the seed by fnv1a hashing and are shared with the review script.
// e.g. axes.imagery decides the metaphor, axes.layout decides the four-view structure.
const design: DesignRecord = {
  id: 'design-a',
  label: 'A',
  seed: 'mkPVYYhEk',
  name: '待设计',
  english: 'PENDING',
  idea: '待设计',
  intro: '待设计',
  device: '待设计',
  axes: {
    imagery: '博物馆展签与恒温展柜',
    layout: '双栏侧栏常驻',
    typography: '无衬线正文+等宽元数据',
    accent: '单一低饱和色',
    mechanism: '大面积色块分割',
    rhythm: '均匀如表格',
  },
};

export default design;
