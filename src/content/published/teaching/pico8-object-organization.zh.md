---
contentId: pico8-object-organization
lang: zh
section: teaching
title: "教学案例：从分散变量到 Lua 对象组织"
description: "用“如何再增加一个物体”引出数据聚合、实例创建和统一更新，而不先引入复杂类系统。"
category: teaching
tags: ["PICO-8", "教学实践"]
draft: false
---

## 用一个实际问题引入结构

这次教学的切入点是：角色已经能够移动，如果还要增加气球、平台或其他物体，该把它们的数据放在哪里？继续复制一组全局变量虽然直观，却会让状态和函数之间的关系越来越难找。

原始 L02 教案记录了 table、模板与实例的讲解，授课回忆则将这段内容放在 L03。这里将其作为跨课时案例，讨论教学方法，不据此重新确定当时每分钟的课程安排。

## 先把数据放在一起

先对照两个版本：分散的 `x`、`y`、`vx` 与属于一个物体的 `object.x`、`object.y`、`object.vx`。变量并没有凭空消失，改变的是这些值如何归属、怎样被传递。

接着明确模板与实例的差别：某种物体可以有共同的更新方式，但不同实例需要保留自己的位置。不要把“所有对象都遵循一个约定”误解成“所有对象共享同一份可变状态”。

## 最小示例

下面是为文章重新编写的教学示例，不是原课堂文件，也没有引入继承框架：

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

这里的练习是对原教案的整理与补充，不是对已经收集到的学生表现作统计。对于刚接触编程的成员，一次把输入、动画、碰撞和对象化结构全改完容易失去对照；更好的节奏是每次保留行为，再改变组织方式。[L03 的生命周期与关卡整理](/teaching/pico8-l03/)继续连接这一约定。

