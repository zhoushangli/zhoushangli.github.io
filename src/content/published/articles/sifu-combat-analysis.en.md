---
contentId: sifu-combat-analysis
lang: en
section: articles
title: "Sifu Combat Analysis"
description: "Using recordings to examine defense, stagger and counterattack opportunities in one-on-one Sifu combat."
category: gameplay
tags: [Combat Design, Core Loops, Action Games, Game Analysis]
draft: false
---

## Why Sifu?

For a project concept centered on close confrontation, I wanted the player and enemy to exchange offensive and defensive initiative quickly. Adding attack, guard, and avoidance actions would not be enough: those actions needed to form a loop that players could understand, learn, and repeatedly vary.

I chose Sifu as a reference for one-on-one exchanges. These notes use my play records, clips and diagrams. “Window,” “short stagger” and “long stagger” describe visible behavior; the underlying values and state machine remain unclear.

## The core loop: earn an opportunity, then convert it

I separate two nested loops:

1. **The objective loop:** reduce an enemy's health or push its structure toward a break, obtain a takedown opportunity, then engage another target.
2. **The exchange loop:** respond to an enemy's offense, earn a counterattack opportunity through defense or avoidance, deal damage during that opportunity, then return to responding.

```text
Enemy attacks
  → Player reads the attack and defends or avoids
  → A counterattack opportunity appears
  → Player attacks and extends or increases the reward
  → Enemy recovers its ability to respond
  → Initiative changes again
```

The original Chinese diagram describes the same exchange: enemy stagger leads to player offense; enemy recovery leads to enemy offense; the player's defensive response creates the next opening. Its early wording about “reducing the structure bar” is interpreted here as advancing toward a structure break, not as a definition of the UI's numerical direction.

<figure>
  <img src="/media/sifu/combat-loop.png" alt="Original diagram of the offense/defense exchange cycle" loading="lazy" />
  <figcaption>Original analysis diagram. Its earlier “reduce the enemy structure bar” wording is read here as advancing toward a structure break, not as a definition of the UI&#x27;s numerical direction.</figcaption>
</figure>

<figure>
<video controls preload="none" playsinline aria-label="Recording of the player and enemy exchanging initiative in Sifu">
  <source src="/media/sifu/turn-exchange.mp4" type="video/mp4" />
  <a href="/media/sifu/turn-exchange.mp4">Download the initiative-exchange recording</a>
</video>
  <figcaption>This clip illustrates the exchange loop. It does not include the full takedown-and-target-change sequence.</figcaption>
</figure>

In this model, defense is not empty time before offense resumes. It determines when the player regains initiative and how long the next attack sequence can remain safe.

## Health, structure and stagger

The initial draft used several “bars” to explain combat: health, structure, and hypothetical hidden accumulations for short and long stagger. I now separate the first two from the latter two:

| Subject | What the image and controls can reveal | What they do not directly establish |
| --- | --- | --- |
| Health | Changes in the health display after damage | The complete damage formula and all modifiers |
| Structure | Display changes and reactions to guarding, hits, and breaks | Each attack's internal increment and recovery rules |
| Short stagger | A brief enemy interruption and a limited attack opportunity | Whether a separate meter exists, or actions and states control it directly |
| Long stagger | A more obvious and sustained loss of balance, such as holding the head | Whether an accumulating hidden resource triggers it, and how that resource decays |

<figure>
<video controls preload="none" playsinline aria-label="Recording of a longer stagger reaction in Sifu">
  <source src="/media/sifu/long-stagger.mp4" type="video/mp4" />
  <a href="/media/sifu/long-stagger.mp4">Download the longer-stagger example</a>
</video>
  <figcaption>The longer-stagger sample was identified through a more pronounced reaction and a longer opportunity to respond.</figcaption>
</figure>

<figure>
<video controls preload="none" playsinline aria-label="Recording of a brief stagger reaction in Sifu">
  <source src="/media/sifu/short-stagger.mp4" type="video/mp4" />
  <a href="/media/sifu/short-stagger.mp4">Download the brief-stagger example</a>
</video>
  <figcaption>The brief-stagger sample draws attention to interruption, recovery, and the moment the player can connect an attack.</figcaption>
</figure>

A hidden stagger meter was an early hypothesis, still unconfirmed by experiments or source code. For a new prototype, I would define the desired response before choosing an implementation.

## Defense and avoidance: similar goals, different costs

To keep the discussion consistent, I define terms by input and outcome. Ordinary guard means maintaining a defensive state. Timed guard means pressing defense close to impact. An interrupting counter means a successful response that pauses the attacker long enough to allow retaliation. These working definitions do not replace the game's complete official move terminology. Avoidance refers to the defensive evasive action used in the recordings to avoid a hit and seek an opening.

The original notes observe that some enemy attacks can be interrupted relatively early through timed defense, while other sequences require continued responses until a safer opening near their end. This changes the player's decisions:

- If responding to one hit ends the enemy sequence, the player can focus on reclaiming initiative early.
- If a successful response does not stop subsequent hits, the player must judge whether the sequence is over.
- If a response substantially affects structure, the player must compare immediate safety with longer-term reward.

The draft characterizes ordinary opponents as easier to interrupt and bosses as demanding more complete sequence recognition before a short retaliation. That is an experiential summary of the recorded sample, not a universal rule across enemies, difficulties, and moves.

Some highlighted attacks in the recordings put more pressure on structure, which made me prefer avoidance. The full relationship between highlights and attack properties needs further checking.

