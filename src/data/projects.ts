import MingEngineImage from '../content/images/ming_engine.png';
import DoomensteinTitleImage from '../content/images/doomenstein_titile.png';
import ThePrimaryColorsImage from '../content/images/the_primary_colors.png';

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
	embedVideo?: {
		src: string;
		title: {
			en: string;
			zh: string;
		};
	};
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
		slug: 'ming-engine',
		category: 'personal',
		title: 'MingEngine',
		summary: {
			en: 'A Godot-inspired 3D game engine and editor built with C++ and DirectX 11, featuring a node-based scene system, asset pipeline, scene serialization, editor tooling, and AngelScript integration.',
			zh: '一款使用 C++ 和 DirectX 11 开发、受 Godot 启发的 3D 游戏引擎与编辑器，包含节点式场景系统、资源管线、场景序列化、编辑器工具和 AngelScript 集成。',
		},
		detail: {
			en: 'MingEngine is a custom 3D game engine and editor built around a reusable C++ runtime. I developed a Godot-inspired node and scene architecture, a DirectX 11 rendering backend, and an ImGui-based editor that connects asset importing, scene authoring, inspection, serialization, and runtime execution into one workflow.',
			zh: 'MingEngine 是一款围绕可复用 C++ 运行时开发的自定义 3D 游戏引擎与编辑器。我构建了受 Godot 启发的节点与场景架构、DirectX 11 渲染后端，以及基于 ImGui 的编辑器，将资源导入、场景编辑、属性检查、序列化和游戏运行连接成一套完整工作流。',
		},
		contribution: {
			en: 'As the solo engine developer, I designed and implemented the engine architecture, rendering backend, scene and resource systems, editor tools, asset pipeline, and scripting integration.',
			zh: '作为独立引擎开发者，我设计并实现了引擎架构、渲染后端、场景与资源系统、编辑器工具、资源管线和脚本集成。',
		},
		duration: '2026.5 - Present',
		role: {
			en: 'Solo Engine Developer',
			zh: '独立引擎开发者',
		},
		tech: {
			en: 'C++ | DirectX 11 | ImGui | AngelScript',
			zh: 'C++ | DirectX 11 | ImGui | AngelScript',
		},
		features: [
			{
				en: 'Built a Godot-inspired node, scene tree, reflection, and class-registration system.',
				zh: '构建了受 Godot 启发的节点、场景树、反射和类注册系统。',
			},
			{
				en: 'Developed an ImGui editor with scene hierarchy, inspector, filesystem, import, viewport, and output panels.',
				zh: '开发了基于 ImGui 的编辑器，包含场景层级、属性检查器、文件系统、资源导入、视口和输出面板。',
			},
			{
				en: 'Implemented interactive translation, rotation, and scale gizmos for editing 3D transforms.',
				zh: '实现了用于编辑 3D 变换的交互式移动、旋转和缩放 Gizmo。',
			},
			{
				en: 'Created an asset pipeline for images, OBJ, and glTF models with custom serialized texture, mesh, and scene resources.',
				zh: '构建了支持图片、OBJ 和 glTF 模型的资源管线，并实现自定义纹理、网格和场景资源序列化。',
			},
			{
				en: 'Built a DirectX 11 renderer supporting material textures, directional and point lights, CPU particles, and post-processing.',
				zh: '构建了支持材质纹理、方向光、点光源、CPU 粒子和后处理的 DirectX 11 渲染器。',
			},
			{
				en: "Integrated AngelScript through generated bindings backed by the engine's reflection metadata.",
				zh: '通过基于引擎反射元数据生成的绑定集成 AngelScript。',
			},
		],
		media: {
			type: 'image',
			src: MingEngineImage.src,
			alt: {
				en: 'MingEngine editor interface',
				zh: 'MingEngine 编辑器界面',
			},
		},
	},
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
		embedVideo: {
			src: 'https://player.bilibili.com/player.html?isOutside=true&bvid=BV1x75d6uEBT&page=1&autoplay=0',
			title: {
				en: 'Doomenstein gameplay video',
				zh: 'Doomenstein 演示视频',
			},
		},
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
		slug: 'the-primary-colors',
		category: 'personal',
		title: 'The Primary Colors',
		summary: {
			en: 'A solo-developed puzzle platformer featuring 30 handcrafted levels, where players gain different abilities by touching colors and use them to overcome environmental challenges.',
			zh: '一款独立开发的平台解谜游戏，包含 30 个手工设计的关卡。玩家通过接触不同颜色改变自身能力，并利用这些能力解决谜题、通过关卡。',
		},
		detail: {
			en: 'The Primary Colors is a puzzle platformer built with Unity and QFramework. Players change their abilities by touching different colors, then combine those abilities with movement and environmental interactions to progress through each level. I independently developed the game and designed 30 handcrafted levels around the color-switching mechanic. The project also became an important milestone in my development career and helped me earn my internship opportunity at Tencent MoreFun Studios.',
			zh: '《三原色》是一款使用 Unity 和 QFramework 制作的平台解谜游戏。玩家通过接触不同颜色改变自己的能力，并结合移动与场景交互逐步通过关卡。我独立完成了游戏开发，并围绕颜色切换机制设计了 30 个手工关卡。这个项目也是我游戏开发经历中的重要里程碑，并帮助我获得了前往腾讯魔方工作室群实习的机会。',
		},
		contribution: {
			en: 'As the solo developer, I designed and implemented the core mechanics, software architecture, event and command systems, presentation, and all 30 levels.',
			zh: '作为独立开发者，我负责核心机制、软件架构、事件与命令系统、表现层以及全部 30 个关卡的设计与实现。',
		},
		duration: '2023.6 - 2023.8',
		role: {
			en: 'Solo Developer',
			zh: '独立开发者',
		},
		tech: {
			en: 'Unity | C# | QFramework | MVC',
			zh: 'Unity | C# | QFramework | MVC',
		},
		features: [
			{
				en: "Designed a color-based ability system that changes the player's capabilities through environmental interaction.",
				zh: '设计了基于颜色的能力系统，玩家通过与环境中的颜色交互改变自身能力。',
			},
			{
				en: 'Created 30 handcrafted puzzle-platforming levels with progressively introduced mechanics.',
				zh: '设计并制作了 30 个手工平台解谜关卡，并逐步引入新的游戏机制。',
			},
			{
				en: 'Structured the project with QFramework and an MVC architecture separating data, presentation, and gameplay control.',
				zh: '使用 QFramework 和 MVC 架构组织项目，分离数据层、表现层和游戏控制逻辑。',
			},
			{
				en: 'Built an event system to decouple communication between gameplay systems and presentation.',
				zh: '构建事件系统，解耦游戏系统与表现层之间的通信。',
			},
			{
				en: 'Implemented a command system to encapsulate gameplay actions and application flow.',
				zh: '实现命令系统，用于封装游戏行为和程序流程。',
			},
		],
		embedVideo: {
			src: 'https://player.bilibili.com/player.html?isOutside=true&bvid=BV1d94y1W7UU&page=1&autoplay=0',
			title: {
				en: 'The Primary Colors gameplay video',
				zh: '《三原色》游戏演示视频',
			},
		},
		media: {
			type: 'image',
			src: ThePrimaryColorsImage.src,
			alt: {
				en: 'The Primary Colors title image',
				zh: '《三原色》封面图',
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
