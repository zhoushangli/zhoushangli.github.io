import MingEngineImage from '../content/images/ming_engine.png';
import DoomensteinTitleImage from '../content/images/doomenstein_titile.png';
import ThePrimaryColorsImage from '../content/images/the_primary_colors.png';
import HamsterballinImage from '../content/images/hamsterballin.jpg';

export type ProjectCategory = 'personal' | 'team';

export interface Project {
	slug: string;
	category: ProjectCategory;
	detailLayout?: 'stacked' | 'split';
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
	platform?: { zh: string; en: string };
	status?: { zh: string; en: string };
	decisions?: { zh: string; en: string }[];
	limitations?: { zh: string; en: string }[];
	relatedArticles?: string[];
	downloads?: { href: string; label: { zh: string; en: string } }[];
	role?: {
		en: string;
		zh: string;
	};
	tech: {
		en: string;
		zh: string;
	};
	renderingNotes?: { title: { zh: string; en: string }; body: { zh: string; en: string } }[];
	designNotes?: { title: { zh: string; en: string }; body: { zh: string; en: string } }[];
	developmentLogs?: { date: string; href: string; label: { zh: string; en: string } }[];
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
	externalLink?: {
		href: string;
		label: {
			en: string;
			zh: string;
		};
	};
	media: {
		type: 'image' | 'video';
		src: string;
		caption?: { zh: string; en: string };
		alt: {
			en: string;
			zh: string;
		};
	};
}

