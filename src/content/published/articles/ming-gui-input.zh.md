---
contentId: ming-gui-input
lang: zh
section: articles
title: "Ming：一次输入如何到达按钮"
description: "从按下、拖出和松开的交互开始，解释输入分发、捕获与焦点、按钮状态机，以及 pressed 信号和 Callable 的对象生命周期。"
category: engine
tags: [C++, GUI, 输入事件, 编辑器]
relatedProject: ming-engine
draft: false
---

## 在按钮上按下，拖出去再松开

假设我在按钮 A 上按下左键，拖到按钮 B 上再松开。A 需要结束按压，B 不应该因为收到一次松开就被激活。如果我拖出后又回到 A 再松开，则通常应该完成 A 的点击。仅在松开时查询鼠标下的控件，无法区分这些过程。

我在 Ming 中把一次交互分成三层：输入系统保留事件顺序，`Viewport` 决定接收者，`BaseButton` 判断一次按压是否构成激活。业务通知发生在状态提交之后。

```text
平台输入 → InputSystem 事件队列
    ↓ 运行窗口的 Window::OnInputEvent
Viewport::ProcessInputEvent
    ↓ 更新布局 / 检查窗口焦点
ProcessGuiInputEvent
    ↓ hover、capture、focus
PropagateGuiInput → BaseButton::GuiInput
    ↓ CompletePress：先提交状态
pressed 回调 → 重新检查按钮 → EmitSignal("pressed")
    ↓ 同步遍历连接快照
Callable → Object::Call → 原生绑定 / 脚本方法
```

这是运行窗口的常规路径。编辑器通过 `EditorUI::HandleInput()` 处理快捷键等逻辑后，也将输入送入根视口的 `ProcessInputEvent()`，复用同一套控件分发。

## hover、capture 与 focus 各自记录什么？

hover 表示鼠标当前位于哪个控件上；capture 表示当前这次鼠标交互属于哪个控件；focus 表示键盘输入的目标。在前面的例子中，hover 可以从 A 变成 B，capture 仍然是 A，直到对应按键松开或交互被取消。

`Viewport::ProcessInputEvent()` 先检查入树状态和窗口焦点，再刷新待处理的容器布局，让后续位置转换与命中测试使用已提交的布局。普通控件接收者以 `ObjectID` 保存，实际分发时重新解析对象，避免把已经销毁的控件继续当作接收者。

当前捕获只记录一个鼠标按钮及其目标。其他按钮不会建立第二份并行捕获；其中，左键捕获期间的右键按下仍会转给捕获目标，以支持控件处理取消等行为。左键按下还可以把焦点交给具备焦点资格的控件。

普通键盘和文本事件定向给焦点控件，Tab 在可聚焦集合中移动焦点。弹出菜单、拖放等交互有自己的优先处理分支，不能把所有输入概括为一次鼠标命中测试。

## 坐标转换与冒泡属于分发层

按钮使用局部坐标判断光标是否在内部。`PropagateGuiInput()` 复制事件，把位置减去控件全局位置，再调用 `GuiInput()`。控件处理结果和 `MouseFilter` 决定指针事件是否继续向父控件传播。

键盘和文本不走同样的父链冒泡。鼠标滚轮在 Stop 过滤器下也有继续向上传播的处理，让父级滚动容器有机会响应。因此，布局上的父子关系、鼠标命中对象和最终处理者，需要分别理解。

## BaseButton 维护一次激活尝试

`BaseButton::GuiInput()` 接受鼠标左键，以及取得焦点后的 Enter、小键盘 Enter 或 Space，并忽略重复按键。按下时建立一次尝试，记录是鼠标还是键盘；鼠标移动时更新是否仍在内部；匹配的松开事件再调用 `CompletePress()`。

`CompletePress()` 先清除尝试状态、更新切换状态并请求重绘，然后执行通知。这样，回调看到的是已经提交的按钮状态。禁用、失焦、退出场景树或输入取消都会结束未完成的交互，避免按钮一直保留按下外观。

当前通知顺序也有明确边界：先执行适用的 toggled 回调，再执行 pressed 回调；重新解析按钮并检查待删除、禁用、可见和入树状态之后，才发射 `pressed` 信号；之后再次解析对象，再处理 button-up 回调。如果前一个回调删除了按钮，后续步骤就不能继续使用旧指针。

## 从 pressed 到 Callable

当我希望按钮通知另一个对象的方法时，可以使用当前对象系统中的连接接口：

```cpp
Signal pressed(button, "pressed");
Callable onPressed(receiver, "OnPressed");
bool const connected = pressed.Connect(onPressed);
```

这个接口示例假定按钮和接收者已经创建，`OnPressed` 能被对象的方法查找发现；调用方应检查连接结果。原生方法需要反射绑定，用户 C# 方法则受当前生成分派支持的签名范围约束。

`Signal` 保存发射对象的 ID 和信号名，连接数据由发射者持有。`Callable` 保存目标 `ObjectID` 和方法名，不持有目标对象。每次调用都重新解析目标，并交给 `Object::Call()`，再由对象系统选择脚本或原生方法。

连接同时写入接收者的反向订阅记录。这样，无论发射者还是接收者先销毁，`ClearSignalConnections()` 都可以清理另一端的记录，再从 `ObjectDatabase` 移除对象。检查 ID 负责判断对象是否还活着，双向记录负责清理连接关系，两者解决的问题不同。

## 回调修改连接表时会怎样？

信号发射前会复制连接和参数，随后同步遍历快照。回调新增的连接从后续发射开始参与；断开连接会修改实际连接表，但不会把当前快照中的条目删除。如果该条目的目标仍存活且可调用，它仍可能在本轮被调用。这是当前实现的快照语义。

每次调用前会解析目标并跳过已销毁或正在预删除的对象，调用后再检查发射者。发射者被销毁或进入预删除状态时停止后续通知。这里讨论的是对象销毁与重入，不代表任意线程都可以安全地修改连接表；当前路径也没有提供延迟投递或一次性连接选项。

## 当前边界与检查方式

我核对了当前源码中的输入与信号链路，本次文档更新没有重新运行引擎窗口。代表性交互应覆盖内部按下松开、拖出松开、拖出再移回、键盘激活、按住时禁用和窗口失焦；连接层还应检查回调删除接收者或按钮，以及发射过程中连接、断开的快照行为。

函数级检查只能验证部分状态逻辑，坐标转换、窗口事件和按压反馈仍需要真实窗口操作。已有文本事件分派也不能直接证明完整输入法和所有文本编辑行为都已支持。

源码入口（相对于 Ming 仓库）：

- `Code/MingEngine/Engine/Input/InputSystem.cpp`
- `Code/MingEngine/Scene/Core/Window.cpp`、`Viewport.cpp`
- `Code/MingEngine/Scene/GUI/BaseButton.cpp`
- `Code/MingEngine/Core/Object/Object.cpp`、`Callable.cpp`、`Signal.cpp`
- `Code/MingEngine/Editor/UI/EditorUI.cpp`

返回 [Ming 项目页](/projects/ming-engine/)。
