---
contentId: animal-well-rendering
lang: zh
section: articles
title: "《动物井》渲染分析"
description: "根据帧捕获截图，分析《动物井》的分层画面、光照和遮罩。"
category: graphics
tags: [RenderDoc, 分层渲染, Shader, 游戏分析]
draft: false
---

## 从一帧画面开始

《动物井》的画面由低分辨率像素素材组成，却能表现出丰富的空间层次、柔和的环境光与清楚的可交互区域。我希望理解：这些效果分别由哪些中间结果产生，又怎样在合成时联系起来？

这篇笔记根据保存的帧捕获截图整理，没有重新回放捕获，也没有游戏源码。EID 295、EID 712—810 是这份捕获中的事件编号；对通道和算法的解释仍有待验证。

## 先看画面的四个层次

为了阅读捕获，我把画面划分为远景、背景、中景和前景。这是分析上的空间分组，并不意味着引擎只有四个绘制阶段；法线、光照、透明效果与后处理会带来额外的中间步骤。

```text
远景图像与扰动
    ↓
背景颜色、法线与背景光照
    ↓
中景角色和交互物体、可见性遮罩
    ↓
前景遮挡与合成
    ↓
最终调色、模糊与辉光
```

先认清每张中间贴图存了什么，再看它怎样参与后续合成。

## 远景：静态图像也能产生流动感

<figure>
  <img src="/media/animal-well/farground_1.png" alt="捕获中的远景基础图像" loading="lazy" />
  <figcaption>远景基础图像。它提供空间背景，不直接承担玩家交互信息。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/farground_2.png" alt="压暗并加入扰动后的远景结果" loading="lazy" />
  <figcaption>经过亮度处理和横向扰动后，静态素材呈现出更柔和的远处层次。</figcaption>
</figure>

原笔记将变化解释为沿 U 方向加入连续噪声，再降低亮度。前后两张图与这个解释相符，具体的噪声函数和动画参数还需要检查。静态素材也可以通过改变采样坐标产生流动感。

## 背景：颜色与法线分开处理

<figure>
  <img src="/media/animal-well/background_1.png" alt="背景颜色层的装饰与空间构成" loading="lazy" />
  <figcaption>背景颜色层。较明亮的原始素材为后续光照和压暗保留了余量。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/background_2.png" alt="与背景颜色对应的法线信息" loading="lazy" />
  <figcaption>对应的法线结果。这里的颜色表达方向，不是物体的表面颜色。</figcaption>
</figure>

颜色贴图可以通过翻转 UV 改变朝向；法线贴图还涉及方向分量，不能只把图像翻过来就假定光照关系仍然正确。原分析注意到法线结果存在相应处理，因此将其作为镜像绘制时需要关注的步骤。

蓝色区域可以帮助判断法线朝向，但要确定坐标约定，还需要检查编码、解码和光照计算。

### 背景合成如何使用光与雾

<figure>
  <img src="/media/animal-well/background_3.png" alt="背景颜色、光照和遮罩参与后的合成结果" loading="lazy" />
  <figcaption>原捕获中 EID 295 附近记录的背景合成结果。</figcaption>
</figure>

原笔记在 EID 295 处关联了背景图像、经过限制的光照以及 `visibility texture` 的 R 通道，并记录它们参与背景合成。可以把其中的关系整理为下列阅读模型：

```text
表面颜色 = lerp(材质颜色, 雾颜色, 雾系数)
照明项   = 局部光照 + 环境项 + 前景光贡献
合成颜色 ≈ 表面颜色 × 照明项
可见性遮罩决定哪些区域保留或受到抑制
```

上面是根据笔记整理的合成示意，省略了未记录的权重、颜色空间转换和分支。

<figure>
  <img src="/media/animal-well/foreground_1.png" alt="参与合成的前景光与噪声结果" loading="lazy" />
  <figcaption>笔记中称为前景光的中间结果，也被用于解释背景的环境照明。</figcaption>
</figure>

这个结果呈现出上下亮度差异。笔记将其归因于两层噪声，并记录遮罩采样中的 `v - 0.05` 偏移；如果按 180 像素高的归一化坐标换算，0.05 对应约 9 像素。偏移究竟朝哪个屏幕方向、是否始终使用这一尺度，仍取决于实际坐标和采样路径。

### 灯光图集：先分开绘制，再统一叠加

<figure>
  <img src="/media/animal-well/background_4.png" alt="由多个格子组成的灯光图集" loading="lazy" />
  <figcaption>保存的光照中间图。多个光源的贡献分布在不同区域。</figcaption>
</figure>

