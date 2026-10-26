---
contentId: ming-gui-input
lang: zh
section: articles
title: "Ming：一次输入如何到达按钮"
description: "沿着输入队列、Viewport 分派、鼠标捕获和按钮状态机，解释原生 GUI 的交互职责与取消边界。"
category: engine
tags: [C++, GUI, 输入事件, 编辑器]
relatedProject: ming-engine
draft: false
---

## 按下与松开，为什么不能分别寻找接收者？

最简单的按钮实现，是在鼠标松开时检查光标是否位于矩形内部。但如果玩家在按钮上按下、拖出后松开，或者在按住时窗口失焦，就需要记录一段持续交互。Ming 将这些问题拆到输入队列、`Viewport` 的接收者管理和 `BaseButton` 的激活状态三个层次。

```text
平台输入 → InputSystem 事件队列 → Window::OnInputEvent
 → Viewport::ProcessInputEvent → ProcessGuiInputEvent
 → PropagateGuiInput → Control / BaseButton::GuiInput
 → CompletePress → 业务回调
```

这条链中的回调是一种调用注册方式，不应仅因形式相似就称为另一套引擎的信号系统。

## Viewport 先决定事件属于谁

`ProcessInputEvent()` 检查入树状态与窗口焦点。位置相关事件处理前，它还调用 `FlushContainerUpdate()`，让命中测试使用已提交的布局。随后 `ProcessGuiInputEvent()` 处理三类不同关系：hover 表示光标下的控件，capture 表示当前鼠标交互接收者，focus 表示键盘输入的目标。

鼠标移动时 hover 可以变化，capture 却保持到与按下相匹配的松开事件。当前实现只跟踪一个鼠标按钮的捕获；捕获期间其他按钮的事件会被消费。这样，松开不会因为光标移动而被投递给另一个控件。左键按下还可以设置具备焦点资格的控件；键盘和文本输入则定向给焦点控件，Tab 根据可聚焦控件集合移动焦点。

这些状态保存的是 `ObjectID`。分派前重新解析对象，有助于处理交互过程中节点退出或被删除的情况，但仍需要在回调之后避免继续使用未经检查的旧指针。

## 分派与冒泡是一项独立职责

`PropagateGuiInput()` 将指针事件的位置转换到控件局部坐标，再调用 `GuiInput()`。它根据 `MouseFilter` 与处理结果决定是否继续沿父控件传播。键盘、文本输入没有沿父控件冒泡的同一条路径。

因此，“命中了某个控件”和“某个控件完成业务动作”之间还有一层规则。容器可以参与父链，却不因此自动取代子控件成为点击对象。这个边界让布局组织和交互处理可以分别讨论。

## BaseButton 管理一次激活尝试

`BaseButton::GuiInput()` 只对符合条件的鼠标左键或获得焦点后的 Enter、Space 等按键建立激活尝试，并忽略重复按键。鼠标移动更新按压是否仍在内部；松开时由 `CompletePress()` 判断是否激活。

`CompletePress()` 先提交内部状态、排队重绘，再执行 toggle、pressed 与 button-up 等回调。回调可能修改场景，因此函数在通知之间通过对象标识重新解析按钮，并检查待删除、禁用与可见状态。失焦、交互取消和退出场景树都会结束未完成尝试，而不是留下持续按压的外观。

## 验证交互，而不只验证函数返回值

检查按钮至少要包含：内部按下并松开、拖出松开、拖出后移回、键盘激活、按住时禁用、失去窗口焦点，以及回调删除自己。对象层检查可以覆盖状态机，真实窗口操作还要验证坐标、窗口事件和视觉反馈。

本次文章依据源码整理，没有重新运行窗口测试。当前代码已经有文本事件的焦点分派，也不能由此推导完整的文本编辑控件、输入法或编辑器属性编辑流程已经完成。

源码入口：`Code/MingEngine/Engine/Input/InputSystem.cpp`、`Code/MingEngine/Scene/Core/Window.cpp`、`Viewport.cpp` 与 `Code/MingEngine/Scene/GUI/BaseButton.cpp`。返回 [Ming 项目页](/projects/ming-engine/)。
