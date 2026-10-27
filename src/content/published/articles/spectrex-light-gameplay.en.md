---
contentId: spectrex-light-gameplay
lang: en
section: articles
title: "SpectreX: turning light paths into interactive rules"
description: "Following optical data from emitters, mirrors, and glass to sensors and doors, with attention to feedback and engineering tradeoffs."
category: gameplay
tags: [Godot, C#, Optical puzzles, Interaction]
relatedProject: spectrex
draft: true
---

## Light needs to be visible and determine mechanism state

Drawing a beam is only part of an optical puzzle. Players need to anticipate occlusion, reflection, and refraction; mechanisms need reliable reception results; and visual feedback needs to explain the rules. SpectreX separates optical data management, path solving, beam rendering, and mechanism feedback, then connects them through shared results.

I contributed technical art, programming, and design to this team project. This article explains how the current code organizes interaction. It does not claim sole ownership of the team's designs or assets, or present the system as a complete physical optics simulation.

```text
Scene components submit transforms, settings, and colliders
 → LightService schedules rays that need updating
 → LightSolver produces paths and hit contributions
 → LightRenderer updates beams / Sensors accumulate intensity
 → LightSensorController updates feedback and events
 → DoorController evaluates opening conditions
```

## Shared data connects different optical objects

`LightService` owns data for emitters, mirrors, converters, glass, players, sensors, and opaque objects, associating it with collision objects through `LID` handles. Components submit position and parameter changes; the service handles solving across objects. Individual mechanism controllers do not have to duplicate ray queries.

`LightSolver::Trace()` advances a path according to the hit type. Opaque objects terminate propagation; sensors record a weighted intensity and absorb the ray; mirrors check enabled state, orientation, and reflection limits before changing direction and applying loss; glass handles refraction, dispersion, and attenuation at medium boundaries. Ray length, reflection count, and a boundary-event cap bound the computation. These are configurable gameplay rules and numerical approximations, not a claim of continuous-spectrum physical accuracy.

## Actual reception and latched appearance are different states

The service accumulates each ray frequency's contribution to a sensor. White sensors receive all frequencies, while colored sensors accumulate the corresponding frequency. `LightSensorController` then evaluates actual activation with `ReceivedIntensity >= RequiredIntensity`.

There is an important distinction between `IsActivated`, which represents the current threshold result, and `IsLightUp`, which can stay latched through `KeepLightUp()`. Emission strength follows the ratio between received intensity and the threshold, providing feedback before activation. `OnLightChanged` and `OnLightUp` notify subscribers when the appropriate state changes.

`DoorController` independently accumulates a light-up confirmation time for its bound sensors. It opens when every required sensor satisfies its condition and records that result through the save system. Sensors can respond promptly while doors apply their own confirmation rule. Default values are implementation parameters, not evidence that every level has the right threshold or delay; those values still need playtesting.

## Interactive devices also need state and authoring interfaces

`SocketController` organizes movable sockets into states including Idle, Occupied, Returning, and ReturnBlocked, and can attach a mirror or converter. Prefab configuration supplies scenes, offsets, and a rotation node. Rotation synchronizes the optical transform back to the solving system. This gives moving and turning a device a concrete implementation path while leaving authoring controls available to level builders.

The implementation alone cannot establish readability. Design acceptance must also observe whether players understand device orientation, color filtering, attenuation, and the connection between a visible beam and mechanism feedback.

## Solving budgets and verification boundaries

The current `LightService::PhysicsUpdate()` tracks geometry changes, marks affected rays, and schedules dirty-ray work under a budget. Converter outputs and ordinary emitters both contribute to sensor reception. Diagnostic values track solved rays, traced frequencies, mesh updates, and timings to make costs inspectable.

Reducing unnecessary recomputation through batching must be checked together with interaction consistency. Useful cases include rotating mirrors, moving occluders, changing rooms, chaining converters, and operating near an intensity threshold. Observe the order of beam, sensor, and door updates. This article checks source behavior and does not report new frame-rate measurements or player-test results.

Source entry points: `Scripts/Core/LightService.cs`, `LightSolver.cs`, `LightRenderer.cs`, and `Scripts/LightSensorController.cs`, `DoorController.cs`, `SocketController.cs`. Return to the [SpectreX project](/projects/spectrex/).
