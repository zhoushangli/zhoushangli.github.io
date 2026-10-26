---
contentId: ming-gui-input
lang: en
section: articles
title: "Ming: following an input event to a button"
description: "Tracing the input queue, Viewport routing, mouse capture, and button activation state in Ming's native GUI."
category: engine
tags: [C++, GUI, Input events, Editor]
relatedProject: ming-engine
draft: false
---

## Why cannot press and release choose recipients independently?

A minimal button might test whether the cursor lies inside its rectangle when the mouse is released. Dragging away after a press, or losing window focus while holding a button, requires a longer-lived interaction state. Ming separates this across the input queue, recipient management in `Viewport`, and activation state in `BaseButton`.

```text
Platform input → InputSystem event queue → Window::OnInputEvent
 → Viewport::ProcessInputEvent → ProcessGuiInputEvent
 → PropagateGuiInput → Control / BaseButton::GuiInput
 → CompletePress → Application callback
```

A callback in this chain is a registered invocation mechanism; superficial similarity does not make it equivalent to another engine's signal system.

## Viewport decides who receives the event

`ProcessInputEvent()` checks tree membership and window focus. Before routing positional input it calls `FlushContainerUpdate()`, so hit testing uses committed layout. `ProcessGuiInputEvent()` then distinguishes hover, the control currently under the cursor; capture, the recipient of an ongoing mouse interaction; and focus, the target of keyboard input.

Hover can change during mouse movement, while capture persists until the matching release. The current implementation captures one mouse button at a time and consumes other button events during that capture. Moving the cursor therefore does not send a release to a different control. A left press may also focus an eligible control. Key and text events go to the focused control, while Tab traverses the focusable controls.

These states store `ObjectID` values. Resolving identifiers before dispatch helps deal with nodes that leave the tree or disappear during interaction. It does not remove the need to avoid using stale pointers after a callback.

## Propagation has its own responsibility

`PropagateGuiInput()` transforms pointer positions into control-local coordinates before calling `GuiInput()`. Its handling result and `MouseFilter` determine whether a pointer event continues up the parent-control chain. Key and text input do not follow the same bubbling path.

Hitting a control and completing an application action are therefore separate steps. A container may appear in the parent chain without automatically replacing the child as the clicked recipient. This distinction keeps layout organization separate from interaction semantics.

## BaseButton tracks an activation attempt

`BaseButton::GuiInput()` starts an attempt for eligible left-button input or focused activation keys such as Enter and Space, while ignoring repeated key events. Mouse movement updates whether the press remains inside. A release asks `CompletePress()` to determine whether activation should occur.

`CompletePress()` commits internal state and queues a redraw before invoking toggle, pressed, and button-up callbacks. Because a callback may alter the scene, the function resolves the button again between notifications and checks deletion, disabled, and visibility states. Focus loss, cancellation, and tree exit finish an incomplete attempt rather than leaving a stuck pressed appearance.

## Verify interactions, not only return values

Useful cases include pressing and releasing inside, releasing outside, leaving and re-entering before release, keyboard activation, disabling during a press, losing window focus, and a callback deleting its own button. Object-level checks can exercise the state machine. Real window interaction must additionally verify coordinates, native events, and visible feedback.

This article is based on source inspection and does not report a new windowed test. Focused text-event dispatch is present in the current code, but that alone does not establish a complete text editor, input-method support, or finished editor property editing.

Source entry points: `Code/MingEngine/Engine/Input/InputSystem.cpp`, `Code/MingEngine/Scene/Core/Window.cpp`, `Viewport.cpp`, and `Code/MingEngine/Scene/GUI/BaseButton.cpp`. Return to the [Ming project](/projects/ming-engine/).
