---
contentId: pico8-a01
lang: en
section: teaching
title: "PICO-8 A01: Breakout Exercise 1"
description: "Follow tutorial parts 1–5 to implement ball movement, boundary collisions and sound."
category: teaching
tags: ["PICO-8", "Teaching practice"]
draft: true
---

## Purpose

A01 is supporting practice for the course. It applies variables, updating and drawing to a small Breakout prototype. The original instruction is to follow parts 1–5 of the reference tutorial and implement a ball, screen-edge collisions and collision sound.

Reference tutorials by external authors:

- [YouTube reference playlist](https://youtube.com/playlist?list=PLea8cjCua_P0qjjiG8G5FBgqwpqMU7rBk)
- [Bilibili: making Breakout with PICO-8](https://www.bilibili.com/video/BV17rAieaEmB/)

## Core task

Make a ball move continuously, add responses to screen boundaries, then play sound when a collision occurs. Retain a working version after each addition.

Explain position and velocity, what a collision changes and when sound should play. A full level, score or win/loss sequence is not required.

## Suggested checks

Observe successive contacts with the horizontal and vertical edges. Approach a corner and inspect the response along both axes. If sound repeats continuously, distinguish being at a boundary from a collision occurring in the current update.

For an error, record the expected result, actual behavior and steps to reproduce it.

## Submission

Submit `A01_Name.zip` containing:

- `A01_Name.p8.png`: the cartridge.
- `A01_Name.mp4`: a demonstration under one minute explaining the main logic.

Run the example, then identify a variable or function involved in a collision. Unresolved problems can be reported by describing expected and actual behavior, making Q&A more useful.

## Further practice

Breakout is a small transfer task: recalling coordinates from the classroom example is insufficient. Learners must apply the relationship between state and feedback to another object. Continue with [A02](/teaching/pico8-a02/) or return to the [series overview](/teaching/pico8-2026/).

