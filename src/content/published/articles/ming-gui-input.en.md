---
contentId: ming-gui-input
lang: en
section: articles
title: "Ming: following an input event to a button"
description: "Starting with pressing, dragging away and releasing, I explain input routing, capture and focus, button activation, and object lifetime across pressed signals and Callable."
category: engine
tags: [C++, GUI, Input events, Editor]
relatedProject: ming-engine
draft: false
---

## Press on one button, drag away, then release

Suppose I press the left mouse button over button A, drag onto button B and release. A needs to end its press, while B should not activate just because it receives a release. If I drag away and return to A before releasing, A should normally complete the click. Looking up the control under the cursor only at release cannot distinguish these interactions.

In Ming, I separate this into three responsibilities: the input system preserves event order, `Viewport` selects recipients, and `BaseButton` decides whether a press attempt becomes an activation. Business notifications happen after state is committed.

```text
Platform input → InputSystem event queue
    ↓ Window::OnInputEvent in the runtime window
Viewport::ProcessInputEvent
    ↓ commit layout / check window focus
ProcessGuiInputEvent
    ↓ hover, capture, focus
PropagateGuiInput → BaseButton::GuiInput
    ↓ CompletePress: commit state first
pressed callback → recheck button → EmitSignal("pressed")
    ↓ synchronous connection snapshot
Callable → Object::Call → native binding / script method
```

This is the normal runtime-window path. In the editor, `EditorUI::HandleInput()` handles shortcuts and related logic, then sends input into the root viewport’s `ProcessInputEvent()`, reusing the same control dispatch.

## What do hover, capture and focus remember?

Hover identifies the control currently under the cursor. Capture identifies the owner of the current mouse interaction. Focus identifies the keyboard recipient. In the example, hover can move from A to B while capture remains A until the matching release or cancellation.

`Viewport::ProcessInputEvent()` checks tree membership and window focus, then flushes pending container layout so positional conversion and hit testing use committed geometry. Ordinary control recipients are stored as `ObjectID` values and resolved during dispatch, preventing a destroyed control from remaining a usable recipient.

Current capture tracks one mouse button and its target. Other buttons do not establish a second simultaneous capture. One explicit case forwards a right-button press to the target during left-button capture, allowing controls to handle cancellation or similar behavior. A left-button press can also assign focus to an eligible control.

Ordinary keyboard and text events go to the focused control, while Tab moves through eligible controls. Popups and drag-and-drop have their own priority branches. Input routing therefore involves more than a single mouse hit test.

## Coordinate conversion and bubbling belong to dispatch

Buttons use local coordinates to test whether the cursor is inside. `PropagateGuiInput()` copies the event, subtracts the control’s global position and calls `GuiInput()`. The handling result and `MouseFilter` determine whether pointer events continue to a parent control.

Keyboard and text events do not follow the same parent bubbling path. Mouse-wheel events can also continue upward through a Stop filter, giving a parent scroll container a chance to respond. Layout parentage, the hit control and the eventual handler are separate concepts.

## BaseButton manages one activation attempt

`BaseButton::GuiInput()` accepts the left mouse button and, when focused, Enter, keypad Enter or Space. It ignores key repeats. A press starts an attempt and records whether it came from the mouse or keyboard. Mouse movement updates whether the pointer is still inside. A matching release calls `CompletePress()`.

`CompletePress()` clears the attempt state, updates toggle state and requests redraw before issuing notifications. Callbacks therefore observe committed button state. Disabling, loss of focus, leaving the scene tree and input cancellation end an incomplete interaction so the button does not remain visually pressed.

Notification order has concrete boundaries. An applicable toggled callback runs first, followed by the pressed callback. Only after resolving the button again and checking deletion, disabled state, visibility and tree membership does it emit the `pressed` signal. It then resolves the object once more before the button-up callback. If an earlier callback deletes the button, later steps cannot keep using its old pointer.

## Connecting pressed to a Callable

To have a button notify a method on another object, I can use the current object-system connection interface:

```cpp
Signal pressed(button, "pressed");
Callable onPressed(receiver, "OnPressed");
bool const connected = pressed.Connect(onPressed);
```

This API example assumes that both objects exist and that method lookup can find `OnPressed`; the caller should check the connection result. Native methods need reflection bindings. User C# methods are limited to signatures supported by the current generated dispatch.

`Signal` stores the emitting object’s ID and signal name, while the emitter owns connection data. `Callable` stores the target’s `ObjectID` and method name without retaining the target. Each invocation resolves the target again and calls `Object::Call()`, which selects script or native method dispatch.

A connection also creates a reverse subscription record on the receiver. Whether emitter or receiver is destroyed first, `ClearSignalConnections()` can remove records from the other endpoint before the object leaves `ObjectDatabase`. Resolving IDs checks whether an object is alive; reverse records clean up relationships. These solve different problems.

## What if a callback changes the connection table?

Signal emission copies connections and arguments, then synchronously iterates the snapshot. Newly connected listeners participate in later emissions. Disconnecting changes the live table but does not remove an entry from the current snapshot. If that entry’s target is still alive and callable, it can still be invoked during this emission. This is the current snapshot behavior.

Before each call, emission resolves the target and skips destroyed or pre-deleting objects. After each call, it checks the emitter again. If the emitter has been destroyed or entered pre-deletion, subsequent notifications stop. These rules address object destruction and reentrancy; they do not establish thread-safe connection mutation. This path also does not provide deferred delivery or one-shot connection options.

## Current limits and useful checks

I checked the input and signal paths in the current source without rerunning the engine window for this documentation update. Representative interactions include pressing and releasing inside, releasing outside, dragging out and back, keyboard activation, disabling during a press and losing window focus. Connection checks should also cover callbacks deleting a receiver or the button, plus connection and disconnection during emission.

Function-level checks cover only part of the state logic. Coordinate conversion, window events and visual press feedback still need real window interaction. Existing text-event routing also does not establish complete input-method support or every text-editing behavior.

Source entry points, relative to the Ming repository:

- `Code/MingEngine/Engine/Input/InputSystem.cpp`
- `Code/MingEngine/Scene/Core/Window.cpp` and `Viewport.cpp`
- `Code/MingEngine/Scene/GUI/BaseButton.cpp`
- `Code/MingEngine/Core/Object/Object.cpp`, `Callable.cpp` and `Signal.cpp`
- `Code/MingEngine/Editor/UI/EditorUI.cpp`

Return to the [Ming project page](/projects/ming-engine/).
