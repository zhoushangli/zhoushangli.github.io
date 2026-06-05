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
	tech: string;
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
		slug: 'dfs-i',
		category: 'personal',
		title: 'DFS I Engine Foundation',
		summary: {
			en: 'An individual engine project focused on rendering, input, update loops, asset handling, and small gameplay tests as the engine grows from a technical base into a playable environment.',
			zh: '一个个人引擎项目，关注渲染、输入、更新循环、资源管理和小型玩法测试，让引擎从技术基础逐渐变成可玩的环境。',
		},
		detail: {
			en: 'DFS I is a placeholder project page for an individual custom engine. This page will later document the architecture, rendering path, input layer, asset pipeline, gameplay experiments, and lessons learned while building the engine.',
			zh: 'DFS I 是一个个人自定义引擎项目的占位详情页。之后这里会记录架构、渲染路径、输入层、资源管线、玩法实验，以及搭建引擎过程中的经验。',
		},
		contribution: {
			en: 'I am responsible for the full technical implementation and documentation of the engine foundation.',
			zh: '我负责引擎基础部分的完整技术实现和文档整理。',
		},
		tech: 'C++ | DirectX11 | Custom Engine',
		media: {
			type: 'image',
			src: '/images/dfs-static-placeholder.svg',
			alt: {
				en: 'DFS I Engine Foundation placeholder image',
				zh: 'DFS I 引擎基础占位图',
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
		tech: 'Unreal Engine | C++ | Team Project',
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
		tech: 'Unreal Engine | C++ | Team Project',
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
