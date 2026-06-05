import DoomensteinTitleImage from '../content/images/doomenstein_titile.png';

export type ProjectCategory = 'personal' | 'team';

export interface Project {
	slug: string;
	category: ProjectCategory;
	title: string;
	summary: {
		en: string;
		zh: string;
	};
	detail: {
		en: string;
		zh: string;
	};
	contribution: {
		en: string;
		zh: string;
	};
	duration?: string;
	role?: {
		en: string;
		zh: string;
	};
	tech: {
		en: string;
		zh: string;
	};
	features?: {
		en: string;
		zh: string;
	}[];
	media: {
		type: 'image' | 'video';
		src: string;
		alt: {
			en: string;
			zh: string;
		};
	};
}

export const projects: Project[] = [
	{
		slug: 'doomenstein',
		category: 'personal',
		title: 'Doomenstein',
		summary: {
			en: 'A solo-developed retro 3D first-person hell shooter with 8-direction sprites, local two-player support, OBJ model loading, post-processing, CPU particles, and simple IK-driven enemies.',
			zh: '一款独立开发的复古 3D 第一人称地狱射击游戏，结合 8 面精灵、本地双人、OBJ 模型加载、后处理、CPU 粒子和简易 IK 敌人。',
		},
		detail: {
			en: 'Doomenstein began as a retro-style 3D first-person shooter using 8-direction sprites, with local multiplayer support for up to two players using keyboard/mouse or Xbox controllers. I later expanded it with OBJ model loading, simple IK, a post-processing chain, CPU quad particles, volumetric clouds, emissive textures, and a hell-themed environment, turning it into a small but complete doomlike shooter prototype.',
			zh: '《末日迷宫》（Doomenstein）最初是一款复古风格的 3D 第一人称射击游戏，使用 8 面精灵图表现角色朝向，并支持最多 2 名玩家通过键盘鼠标或 Xbox 手柄进行本地多人游玩。随后我为项目加入了 OBJ 3D 模型加载、简易 IK、后处理链、CPU quad 粒子、体积云、自发光贴图和地狱风格场景，将它扩展成一个简单但完整的 doomlike 地狱射击游戏原型。',
		},
		contribution: {
			en: 'As the solo developer, I built the node-style gameplay framework, rendering features, input and controller support, local multiplayer, enemy behavior, IK, particles, post-processing, and hell-themed scene content.',
			zh: '作为独立开发者，我负责类 Godot node 系统、渲染表现、键鼠与手柄输入、本地多人、敌人行为、IK、粒子、后处理和地狱风格场景内容。',
		},
		duration: '2026.1 - 2026.5',
		role: {
			en: 'Solo Developer',
			zh: '独立开发',
		},
		tech: {
			en: 'Node System | Hell-Styled Scene | IK Spider',
			zh: '节点系统 | 地狱风格化场景 | IK 蜘蛛',
		},
		features: [
			{
				en: 'Built a Godot-like node system to organize gameplay objects, scene logic, and reusable behaviors.',
				zh: '搭建类 Godot node 系统，用于组织玩法对象、场景逻辑和可复用行为。',
			},
			{
				en: 'Implemented 8-direction sprite rendering for retro FPS-style enemies and characters.',
				zh: '实现 8 面精灵渲染，用于复古 FPS 风格的角色和敌人表现。',
			},
			{
				en: 'Added local multiplayer for up to two players using keyboard/mouse or Xbox controllers.',
				zh: '支持最多 2 名玩家通过键盘鼠标或 Xbox 手柄进行本地多人游玩。',
			},
			{
				en: 'Loaded 3D models from OBJ files for environment and gameplay assets.',
				zh: '实现 OBJ 3D 模型加载，用于场景和玩法资产。',
			},
			{
				en: 'Built a post-processing chain to strengthen the hell-themed visual style.',
				zh: '搭建后处理链，强化整体地狱风格视觉。',
			},
			{
				en: 'Implemented a simple CPU quad particle system for gameplay effects.',
				zh: '实现简易 CPU quad 粒子系统，用于游戏特效。',
			},
			{
				en: 'Added simple IK behavior for spider enemies.',
				zh: '为蜘蛛敌人加入简易 IK 行为。',
			},
			{
				en: 'Used emissive textures, volumetric clouds, and hell-themed scene composition to shape the final mood.',
				zh: '使用自发光贴图、体积云和地狱风格场景搭建形成最终氛围。',
			},
		],
		media: {
			type: 'image',
			src: DoomensteinTitleImage.src,
			alt: {
				en: 'Doomenstein title image',
				zh: 'Doomenstein 标题图',
			},
		},
	},
	{
		slug: 'tgp-i',
		category: 'team',
		title: 'TGP I',
		summary: {
			en: 'A team game project placeholder prepared for a final trailer, gameplay description, team responsibilities, and production notes.',
			zh: '团队游戏项目占位展示，后续用于放置正式预告片、玩法描述、团队职责和制作说明。',
		},
		detail: {
			en: 'TGP I is a placeholder team-project detail page. The final page will include the trailer, project pitch, production scope, my role, and specific systems or content I contributed.',
			zh: 'TGP I 是团队项目详情页占位。最终页面会包含预告片、项目介绍、制作范围、我的职责，以及我参与完成的具体系统或内容。',
		},
		contribution: {
			en: 'Role and contribution details will be added after the final project materials are ready.',
			zh: '具体职责和贡献会在最终项目素材准备好后补充。',
		},
		tech: {
			en: 'Unreal Engine | C++ | Team Project',
			zh: 'Unreal Engine | C++ | 团队项目',
		},
		media: {
			type: 'video',
			src: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
			alt: {
				en: 'TGP I placeholder video',
				zh: 'TGP I 视频占位',
			},
		},
	},
	{
		slug: 'tgp-ii',
		category: 'team',
		title: 'TGP II',
		summary: {
			en: 'A second team project placeholder focused on collaboration, iteration, production scope, and the work I contributed to the team.',
			zh: '第二个团队项目占位展示，重点呈现协作、迭代、制作规模，以及我在团队中完成的工作。',
		},
		detail: {
			en: 'TGP II is a placeholder detail page for the second team game project. The final page will focus on the project goals, team process, implementation decisions, and the parts I owned or supported.',
			zh: 'TGP II 是第二个团队游戏项目的详情页占位。最终页面会重点展示项目目标、团队流程、实现决策，以及我负责或支持的部分。',
		},
		contribution: {
			en: 'Role and contribution details will be added after the final project materials are ready.',
			zh: '具体职责和贡献会在最终项目素材准备好后补充。',
		},
		tech: {
			en: 'Unreal Engine | C++ | Team Project',
			zh: 'Unreal Engine | C++ | 团队项目',
		},
		media: {
			type: 'video',
			src: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
			alt: {
				en: 'TGP II placeholder video',
				zh: 'TGP II 视频占位',
			},
		},
	},
];

export function getProjectsByCategory(category: ProjectCategory) {
	return projects.filter((project) => project.category === category);
}

export function getProjectBySlug(slug: string) {
	return projects.find((project) => project.slug === slug);
}
