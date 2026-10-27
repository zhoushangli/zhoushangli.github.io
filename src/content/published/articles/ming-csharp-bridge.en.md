---
contentId: ming-csharp-bridge
lang: en
section: articles
title: "Ming: bridging C++ objects and C# scripts"
description: "Following .NET hosting, reflected bindings, object handles, and assembly-reload recovery in Ming's current scripting implementation."
category: engine
tags: [C++, C#, Scripting, Object lifetime]
relatedProject: ming-engine
draft: true
---

## Object relationships come before cross-language calls

Exposing a C++ method to C# addresses only part of a scripting system. The engine also needs to associate script resources with managed types, native objects with managed instances, and surviving owners with reconstructed instances after an assembly replacement. Ming's current source uses a C#/.NET bridge; earlier descriptions of AngelScript no longer describe its present implementation.

Three identities matter here: `CSharpScript` represents the script resource, `CSharpInstance` connects a script to a particular native owner, and a handle provides access to its managed instance. Collapsing these into a single “script pointer” makes resource sharing, multiple instances, and post-reload relationships difficult to explain.

## Calls travel in both directions

`ScriptSystem::Startup()` initializes the .NET runtime and managed bridge. `InitializeDotNetRuntime()` obtains runtime entry points through `hostfxr` and loads the managed initialization function. Native callbacks are passed to managed code, while native code retains entry points for managed operations.

```text
Generated C# API → NativeFuncs.MethodBindPtrCall → C++ method binding
C++ notification → CSharpInstance → ScriptSystem → Managed script method
```

`CSharpScriptGenerator` reads engine reflection metadata to produce class bindings, construction interfaces, and call wrappers. Reflection registration therefore acts as a shared source for native and script-facing interfaces. Generation must still handle argument layout, return values, and built-in type conversion; it is more than writing method names into strings.

In the other direction, `CSharpInstance::Call()` and its notification entry point forward work to `ScriptSystem`. Scene nodes do not have to take responsibility for loading managed assemblies themselves.

## Resolving a script resource to a managed type

On the managed side, `ScriptManagerBridge` maps script paths to `Type` objects and associates native script resource pointers with those types. `AddScriptBridge()` converts the incoming path to a managed string, resolves a registered type, and creates the association. It rejects conditions such as null pointers and types that cannot serve as instantiable scripts.

Native object wrappers and user script instances also have different roles. `GetOrCreateNativeManagedWrapper()` reuses an owner's existing native-binding handle when possible, while user instances use a separate creation and recovery path. `ManagedGCHandle` is movable but non-copyable and releases its handle, avoiding accidental duplication of ownership. Managed code distinguishes user-script handles from native-binding handles and tracks references by assembly load context.

## Reloading includes a failure state

`ReloadProjectAssembly()` suspends script execution, gathers instance recovery information, detaches old instances, unloads the assembly, loads the replacement, and restores instances. Only a complete success clears recovery data and resumes execution. A failed attempt retains recovery information and suspension for a later retry. `PackedScene::Pack()` also checks whether script execution is suspended, preventing a scene save during an incomplete recovery.

Loading a DLL again and completing a safe scripting reload are therefore different capabilities. The current code explicitly manages reconstruction and failed retries, but a method name cannot establish that every arbitrary C# field survives. Field persistence, cross-object references, owners destroyed during reload, and actual assembly unloadability need their own checks.

## A useful verification sequence

A native node with a small C# script provides a starting point: invoke a generated API, dispatch a script notification, then exercise a successful reload, a failed load, and a retry. Observe handle counts, old-object validity, and scene-saving behavior as well. This write-up checks the source chain; it does not introduce new compilation or runtime results, and a working development-machine assembly path is not evidence of an independently distributable application.

Source entry points: `Code/MingEngine/Engine/Script/ScriptSystem.cpp`, `CSharpScript.cpp`, `CSharpScriptGenerator.cpp`, and `Code/CSharp/MingSharp/Core/ScriptManagerBridge.cs`. Return to the [Ming project](/projects/ming-engine/).
