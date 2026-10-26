// Prefix article heading anchors so translated bodies never share DOM IDs.
// e.g. a heading named overview in a .en.md file becomes en-overview.
export default function languageHeadings() {
	return (tree, file) => {
		const language = String(file.path ?? '').match(/\.(zh|en)\.mdx?$/)?.[1];
		if (!language) {
			return;
		}

		function visit(node) {
			if (node.type === 'element' && /^h[1-6]$/.test(node.tagName) && node.properties?.id) {
				node.properties.id = `${language}-${node.properties.id}`;
			}

			if (node.type === 'element' && node.tagName === 'a' && String(node.properties?.href).startsWith('#')) {
				node.properties.href = `#${language}-${String(node.properties.href).slice(1)}`;
			}

			for (const child of node.children ?? []) {
				visit(child);
			}
		}

		visit(tree);
	};
}
