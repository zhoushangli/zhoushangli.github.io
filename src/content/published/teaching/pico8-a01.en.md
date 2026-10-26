---
contentId: pico8-a01
lang: en
section: teaching
title: "PICO-8 A01: Practising Movement and Collision with Breakout"
description: "The first supporting assignment: build a small ball prototype and explain movement, boundaries and sound."
category: teaching
tags: ["PICO-8", "Teaching practice"]
draft: false
---

## Purpose

A01 is supporting practice for the course. It applies variables, updating and drawing to a small Breakout prototype. The original instruction is to follow parts 1–5 of the reference tutorial and implement a ball, screen-edge collisions and collision sound.

The tutorials are external learning resources, not recordings created by me:

- [YouTube reference playlist](https://youtube.com/playlist?list=PLea8cjCua_P0qjjiG8G5FBgqwpqMU7rBk)
- [Bilibili: making Breakout with PICO-8](https://www.bilibili.com/video/BV17rAieaEmB/)

## Core task

Make a ball move continuously, add responses to screen boundaries, then play sound when a collision occurs. Retain a working version after each addition.

Be ready to explain what position and velocity store, whether collision changes one or both, and why sound should respond to a collision event. The original assignment does not require a full level, score or win/loss sequence; those should not become extra barriers for this first exercise.

## Suggested checks

Observe successive contacts with the horizontal and vertical edges. Approach a corner and inspect the response along both axes. If sound repeats continuously, distinguish being at a boundary from a collision occurring in the current update.

These are checks added in the public editorial version to support explanation, not evidence of a standardized assessment already conducted.

## Submission

Submit `A01_Name.zip` containing:

- `A01_Name.p8.png`: the cartridge.
- `A01_Name.mp4`: a demonstration under one minute explaining the main logic.

Run the example, then identify a variable or function involved in a collision. Unresolved problems can be reported by describing expected and actual behavior, making Q&A more useful.

## Why this exercise?

Breakout is a small transfer task: recalling coordinates from the classroom example is insufficient. Learners must apply the relationship between state and feedback to another object. Continue with [A02](/teaching/pico8-a02/) or return to the [series overview](/teaching/pico8-2026/).

