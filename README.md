# loop-goal

A discipline skill for running **long tasks** reliably — tasks that
either repeat on a schedule (**loops**) or run until a goal is met
(**goals**).

## The problem

Long-running agent tasks fail in three quiet ways:

1. **Lost progress** — conversation context gets compacted and the
   agent forgets what it already did.
2. **Polluted context** — tool output piles up across iterations,
   degrading reasoning over a long run.
3. **No exit** — a loop with no written stop condition runs forever.

The fixes are well known (checkpoint to a file, isolate context per
iteration, write the exit condition down). The trouble is they rely on
the agent *remembering* to do them — and discipline drifts over a long
run. This skill turns the three fixes into enforced rules.

## What it does

When invoked, the skill:

1. **Detects the mode** — LOOP (time-driven, recurring) vs GOAL
   (result-driven, run-until-done).
2. **Mandates a checkpoint file** — `.loopgoal/state.json` holds the
   single recoverable state; git commits hold history.
3. **Enforces six rules** — init with an explicit exit condition, run
   each iteration in a fresh subagent (context isolation), checkpoint
   in a fixed order, verify on resume, log decisions, exit cleanly.

It is **pure discipline**: it writes no code, runs no commands, and
does not wrap `/loop` or `/schedule` — it constrains *how* you run them.

## When it triggers

Phrases like "持续做", "每隔", "循环跑", "直到…为止", "自主跑",
"跑个 loop", "loop", "goal", or an explicit "用 loop-goal skill".

## Self-contained

Works in any project. It depends only on built-in tools (`Agent`, git)
and harness mechanisms (`/loop`, `ScheduleWakeup`). The superpowers
plugin is an optional companion, never a requirement.

## Files

- `SKILL.md` — the skill itself: mode detection, the checkpoint format,
  the six rules.
- `DESIGN.md` — design rationale and decisions.
- `templates/state.json` — the checkpoint skeleton, copied into a
  project by rule R1.
