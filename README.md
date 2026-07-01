**English** · [简体中文](docs/i18n/README.zh-Hans.md) · [繁體中文](docs/i18n/README.zh-Hant.md) · [日本語](docs/i18n/README.ja.md) · [Español](docs/i18n/README.es.md) · [Français](docs/i18n/README.fr.md) · [العربية](docs/i18n/README.ar.md) · [हिन्दी](docs/i18n/README.hi.md) · [Português (BR)](docs/i18n/README.pt-BR.md) · [Русский](docs/i18n/README.ru.md) · [বাংলা](docs/i18n/README.bn.md)

# loop-goal

A discipline skill for running **long tasks** reliably — tasks that
either repeat on a schedule (**loops**) or run until a goal is met
(**goals**).

## Install

Add it with the [`skills`](https://github.com/vercel-labs/skills) CLI —
no clone, no manual copy:

```bash
# Into the current project → .claude/skills/
npx skills add lgqyhm2010/loop-goal

# For every project → ~/.claude/skills/
npx skills add lgqyhm2010/loop-goal -g
```

`skills` finds the `SKILL.md` at the repo root and drops it (plus
`templates/`) into your skills directory. Add `-a claude-code -y` to
install non-interactively.

Prefer to do it by hand? Copy `SKILL.md` and `templates/` into
`.claude/skills/loop-goal/`.

Once installed, just describe a looping or run-until-done task — the
skill triggers on its own (see [When it triggers](#when-it-triggers)).

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

Phrases like "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously" — or their Chinese equivalents "持续做", "每隔", "循环跑",
"直到…为止", "自主跑", "跑个 loop" — or an explicit "use the loop-goal skill".

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
