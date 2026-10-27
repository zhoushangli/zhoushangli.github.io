---
contentId: ming-csharp-bridge
lang: zh
section: articles
title: "Ming：连接 C++ 对象与 C# 脚本"
description: "从 .NET 托管、反射绑定和对象句柄，到程序集重载的恢复流程，说明 Ming 当前的跨语言职责边界。"
category: engine
tags: [C++, C#, 脚本系统, 对象生命周期]
relatedProject: ming-engine
draft: true
---

## 跨语言调用之前，先解决对象关系

把一个 C++ 方法暴露给 C#，只解决了脚本系统的一部分问题。引擎还需要知道脚本资源对应哪个托管类型、原生对象对应哪个托管实例，以及程序集替换之后哪些对象应当恢复。Ming 当前源码已采用 C# 与 .NET 桥接；早期介绍中的 AngelScript 不能继续作为现状描述。

这里有三个需要分开的身份：`CSharpScript` 表示脚本资源，`CSharpInstance` 连接脚本与某个原生 owner，托管侧的脚本对象则通过句柄参与跨语言调用。把它们混成“一个脚本指针”，会很难解释共享资源、多个实例与重载后的对象关系。

## 两个方向的调用

`ScriptSystem::Startup()` 初始化 .NET 运行时和托管桥接，`InitializeDotNetRuntime()` 使用 `hostfxr` 获取所需入口，并加载托管初始化函数。原生接口以回调表交给托管侧，托管函数入口也被原生侧保存。

```text
C# 生成接口 → NativeFuncs.MethodBindPtrCall → C++ 方法绑定
C++ 对象通知 → CSharpInstance → ScriptSystem → 托管脚本方法
```

`CSharpScriptGenerator` 读取引擎反射元数据，生成类绑定、构造接口与调用封装。这样，反射注册成为原生接口和脚本接口之间的一处事实来源，但绑定生成仍需要处理参数布局、返回值以及内建类型转换，不能简单理解为把函数名写进字符串。

反方向上，`CSharpInstance::Call()` 和通知入口将请求交给 `ScriptSystem`。这种职责划分让场景节点不必自己处理托管程序集的加载细节。

## 脚本资源如何找到托管类型

托管侧 `ScriptManagerBridge` 维护脚本路径到 `Type` 的映射，也维护原生脚本资源指针到 `Type` 的关联。`AddScriptBridge()` 将原生路径转换为托管字符串，解析已注册类型，再建立关联。它会拒绝空指针、无法实例化的类型等不符合条件的数据。

原生对象包装和用户脚本实例的用途也不同。`GetOrCreateNativeManagedWrapper()` 尽量复用 owner 上已有的原生绑定句柄；用户脚本实例则通过独立创建与恢复流程连接 owner。`ManagedGCHandle` 禁止复制，允许移动并负责释放，避免把同一个句柄误当成两个独立所有者。托管侧还区分脚本实例句柄与原生绑定句柄，并按程序集加载上下文跟踪引用。

## 重载是一段有失败状态的流程

`ReloadProjectAssembly()` 先暂停脚本执行，再收集待恢复实例、解除旧实例、卸载程序集、加载新程序集并恢复实例。只有整条链成功才清除备份并恢复执行；失败后保留恢复信息和暂停状态，供后续重试使用。`PackedScene::Pack()` 也检查脚本执行是否暂停，防止在恢复未完成时保存不完整状态。

这说明“能重新加载 DLL”和“完成安全的脚本重载”不是同一件事。当前流程明确管理重建与失败重试，但不能从函数名称推断任意 C# 字段都能完整迁移。需要单独检查字段的保存范围、跨对象引用、重载时对象销毁，以及程序集是否真正可卸载。

## 可以怎样检查

最小检查可以从一个原生节点与一个 C# 脚本开始：调用生成接口，触发脚本通知，再测试成功重载、加载失败和失败后重试。句柄计数、旧对象有效性及场景保存行为都应纳入观察。本次整理进行了源码链路核对，没有新增编译或运行验证，也不把当前开发机的程序集加载路径当成独立发行版的证明。

源码入口：`Code/MingEngine/Engine/Script/ScriptSystem.cpp`、`CSharpScript.cpp`、`CSharpScriptGenerator.cpp`，以及 `Code/CSharp/MingSharp/Core/ScriptManagerBridge.cs`。返回 [Ming 项目页](/projects/ming-engine/)。
