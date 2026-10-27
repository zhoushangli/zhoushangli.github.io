---
contentId: pico8-l03
lang: en
section: teaching
title: "PICO-8 L03: Objects and Levels"
description: "Update game objects together and create level content from map markers."
category: teaching
tags: ["PICO-8", "Teaching practice"]
draft: false
---

## Lesson content

The original L03 plan concentrates on structure: adding objects to a collection, updating and drawing them consistently, and creating runtime objects from map data. Time also needs to remain for other contributors, so the final class should not become a rush to add every unfinished feature.

This page follows the L03 plan for object collections and map loading. The [teaching case](/teaching/pico8-object-organization/) explains the object structure in more detail.

## Give objects a shared entry point

A single character can be called directly. Adding balloons, platforms and other objects through special-case calls makes the main loop grow. A collection lets created instances enter a common update path.

Draw the sequence before writing the loop:

```text
create room
  → construct object instances
  → add them to a collection
  → call object behavior during updates
  → read object state during drawing
  → clear or rebuild the collection on room changes
```

The learning goal is to identify who calls the behavior, not to give all objects identical abilities. A stationary object can still draw, and special interactions should not force every rule back into the main loop. See the [object organization case](/teaching/pico8-object-organization/).

## Map data and runtime objects

The room-loading example distinguishes editable configuration from current game state. Map markers make level layout convenient to edit; runtime objects store state and execute behavior. The program needs a mapping between the two.

A small exercise is to draw a room, choose a marker for a spawn point, and explain what should be created when the scan encounters it. Check for objects left over after reloading, correct spawn coordinates and behavior when no marker is present.

## Leave room for making

The follow-on plan includes reports, the jam, online prototype discussions, peer playtesting and a showcase. Reports start with a runnable version and explain the next steps.

The closing class should help learners choose a manageable next step: retain one core interaction, remove features they cannot yet explain or finish, and prepare for someone else to play. A short report can describe one design tradeoff and one unresolved problem.

## Recording and follow-on work

[Pico8 Training L03 recording](https://meeting.tencent.com/crm/NARXvk9acd), dated October 7, 2026, in Chinese.

See the later [game jam submissions](/teaching/pico8-game-jam/).

