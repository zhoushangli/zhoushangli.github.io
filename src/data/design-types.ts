// Describe one design slot that the preview routes can render.
// e.g. design-a holds seed, axes and the memory device of concept A.
export type DesignAxes = {
  imagery: string;
  layout: string;
  typography: string;
  accent: string;
  mechanism: string;
  rhythm: string;
};

// Describe the full record a slot file must provide to become a preview route.
// e.g. { id: 'design-a', label: 'A', seed: 'mkPVYYhEk', ... }
export type DesignRecord = {
  id: string;
  label: string;
  seed: string;
  name: string;
  english: string;
  idea: string;
  intro: string;
  device: string;
  axes: DesignAxes;
  axesNote?: string;
};
