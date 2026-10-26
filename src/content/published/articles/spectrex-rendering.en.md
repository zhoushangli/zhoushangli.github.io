---
contentId: spectrex-rendering
lang: en
section: articles
title: "SpectreX: layered capture, lighting, and compositing"
description: "Following RenderService and RenderPipeline from layered viewports and data masks to beams, emission, and the final image."
category: graphics
tags: [Godot, C#, Shader, Rendering pipeline]
relatedProject: spectrex
draft: false
---

## A final screenshot does not explain the whole image

SpectreX's pixel scenes combine interactive midground objects, decorative backgrounds, foreground occlusion, and light beams that communicate core gameplay. These layers need different lighting, transparency, and visibility rules. The project separates capture, material data, layer processing, and final composition so intermediate results have identifiable responsibilities.

This article describes the team project's current implementation. My work spans technical art, programming, and design. It does not claim personal authorship of all visual assets or art decisions, and the existence of source code is not a final image-quality or performance acceptance result.

## A service manages entry points; a pipeline manages dependencies

`RenderService` instantiates `RenderPipeline` from its configured `PipelineScene`, applies a default background configuration, and supplies the active scene viewport and visibility texture. `UsePipeline` switches between the pipeline output and direct scene rendering, providing a way to compare source imagery with processed results.

`RenderPipeline` holds exported references to capture viewports, materials, and processing stages. Capture viewports share the source scene's `World2D` and follow its camera transform; processing, blur, and compositing stages remain in screen space. When the source viewport changes, the pipeline restores the old cull mask, then hides the new source's raw scene layers and shows the final output. This prevents the scene from appearing twice.

```text
Farground / Background / Midground / Foreground / Beam and data capture
                      ↓ Layer processing, transparency, masks
Composite A: farground + background + beams
Composite B: A + transparent midground + ordinary midground
Composite C: B + foreground
                      ↓ Emission → Visibility/color filter → Color adjustment → Final post-process
                                  Final output
```

This overview omits individual blur and material branches. Prefab bindings and shader texture inputs define the actual dependencies.

## Data textures and color textures serve different purposes

`SceneMask.gdshader` writes foreground, midground, and background coverage into RGB, and visibility into A. Transparent midground also contributes to the combined midground coverage. This channel convention belongs to SpectreX's current implementation and should not be transferred uncritically to a frame capture from another game.

Normals, background lighting, emission, and transparent material data are captured through dedicated visibility layers. `RenderService` excludes auxiliary layers from the main viewport. Treating these textures as data rather than ordinary artwork helps determine whether an unexpected color originates in capture or compositing.

The background final pass combines ambient illumination, local glow, background light, and negative light, multiplies the background color, and retains coverage. Glow uses quantized brightness levels and Bayer thresholds for dithered transitions. A blurred signal can therefore still be constrained by the pixel presentation instead of being applied unchanged to the base image.

## Beams and transparent surfaces use different composition rules

`CompositeA.gdshader` first combines farground and background, decodes the base into linear color, and mixes in the original beam and blurred glow. A peak-based compression limits brightness while retaining channel proportions, after which the shader encodes the result again. Whether the result communicates the desired light colors still requires visual comparison.

Ordinary and transparent layers use premultiplied-alpha composition, summarized by:

```text
result = source + destination × (1 − source.alpha)
```

`CompositeB` applies transparent midground before ordinary midground to retain solid detail. Final scene composition adds the foreground. `EmissivePass` subsequently adds original emission and blurred glow. These dependencies decide which content occludes which effect; changing the order changes the image.

## Inspect intermediate results before judging the final image

Useful checks start with layer colors, coverage, normals, and beams, then move to transparent edges, camera movement, room changes, and leaving the main menu. When the pipeline loses its source viewport, it hides output and disables relevant viewport updates. Switching and teardown are consequently part of rendering acceptance too.

A multi-viewport design makes dependencies explicit and easier to inspect, while introducing capture, texture, and composition costs. The source establishes structure, but measuring actual cost requires representative scenes, resolution, and target hardware. This article reports static inspection only, with no new GPU capture or performance measurement.

Source entry points: `Scripts/Core/RenderService.cs`, `RenderPipeline.cs`, and `Shaders/RenderPipeline/SceneMask.gdshader`, `CompositeA.gdshader`, `CompositeB.gdshader`, `SceneComposite.gdshader`. Return to the [SpectreX project](/projects/spectrex/).
