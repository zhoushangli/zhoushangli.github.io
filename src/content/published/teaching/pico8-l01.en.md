---
contentId: pico8-l01
lang: en
section: teaching
title: "PICO-8 L01: Making Input Visible"
description: "Connecting variables, functions and drawing through a small movement exercise."
category: teaching
tags: ["PICO-8", "Teaching practice"]
draft: false
---

## The question for this lesson

A first coding class needs observable results quickly. The original plan starts with a rectangle, introduces variables and button input, then prepares collision and platform movement. This page retains that progression without treating every planned topic as confirmed classroom coverage.

The goal is to identify where input is read, where position is stored and where the picture uses that position. Explaining those relationships makes a small example useful for later debugging and extension.

## From a rectangle to interaction

Begin with a stationary rectangle. Change its coordinates and color, then replace its horizontal position with a variable. Finally update that variable in response to input. This minimal example is edited for the teaching case, not a verbatim classroom listing:

```lua
function _init()
 x=60
end

function _update()
 if btn(0) then
  x=x-1
 end
 if btn(1) then
  x=x+1
 end
end

function _draw()
 cls(0)
 rectfill(x,60,x+7,67,7)
end
```

Ask learners to predict the result before running a change. After demonstrating horizontal movement, pause so they can add vertical movement themselves. Gravity, collisions and animation need not enter the same exercise.

## Separate update from drawing

The preparation notes use a simplified comparison between `_update` and `_draw`. In a public lesson, their responsibilities should be explicit: update handles input and state, while drawing reads that state to produce the image. Both are callbacks, but teaching them as identical would be misleading.

This separation helps explain why a changed position might not appear on screen and discourages duplicated gameplay logic in drawing. Refer to the [official manual](https://www.lexaloffle.com/dl/docs/pico-8_manual.html) for callback behavior.

## Exercise and checks

Add vertical movement, then explain why the rectangle remains visible after clearing the screen, how reassigning position every frame affects movement, and what the current code does when left and right are held together.

An extension is to keep the rectangle inside the screen and record the first boundary error. Assessment should ask learners to explain state changes rather than merely match the example.

## Towards collision and jumping

Later preparation covers map data, `mget`, `fget`, object bounds, velocity, gravity and grounded checks. These are better separated: test one blocking location, expand to the object's bounds, then introduce vertical velocity. A platform visible on screen does not itself imply correct collision behavior.

Pause between these goals to check progress. Unfinished material can become supported practice instead of introducing several new concepts at once. [L02](/teaching/pico8-l02/) continues with debugging and organizing a growing program.

