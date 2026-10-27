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

文中的 EID 295、EID 712—810 对应这份帧捕获中的事件编号。

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

这里可能沿 U 方向扰动采样坐标，再降低亮度，让静态背景产生流动感。具体使用什么噪声，仅凭这两张图还无法确定。

## 背景：颜色与法线分开处理

<figure>
  <img src="/media/animal-well/background_1.png" alt="背景颜色层的装饰与空间构成" loading="lazy" />
  <figcaption>背景颜色层。较明亮的原始素材为后续光照和压暗保留了余量。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/background_2.png" alt="与背景颜色对应的法线信息" loading="lazy" />
  <figcaption>对应的法线结果。这里的颜色表达方向，不是物体的表面颜色。</figcaption>
</figure>

颜色贴图可以通过翻转 UV 改变朝向，法线贴图还涉及方向分量。翻转图像时，需要同时处理法线方向，才能保持光照关系正确。图中的法线结果也有相应变化，值得继续检查。

蓝色区域可以帮助判断法线朝向，但要确定坐标约定，还需要检查编码、解码和光照计算。

### 背景合成如何使用光与雾

<figure>
  <img src="/media/animal-well/background_3.png" alt="背景颜色、光照和遮罩参与后的合成结果" loading="lazy" />
  <figcaption>EID 295 附近的背景合成结果。</figcaption>
</figure>

EID 295 附近的背景合成涉及背景颜色、局部光照和 `visibility texture` 的 R 通道。我把它们的关系概括为：

```text
表面颜色 = lerp(材质颜色, 雾颜色, 雾系数)
照明项   = 局部光照 + 环境项 + 前景光贡献
合成颜色 ≈ 表面颜色 × 照明项
可见性遮罩决定哪些区域保留或受到抑制
```

这是合成关系的示意，具体权重、颜色空间转换和分支还需要检查。

<figure>
  <img src="/media/animal-well/foreground_1.png" alt="参与合成的前景光与噪声结果" loading="lazy" />
  <figcaption>用于分析背景环境照明的光照中间结果。</figcaption>
</figure>

这个结果呈现出上下亮度差异。我认为它与两层噪声有关，遮罩采样中还使用了 `v - 0.05` 偏移。如果按 180 像素高的归一化坐标换算，0.05 约为 9 像素；实际方向与尺度仍要结合采样坐标判断。

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

| 通道 | 我的判断 | 需要继续确认的内容 |
| --- | --- | --- |
| R | 可见性及带有过渡的区域遮罩 | 过渡可见；具体扩散或滤波算法尚未复现 |
| G | 与中景区域相关的遮罩 | 通过该场景的空间对应关系判断 |
| B | 与前景遮挡相关的遮罩 | 后续边缘判断使用该通道的模型见下文 |
| A | 与草、吊灯、玩家等动态物体相关的区域 | 不能由单帧证明完整分类规则 |

<figure>
  <img src="/media/animal-well/midground_3.png" alt="可见性贴图的 R 通道观察" loading="lazy" />
  <figcaption>R 通道的明暗过渡，可能与扩散和网格化滤波有关。</figcaption>
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

我推测 R 通道从平台遮挡出发，通过多次扩散形成过渡，并可能按 4×4 单元处理。要确定算法，还需要逐事件比较输入输出，或做一个最小复现。

## 透明效果与边缘提亮

<figure>
  <img src="/media/animal-well/foreground_2.png" alt="透明效果的中间结果" loading="lazy" />
  <figcaption>瀑布等效果相关的中间图像。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/foreground_3.png" alt="透明效果参与合成后的结果" loading="lazy" />
  <figcaption>透明效果参与合成后的结果。</figcaption>
</figure>

瀑布等透明效果经过了单独处理。画面上处于同一个空间层次的物体，渲染时仍可能分属不同 Pass。

遮罩还可以参与边缘提亮：先判断内部，再找出边缘区域，最后调整光照。下面用示意代码表达这一关系：

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

示意代码中的阈值用于说明判断关系，具体数值需要在复现时检查。

<figure>
  <img src="/media/animal-well/midground_7.png" alt="用于边缘判断的遮罩观察" loading="lazy" />
  <figcaption>遮罩提供区域边界，后续步骤可以利用边界附近的变化。</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_8.png" alt="中景边缘与光照结果" loading="lazy" />
  <figcaption>边缘与照明共同提高了区域之间的可读性。</figcaption>
</figure>

EID 712—810 一带还有压暗、模糊与 Bloom。具体的采样核和合成权重需要继续检查。

## 后续尝试

把画面拆开后，可以分别追踪颜色、法线、区域遮罩和光照。它们在合成时共同决定空间层次和物体的可读性。

如果要复现其中的思路，我会从三步开始：先建立独立的颜色与遮罩输出；再让同一遮罩同时控制可见性和边缘照明；最后加入光照图集与透明效果。每一步都保存中间结果，并在固定场景下比较启用、关闭后的差异。

复现时，我会优先检查法线镜像、通道用途、扩散过程和图集采样，再比较画面和性能。