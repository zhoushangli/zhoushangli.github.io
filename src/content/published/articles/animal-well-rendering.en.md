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

These notes use saved frame-capture screenshots. I have not replayed the capture for this edit and do not have the source code. EID 295 and EID 712–810 identify events in that capture; the channel and algorithm interpretations still need verification.

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

The original notes explain this change as continuous noise applied along U, followed by darkening. That explanation is consistent with the retained before-and-after images, but two images do not establish the exact noise function, sampling frequency, or animation parameters. The design lesson is that an asset need not contain frame-by-frame animation for sampling coordinates and composition to change its spatial character.

## Background: separate color from direction

<figure>
  <img src="/media/animal-well/background_1.png" alt="Decorative elements and spatial composition in the background color layer" loading="lazy" />
  <figcaption>The background color layer. Relatively bright source assets leave room for later lighting and darkening.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/background_2.png" alt="Normal information corresponding to the background color layer" loading="lazy" />
  <figcaption>The corresponding normal result. Its colors represent directions rather than surface colors.</figcaption>
</figure>

Flipping UVs can mirror a color texture. A normal texture also encodes direction components, so mirroring its image alone does not guarantee consistent lighting. The original analysis noticed corresponding changes in the normal result and identified this as a step to inspect when studying mirrored drawing.

Blue-looking regions are a clue to a default direction, but the displayed color alone does not establish the complete coordinate convention. Normal encoding, decoding, transforms, and lighting must be checked together. I therefore do not treat “blue means out of the screen” as a verified implementation result.

### How the background combines light and fog

<figure>
  <img src="/media/animal-well/background_3.png" alt="Background composition after color, lighting, and masks are combined" loading="lazy" />
  <figcaption>The background composition recorded near EID 295 in the original capture.</figcaption>
</figure>

At EID 295, the notes associate background images, spatially restricted lighting, and the R channel of a `visibility texture` with the background composition. Their responsibilities can be summarized by this reading model:

```text
surface color = lerp(material color, fog color, fog factor)
lighting      = local lighting + ambient term + foreground-light contribution
composed color ≈ surface color × lighting
visibility masks retain or suppress selected regions
```

This is a conceptual description of the inputs, not a complete shader copied from the game's source. The original notes do not preserve every weight, color-space conversion, or branch, so the model should not be considered pixel-equivalent to the game.

<figure>
  <img src="/media/animal-well/foreground_1.png" alt="Foreground-light and noise result used during composition" loading="lazy" />
  <figcaption>The intermediate result called foreground light in the notes also helps explain the background&#x27;s environmental illumination.</figcaption>
</figure>

The result has a vertical brightness variation. The notes attribute it to two noise layers and record a `v - 0.05` mask-sampling offset. At a normalized height of 180 pixels, 0.05 corresponds to approximately 9 pixels. Its actual screen direction and whether that scale applies elsewhere still depend on the coordinate and sampling paths.

### A lighting atlas: draw separately, combine later

<figure>
  <img src="/media/animal-well/background_4.png" alt="Lighting atlas divided into multiple cells" loading="lazy" />
  <figcaption>A retained lighting intermediate. Contributions from different lights occupy different regions.</figcaption>
</figure>

The capture notes record a 1280×720 lighting texture, interpreted as a 4×4 grid of 320×180 regions. This size relationship supports the explanation that individual light results are placed in an atlas and sampled during composition. It provides a way to investigate isolation between lights. It does not establish a permanent game-wide limit of 16 lights, or prove that every cell is active in every frame.

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

| Channel | Interpretation in the original notes | Evidence limit |
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

The draft proposes that the R channel starts from platform occlusion and develops a transition through repeated diffusion. It further suggests processing in 4×4 units. These are useful hypotheses to test. Establishing the algorithm requires comparing inputs and outputs event by event, or constructing a minimal reproduction; a block-like appearance alone is insufficient.

## Transparent effects and rim lighting

<figure>
  <img src="/media/animal-well/foreground_2.png" alt="Intermediate image associated with transparent effects" loading="lazy" />
  <figcaption>An intermediate associated with effects such as the waterfall.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/foreground_3.png" alt="Another stage of transparent-effect composition" loading="lazy" />
  <figcaption>Another composition stage. The image retains its original note correspondence; its filename does not establish an engine-layer classification.</figcaption>
</figure>

In the reading model for this scene, transparent effects such as waterfalls receive separate processing rather than simply joining ordinary midground drawing. A spatial “midground” is therefore not necessarily one implementation pass.

Rim lighting provides another useful connection: a mask can control illumination as well as clipping. The original notes assembled the following illustrative code to express “classify the interior, identify an edge region, then adjust lighting”:

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

The illustrative code retains the thresholds from the original notes. They explain this analysis and are not suggested settings for other scenes.

<figure>
  <img src="/media/animal-well/midground_7.png" alt="Mask observation used to understand edge classification" loading="lazy" />
  <figcaption>The mask supplies boundaries whose nearby changes can be used in later stages.</figcaption>
</figure>

<figure>
  <img src="/media/animal-well/midground_8.png" alt="Midground edges and lighting recorded in the notes" loading="lazy" />
  <figcaption>Edges and illumination work together to improve separation between regions.</figcaption>
</figure>

The notes also record darkening, blur and bloom around EID 712–810. Sampling kernels and composition weights need a later replay.

## Further work

Separating the image makes it possible to follow color, normals, region masks and lighting individually. Composition uses them together to establish depth and readable objects.

For a reproduction, I would begin with separate color and mask outputs, use one mask to control both visibility and edge illumination, then add a lighting atlas and transparent effects. At every step, I would preserve intermediates and compare enabled and disabled results in a fixed scene.

I have not yet reproduced the image or measured performance. The next checks are mirrored normals, channel usage, diffusion and atlas sampling.