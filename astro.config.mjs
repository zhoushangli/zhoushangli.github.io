// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { rehypeHeadingIds, unified } from '@astrojs/markdown-remark';
import { defineConfig, fontProviders } from 'astro/config';
import languageHeadings from './src/utils/rehype-language.mjs';

// https://astro.build/config
export default defineConfig({
	site: 'https://zhoushangli.github.io',
	integrations: [mdx(), sitemap({ filter: (page) => !page.includes('/previews/') })],
	// Astro's built-in heading-id plugin runs after user rehype plugins, so run it
	// explicitly first: languageHeadings then prefixes the generated ids with zh-/en-.
	markdown: { processor: unified({ rehypePlugins: [rehypeHeadingIds, languageHeadings] }) },
	fonts: [
		{
			provider: fontProviders.local(),
			name: 'Atkinson',
			cssVariable: '--font-atkinson',
			fallbacks: ['sans-serif'],
			options: {
				variants: [
					{
						src: ['./src/assets/fonts/atkinson-regular.woff'],
						weight: 400,
						style: 'normal',
						display: 'swap',
					},
					{
						src: ['./src/assets/fonts/atkinson-bold.woff'],
						weight: 700,
						style: 'normal',
						display: 'swap',
					},
				],
			},
		},
	],
});
