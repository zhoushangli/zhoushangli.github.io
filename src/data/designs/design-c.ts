import type { DesignRecord } from '../design-types';

// Slot C axes were derived from the seed by fnv1a hashing and are shared with the review script.
// e.g. axes.imagery decides the metaphor, axes.layout decides the four-view structure.
const design: DesignRecord = {
  id: 'design-c',
  label: 'C',
  seed: 'pLJGAJ9m',
  name: '待设计',
  english: 'PENDING',
  idea: '待设计',
  intro: '待设计',
  device: '待设计',
  axes: {
    imagery: '老式放映机光斑与胶片齿孔',
    layout: '模块拼贴网格',
    typography: '无衬线正文+等宽元数据',
    accent: '同色系渐层',
    mechanism: '网格与刻度系统',
    rhythm: '均匀如表格',
  },
};

export default design;
