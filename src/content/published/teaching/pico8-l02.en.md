---
contentId: pico8-l02
lang: en
section: teaching
title: "PICO-8 L02: Debugging, Movement and Animation"
description: "Investigate jumping problems, organize movement functions and select animations from state."
category: teaching
tags: ["PICO-8", "Teaching practice"]
draft: false
---

## Begin with a program that already moves

The retained L02 plan covers code cleanup, movement debugging, movement functions, animation and object refactoring. Rather than starting a new game, the lesson addresses a program that has grown enough to become difficult to change.

This lesson uses position and velocity to investigate faults, then groups related object data. The refactoring method has a separate [object-management case](/teaching/pico8-object-organization/).

## Describe the fault before changing a formula

The notes record unusual jumping behavior and propose printing vertical velocity and pausing/resuming execution. The edited sequence asks whether the fault occurs on takeoff, ascent, descent or landing, whether displacement matches velocity, and whether movement is applied more than once in an update.

Track position, vertical velocity and the grounded condition within one update before choosing a fix. Movement formulas need to be read alongside the complete collision and displacement logic.

## Separate movement from presentation

Cleanup first groups input handling, then places displacement in functions with clear responsibilities. The point is to locate “read the controls,” “choose velocity” and “attempt movement,” rather than immediately teach an entire framework.

Animation reads movement and grounding state to choose a presentation. Check idle, movement, facing and jumping separately. Wrong facing calls for inspecting sprite selection and flipping; moving through a platform calls for revisiting displacement and collision.

## Make a second object the reason for a table

What happens if adding a balloon means adding another group of global variables? This question gives tables a practical purpose. Complex inheritance is unnecessary: compare scattered variables with grouped object data, then identify shared behavior and state that each object must own.

Dashing is optional in the plan and can be cut or deferred when time is short.

## Practice and reflection

Keep a working version and change one responsibility at a time. After extracting movement into a function, compare the old behavior before adding an ability. Learners should be able to name the caller, inputs and state being changed.

Inertia-based movement is an extension exercise in the plan. Each change should be explainable and easy to check.

