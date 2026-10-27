---
contentId: ming-scene-resources
lang: en
section: articles
title: "Ming: connecting nodes, scenes, and resources"
description: "Tracing scene lifetime, two-phase PackedScene instantiation, and resource identity in Ming's C++ runtime."
category: engine
tags: [C++, Scene tree, Serialization, Resources]
relatedProject: ming-engine
draft: true
---

## Why does a scene need several representations?

An editor scene is both a collection of running objects and data that can be saved, loaded, and instantiated repeatedly. Writing an object's memory layout directly to disk would also write assumptions about pointers, transient state, and resource references. Ming separates these responsibilities across `Node`, `SceneTree`, `PackedScene`, and resource format loaders: nodes organize relationships, the tree drives lifetime, a packed scene records reconstructible data, and loaders handle its disk representation.

```text
Scene file ↔ PackedScene data ↔ Detached node hierarchy
                                         ↓ ChangeScene
                                SceneTree / root Window
```

This separates reconstructing a scene from starting its execution, and makes initialization order easier to reason about.

## Relationships belong to nodes; execution belongs to the tree

`Node` stores a name, parent and children, and processing switches. Its interfaces include `AddNode()`, `GetNode()`, and `QueueFree()`. `SceneTree` creates a root `Window` named Root, stores the active scene through an `ObjectID`, and coordinates updates, deferred deletion, transform notifications, and container layout.

For example, `QueueDestroyNode()` records an object identifier and marks the node for deletion. Later, `FlushPendingNode()` resolves objects that still exist, detaches them, propagates their exit from the tree, and deletes them. Moving destruction to a controlled point avoids immediately invalidating the collection currently being traversed by an update or callback. Callers must still distinguish a queued node from an object that has already disappeared.

`UpdateScene()` advances physics at a fixed interval, then sends process notifications to registered nodes that have processing enabled. A scene tree therefore participates in runtime scheduling and lifetime management, rather than serving only as an editor hierarchy.

## Reconstructing PackedScene in two phases

Each `PackedNode` records a name, type, relative parent path, and property list. `Pack()` traverses parents before children. Only properties marked `Storage` with a getter are considered, and values equal to those on a default instance are omitted when possible.

`Instantiate()` first creates all nodes through `ClassDatabase::CreateInstance()` and rebuilds a detached hierarchy. It then resolves reflected properties, checks compatibility, and calls their setters. A setter can consequently inspect the already constructed parent and child relationships before scene-tree lifecycle callbacks begin.

There are concrete failure boundaries: the first node must be the sole root, later parent paths must be valid and resolvable, and attaching a node must not silently change its sibling name. Unknown or incompatible properties produce warnings and are skipped. This accommodates some data evolution; it does not guarantee compatibility with arbitrary scene format revisions.

## Resource paths and object identity

`ResourceLoader::Load()` first checks a cache keyed by `VirtualPath`. On a miss, `LoadInternal()` checks import metadata, follows an imported-file path when appropriate, and selects a registered format loader. It also retains the original source path so the editor can show the resource the user selected, rather than only an internal cache filename.

`Reload()` makes another useful tradeoff. It loads fresh data without using the cache, then attempts to move that data into the cached resource through `CopyFrom()`. Existing `Ref<Resource>` holders can keep referring to the same object. If loading or copying fails, the old cached object remains available. This helps preserve editor state, while placing a clear responsibility on each resource type to implement appropriate copy semantics.

## Inspection and verification boundaries

A small scene containing a root, a child, and a shared resource provides useful acceptance cases: restore relationships and non-default properties after saving; check resource reuse across repeated loads; retain valid references after a failed reload; and observe correct tree exit during deletion and scene changes. This article documents current source behavior and verification ideas. The reading itself is not a new runtime test, and does not establish that a distributable game export is complete.

Source entry points: `Code/MingEngine/Scene/Core/Node.cpp`, `SceneTree.cpp`, `PackedScene.cpp`, and `Code/MingEngine/Core/Object/ResourceLoader.cpp`. Return to the [Ming project](/projects/ming-engine/).
