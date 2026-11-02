import { getCollection, type CollectionEntry } from 'astro:content';

export const teachingOrder = ['pico8-2026', 'pico8-game-jam'];

export const categories = {
	engine: { zh: '引擎开发', en: 'Engine development' },
	graphics: { zh: '图形渲染', en: 'Graphics & rendering' },
	gameplay: { zh: '游戏机制与设计', en: 'Game systems & design' },
	development: { zh: '开发实践', en: 'Development practice' },
	teaching: { zh: '教学实践', en: 'Teaching practice' },
};

export interface ContentPair {
	zh: CollectionEntry<'published'>;
	en: CollectionEntry<'published'>;
}

// Pair translations, using Chinese for entries explicitly published in Chinese only.
// e.g. getContentPairs('articles') still rejects an accidentally missing translation.
export async function getContentPairs(section: 'articles' | 'teaching'): Promise<ContentPair[]> {
	const entries = await getCollection('published');
	const groups = new Map<string, Partial<ContentPair>>();
	for (const entry of entries.filter((item) => item.data.section === section)) {
		const group = groups.get(entry.data.contentId) ?? {};
		if (group[entry.data.lang]) {
			throw new Error(`Duplicate ${entry.data.lang} content: ${entry.data.contentId}`);
		}

		group[entry.data.lang] = entry;
		groups.set(entry.data.contentId, group);
	}

	const pairs: ContentPair[] = [];
	for (const [id, group] of groups) {
		if (group.zh?.data.chineseOnly && !group.en) {
			group.en = group.zh;
		}

		if (!group.zh || !group.en) {
			throw new Error(`Missing translation: ${id}`);
		}

		if (group.zh.data.category !== group.en.data.category || group.zh.data.relatedProject !== group.en.data.relatedProject) {
			throw new Error(`Translation metadata mismatch: ${id}`);
		}

		if (!group.zh.data.draft && !group.en.data.draft) {
			pairs.push(group as ContentPair);
		}
	}

	return pairs;
}

// Show series introductions in indexes while keeping chapters on their own routes.
// e.g. isContentIndexEntry(pair) includes a series introduction with order zero.
export function isContentIndexEntry(pair: ContentPair): boolean {
	return !pair.zh.data.seriesId || pair.zh.data.seriesOrder === 0;
}
