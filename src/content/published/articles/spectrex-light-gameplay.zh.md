---
contentId: spectrex-light-gameplay
lang: zh
section: articles
title: "SpectreX：让光路成为可交互的游戏规则"
description: "从光源、镜面与玻璃，到感光器和门，梳理 SpectreX 光学玩法的数据流、反馈与工程取舍。"
category: gameplay
tags: [Godot, C#, 光学解谜, 交互系统]
relatedProject: spectrex
draft: true
---

## 光既要看得见，也要能决定机关状态

在光学解谜中，画出一条光带还不够。玩家需要预判遮挡、反射和折射，机关需要获得稳定的接收结果，视觉表现也要让规则可读。SpectreX 将光学对象的数据管理、光路求解、光带绘制和机关反馈分别处理，再通过共享结果连接起来。

我在这个团队项目中承担技术美术、程序和策划工作。本文说明当前代码如何组织这套交互，不将所有团队设计或资产归为个人创作，也不把它称为完整的物理光学模拟。

```text
场景组件提交变换、配置与碰撞对象
 → LightService 调度需要更新的光线
 → LightSolver 产生路径与命中贡献
 → LightRenderer 更新光带 / 感光器汇总接收强度
 → LightSensorController 更新反馈与事件
 → DoorController 判断开门条件
```

## 用统一数据连接不同光学对象

`LightService` 持有光源、镜面、转换器、玻璃、玩家、感光器和不透明体的数据，并通过 `LID` 与碰撞对象关联。场景组件负责提交位置或参数变化，服务负责跨对象求解。这样，机关控制器不用自己重复实现一套光线查询。

`LightSolver::Trace()` 根据命中对象类型推进路径：不透明体结束传播；感光器记录加权强度后吸收光线；镜面检查启用状态、正反面与反射次数，再改变方向并应用反射损耗；玻璃处理进入与离开介质时的折射、色散和损耗。光线长度、最大反射次数及边界事件上限为计算提供终止条件。它们是可配置的游戏规则与数值近似，不能直接等同于连续光谱的真实传播。

## 将“接收到光”与“视觉保持点亮”分开

服务汇总每条光线、每个频率对感光器的贡献，白色感光器接收各频率，彩色感光器只累加对应频率。`LightSensorController` 再用 `ReceivedIntensity >= RequiredIntensity` 判断实际激活状态。

这里有一个很具体的状态区分：`IsActivated` 表示当前强度是否达标，`IsLightUp` 还可以因 `KeepLightUp()` 而保持点亮。自发光强度会随接收强度与阈值的比例变化，让达标前也能提供反馈；状态变化通过 `OnLightChanged` 和 `OnLightUp` 通知订阅者。

`DoorController` 独立为绑定的感光器累计点亮确认时间，全部满足后开门，并通过保存系统记录。这个拆分允许感光器及时响应，同时让门采用自己的确认规则。默认参数不是对所有关卡体验的结论，实际阈值和延时仍需通过游玩调整。

## 可交互的装置需要状态和制作接口

`SocketController` 将可移动插槽组织为 Idle、Occupied、Returning、ReturnBlocked 等状态，并允许安装镜面或转换器。安装资源、偏移和旋转节点来自预制体配置；旋转逻辑将光学变换同步回求解系统。它让“移动、转向、改变光路”的操作具备明确的实现入口，也为关卡搭建保留配置空间。

这并不自动证明规则容易理解。设计验收还需要观察玩家能否理解装置朝向、颜色过滤、能量衰减，以及光带和机关反馈之间的关系。

## 求解预算与检查边界

当前 `LightService::PhysicsUpdate()` 记录几何变化，标记受影响光线，再通过调度预算处理脏光线；转换器输出与普通光源共同进入感光贡献汇总。源码也记录求解光线数、频率追踪数、网格更新数及耗时，便于定位成本。

分批更新减少无关重算的目标，需要与交互响应一致性一起验收。可以分别测试转动镜面、移动遮挡物、切换房间、连续转换和强度临界点，并检查光带、感光器与门的顺序。本次仅核对源码，没有提供新的帧率结果或玩家测试数据。

源码入口：`Scripts/Core/LightService.cs`、`LightSolver.cs`、`LightRenderer.cs`，以及 `Scripts/LightSensorController.cs`、`DoorController.cs`、`SocketController.cs`。返回 [SpectreX 项目页](/projects/spectrex/)。
