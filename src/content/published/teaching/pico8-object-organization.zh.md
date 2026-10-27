---
contentId: pico8-object-organization
lang: zh
section: teaching
title: "PICO-8 对象管理案例"
description: "用 table 保存物体数据，创建多个实例并统一更新。"
category: teaching
tags: ["PICO-8", "教学实践"]
draft: true
---

## 用一个实际问题引入结构

这次教学的切入点是：角色已经能够移动，如果还要增加气球、平台或其他物体，该把它们的数据放在哪里？继续复制一组全局变量虽然直观，却会让状态和函数之间的关系越来越难找。

table、模板和实例写在 L02 教案中，我的授课回忆则将它们放在 L03。这里单独整理这个案例。

## 先把数据放在一起

先对照两个版本：分散的 `x`、`y`、`vx` 与属于一个物体的 `object.x`、`object.y`、`object.vx`。变量并没有凭空消失，改变的是这些值如何归属、怎样被传递。

接着明确模板与实例的差别：某种物体可以有共同的更新方式，但不同实例需要保留自己的位置。不要把“所有对象都遵循一个约定”误解成“所有对象共享同一份可变状态”。

## 最小示例

下面是为这篇笔记编写的简化示例：

```lua
function make_actor(x,y)
 return {x=x,y=y,vx=0}
end

function update_actor(actor)
 actor.x=actor.x+actor.vx
end

function _init()
 actors={}
 add(actors,make_actor(24,40))
 add(actors,make_actor(80,40))
 actors[1].vx=1
end

function _update()
 foreach(actors,update_actor)
end

function _draw()
 cls(0)
 for actor in all(actors) do
  rectfill(actor.x,actor.y,
   actor.x+7,actor.y+7,7)
 end
end
```

这个示例有意只展示创建、数据和调用三个关系。它不实现碰撞、边界限制或完整的物体生命周期；让学生先看到两个实例能保留不同状态，再继续扩展。

## 类比的用途与限度

可以用“蓝图和造出的物体”解释模板与实例，但必须回到代码：本例的构造函数每次返回一个新的 table，共享的是 `update_actor` 的处理约定，而不是 C++ 类声明。称它为“模拟类”是帮助理解的类比，不能据此声称 Lua 自动具备同样的访问控制和类型约束。

接着请学生沿着主循环指出：对象由谁创建、在哪里加入集合、更新函数怎样拿到当前实例。能讲清调用过程，比只把变量名换成带点号的写法更重要。

## 练习与教学反思

第一步只改变第二个实例的速度，预测另一个物体是否受影响。第二步给对象增加独立颜色，再修改绘制读取它。第三步讨论离开关卡后对象集合应该怎样处理。

这些练习根据教案整理并补充。一次同时修改输入、动画、碰撞和对象结构，容易失去对照；可以先保留行为，每次只改一种组织方式。后续见 [L03：对象管理与关卡](/teaching/pico8-l03/)。

