---
contentId: sifu-combat-analysis
lang: zh
section: articles
title: "《师父》战斗分析"
description: "结合录屏，分析《师父》一对一战斗中的防御、硬直和反击机会。"
category: gameplay
tags: [战斗设计, 核心循环, 动作游戏, 游戏分析]
draft: false
---

## 为什么分析《师父》

在一个强调近距离对抗的项目构想中，我希望玩家与敌人能够快速交换进攻和防守的主动权。问题不只是给角色增加攻击、防御和闪避动作，而是让这些动作形成可以理解、学习和反复变化的循环。

我选择《师父》作为参考，重点看一对一的攻守交替。这篇根据当时的游玩记录、录屏和分析图整理；“窗口”“短硬直”“长硬直”描述的是可见表现，内部数值和状态机仍不清楚。

## 核心循环：先争取机会，再消耗敌人

我把战斗分为两个互相嵌套的循环：

1. **目标循环**：逐步消耗敌人生命或推动其架势达到破坏状态，获得处决机会，再转向下一个目标。
2. **交换循环**：应对敌人进攻，利用成功防御或闪避争取反击窗口，在窗口中输出，然后重新进入应对阶段。

<figure>
  <img src="/media/sifu/combat-loop.png" alt="原始分析中绘制的攻守交替循环" loading="lazy" />
  <figcaption>原始分析图。图中“减少敌人架势条”的早期措辞，在本文统一理解为推动敌人接近架势破坏，而不是对 UI 数值增减方向的定义。</figcaption>
</figure>

```text
敌人进攻
  → 玩家观察并防御或闪避
  → 出现反击机会
  → 玩家攻击、延续或扩大收益
  → 敌人恢复应对能力
  → 再次交换主动权
```

<figure>
<video controls preload="none" playsinline aria-label="《师父》玩家与敌人攻守交替的录屏示例">
  <source src="/media/sifu/turn-exchange.mp4" type="video/mp4" />
  <a href="/media/sifu/turn-exchange.mp4">下载攻守交替演示视频</a>
</video>
  <figcaption>这段录屏用于观察交换循环，不包含完整的处决与更换目标过程。</figcaption>
</figure>

在这个模型中，防守并非等待进攻重新开始的空白时间。它决定玩家何时拿回主动权，以及接下来可以安全攻击多久。

## 血量、架势和硬直

原稿尝试用几种“条”解释战斗：血条、架势条，以及隐藏的长短硬直累积。整理时，我更愿意把前两者与后两者分开：

| 分析对象 | 能从画面与操作中观察什么 | 不能直接确定什么 |
| --- | --- | --- |
| 生命 | 伤害后生命显示的变化 | 完整伤害公式及所有修正条件 |
| 架势 | 防御、受击与破坏时的显示和反应 | 每个招式的内部增量、恢复规则 |
| 短硬直 | 敌人短暂停顿，玩家获得有限攻击机会 | 是否存在独立数值条，或由动作与状态直接控制 |
| 长硬直 | 更明显、更持久的失衡表现，如捂头 | 是否由某个隐藏槽积累触发，以及槽的衰退方式 |

<figure>
<video controls preload="none" playsinline aria-label="《师父》较长硬直反应的录屏示例">
  <source src="/media/sifu/long-stagger.mp4" type="video/mp4" />
  <a href="/media/sifu/long-stagger.mp4">下载长硬直示例视频</a>
</video>
  <figcaption>长硬直样本：原记录以较明显的失衡动作和较长的反击机会识别它。</figcaption>
</figure>

<figure>
<video controls preload="none" playsinline aria-label="《师父》短暂硬直反应的录屏示例">
  <source src="/media/sifu/short-stagger.mp4" type="video/mp4" />
  <a href="/media/sifu/short-stagger.mp4">下载短硬直示例视频</a>
</video>
  <figcaption>短硬直样本：关注停顿、恢复与玩家能够接入攻击的时机。</figcaption>
</figure>

“隐藏硬直条”是当时的猜测，尚未通过实验或源码确认。制作自己的原型时，可以先定义想要的硬直表现，再选择实现方式。

## 防御与闪避：相近目的，不同机会成本

为避免混用术语，本文按操作和结果定义三个概念：普通防御指持续防御状态；及时防御指接近命中时输入防御；打断型反制指成功应对后，攻击者出现足以接入反击的停顿。它们不替代游戏完整的官方招式术语。闪避在这里指录屏中用于避开攻击并寻找反击时机的防御行动。

原记录注意到，部分敌人的招式可以通过及时防御较早中断，而另一些连段则需要持续应对，直到末尾才更容易找到安全反击机会。这个差别会改变玩家的决策：

- 如果应对某一击就能结束敌人连段，玩家会关注尽早夺回主动权。
- 如果应对成功仍不足以中断后续攻击，玩家需要判断连段是否结束。
- 如果某次应对会显著推动架势变化，玩家还要比较立即安全与长期收益。

原稿把普通敌人与首领的区别概括为：前者更容易被打断，进攻可以更连续；后者往往要求更完整地识别连段，再利用较短窗口反击。这是对当时样本的体验归纳，不是所有敌人、难度和招式都遵守的统一规则。

原记录中，一些高亮攻击带来的架势压力较大，因此我更倾向于闪避。提示颜色与攻击属性的完整对应关系还需要继续确认。

## 进攻窗口为何会让连段收敛

获得反击机会后，玩家要在有限时间中做两件事：制造足够收益，并避免在敌人恢复时仍留在危险的动作后摇中。

