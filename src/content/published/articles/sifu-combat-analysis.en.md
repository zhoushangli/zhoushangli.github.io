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

I chose Sifu as a reference for one-on-one exchanges, using play sessions, recordings and diagrams to examine how defense creates counterattack opportunities.

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

The diagram shows how enemy stagger opens a player attack, enemy recovery restores enemy offense, and defense creates the next opening.

<figure>
  <img src="/media/sifu/combat-loop.png" alt="Offense and defense exchange cycle" loading="lazy" />
  <figcaption>Offense and defense exchange cycle. “Reduce the enemy structure bar” means moving the enemy closer to a structure break.</figcaption>
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

Health and structure are visible in the interface. Short and long stagger need to be judged from reactions and recovery time. I separate these two kinds of information:

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

I suspect stagger may depend on a hidden accumulated value, but this needs testing. For a new prototype, I would define the desired response before choosing an implementation.

## Defense and avoidance: similar goals, different costs

To keep the discussion consistent, I define terms by input and outcome. Ordinary guard means maintaining a defensive state. Timed guard means pressing defense close to impact. An interrupting counter means a successful response that pauses the attacker long enough to allow retaliation. These working definitions do not replace the game's complete official move terminology. Avoidance refers to the defensive evasive action used in the recordings to avoid a hit and seek an opening.

I observed that some enemy attacks can be interrupted relatively early through timed defense, while other sequences require continued responses until a safer opening near their end. This changes the player's decisions:

- If responding to one hit ends the enemy sequence, the player can focus on reclaiming initiative early.
- If a successful response does not stop subsequent hits, the player must judge whether the sequence is over.
- If a response substantially affects structure, the player must compare immediate safety with longer-term reward.

In the examples I observed, ordinary opponents were easier to interrupt, allowing more continuous offense. Bosses often required reading a whole sequence before taking a short opening. Specific enemies, moves and difficulties still need separate observation.

Some highlighted attacks in the recordings put more pressure on structure, which made me prefer avoidance. The full relationship between highlights and attack properties needs further checking.

## Why attack windows can make combos converge

After gaining an opening, the player must obtain enough reward while avoiding an unsafe recovery animation when the enemy becomes active again.

I frequently used a heavy attack, push and follow-up because the sequence was easy to execute and reliable. This made me wonder: if one combo works in most situations, when is another attack worth choosing?

<figure>
<video controls preload="none" playsinline aria-label="A frequently used heavy attack, push, and follow-up sequence in Sifu">
  <source src="/media/sifu/basic-combo.mp4" type="video/mp4" />
  <a href="/media/sifu/basic-combo.mp4">Download the frequently used combo example</a>
</video>
  <figcaption>This sample documents convergence in my own strategy. It does not prove the sequence is optimal in every situation.</figcaption>
</figure>

I want the situation to give different attacks a purpose. Short windows can favor quick damage, while longer ones allow slower moves. Near a boundary, displacement may matter more than damage; enemy state may also change the value of control. These are directions I would try in a prototype.

I would also like to compare scoring incentives and move choices in Devil May Cry 5 and Hi-Fi Rush. A broader set of players and situations would help test how fixed combos develop.

## Player stagger: when can the player choose again?

Exchanging initiative depends on both enemy recovery and the actions still available after the player's setback. Two recordings show an interesting difference: after an attack is countered, another attack and a renewed guard appear not to become available at the same moment.

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

Different cancellation conditions could explain this, though action state, input buffering or timing might also contribute. I would need more precise tests to distinguish them. The result interests me: a failed attack can give up offense while leaving a limited defensive choice.

When the player's structure breaks, I also see more pronounced staggering, knockdown, or displacement. Attack type and direction can produce different consequences.

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

Some stagger periods appear to last about one second, but I have not measured them frame by frame. Structure multipliers for highlighted attacks also need checking. Further work could compare stagger duration, action-recovery order and how clearly the next threat is signaled.

## Enemy behavior

<figure>
  <img src="/media/sifu/enemy-flow.png" alt="Observed enemy behavior" loading="lazy" />
  <figcaption>Enemy behavior. The “short/long stagger bars” represent a hypothesis about stagger.</figcaption>
</figure>

The enemy behavior flow can be expressed as follows:

```text
Offensive behavior:
approach player → choose a sequence → select a follow-up based on player state
               → pause → choose another sequence

Observed reactions:
successful defensive response or selected attacks → short stagger
more sustained loss-of-balance condition          → long stagger
```

The diagram describes visible stagger states and changes of initiative. Whether hidden meters control these states is still unclear. Group attacks, attack opportunities, spatial coordination and difficulty differences need further study.

## A possible prototype

For a prototype focused on one-on-one exchange, I would first implement a few clear rules: enemies provide recognizable sequences; a successful response creates a limited counterattack window; recovery has readable feedback; excessive attacking loses initiative; and the player retains defensive options appropriate to the severity of the failure.

I would then vary window length, action-recovery order, and attack rewards while holding the move set constant. I would record whether players can identify whose turn it is, and whether they always use the same offense. First-time and practiced players should be considered separately, with failure reasons and comparisons between alternatives recorded rather than tuning everything until it merely looks fluid.

I am interested in the choices combat allows: when to act, what an action changes and what remains possible after a mistake. A prototype could test these ideas while I investigate hidden values and cancellation rules.