---
contentId: ming-scene-resources
lang: zh
section: articles
title: "Ming：节点、场景与资源如何连接起来"
description: "从场景树的生命周期，到 PackedScene 的两阶段实例化与资源缓存，梳理 Ming 中运行对象和持久化数据的边界。"
category: engine
tags: [C++, 场景树, 序列化, 资源管理]
relatedProject: ming-engine
draft: false
---

## 一个场景，为什么需要几种表示？

编辑器中的场景既是运行中的对象集合，也是一份能够保存、重新加载并反复实例化的数据。如果直接把对象的内存布局写入文件，指针、运行状态和资源引用都会成为问题。Ming 将这些职责拆成 `Node`、`SceneTree`、`PackedScene` 与资源格式加载器：节点组织对象关系，场景树驱动生命周期，打包场景记录可恢复的数据，格式加载器处理磁盘表示。

```text
场景文件 ↔ PackedScene 数据 ↔ 脱离场景树的节点层级
                                      ↓ ChangeScene
                              SceneTree / 根 Window
```

这条链把“恢复一个场景”和“开始运行一个场景”分开，是理解其他系统接入顺序的起点。

## 节点负责关系，场景树负责运行

`Node` 保存名称、父子关系及处理开关，并提供 `AddNode()`、`GetNode()`、`QueueFree()` 等接口。`SceneTree` 创建名为 Root 的根 `Window`，保存当前场景的 `ObjectID`，集中处理更新、延迟删除、变换通知和容器布局。

例如，`QueueDestroyNode()` 先记录对象标识并设置待删除状态，`FlushPendingNode()` 再解析仍然存在的对象，解除父子关系、退出场景树并删除。将实际删除放到受控时点，可以避免在遍历节点或执行回调的中途直接破坏当前集合。这种安排仍要求调用方正确处理“已排队删除”的状态，不能把排队等同于对象已经消失。

`UpdateScene()` 使用固定间隔推进物理更新，再对允许处理的已注册节点发送处理通知。它说明场景树不仅是用于展示的层级，也是运行时调度与生命周期的组织者。

## PackedScene 的两阶段恢复

`PackedNode` 记录节点名称、类型、相对父路径和属性列表。`Pack()` 按父节点优先的顺序遍历；只有带 `Storage` 标记且具有 getter 的属性才参与保存，并尽量省略与默认对象相同的值。

`Instantiate()` 则分成两个阶段：先通过 `ClassDatabase::CreateInstance()` 创建全部节点并重建脱离场景树的层级，再通过反射查找属性、检查兼容性并调用 setter。这样，setter 查询父子节点时，层级已经存在，而入树后的生命周期回调尚未开始。

恢复过程也包含具体的失败边界：首节点必须是唯一根节点；后续父路径必须有效且可解析；同级名称不能在挂接时被悄悄改写。未知或不兼容的属性会被跳过并记录警告。它允许有限的数据演进，但不代表任意版本的场景文件都能兼容。

## 资源路径与对象身份

`ResourceLoader::Load()` 先查询以 `VirtualPath` 为键的缓存。未命中时，`LoadInternal()` 检查导入配置，必要时跳转到内部导入文件，再选择支持该路径的格式加载器。加载后保留原始来源路径，让编辑器能展示用户选择的资源，而不是只显示缓存文件。

`Reload()` 的取舍更值得注意：它先无缓存加载新数据，再尝试通过 `CopyFrom()` 更新原缓存对象。这样已有 `Ref<Resource>` 持有者可以继续引用同一对象。失败时保留旧缓存，比无条件替换指针更有利于维持编辑器当前状态；具体资源仍必须实现正确的复制语义。

## 检查方式与当前边界

这个案例适合用一个“根节点—子节点—共享资源”的小场景来验证：保存后恢复层级与非默认属性；同一资源重复加载是否复用；重载失败后旧引用是否仍有效；删除或换场景时是否正确退出。这里整理的是当前源码中的实现与可执行检查思路，没有把本次阅读当成新的运行验收，也不据此宣称打包导出已经完成。

源码入口：`Code/MingEngine/Scene/Core/Node.cpp`、`SceneTree.cpp`、`PackedScene.cpp`，以及 `Code/MingEngine/Core/Object/ResourceLoader.cpp`。返回 [Ming 项目页](/projects/ming-engine/)。
