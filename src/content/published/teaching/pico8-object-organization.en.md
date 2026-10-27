---
contentId: pico8-object-organization
lang: en
section: teaching
title: "PICO-8 Object Management Example"
description: "Group object data in tables, create multiple instances and update them together."
category: teaching
tags: ["PICO-8", "Teaching practice"]
draft: false
---

## Introduce structure through a concrete problem

The starting question is practical: a character already moves, so where should the data for a balloon, platform or another object go? Copying groups of global variables is easy initially, but makes their relationship to functions harder to follow.

Tables, templates and instances appear in the L02 notes, while my recollection places them in L03. This case is presented separately.

## Group data before introducing more machinery

Compare separate `x`, `y` and `vx` variables with `object.x`, `object.y` and `object.vx`. The values still exist; what changes is their ownership and how they are passed around.

Then distinguish shared behavior from per-instance state. Objects may follow one update convention while retaining independent positions. A common convention does not imply a shared mutable state object.

## A minimal example

The following simplified example was written for these notes:

```lua
function make_actor(x,y)
 return {x=x,y=y,vx=0}
end

function update_actor(actor)
 actor.x=actor.x+actor.vx
end

function _init()
 actors={}
 add(actors,make_actor(24,40))
 add(actors,make_actor(80,40))
 actors[1].vx=1
end

function _update()
 foreach(actors,update_actor)
end

function _draw()
 cls(0)
 for actor in all(actors) do
  rectfill(actor.x,actor.y,
   actor.x+7,actor.y+7,7)
 end
end
```

It deliberately covers only construction, data and calling. It does not implement collision, boundary constraints or a complete object lifecycle. First observe independent state in two instances, then extend the example.

## What the class analogy explains

A blueprint-and-object analogy can help introduce templates and instances, but it must return to code. Here the constructor returns a new table on each call, and objects share the `update_actor` convention. This is not a C++ class declaration; the analogy does not imply equivalent access control or type constraints.

Ask learners to trace who creates an object, where it enters the collection and how the update function receives an instance. Understanding that path matters more than replacing variable names with dotted expressions.

## Exercise and reflection

First change only the second instance's velocity and predict the effect on the other object. Next give objects independent colors and update drawing to use them. Finally discuss what should happen to the collection when changing rooms.

These exercises adapt and extend the plan. Changing input, animation, collision and structure at once makes comparison difficult. Preserve behavior and change one organizational idea at a time. Continue with [L03: Objects and Levels](/teaching/pico8-l03/).