这份捕获中的光照贴图为 1280×720，可以按 320×180 划分为 4×4 格。这提示单个光源可能先分别绘入图集，再参与合成；每一格是否都有效，还要检查具体事件。

## 中景：颜色之外，还需要可见性信息

<figure>
  <img src="/media/animal-well/midground_1.png" alt="角色与可交互区域所在的中景图像" loading="lazy" />
  <figcaption>中景包含角色及与玩法相关的物体，是阅读画面时的重要层次。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_2.png" alt="将多种遮罩打包在一起的可见性贴图" loading="lazy" />
  <figcaption>直接显示整张 RGBA 贴图时，颜色混合容易掩盖各通道的独立作用。</figcaption>
</figure>

将通道分开查看，能更清楚地比较它们与场景区域的关系：

| 通道 | 原笔记对该捕获的解释 | 证据边界 |
| --- | --- | --- |
| R | 可见性及带有过渡的区域遮罩 | 过渡可见；具体扩散或滤波算法尚未复现 |
| G | 与中景区域相关的遮罩 | 通过该场景的空间对应关系判断 |
| B | 与前景遮挡相关的遮罩 | 后续边缘判断使用该通道的模型见下文 |
| A | 与草、吊灯、玩家等动态物体相关的区域 | 不能由单帧证明完整分类规则 |

<figure>
  <img src="/media/animal-well/midground_3.png" alt="可见性贴图的 R 通道观察" loading="lazy" />
  <figcaption>R 通道观察。原笔记据其过渡形态提出扩散与网格化滤波的解释。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_4.png" alt="可见性贴图的 G 通道观察" loading="lazy" />
  <figcaption>G 通道观察。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_5.png" alt="可见性贴图的 B 通道观察" loading="lazy" />
  <figcaption>B 通道观察。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_6.png" alt="可见性贴图的 A 通道观察" loading="lazy" />
  <figcaption>A 通道观察。</figcaption>
</figure>

原笔记推测 R 通道从平台遮挡出发，通过多次扩散形成过渡，并可能按 4×4 单元处理。要确定算法，需要逐事件比较输入输出，或做一个最小复现。

## 透明效果与边缘提亮

<figure>
  <img src="/media/animal-well/foreground_2.png" alt="笔记中记录的透明效果中间结果" loading="lazy" />
  <figcaption>瀑布等效果相关的中间图像。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/foreground_3.png" alt="透明效果参与合成后的结果" loading="lazy" />
  <figcaption>透明效果的另一合成阶段。图片沿用原笔记文件对应关系，不能仅凭文件名判断其引擎层级。</figcaption>
</figure>

在该场景的阅读模型中，瀑布等透明效果并不完全并入普通中景绘制，而是经过单独处理。这提醒我：空间上的“中景”与渲染实现上的一个 Pass 并不是一一对应的。

边缘提亮是另一个值得借鉴的联系：遮罩不仅用于裁剪，也可以改变照明。原笔记整理过下面的示意代码，用来表达“先判断内部，再判断边缘，最后调整光照”的关系：

```hlsl
bool inside = B >= 0.7874;
bool addRim = !inside && R > 0.35;

float3 lighting =
    foregroundLight.rgb
    + (inside ? 0.05 : 1.0) * lightMask.rgb
    + (addRim ? ambientLightColor.rgb * rimLightBrightness : 0)
    + ambientLightColor.rgb * fgAmbientLightColor.rgb;

output.rgb = foreground.rgb * lighting;
output.a = foreground.a;
```

这段示意代码保留了当时笔记中的阈值，具体数值只用于说明这份分析，不直接作为其他场景的参数。

<figure>
  <img src="/media/animal-well/midground_7.png" alt="用于边缘判断的遮罩观察" loading="lazy" />
  <figcaption>遮罩提供区域边界，后续步骤可以利用边界附近的变化。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_8.png" alt="笔记中记录的中景边缘与光照结果" loading="lazy" />
  <figcaption>边缘与照明共同提高了区域之间的可读性。</figcaption>
</figure>

原笔记还记录了 EID 712—810 一带的压暗、模糊与 Bloom。具体的采样核和合成权重留待重新回放时检查。

## 后续尝试

把画面拆开后，可以分别追踪颜色、法线、区域遮罩和光照。它们在合成时共同决定空间层次和物体的可读性。

如果要复现其中的思路，我会从三步开始：先建立独立的颜色与遮罩输出；再让同一遮罩同时控制可见性和边缘照明；最后加入光照图集与透明效果。每一步都保存中间结果，并在固定场景下比较启用、关闭后的差异。

目前还没有完成画面复现或性能测量。下一步优先检查法线镜像、通道用途、扩散过程和图集采样。