原记录中，我经常使用“重击—推击—追击”这样的固定组合，因为它容易执行，也能提供稳定收益。它引出了一个设计问题：如果不同攻击只在动画观赏性上不同，而一套组合在多数情境中都足够好，玩家就容易反复使用同一套答案。

<figure>
<video controls preload="none" playsinline aria-label="《师父》重击、推击与追击组成的常用连段演示">
  <source src="/media/sifu/basic-combo.mp4" type="video/mp4" />
  <a href="/media/sifu/basic-combo.mp4">下载常用连段演示视频</a>
</video>
  <figcaption>原笔记中的常用连段样本。它说明个人策略的收敛，不证明这套组合在所有情况下最优。</figcaption>
</figure>

我的设计倾向是让战斗局势为不同进攻方式创造理由。例如，较短窗口适合快速确认伤害，较长窗口允许高承诺动作；靠近边界时，位移收益可能超过纯伤害；敌人的状态也可以改变控制与输出的相对价值。这些是从分析提出的原型方向，并非本文已经在《师父》中验证的机制清单。

我也想结合《鬼泣5》和《Hi-Fi Rush》，继续比较评分激励与招式选择的关系。是否会形成固定连段，需要更多玩家和场景来观察。

## 玩家硬直：什么时候允许重新作出选择

攻守交替不仅取决于敌人何时恢复，也取决于玩家受挫后还能做什么。两段原始录屏记录了一个值得研究的差异：攻击被应对后，继续攻击与重新防御似乎并不在同一时刻恢复可用。

<figure>
<video controls preload="none" playsinline aria-label="玩家攻击被应对后，尝试立即继续攻击的录屏">
  <source src="/media/sifu/attack-after-parry.mp4" type="video/mp4" />
  <a href="/media/sifu/attack-after-parry.mp4">下载继续攻击的对照视频</a>
</video>
  <figcaption>对照样本一：观察被反制后再次进攻的时机。</figcaption>
</figure>

<figure>
<video controls preload="none" playsinline aria-label="玩家攻击被应对后，尝试立即恢复防御的录屏">
  <source src="/media/sifu/guard-after-parry.mp4" type="video/mp4" />
  <a href="/media/sifu/guard-after-parry.mp4">下载恢复防御的对照视频</a>
</video>
  <figcaption>对照样本二：观察相近情境下恢复防御的时机。两段视频并非逐帧同步的控制实验。</figcaption>
</figure>

这个现象可以用“不同输入拥有不同取消条件”来解释，也可能与动作状态、输入缓冲或采样时机有关。仅凭录屏无法确定游戏采用了统一的打断优先级表。对自己的设计而言，值得借鉴的是结果：一次进攻失败可以迫使玩家让出进攻权，同时保留有限的防守选择。

当玩家架势被破坏时，原记录还观察到更显著的失衡、倒地或位移反应；受击方向与攻击种类会影响结果。

<figure>
<video controls preload="none" playsinline aria-label="推击造成架势破坏后的玩家位移反应">
  <source src="/media/sifu/push-structure-break.mp4" type="video/mp4" />
  <a href="/media/sifu/push-structure-break.mp4">下载推击破坏架势示例</a>
</video>
  <figcaption>推击样本：关注架势破坏后的位移与恢复过程。</figcaption>
</figure>

<figure>
<video controls preload="none" playsinline aria-label="扫腿造成架势破坏后的玩家倒地反应">
  <source src="/media/sifu/sweep-structure-break.mp4" type="video/mp4" />
  <a href="/media/sifu/sweep-structure-break.mp4">下载扫腿破坏架势示例</a>
</video>
  <figcaption>扫腿样本：相似的失败条件可以产生不同的空间与姿态后果。</figcaption>
</figure>

原记录对部分失衡时间有约一秒的粗略估计，也猜测过高亮攻击的架势倍率。这些值没有逐帧核对。后续需要测量失衡持续多久、哪些行动先恢复，以及玩家能否看懂下一次威胁。

## 敌人的行为流程

<figure>
  <img src="/media/sifu/enemy-flow.png" alt="原始笔记中的敌人行为观察模型" loading="lazy" />
  <figcaption>原图中的“大小硬直条”保留了早期分析思路；这里将其读作可见的短、长失衡状态。</figcaption>
</figure>

图中把敌人的可见行为概括为靠近玩家、选择连段、根据玩家状态使用衍生攻击、短暂停留，以及被反制后进入不同失衡状态。这个模型有助于讨论攻守转换，却不足以证明真实 AI 简单，也没有覆盖多人围攻、攻击名额分配、空间协调和完整的难度差异。

## 原型可以怎样尝试

如果制作一个强调一对一交换的原型，我会先实现少量明确规则：敌人提供可辨认的连段；玩家成功应对后获得有限反击窗口；敌人恢复前给出清楚反馈；玩家连续贪攻时失去主动权，但保留与失败程度相匹配的防御机会。

随后用同一组招式改变窗口长度、输入恢复顺序和攻击收益，记录玩家能否判断“现在是谁的回合”，以及是否总使用同一套进攻。测试时区分首次接触与熟练玩家，记录失败原因，并比较不同方案，而不是先把所有时间与数值调成看起来流畅。

这份分析让我更关注战斗中的选择：什么时候可以行动，行动能改变什么，失误后还剩哪些应对。上面的原型方案尚未做玩家测试，隐藏数值和取消规则也需要继续研究。