export const projects: Project[] = [
	{
		slug: 'ming-engine',
		"platform": {"zh": "Windows · Direct3D 11", "en": "Windows · Direct3D 11"},
		"status": {"zh": "持续开发中的个人引擎", "en": "Personal engine in active development"},
		"decisions": [{"zh": "参考 Godot 的节点与资源职责划分，将场景对象、序列化数据和渲染提交分开。", "en": "Use Godot as a reference for separating scene objects, serialized data and rendering submission."}, {"zh": "脚本桥接使用生成代码与反射绑定，编辑器逐步引入原生 UI。", "en": "Use generated code and reflection for script bindings while incrementally introducing native editor UI."}],
		"limitations": [{"zh": "原生编辑器 UI 与导出流程仍在完善，现有截图来自较早的编辑器阶段。", "en": "Native editor UI and export workflows are still evolving; the displayed screenshot is from an earlier editor stage."}],
		"relatedArticles": [],
		category: 'personal',
		title: 'MingEngine',
		summary: {
			en: 'A custom 3D game engine and editor I am building in C++, with DirectX 11 rendering and C#/.NET scripting.',
			zh: '我用 C++ 自研的 3D 游戏引擎与编辑器，使用 DirectX 11 渲染，支持 C#/.NET 脚本。',
		},
		detail: {
			en: 'MingEngine is a custom 3D game engine and editor built around a reusable C++ runtime. I developed a Godot-inspired node and scene architecture, a DirectX 11 rendering backend, and editor tools for importing assets, authoring scenes, inspecting properties and running gameplay. The current code integrates C# through .NET and introduces native CanvasItem/Control UI alongside the existing ImGui tooling.',
			zh: 'MingEngine 是一款围绕可复用 C++ 运行时开发的自定义 3D 游戏引擎与编辑器。我构建了受 Godot 启发的节点与场景架构、DirectX 11 渲染后端，以及资源导入、场景编辑、属性检查与运行工具。目前源码采用 C#/.NET 脚本集成，并在既有 ImGui 工具之外推进原生 CanvasItem/Control UI。',
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
			en: 'Custom engine | C++ | DirectX 11',
			zh: '自研引擎 | C++ | DirectX 11',
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
				en: "Integrated C# through hostfxr, generated managed wrappers and reflection-backed native method bindings.",
				zh: '通过 hostfxr、生成的托管包装和反射方法绑定接入 C#。',
			},
		],
		media: {
			type: 'image',
			src: MingEngineImage.src,
			caption: {
				en: 'MingEngine editor screenshot from an earlier development stage',
				zh: 'MingEngine 较早开发阶段的编辑器截图',
			},
			alt: {
				en: 'MingEngine editor showing its scene and tool panels',
				zh: 'MingEngine 编辑器中的场景和工具面板',
			},
		},
	},
	{
  "slug": "spectrex",
  "category": "team",
  "detailLayout": "stacked",
  "title": "SpectreX",
  "summary": {
    "zh": "一款结合光学解谜的类银河恶魔城游戏。我担任策划，负责全部三章的关卡设计，并参与程序和技术美术。",
    "en": "A Metroidvania with optical puzzles. I was the designer for all three chapters and also contributed programming and technical art."
  },
  "detail": {
    "zh": "SpectreX 由团队使用 Godot 与 C# 制作，围绕光路、颜色与场景交互设计谜题。玩家通过反射、分光和合光操作机关，在相互连接的场景中探索。",
    "en": "SpectreX is a team project built with Godot and C#. Puzzles use light paths, colors and environmental interactions. Players reflect, split and combine light to operate mechanisms and explore connected spaces."
  },
  "contribution": {
    "zh": "我负责全部三章的关卡设计，并参与玩法简化、程序和技术美术。开发期间，我全程观察了约 10 小时的深度试玩，与测试者一起复盘，并根据反馈调整关卡。",
    "en": "I designed the levels across all three chapters and contributed to simplifying the mechanics, programming and technical art. During development, I closely observed about 10 hours of in-depth playtesting, reviewed the levels with testers and revised them based on feedback."
  },
  "role": {
    "zh": "策划 · 程序 · 技术美术",
    "en": "Game designer · programmer · technical artist"
  },
  "tech": {
    "zh": "Godot | C#",
    "en": "Godot | C#"
  },
  "platform": {
    "zh": "桌面端 · Godot",
    "en": "Desktop · Godot"
  },
  "status": {
    "zh": "团队制作项目",
    "en": "Team production"
  },
  "features": [
    {
      "zh": "按颜色频率处理光线传播、反射与感光器输入。",
      "en": "Process light propagation, reflections and sensor input by color frequency."
    },
    {
      "zh": "通过脏标记与求解预算分配光路更新。",
      "en": "Schedule light-path updates with dirty flags and solving budgets."
    },
    {
      "zh": "使用房间、存档、UI 与编辑器插件支持内容制作。",
      "en": "Support content production with room, save and UI services and editor plugins."
    },
    {
      "zh": "区分真实的机关激活条件与用于阅读场景的视觉反馈状态。",
      "en": "Separate actual mechanism activation from visual feedback used to read the scene."
    },
    {
      "zh": "将光学求解与画面合成分开，使玩法状态和视觉效果各自维护。",
      "en": "Keep optical solving separate from image compositing so gameplay state and presentation can be maintained independently."
    }
  ],
  "decisions": [],
  "limitations": [],
  "relatedArticles": [],
  "externalLink": {
    "href": "https://www.bilibili.com/video/BV1gEny6hEAC/",
    "label": {
      "zh": "在 B 站观看宣传视频 ↗",
      "en": "Watch the trailer on Bilibili ↗"
    }
  },
  "embedVideo": {
    "src": "https://player.bilibili.com/player.html?bvid=BV1gEny6hEAC&page=1&autoplay=0",
    "title": {
      "zh": "[2026 TapTap 聚光灯] SpectreX——我们用三周做了一款光学解谜游戏！",
      "en": "[2026 TapTap Spotlight] SpectreX — We made an optical puzzle game in three weeks!"
    }
  },
  "media": {
    "type": "image",
    "src": "/media/projects/spectrex-cover.jpg",
    "caption": {
      "zh": "SpectreX 宣传封面",
      "en": "SpectreX promotional cover"
    },
    "alt": {
      "zh": "SpectreX 彩色标题与像素风场景",
      "en": "The SpectreX title in rainbow colors over a pixel-art scene"
    }
  },
  "designNotes": [
    {
      "title": {
        "zh": "章节与关卡设计",
        "en": "Chapters and levels"
      },
      "body": {
        "zh": "我先确定章节整体的行进方式，再安排房间里的教学、挑战和变化。第一章围绕下落与返回展开，第三章围绕光路回环组织关卡。各个房间的小动态与章节整体的大动态配合。",
        "en": "I planned the overall movement through each chapter before designing individual rooms for teaching, challenges and variations. The first chapter centers on descent and return; the third uses looping light paths. Each room supports the larger movement of the chapter."
      }
    },
    {
      "title": {
        "zh": "玩法简化",
        "en": "Simplifying the mechanics"
      },
      "body": {
        "zh": "我将原先 16 个光的频率简化为 3 个，并通过明确的分光镜和合光镜组织玩法，让光路规则更容易理解，也方便围绕有限规则设计谜题。",
        "en": "I simplified the original 16 light frequencies to three and organized the mechanics around explicit light-splitting and combining devices. This made the rules easier to understand and gave level design a smaller set of mechanics to combine."
      }
    },
    {
      "title": {
        "zh": "试玩与关卡调整",
        "en": "Playtesting and iteration"
      },
      "body": {
        "zh": "我邀请同学进行多轮深度试玩，让他们边玩边说出自己的想法，并全程观察约 10 小时。测试结束后，我们一起重走关卡，复盘卡住的位置和当时的判断。早期部分关卡难度过高，原本安排在第二章的内容后来移到了第三章。测试也暴露了背景被误认为平台、出口藏在暗处等引导问题。",
        "en": "I invited classmates to multiple in-depth playtests and asked them to think aloud, closely observing about 10 hours in total. Afterwards, we walked through the levels again to discuss where they got stuck and what they had expected. Some early levels were too difficult, so content originally planned for chapter two moved to chapter three. Testing also revealed misleading background platforms and exits hidden in darkness."
      }
    }
  ],
  "developmentLogs": [
    {
      "date": "2026-10-03",
      "href": "https://www.taptap.cn/moment/855777399978066391",
      "label": {
        "zh": "第一周开发日志",
        "en": "Week one"
      }
    },
    {
      "date": "2026-10-07",
      "href": "https://www.taptap.cn/moment/857245166883311389",
      "label": {
        "zh": "第二周开发日志",
        "en": "Week two"
      }
    },
    {
      "date": "2026-10-11",
      "href": "https://www.taptap.cn/moment/858659679956370829",
      "label": {
        "zh": "第二周开发日志",
        "en": "Week two"
      }
    },
    {
      "date": "2026-10-18",
      "href": "https://www.taptap.cn/moment/861213861250862698",
      "label": {
        "zh": "第三周开发日志",
        "en": "Week three"
      }
    },
    {
      "date": "2026-10-20",
      "href": "https://www.taptap.cn/moment/861635509066140433",
      "label": {
        "zh": "第三周开发日志",
        "en": "Week three"
      }
    },
    {
      "date": "2026-10-24",
      "href": "https://www.taptap.cn/moment/863177748976239312",
      "label": {
        "zh": "开发总结",
        "en": "Development retrospective"
      }
    }
  ],
  "renderingNotes": [
    {
      "title": {
        "zh": "分层采集与多阶段合成",
        "en": "Layer capture and staged composition"
      },
      "body": {
        "zh": "我基于 Godot 的 SubViewport 和 CanvasItem Shader 搭建了多阶段 2D 渲染管线。场景按远景、背景、中景和前景分别采集，先完成各层的处理，再通过 Composite A/B/C 逐步合成。这让我可以控制光带、透明物体和普通场景层之间的先后关系。",
        "en": "I built a multi-stage 2D rendering pipeline using Godot SubViewports and CanvasItem shaders. Far background, background, midground and foreground are captured separately, processed, then combined through Composite A/B/C. This gives me control over the order of light beams, transparent objects and ordinary scene layers."
      }
    },
    {
      "title": {
        "zh": "分开处理颜色与材质数据",
        "en": "Separate color and material data"
      },
      "body": {
        "zh": "透明物体分别输出颜色覆盖、法线与粗糙度，再读取前一阶段的场景颜色进行扭曲和模糊，最后恢复自身颜色与高光。中景和前景各有处理阶段，可以使用不同的背景输入。背景光照也单独采集法线与局部光源，再结合环境光、Glow 和负光合成。",
        "en": "Transparent objects output color coverage, normals and roughness separately. Their passes sample the preceding scene color for distortion and blur, then restore surface color and highlights. Midground and foreground have separate stages with different scene inputs. Background lighting also captures normals and local lights separately before combining them with ambient light, glow and negative light."
      }
    },
    {
      "title": {
        "zh": "分层自发光与后处理",
        "en": "Layered emission and post-processing"
      },
      "body": {
        "zh": "自发光按背景、中景透明、中景、前景透明和前景分别采集，并结合普通场景层的覆盖关系合成。合成后的可见发光统一生成光晕，再与场景颜色叠加。之后依次处理可见性、渐变调色和颜色调整，让遮挡、光晕与最终色彩各有明确的位置。",
        "en": "Emission is captured separately for background, transparent midground, midground, transparent foreground and foreground. It is composited using the coverage of ordinary scene layers, then blurred into a shared glow and added to scene color. Visibility, gradient color filtering and color adjustment follow, giving occlusion, glow and final color distinct stages."
      }
    },
    {
      "title": {
        "zh": "管线调度与配置分工",
        "en": "Scheduling and configuration"
      },
      "body": {
        "zh": "RenderService 负责管线生命周期、当前场景接入和配置切换；RenderPipeline 负责中间纹理连接、视口依赖顺序、启停与最终输出。具体效果放在对应 ShaderMaterial 和配置资源中。采集阶段跟随场景相机，处理与合成阶段使用屏幕坐标；运行时还可以保存材质参数、重载背景配置，便于调试画面。",
        "en": "RenderService handles pipeline lifetime, current-scene integration and configuration changes. RenderPipeline connects intermediate textures, orders viewport dependencies and controls activation and output. Effects are authored in their ShaderMaterials and configuration resources. Capture follows the scene camera while processing and composition use screen coordinates. Runtime material saving and background-configuration reloading support visual tuning."
      }
    }
  ]
},
	{
		slug: 'doomenstein',
		"platform": {"zh": "桌面端 · 键鼠与 Xbox 手柄", "en": "Desktop · keyboard/mouse & Xbox controllers"},
		"status": {"zh": "复古射击游戏原型", "en": "Retro shooter prototype"},
		"decisions": [{"zh": "用八方向精灵保留复古角色表现，再以模型、粒子与后处理扩展场景层次。", "en": "Retain a retro character style with eight-direction sprites, then extend scene depth with models, particles and post-processing."}, {"zh": "将输入与玩家实例分开组织，以支持本地双人。", "en": "Separate input handling from player instances to support local two-player play."}],
		"limitations": [{"zh": "项目以小规模可玩原型为范围，蜘蛛 IK 与敌人逻辑服务于该范围。", "en": "The project is scoped as a small playable prototype; spider IK and enemy behavior are designed for that scope."}],
		"relatedArticles": [],
		category: 'personal',
		title: 'Doomenstein',
		summary: {
			en: 'A retro 3D first-person shooter built on my own C++ engine, with eight-direction sprites and local two-player support.',
			zh: '基于自研 C++ 引擎制作的复古 3D 第一人称射击游戏，使用八方向精灵，支持本地双人。',
		},
		detail: {
			en: 'Built on my own C++ engine, Doomenstein began as a retro-style 3D first-person shooter using 8-direction sprites, with local multiplayer support for up to two players using keyboard/mouse or Xbox controllers. I later expanded it with OBJ model loading, simple IK, a post-processing chain, CPU quad particles, volumetric clouds, emissive textures, and a hell-themed environment, turning it into a small but complete doomlike shooter prototype.',
			zh: '《末日迷宫》（Doomenstein）基于我的自研 C++ 引擎开发，最初是一款复古风格的 3D 第一人称射击游戏，使用 8 面精灵图表现角色朝向，并支持最多 2 名玩家通过键盘鼠标或 Xbox 手柄进行本地多人游玩。随后我为项目加入了 OBJ 3D 模型加载、简易 IK、后处理链、CPU quad 粒子、体积云、自发光贴图和地狱风格场景，将它扩展成一个简单但完整的 doomlike 地狱射击游戏原型。',
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
			en: 'Custom engine | C++ | DirectX 11',
			zh: '自研引擎 | C++ | DirectX 11',
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
			caption: {
				en: 'Doomenstein title image',
				zh: 'Doomenstein 标题图',
			},
			alt: {
				en: 'Doomenstein title image',
				zh: 'Doomenstein 标题图',
			},
		},
	},
	{
		slug: 'the-primary-colors',
		"platform": {"zh": "Unity 桌面游戏", "en": "Unity desktop game"},
		"status": {"zh": "独立完成的解谜平台游戏", "en": "Independently developed puzzle platformer"},
		"decisions": [{"zh": "以颜色切换能力为核心，通过三十个手工关卡逐步引入机制与组合。", "en": "Build around color-dependent abilities, introducing mechanics and combinations across thirty handcrafted levels."}, {"zh": "使用 QFramework 与 MVC 分离数据、表现和控制，使用事件与命令组织交互。", "en": "Separate data, presentation and control with QFramework/MVC, and organize interactions with events and commands."}],
		"limitations": [{"zh": "关卡与表现围绕颜色能力展开，重点是机制表达和独立制作实践。", "en": "Levels and presentation focus on color abilities, emphasizing mechanic communication and independent production."}],
		"relatedArticles": [],
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
			en: 'Unity | C# | QFramework',
			zh: 'Unity | C# | QFramework',
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
			caption: {
				en: 'The Primary Colors title image',
				zh: '《三原色》封面图',
			},
			alt: {
				en: 'The Primary Colors title image',
				zh: '《三原色》封面图',
			},
		},
	},
	{
		slug: 'hamsterballin',
		"platform": {"zh": "PC · Unreal Engine 5", "en": "PC · Unreal Engine 5"},
		"status": {"zh": "团队游戏项目 · Steam 页面可访问", "en": "Team game project · Steam page available"},
		"decisions": [{"zh": "将重复的赛道制作任务转化为 PCG 道路生成流程，配合美术生产使用。", "en": "Turn repetitive track-authoring work into a PCG road-generation workflow for art production."}, {"zh": "围绕实际制作需求处理生成开销，并协作完成材质、视觉效果和部分 UI。", "en": "Address generation overhead for production needs and collaborate on materials, effects and selected UI features."}],
		"limitations": [{"zh": "游戏由团队共同制作，我主要参与道路生成工具、技术美术和部分 UI。", "en": "The game was made by a team. My work focused on road-generation tools, technical art and selected UI features."}],
		"relatedArticles": [],
		category: 'team',
		detailLayout: 'stacked',
		title: "Hamsterballin'",
		summary: {
			en: 'A competitive arcade racer developed by a team in Unreal Engine 5, where players roll, bounce, disrupt rivals, and discover creative shortcuts as hamsters racing inside balls.',
			zh: '一款由团队使用 Unreal Engine 5 开发的竞技街机赛车游戏。玩家操控仓鼠球滚动、弹跳、干扰对手，并在充满想象力的赛道中寻找捷径。',
		},
		detail: {
			en: "Hamsterballin' is a competitive arcade racing game developed by an SMU Guildhall team in Unreal Engine 5. Players race through imaginative tracks as hamsters inside rolling balls, using momentum, environmental interactions, and creative shortcuts to gain an advantage over their opponents.",
			zh: "《Hamsterballin'》是一款由 SMU Guildhall 团队使用 Unreal Engine 5 开发的竞技街机赛车游戏。玩家操控仓鼠球穿越充满想象力的赛道，利用动量、场景交互和隐藏捷径取得比赛优势。",
		},
		contribution: {
			en: "My primary responsibility was developing the procedural road-generation workflow with Unreal Engine 5's PCG framework and optimizing its performance for production use. I also collaborated with artists to build materials and other visual effects, supported technical art workflows during track production, and contributed to selected UI features.",
			zh: '我的主要职责是使用 Unreal Engine 5 的 PCG 框架开发程序化道路生成流程，并对 PCG 系统进行性能优化，使其能够稳定用于赛道生产。我也与美术成员合作搭建材质和其他视觉效果，为赛道制作提供技术美术支持，并参与部分 UI 功能的实现。',
		},
		duration: '2026.1 - 2026.5',
		role: {
			en: 'Game Programmer',
			zh: '游戏程序',
		},
		tech: {
			en: 'Unreal Engine 5 | PCG',
			zh: 'Unreal Engine 5 | PCG',
		},
		features: [
			{
				en: 'Developed PCG-based procedural road-generation tools for track production.',
				zh: '开发基于 PCG 的程序化道路生成工具，用于赛道生产。',
			},
			{
				en: 'Optimized PCG generation performance to support an efficient production workflow.',
				zh: '优化 PCG 生成性能，提升赛道制作流程的效率。',
			},
			{
				en: 'Collaborated with artists on materials and other visual effects, providing technical support for asset integration.',
				zh: '与美术成员合作搭建材质和其他视觉效果，并为美术资源整合提供技术支持。',
			},
			{
				en: 'Implemented and supported selected UI functionality.',
				zh: '实现并协助完善部分 UI 功能。',
			},
		],
		embedVideo: {
			src: 'https://www.youtube.com/embed/ogLB5EIMdcw',
			title: {
				en: "Hamsterballin' gameplay video",
				zh: "《Hamsterballin'》游戏演示视频",
			},
		},
		externalLink: {
			href: 'https://store.steampowered.com/app/4319370/Hamsterballin/',
			label: {
				en: 'View on Steam',
				zh: '前往 Steam',
			},
		},
		media: {
			type: 'image',
			src: HamsterballinImage.src,
			caption: {
				en: "Hamsterballin' title image",
				zh: "《Hamsterballin'》封面图",
			},
			alt: {
				en: "Hamsterballin' title image",
				zh: "《Hamsterballin'》封面图",
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
