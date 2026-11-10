---
contentId: ming-scene-resources
lang: en
section: articles
title: "Ming: connecting nodes, scenes and resources"
description: "Starting with saving and reopening a scene with shared resources, I explain node lifecycles, two-stage instantiation and resource reload that preserves object identity."
category: engine
tags: [C++, Scene tree, Serialization, Resource management]
relatedProject: ming-engine
draft: false
---

## What does saving a scene actually save?

Suppose I place two models in the editor, give them the same texture resource and change one node’s position. After closing and reopening the editor, I want the names, hierarchy and position restored, with both models still sharing the resource.

Those requirements cannot be satisfied by copying object memory. A parent pointer is valid only in the current process, render handles need rebuilding, and an interaction in progress should not become part of a saved scene. In Ming, I divide these responsibilities between `Node`, `SceneTree`, `PackedScene` and resource loaders: object relationships, runtime execution, recoverable data and resource file representations.

```text
Node hierarchy in the editor
    ↓ PackedScene::Pack / format saver
Scene file: types, names, parent paths, storage properties
    ↓ format loader / PackedScene::Instantiate
Create nodes and rebuild hierarchy → apply properties
    ↓ SceneTree::ChangeScene / FlushPendingNode
Attach to scene viewport → begin tree-entry lifecycle

Resource paths in properties → ResourceLoader
    ↓ import output / format loader
Resource object cached by path
```

Recovering a hierarchy and entering the scene tree are separate steps. That separation makes it possible to explain which objects exist during initialization and which lifecycle notifications have not happened yet.

## Node owns relationships; SceneTree controls runtime timing

`Node` stores its name, parent, children and processing flags, with interfaces such as `AddNode()`, `GetNode()` and `QueueFree()`. `SceneTree` owns the root `Window`, manages the current scene and update scheduling, and maintains queues for deletion, transform notifications and container layout. The editor can select a scene viewport so the edited scene lives inside an embedded view rather than occupying the whole window.

Consider a button callback that requests deletion of a node still involved in the current traversal. `QueueDestroyNode()` first marks it for deletion and records its `ObjectID`. `FlushPendingNode()` resolves the object again, detaches it, moves it out of the tree and deletes it. This provides a controlled boundary between requesting deletion and freeing memory.

It also imposes a constraint: a queued node may still be found by ID. Subsequent code must check `IsQueuedForDeletion()` instead of treating every non-null pointer as a usable node.

## Why rebuild the whole hierarchy before applying properties?

A child’s setter might query its parent or adjust state using a sibling. If I created each node and immediately applied all its properties, later nodes would not exist yet. The setter would see an incomplete scene.

`PackedScene::Instantiate()` therefore makes two passes. The first creates nodes through `ClassDatabase::CreateInstance()` and restores names and parent relationships. The second looks up property metadata, checks the setter and value type, and invokes the setter. Both passes operate on a detached hierarchy, before tree-entry lifecycle notifications begin.

Reconstruction also validates the data. The first node must be the root; subsequent nodes need valid relative parent paths and existing parents. Attaching a node must not silently rename it to resolve a sibling-name collision. Structural errors fail instantiation. Unknown properties and incompatible types are skipped with warnings. This is limited tolerance for change, rather than a guarantee of compatibility between arbitrary file versions.

## Storage defines what persists

I use the `Storage` flag in reflected property metadata to decide what is saved. `ParseNodeRecursively()` traverses parents before children, reads only properties with that flag and a getter, and attempts to omit values equal to those on a default object. Non-serializable nodes are skipped together with their subtrees.

This lets live objects and saved representations evolve separately. In the example, position should be recovered through a storage property. Temporary selection state and input capture should not enter the scene file merely because an object stores them. Scene formats and `Variant` serialization define the actual file representation; a runtime pointer cannot serve directly as a persistent identity.

## Shared resources have a different identity from nodes

Reopening a scene usually creates new nodes, while resources may need to be reused. `ResourceLoader::Load()` checks a cache keyed by `VirtualPath` and returns the existing resource on a hit. Reuse follows the cache key: whether different path aliases refer to the same file is a separate concern.

On a miss, `LoadInternal()` checks import configuration, redirects to an internal import file when needed, and selects a format loader supporting that path. It retains the source path so the editor can display the file the user selected rather than only an internal cache file.

Now suppose I edit and reimport the texture while both models still hold their old `Ref<Resource>`. Replacing the pointer in the cache would leave those references pointing at the original object. Ming’s `Reload()` loads fresh data without using the cache, then attempts to update that object:

```cpp
if (cachedResource.IsValid())
{
    if (!cachedResource->CopyFrom(std::move(*freshResource)))
    {
        return cachedResource;
    }

    return cachedResource;
}
```

This excerpt from `ResourceLoader::Reload()` preserves the cached object’s identity so existing references can observe its updated contents. Each resource must implement `CopyFrom()` correctly, including any required render-resource refresh. A failed fresh load returns the old cached object directly. A failed copy also returns the old object; whether its contents remain fully intact depends on the concrete copy implementation.

## Current limits and useful checks

I traced this flow in the current working-tree source without rerunning the engine for this documentation update. A representative runtime check would save and reopen a scene, compare its hierarchy and non-default properties, verify reuse for repeated loads of the same path, and check that existing references survive resource reload. Scene replacement and queued deletion should also deliver the expected exit notifications.

This flow explains scene recovery and resource identity. A complete standalone game packaging and export workflow remains future work; editor-side scene saving and loading do not establish that capability.

Source entry points, relative to the Ming repository:

- `Code/MingEngine/Scene/Core/Node.cpp`
- `Code/MingEngine/Scene/Core/SceneTree.cpp`
- `Code/MingEngine/Scene/Core/PackedScene.cpp`
- `Code/MingEngine/Scene/Core/PackedSceneFormat.cpp`
- `Code/MingEngine/Core/IO/ResourceLoader.cpp`

Return to the [Ming project page](/projects/ming-engine/).
