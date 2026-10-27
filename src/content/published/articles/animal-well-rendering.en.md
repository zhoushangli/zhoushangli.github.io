---
contentId: animal-well-rendering
lang: en
section: articles
title: "Animal Well Rendering Analysis"
description: "A frame-capture study of layers, lighting and masks in Animal Well."
category: graphics
tags: [RenderDoc, Layered Rendering, Shader, Game Analysis]
draft: false
---

## Starting with one frame

Animal Well builds a rich sense of depth, soft environmental lighting, and readable interactive spaces from low-resolution pixel assets. I wanted to understand which intermediate results produce these effects, and how the final composition connects them.

EID 295 and EID 712–810 identify events in this frame capture.

## Start with four spatial layers

I divide the image into far background, background, midground, and foreground to make the capture easier to read. These are analytical spatial groups, not a claim that the engine has exactly four rendering passes. Normals, lighting, transparency, and post-processing introduce additional intermediate steps.

```text
Far-background image and distortion
    ↓
Background color, normals, and lighting
    ↓
Midground characters, interactive objects, and visibility masks
    ↓
Foreground occlusion and composition
    ↓
Final grading, blur, and bloom
```

First identify what each intermediate texture stores, then follow how it is used in the composition.

## Far background: motion from a static image

<figure>
  <img src="/media/animal-well/farground_1.png" alt="Base image used for the far background in the capture" loading="lazy" />
  <figcaption>The far-background base image supplies spatial context rather than direct interaction information.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/farground_2.png" alt="Far background after darkening and distortion" loading="lazy" />
  <figcaption>Brightness processing and horizontal distortion give the static asset a softer, more distant appearance.</figcaption>
</figure>

The background may use continuous noise to offset sampling along U, followed by darkening. This would give a static image a sense of motion. The two images alone do not reveal the exact noise function or animation settings.

## Background: separate color from direction

<figure>
  <img src="/media/animal-well/background_1.png" alt="Decorative elements and spatial composition in the background color layer" loading="lazy" />
  <figcaption>The background color layer. Relatively bright source assets leave room for later lighting and darkening.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/background_2.png" alt="Normal information corresponding to the background color layer" loading="lazy" />
  <figcaption>The corresponding normal result. Its colors represent directions rather than surface colors.</figcaption>
</figure>

Flipping UVs can mirror a color texture, but a normal texture also encodes direction. Its direction components need corresponding changes to preserve the lighting. The normal image shows such changes, which are worth inspecting further.

Blue regions can help identify the normal direction. To determine the coordinate convention, I would need to check the encoding, decoding, transforms and lighting together.

### How the background combines light and fog

<figure>
  <img src="/media/animal-well/background_3.png" alt="Background composition after color, lighting, and masks are combined" loading="lazy" />
  <figcaption>Background composition near EID 295.</figcaption>
</figure>

The background composition around EID 295 uses background color, local lighting and the R channel of a `visibility texture`. I summarize their relationship as follows:

```text
surface color = lerp(material color, fog color, fog factor)
lighting      = local lighting + ambient term + foreground-light contribution
composed color ≈ surface color × lighting
visibility masks retain or suppress selected regions
```

This is a sketch of the composition. Exact weights, color-space conversions and branches still need checking.

<figure>
  <img src="/media/animal-well/foreground_1.png" alt="Foreground-light and noise result used during composition" loading="lazy" />
  <figcaption>A lighting intermediate used to examine background illumination.</figcaption>
</figure>

The image varies in brightness from top to bottom. I suspect two noise layers contribute to this, together with a `v - 0.05` mask-sampling offset. At a height of 180 pixels, a normalized offset of 0.05 is about 9 pixels. The actual direction and scale depend on the sampling coordinates.

### A lighting atlas: draw separately, combine later

<figure>
  <img src="/media/animal-well/background_4.png" alt="Lighting atlas divided into multiple cells" loading="lazy" />
  <figcaption>A retained lighting intermediate. Contributions from different lights occupy different regions.</figcaption>
</figure>

The lighting texture in this capture is 1280×720, which divides into a 4×4 grid of 320×180 regions. This suggests individual light results may be drawn into an atlas before composition. Whether every cell is active needs checking in the relevant events.

## Midground: visibility is another kind of data

<figure>
  <img src="/media/animal-well/midground_1.png" alt="Midground image containing characters and interactive regions" loading="lazy" />
  <figcaption>The midground includes the character and gameplay-related objects, making it central to scene readability.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_2.png" alt="Visibility texture packing several masks into RGBA channels" loading="lazy" />
  <figcaption>Displaying the combined RGBA texture can obscure the independent purpose of each channel.</figcaption>
</figure>

Inspecting channels separately makes their spatial relationship to the scene easier to compare:

| Channel | My interpretation | What needs checking |
| --- | --- | --- |
| R | Visibility and a mask with transition regions | The transitions are visible; the exact diffusion or filtering algorithm has not been reproduced |
| G | A mask associated with midground regions | Inferred from spatial correspondence in this scene |
| B | A mask associated with foreground occlusion | Used in the rim-lighting reading model below |
| A | Regions associated with moving elements such as grass, lamps, and the character | A single frame cannot establish the full classification rule |

<figure>
  <img src="/media/animal-well/midground_3.png" alt="R-channel observation from the visibility texture" loading="lazy" />
  <figcaption>The R-channel observation led to a hypothesis involving diffusion and grid-based filtering.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_4.png" alt="G-channel observation from the visibility texture" loading="lazy" />
  <figcaption>G-channel observation.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_5.png" alt="B-channel observation from the visibility texture" loading="lazy" />
  <figcaption>B-channel observation.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_6.png" alt="A-channel observation from the visibility texture" loading="lazy" />
  <figcaption>A-channel observation.</figcaption>
</figure>

I suspect the R channel starts from platform occlusion and forms a transition through repeated diffusion, possibly in 4×4 units. Confirming the algorithm requires event-by-event comparison or a small reproduction.

## Transparent effects and rim lighting

<figure>
  <img src="/media/animal-well/foreground_2.png" alt="Intermediate image associated with transparent effects" loading="lazy" />
  <figcaption>An intermediate associated with effects such as the waterfall.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/foreground_3.png" alt="Another stage of transparent-effect composition" loading="lazy" />
  <figcaption>The result after transparent effects are composited.</figcaption>
</figure>

Transparent effects such as waterfalls receive separate processing. Objects at the same spatial depth can still use different rendering passes.

A mask can also control rim lighting: classify the interior, find edge regions and adjust illumination. The following code sketches that relationship:

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

The thresholds illustrate the decision process. Their values need checking during a reproduction.

<figure>
  <img src="/media/animal-well/midground_7.png" alt="Mask observation used to understand edge classification" loading="lazy" />
  <figcaption>The mask supplies boundaries whose nearby changes can be used in later stages.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_8.png" alt="Midground edges and lighting" loading="lazy" />
  <figcaption>Edges and illumination work together to improve separation between regions.</figcaption>
</figure>

Darkening, blur and bloom appear around EID 712–810. The sampling kernels and composition weights need further inspection.

## Further work

Separating the image makes it possible to follow color, normals, region masks and lighting individually. Composition uses them together to establish depth and readable objects.

For a reproduction, I would begin with separate color and mask outputs, use one mask to control both visibility and edge illumination, then add a lighting atlas and transparent effects. At every step, I would preserve intermediates and compare enabled and disabled results in a fixed scene.

For a reproduction, I would check mirrored normals, channel usage, diffusion and atlas sampling before comparing the image and performance.