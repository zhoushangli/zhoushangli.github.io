---
contentId: ming-scene-resources
lang: zh
section: articles
title: "Ming：节点、场景与资源如何连接起来"
description: "从保存并重开一个包含共享资源的场景开始，解释节点生命周期、两阶段实例化，以及保持资源对象身份的重载。"
category: engine
tags: [C++, 场景树, 序列化, 资源管理]
relatedProject: ming-engine
draft: false
---

## 保存一个场景，究竟保存了什么？

假设我在编辑器中放置两个模型，让它们使用同一个纹理资源，再修改其中一个节点的位置。关闭编辑器后重新打开，我希望节点名称、父子关系和位置能够恢复，也希望两个模型继续共享资源。

这些内容不能直接等同于对象的内存。父节点指针只在本次进程中有效，渲染句柄需要重新建立，正在执行的交互也不应该随场景保存。我在 Ming 中将这些职责分给 `Node`、`SceneTree`、`PackedScene` 和资源加载器：分别组织对象关系、驱动运行、记录可恢复的数据、处理资源的磁盘表示。

```text
编辑器中的节点层级
    ↓ PackedScene::Pack / 格式保存器
场景文件：节点类型、名称、父路径与存储属性
    ↓ 格式加载器 / PackedScene::Instantiate
创建全部节点并恢复层级 → 设置属性
    ↓ SceneTree::ChangeScene / FlushPendingNode
挂入场景视口 → 开始入树生命周期

属性中的资源路径 → ResourceLoader
    ↓ 导入结果 / 格式加载器
按路径缓存的资源对象
```

这里有两个独立步骤：恢复出一个节点层级，以及让它进入场景树开始运行。把它们分开，才能解释初始化时哪些对象已经存在、哪些通知还没有发生。

## Node 组织关系，SceneTree 管理运行时机

`Node` 保存名称、父子关系和处理开关，提供 `AddNode()`、`GetNode()`、`QueueFree()` 等接口。`SceneTree` 则持有根 `Window`，管理当前场景、更新调度，以及待删除节点、变换通知和容器布局队列。编辑器可以指定场景视口，让被编辑的场景挂入嵌入视口，而不是直接占用整个窗口。

以删除为例，按钮回调可能要求删除一个仍在当前遍历中的节点。`QueueDestroyNode()` 先设置待删除标记并记录 `ObjectID`，`FlushPendingNode()` 再重新查找对象，解除父子关系、退出场景树并删除。这样，发出删除请求和真正释放对象之间有一个受控边界。

这个安排也带来调用约束：排队删除之后，对象可能仍能通过 ID 找到。后续逻辑还要检查 `IsQueuedForDeletion()`，不能仅凭指针非空就继续把它当作正常节点使用。

## 为什么先建完整层级，再设置属性？

假设子节点的某个 setter 需要查询父节点，或者根据兄弟节点调整状态。如果我创建一个节点就立即写入全部属性，后续节点尚未创建，setter 看到的就是不完整的场景。

因此，`PackedScene::Instantiate()` 分为两轮。第一轮通过 `ClassDatabase::CreateInstance()` 创建节点，恢复名称与父子关系；第二轮查找属性元数据、检查 setter 和值类型，再调用 setter。两轮都发生在层级脱离场景树时，入树生命周期尚未开始。

恢复层级也需要检查数据：第一个节点必须是根，后续节点必须具有有效的相对父路径；父节点需要已经存在，同级名称不能在挂接时被自动改成另一个名字。结构错误会使实例化失败。未知或类型不兼容的属性会被警告并跳过；这是一种有限的容错，不是任意版本数据的兼容保证。

## Storage 决定持久化范围

我用反射属性中的 `Storage` 标记决定哪些值参与保存。`ParseNodeRecursively()` 按父节点优先的顺序遍历，只读取具有该标记和 getter 的属性，并尝试省略与默认对象相同的值。不可序列化节点会被跳过，其子树也不会继续打包。

这使运行对象和存储表示可以分别演进。前面的例子中，位置应通过存储属性恢复；临时选中状态、输入捕获等编辑器运行状态则不应因为存在于对象里就自动进入场景文件。具体值如何写入文件，由场景格式和 `Variant` 的序列化逻辑负责，不能把运行指针原样当作持久化身份。

## 共享资源与节点不是同一种身份

重开场景时，节点通常是新创建的对象；资源却可能需要复用。`ResourceLoader::Load()` 以 `VirtualPath` 查询缓存，命中时返回已有资源。只有使用相同缓存键的请求才能据此获得复用，路径别名是否指向同一文件是另一个问题。

缓存未命中时，`LoadInternal()` 查询导入配置，必要时转向内部导入文件，再交给支持该路径的格式加载器。加载结果保留来源路径，让编辑器可以展示用户选择的源文件，而不是只显示内部缓存文件。

接下来是更容易忽略的情况：我修改纹理并重新导入，两个模型还持有旧的 `Ref<Resource>`。如果只把缓存表中的指针换掉，它们仍然引用原对象。Ming 的 `Reload()` 会先绕过缓存读取新数据，再尝试更新原对象：

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

这是 `ResourceLoader::Reload()` 的实现片段。它保留缓存对象的身份，使已有引用能够观察到更新；相应地，每种资源必须正确实现 `CopyFrom()`，包括所需的渲染资源刷新。新数据加载失败时直接返回旧缓存；复制失败时也返回旧对象，失败路径是否完整保留其内容仍取决于具体复制实现。

## 当前边界与检查方式

我用当前工作区源码梳理了上述流程，没有在这次文档更新中重新运行引擎。对应的最小运行检查是：保存并重开场景，核对父子关系和非默认属性；重复加载同一路径，检查共享对象；重载资源后确认既有引用仍有效；最后检查换场景和排队删除时的退出通知。

这条链说明了场景恢复与资源身份的处理方式。独立游戏的打包导出仍属于后续工作，不能由编辑器内保存和加载场景的能力推导出来。

源码入口（相对于 Ming 仓库）：

- `Code/MingEngine/Scene/Core/Node.cpp`
- `Code/MingEngine/Scene/Core/SceneTree.cpp`
- `Code/MingEngine/Scene/Core/PackedScene.cpp`
- `Code/MingEngine/Scene/Core/PackedSceneFormat.cpp`
- `Code/MingEngine/Core/IO/ResourceLoader.cpp`

返回 [Ming 项目页](/projects/ming-engine/)。