## Why attack windows can make combos converge

After gaining an opening, the player must obtain enough reward while avoiding an unsafe recovery animation when the enemy becomes active again.

In my original notes, I repeatedly used a heavy-attack, push, and follow-up sequence because it was easy to execute and produced dependable results. This raises a design question: if attacks mainly differ in visual spectacle, and one sequence is good enough in most situations, players have little reason to choose another answer.

<figure>
<video controls preload="none" playsinline aria-label="A frequently used heavy attack, push, and follow-up sequence in Sifu">
  <source src="/media/sifu/basic-combo.mp4" type="video/mp4" />
  <a href="/media/sifu/basic-combo.mp4">Download the frequently used combo example</a>
</video>
  <figcaption>This sample documents convergence in my own strategy. It does not prove the sequence is optimal in every situation.</figcaption>
</figure>

My design preference is to let the situation create reasons for different offensive choices. A short window might favor quick confirmed damage, while a longer one permits a higher-commitment action. Near a boundary, displacement might be more valuable than raw damage. An enemy's state might change the relative value of control and damage. These are prototype directions suggested by the analysis, not a list of systems verified in Sifu by this article.

I would also like to compare scoring incentives and move choices in Devil May Cry 5 and Hi-Fi Rush. A broader set of players and situations would help test how fixed combos develop.

## Player stagger: when can the player choose again?

Exchanging initiative depends on both enemy recovery and the actions still available after the player's setback. Two original recordings note an interesting difference: after an attack is countered, another attack and a renewed guard appear not to become available at the same moment.

<figure>
<video controls preload="none" playsinline aria-label="Attempting another attack immediately after the player's offense is countered">
  <source src="/media/sifu/attack-after-parry.mp4" type="video/mp4" />
  <a href="/media/sifu/attack-after-parry.mp4">Download the repeated-attack comparison</a>
</video>
  <figcaption>Comparison one: observe when offense becomes available after a counter.</figcaption>
</figure>

<figure>
<video controls preload="none" playsinline aria-label="Attempting to resume guarding immediately after the player's offense is countered">
  <source src="/media/sifu/guard-after-parry.mp4" type="video/mp4" />
  <a href="/media/sifu/guard-after-parry.mp4">Download the guard-recovery comparison</a>
</video>
  <figcaption>Comparison two: observe guard recovery in a similar situation. The two recordings are not synchronized, frame-controlled trials.</figcaption>
</figure>

Different cancellation conditions for different inputs could explain the observation. Action state, input buffering, or sampling timing might also contribute. The clips do not establish that the game implements one general interruption-priority table. For an original design, the interesting result is that a failed attack can surrender offensive initiative while leaving a limited defensive choice.

When the player's structure breaks, the notes also record more pronounced staggering, knockdown, or displacement. Attack type and direction can produce different consequences.

<figure>
<video controls preload="none" playsinline aria-label="Player displacement following a structure break caused by a push">
  <source src="/media/sifu/push-structure-break.mp4" type="video/mp4" />
  <a href="/media/sifu/push-structure-break.mp4">Download the push-induced structure-break example</a>
</video>
  <figcaption>The push sample emphasizes displacement and the following recovery.</figcaption>
</figure>

<figure>
<video controls preload="none" playsinline aria-label="Player knockdown following a structure break caused by a sweep">
  <source src="/media/sifu/sweep-structure-break.mp4" type="video/mp4" />
  <a href="/media/sifu/sweep-structure-break.mp4">Download the sweep-induced structure-break example</a>
</video>
  <figcaption>The sweep sample shows how a similar failure condition can have a different spatial and postural consequence.</figcaption>
</figure>

The notes roughly estimated some stagger periods at one second and suggested a structure multiplier for highlighted attacks. Neither was checked frame by frame. Further measurements should cover stagger duration, action-recovery order and how clearly the next threat is signaled.

## Enemy behavior

<figure>
  <img src="/media/sifu/enemy-flow.png" alt="Enemy behavior model recorded in the original notes" loading="lazy" />
  <figcaption>The original diagram&#x27;s “short/long stagger bars” preserve an early analysis idea; they are read here as visible short and long loss-of-balance states.</figcaption>
</figure>

The original enemy-flow diagram can be expressed in English as follows:

```text
Offensive behavior:
approach player → choose a sequence → select a follow-up based on player state
               → pause → choose another sequence

Observed reactions:
successful defensive response or selected attacks → short stagger
more sustained loss-of-balance condition          → long stagger
```

The diagram's original “short/long stagger bars” preserve an early hypothesis; I read them here as visible stagger states. The model helps discuss changes of initiative. It does not establish that the real AI is simple, and does not cover group attacks, allocation of attack opportunities, spatial coordination, or all difficulty differences.

## A possible prototype

For a prototype focused on one-on-one exchange, I would first implement a few clear rules: enemies provide recognizable sequences; a successful response creates a limited counterattack window; recovery has readable feedback; excessive attacking loses initiative; and the player retains defensive options appropriate to the severity of the failure.

I would then vary window length, action-recovery order, and attack rewards while holding the move set constant. I would record whether players can identify whose turn it is, and whether they always use the same offense. First-time and practiced players should be considered separately, with failure reasons and comparisons between alternatives recorded rather than tuning everything until it merely looks fluid.

This analysis made me focus on the choices combat allows: when to act, what an action changes and what remains possible after a mistake. The prototype has not been playtested; hidden values and cancellation rules still need further study.