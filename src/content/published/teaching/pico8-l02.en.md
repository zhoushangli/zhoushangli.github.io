---
contentId: pico8-l02
lang: en
section: teaching
title: "PICO-8 L02: From Debugging Movement to Organizing Objects"
description: "A lesson-plan reconstruction connecting movement debugging, animation and Lua tables."
category: teaching
tags: ["PICO-8", "Teaching practice"]
draft: false
---

## Begin with a program that already moves

The retained L02 plan covers code cleanup, movement debugging, movement functions, animation and object refactoring. Rather than starting a new game, the lesson addresses a program that has grown enough to become difficult to change.

The intended goals are to narrow a bug through observable state and explain why grouping related data helps when adding objects. The written plan and my recollection number the refactoring differently; this page follows the plan, with the method presented separately as a [teaching case](/teaching/pico8-object-organization/).

## Describe the fault before changing a formula

The notes record unusual jumping behavior and propose printing vertical velocity and pausing/resuming execution. The edited sequence asks whether the fault occurs on takeoff, ascent, descent or landing, whether displacement matches velocity, and whether movement is applied more than once in an update.

Track only the relevant position, vertical velocity and grounded condition. Inspect how they change within an update before choosing a fix. A local correction written in preparation notes should not be presented as a general formula without the complete algorithm.

## Separate movement from presentation

Cleanup first groups input handling, then places displacement in functions with clear responsibilities. The point is to locate “read the controls,” “choose velocity” and “attempt movement,” rather than immediately teach an entire framework.

Animation reads movement and grounding state to choose a presentation. Check idle, movement, facing and jumping separately. Wrong facing calls for inspecting sprite selection and flipping; moving through a platform calls for revisiting displacement and collision.

## Make a second object the reason for a table

What happens if adding a balloon means adding another group of global variables? This question gives tables a practical purpose. Complex inheritance is unnecessary: compare scattered variables with grouped object data, then identify shared behavior and state that each object must own.

The notes also prepare dashing, alongside reminders to cut it or defer it if time runs short. This is evidence of scope adjustment, not proof that a complete dash system was delivered in the lesson.

## Practice and reflection

Keep a working version and change one responsibility at a time. After extracting movement into a function, compare the old behavior before adding an ability. Learners should be able to name the caller, inputs and state being changed.

The plan proposes inertia-based movement for exercise support. Such preparation items are practice directions, not verified completed teaching outcomes. The useful progression is towards a repeatable, explainable way of investigating faults.

