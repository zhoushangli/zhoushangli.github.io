---
contentId: ming-csharp-bridge
lang: zh
section: articles
title: "Ming：连接 C++ 对象与 C# 脚本"
description: "从一个挂载 C# 脚本的节点出发，解释两类代码生成、原生与托管对象身份，以及程序集重载的实例重建和失败重试。"
category: engine
tags: [C++, C#, 脚本系统, 对象生命周期]
relatedProject: ming-engine
draft: false
---

## 一个节点，为什么还需要几种脚本对象？

假设我给一个原生 `Node3D` 挂载 C# 控制脚本，让它在更新时修改位置。表面上只是把引擎函数暴露给 C#，实际还需要回答三个问题：脚本文件对应哪个托管类型，这个类型的实例连接哪个原生节点，以及重新编译程序集后如何建立新的连接。

我在 Ming 中把这些身份分开：原生节点是 owner，`CSharpScript` 是可以共享的脚本资源，`CSharpInstance` 连接某个 owner 与该资源，GC 句柄让原生侧能够访问对应的托管实例。两个节点使用同一个脚本资源时，仍然需要各自的实例。

```text
引擎反射元数据
    ↓ CSharpScriptGenerator（原生工具）
引擎 C# API → MethodBindPtrCall → 原生 MethodBind

用户 C# 源码
    ↓ ScriptPathGenerator（Roslyn 编译期）
脚本路径标记 + 用户方法分派 → 项目程序集
    ↓ hostfxr 承载的 .NET / 托管桥接
CSharpScript 路径 → 托管 Type
    ↓ Instantiate(owner)
原生 owner ↔ CSharpInstance / GC 句柄 ↔ 托管实例
```

## hostfxr 连接运行时，生成代码连接 API

`ScriptSystem::Startup()` 初始化脚本系统，`InitializeDotNetRuntime()` 使用 `hostfxr` 获取 .NET 加载入口。系统加载托管入口、交换回调表，再通过桥接加载项目程序集。这样，场景节点不需要自行寻找 DLL 或管理运行时入口。

这里有两类生成器，职责不能混为一谈。原生的 `CSharpScriptGenerator` 读取 `ClassDatabase` 中的类型、方法和属性元数据，生成引擎 API 的 C# 包装、构造入口和调用封装。C# 调用引擎方法时，经由 `NativeFuncs.MethodBindPtrCall` 到达原生 `MethodBind`。参数布局、对象指针与返回值转换都在这个过程中被明确处理。

另一类是项目编译时运行的 Roslyn `ScriptPathGenerator`。它检查用户脚本声明，生成 `ScriptPathAttribute`，把项目内文件映射到 `res://` 路径；它还生成用户方法的查找与调用分派。当前脚本要求顶层、非泛型、所有声明为 `partial`，并有与类名匹配的文件名。用户方法分派目前选择无参数、返回 `void` 的普通实例方法，不等于支持任意 C# 方法签名。

## 脚本路径如何落到一个 owner 上？

托管侧按脚本路径登记 `Type`。`CSharpScript::Instantiate(owner)` 先通过 `AddScriptBridge()` 建立原生脚本资源到托管类型的关联，再创建 `CSharpInstance` 并挂到 owner 上，最后请求托管桥接创建用户实例。

托管 `ScriptManagerBridge.CreateUserManagedInstance()` 检查脚本类型与 owner 原生类型是否兼容，建立 `NativePtr`，执行构造并返回句柄。原生侧将句柄交给该 owner 的脚本实例管理；如果创建或句柄安装失败，就清理这次实例化。这里描述的是实际脚本实例，编辑器使用的占位实例是另一条路径。

原生 API 包装与用户脚本实例也有不同用途。`GetOrCreateNativeManagedWrapper()` 尽量复用 owner 上的原生绑定句柄；用户脚本实例则持有自己的脚本句柄。`ManagedGCHandle` 禁止复制、允许移动，并在释放时通知托管侧。这样，C++ 中复制一个看似普通的句柄值，不会被误当作两个独立的所有者。

## 原生通知与按名称调用如何返回 C#？

脚本中的位置操作沿生成的 API 返回 C++；反方向上，原生通知由 `CSharpInstance::Notification()` 转给托管 `_Notification`，再进入脚本生命周期方法。按名称调用则由 `CSharpInstance::Call()` 经 `ScriptSystem` 和托管桥接进入生成的分派代码。

`Object::Call()` 还定义了一个重要规则：先尝试脚本方法，只有结果为 `InvalidMethod` 才查找原生绑定。参数错误或执行失败会作为错误返回，不会被误当作“没有这个脚本方法”而继续调用同名原生方法。这让 Callable 等调用方可以获得明确的失败原因。

## 重载需要重建连接，也需要保留失败后的退路

重新编译 DLL 后，旧托管实例不能继续当作新程序集中的对象。我在 `ReloadProjectAssembly()` 中先暂停脚本执行，再记录实例关联、解除旧实例、卸载旧程序集、加载新程序集，最后重建实例。

理解能力边界最直接的方式，是看备份结构本身：

```cpp
struct StateBackup
{
    ObjectID          m_owner;
    Ref<CSharpScript> m_script;
};
```

它来自 `ScriptSystem.hpp`，记录的是“哪个 owner 应该重新挂载哪个脚本”，并用资源引用维持脚本资源的寿命。它没有任意 C# 字段的值。因此，当前流程是实例重建，不能承诺完整保留控制脚本中的计时器、集合或对象引用。

如果卸载、加载或恢复失败，存在待恢复记录时，系统保留原始记录和暂停状态。重试时先解除已经部分恢复的实例，再重新加载并恢复；恢复期间已经销毁的 owner 会被跳过。成功后才清除记录并恢复执行。没有待恢复记录的失败路径会解除暂停，不能笼统理解为任何失败都会永久暂停。

`PackedScene::Pack()` 同时拒绝在脚本执行暂停时打包，避免恢复未完成的场景被当作正常状态保存。这体现了脚本重载与场景持久化之间的约束。

## 当前边界与检查方式

我核对了当前源码中的生成、调用、句柄与重载链路，本次文档更新没有重新编译或运行引擎。最小运行检查应覆盖：两个节点共享脚本资源但拥有不同实例；脚本调用原生 API；通知和无参数方法返回托管侧；成功重载、加载失败及重试；恢复期间 owner 被删除后的处理。

字段状态迁移、复杂跨对象引用和程序集是否真正完成卸载，需要各自的运行证据。能够重新加载项目程序集，也不代表独立发行环境和打包导出已经完成。

源码入口（相对于 Ming 仓库）：

- `Code/MingEngine/Engine/Script/ScriptSystem.cpp`、`ScriptSystem.hpp`
- `Code/MingEngine/Engine/Script/CSharpScript.cpp`
- `Code/MingEngine/Engine/Script/CSharpScriptGenerator.cpp`
- `Code/CSharp/Ming.SourceGenerators/ScriptPathGenerator.cs`
- `Code/CSharp/MingSharp/Core/ScriptManagerBridge.cs`
- `Code/MingEngine/Core/Object/ManagedGCHandle.cpp`、`Object.cpp`

返回 [Ming 项目页](/projects/ming-engine/)。
