import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const published = defineCollection({
	loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/published' }),
	schema: z.object({
		contentId: z.string(),
		lang: z.enum(['zh', 'en']),
		section: z.enum(['articles', 'teaching']),
		title: z.string(),
		description: z.string(),
		category: z.enum(['engine', 'graphics', 'gameplay', 'development', 'teaching']),
		tags: z.array(z.string()),
		relatedProject: z.string().optional(),
		draft: z.boolean().default(false),
	}),
});

export const collections = { published };
