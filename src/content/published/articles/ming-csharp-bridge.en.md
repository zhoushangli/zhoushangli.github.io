---
contentId: ming-csharp-bridge
lang: en
section: articles
title: "Ming: connecting C++ objects and C# scripts"
description: "Following a node with an attached C# script through two kinds of code generation, native and managed identities, and instance recreation with retry after assembly reload failure."
category: engine
tags: [C++, C#, Scripting, Object lifetime]
relatedProject: ming-engine
draft: false
---

## Why does one node need several script objects?

Suppose I attach a C# controller to a native `Node3D` and use it to change the node’s position during updates. Exposing engine functions to C# is only part of the problem. I also need to identify the managed type associated with the file, connect an instance to the correct native node, and rebuild that connection after recompiling the assembly.

In Ming, I separate these identities. The native node is the owner, `CSharpScript` is a shareable script resource, and `CSharpInstance` connects one owner to that resource. A GC handle gives the native side access to the corresponding managed instance. Two nodes using the same script resource still require separate instances.

```text
Engine reflection metadata
    ↓ CSharpScriptGenerator (native tool)
Engine C# API → MethodBindPtrCall → native MethodBind

User C# source
    ↓ ScriptPathGenerator (Roslyn, during compilation)
Script path attribute + method dispatch → project assembly
    ↓ hostfxr-hosted .NET / managed bridge
CSharpScript path → managed Type
    ↓ Instantiate(owner)
Native owner ↔ CSharpInstance / GC handle ↔ managed instance
```

## hostfxr connects the runtime; generated code connects the API

`ScriptSystem::Startup()` initializes the scripting system. `InitializeDotNetRuntime()` uses `hostfxr` to obtain the .NET loading entry point. The system loads managed entry points, exchanges callback tables and loads the project assembly through the bridge. Scene nodes do not need to locate DLLs or manage runtime entry points themselves.

There are two kinds of generator with different responsibilities. The native `CSharpScriptGenerator` reads type, method and property metadata from `ClassDatabase`. It generates C# engine API wrappers, constructor entry points and call adapters. Calls from C# reach native `MethodBind` through `NativeFuncs.MethodBindPtrCall`, with explicit handling of argument layouts, object pointers and return conversions.

The Roslyn `ScriptPathGenerator` runs when the user project compiles. It validates script declarations and generates `ScriptPathAttribute`, mapping files inside the project to `res://` paths. It also generates user method lookup and dispatch. Scripts currently require a non-generic top-level class, `partial` on every declaration, and a filename matching the class name. User method dispatch currently selects ordinary instance methods with no parameters and a `void` return. This does not imply support for arbitrary C# signatures.

## How does a script path become an instance on an owner?

The managed side registers a `Type` by script path. `CSharpScript::Instantiate(owner)` first uses `AddScriptBridge()` to associate the native resource with that type. It then creates a `CSharpInstance`, attaches it to the owner and requests a user instance from the managed bridge.

`ScriptManagerBridge.CreateUserManagedInstance()` checks compatibility between the script type and the owner’s native type, establishes `NativePtr`, executes construction and returns a handle. The native side installs that handle on the owner’s script instance. Failed creation or handle installation cleans up the attempted instantiation. This describes a real script instance; editor placeholder instances follow a separate path.

Native API wrappers and user script instances also have different roles. `GetOrCreateNativeManagedWrapper()` attempts to reuse the owner’s native binding handle. A user script instance has its own script handle. `ManagedGCHandle` disallows copying, supports moving and informs the managed side when released. A handle value therefore cannot accidentally be copied in C++ and treated as two independent owners.

## How do native notifications and named calls reach C#?

Position changes in the script travel through the generated API to C++. In the other direction, `CSharpInstance::Notification()` forwards native notifications to managed `_Notification`, which leads into script lifecycle methods. Named calls pass through `CSharpInstance::Call()`, `ScriptSystem` and the managed bridge to generated dispatch code.

`Object::Call()` defines an important fallback rule: it tries the script first and looks up a native binding only if the result is `InvalidMethod`. Argument errors and execution failures remain errors. They are not mistaken for a missing script method and followed by a call to a native method with the same name. Callers such as Callable can therefore receive a meaningful failure reason.

## Reload must rebuild connections and retain a path to retry

After recompiling a DLL, an old managed instance cannot be treated as an object from the new assembly. In `ReloadProjectAssembly()`, I suspend script execution, record instance associations, detach old instances, unload the old assembly, load the new one and recreate instances.

The backup structure makes the current capability precise:

```cpp
struct StateBackup
{
    ObjectID          m_owner;
    Ref<CSharpScript> m_script;
};
```

This structure in `ScriptSystem.hpp` records which owner should receive which script, and keeps the script resource alive through a reference. It does not record arbitrary C# field values. The current flow recreates instances; it cannot promise complete preservation of controller timers, collections or object references.

If unloading, loading or restoration fails while recovery records remain, the system retains the original records and suspended state. A retry first detaches any partially restored instances, then loads and restores again. Owners destroyed during recovery are skipped. Success clears the records and resumes execution. A failure with no pending recovery records releases suspension, so it would be inaccurate to describe every failure as leaving execution indefinitely paused.

`PackedScene::Pack()` also rejects packing while script execution is suspended. This prevents an incompletely restored scene from being saved as normal state and establishes a concrete constraint between assembly reload and scene persistence.

## Current limits and useful checks

I checked the generation, call, handle and reload paths in the current source without recompiling or running the engine for this documentation update. A minimal runtime check should cover two owners sharing a script resource but receiving separate instances, calls into native APIs, managed notifications and parameterless methods, successful reload, failure followed by retry, and deletion of an owner during recovery.

Field-state migration, complex cross-object references and actual assembly unloading each need their own runtime evidence. Reloading a project assembly also does not establish a complete standalone distribution or packaging workflow.

Source entry points, relative to the Ming repository:

- `Code/MingEngine/Engine/Script/ScriptSystem.cpp` and `ScriptSystem.hpp`
- `Code/MingEngine/Engine/Script/CSharpScript.cpp`
- `Code/MingEngine/Engine/Script/CSharpScriptGenerator.cpp`
- `Code/CSharp/Ming.SourceGenerators/ScriptPathGenerator.cs`
- `Code/CSharp/MingSharp/Core/ScriptManagerBridge.cs`
- `Code/MingEngine/Core/Object/ManagedGCHandle.cpp` and `Object.cpp`

Return to the [Ming project page](/projects/ming-engine/).
