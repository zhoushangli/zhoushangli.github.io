import { render } from 'astro:content';
import { getContentPairs, categories } from './content';
import { projects } from './projects';

export async function getDesignContent() {
  const pairs = await getContentPairs('articles');
  const sample = pairs.find((pair) => pair.zh.data.contentId === 'animal-well-rendering')!.zh;
  const rendered = await render(sample);
  return {
    articles: pairs.map(({ zh }) => ({
      id: zh.data.contentId,
      title: zh.data.title,
      description: zh.data.description,
      category: zh.data.category,
      categoryLabel: categories[zh.data.category].zh,
      sample: zh.data.contentId === sample.data.contentId,
    })).sort((a, b) => Number(b.sample) - Number(a.sample)),
    categories: Object.entries(categories)
      .filter(([key]) => pairs.some(({ zh }) => zh.data.category === key))
      .map(([id, label]) => ({ id, label: label.zh })),
    projects: projects.slice(0, 4),
    sample: sample.data,
    Content: rendered.Content,
    headings: rendered.headings.filter((heading) => heading.depth === 2)
      .map((heading) => ({ ...heading, slug: heading.slug.startsWith('zh-') ? heading.slug : 'zh-' + heading.slug })),
  };
}

export type DesignContent = Awaited<ReturnType<typeof getDesignContent>>;
export type DesignProps = {
  view: 'home' | 'articles' | 'article';
  base: string;
  concept: import('./design-types').DesignRecord;
  data: DesignContent;
};
