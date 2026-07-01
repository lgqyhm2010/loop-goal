# loop-goal skill — Design Spec

**Date:** 2026-05-17
**Status:** Implemented — shipped as a standalone skill repo
**Location:** `loop-goal/` (standalone skill repo; extracted from `ai-config/skills/loop-goal/`)

---

## Goal

A pure-discipline skill that activates when an agent is about to run a
**long-running task** — either a recurring **loop** or a run-until-done
**goal** — and turns three otherwise-self-disciplined behaviors into
enforced rules: checkpointing, context isolation, and explicit exit
conditions.

The skill writes no code and runs no commands. It only constrains *how*
the agent runs the task.

## Scope

- **In scope:** mode detection, a standard checkpoint file format, six
  enforced rules, loop/goal-specific guidance.
- **Out of scope:** the skill does NOT wrap or replace `/loop`,
  `ScheduleWakeup`, `CronCreate`, or `subagent-driven-development`. It
  references them; it does not take them over.

## Self-containment (no superpowers dependency)

The skill must work in any project, including ones without the
superpowers plugin installed.

- Heavy-work delegation uses the built-in `Agent` tool — not a
  superpowers feature.
- `/loop`, `ScheduleWakeup`, `CronCreate`, `/schedule` are harness
  built-ins — not superpowers features.
- `superpowers:subagent-driven-development` is listed in README only as
  an **optional companion**, never a dependency. Rule R2 fully
  describes subagent delegation on its own.
- The checkpoint path is the neutral `.loopgoal/state.json`, never a
  superpowers-specific path.

## Mode detection (skill entry, step 1)

| Mode | Trigger signals | End condition |
|------|-----------------|---------------|
| **LOOP** | time-driven, recurring — "every N…" / "每隔…", "keep monitoring" / "持续监控", an interval given, `/loop` | no intrinsic end; needs a written exit condition |
| **GOAL** | result-driven, run-until-done — "turn all tests green" / "把所有测试修绿", "until X" / "直到 X 为止" | a completion criterion exists |

## Trigger

Automatic (via the `description` field) plus explicit invocation.
Trigger phrases (English or Chinese): "loop", "goal", "keep running",
"run in a loop", "until X", "run autonomously" — or their Chinese
equivalents "持续做", "每隔", "循环跑", "直到…为止", "自主跑", "跑个 loop"
— and an explicit "use the loop-goal skill".

## Checkpoint file: `.loopgoal/state.json`

A single JSON state file is the recoverable source of truth. Git
commits hold history.

```json
{
  "mode": "goal",
  "objective": "Migrate the auth module to the new API",
  "exit_condition": "all auth/ tests pass and the old middleware is removed",
  "status": "in_progress",
  "iteration": 3,
  "phases": [
    {"name": "Inventory call sites", "status": "done"},
    {"name": "Refactor token refresh", "status": "in_progress"}
  ],
  "current": {
    "focus": "Refactor token refresh",
    "next_action": "Wire refresh.ts retry into the new client",
    "blockers": "The new client's default timeout is unknown"
  },
  "decisions": ["Dropped patching axios; standardize on the new SDK — reason: …"],
  "verify_cmd": "npm test -- auth/",
  "updated_at": "2026-05-17T15:00:00"
}
```

`decisions[]` exists to survive context compaction — the field
compaction is most likely to silently drop.

## Enforced rules

### Common (loop + goal)

- **R1 — Init.** Before starting, create `.loopgoal/state.json` and
  write the exit condition into `exit_condition` explicitly.
- **R2 — Context isolation.** Run each unit of work in a fresh
  subagent: a LOOP iteration or a GOAL phase. The subagent reads the
  checkpoint, advances one step, writes the checkpoint, returns a
  one-line summary. This is equivalent to clearing context every
  iteration — the main session never accumulates.
  - **Exception:** if a single iteration is genuinely lightweight (no
    file reads, no long command output — e.g. one `curl` for a status
    code), it may run in the main session directly.
- **R3 — Checkpoint order.** At every safe point: **write the state
  file first → then `git commit` → then continue / schedule next.**
  Order is fixed.
- **R4 — Resume.** At the start of every iteration/step: read the state
  file, run `verify_cmd`, reconcile against reality. If they disagree,
  reality wins — fix the file first.
- **R5 — Decision log.** Record every meaningful tradeoff in
  `decisions[]` as it is made.
- **R6 — Exit.** When the written exit condition is met: set `status`,
  stop scheduling. If `BLOCKED` and unrecoverable: stop and ask the
  user.

### LOOP-specific

- Safe point = each iteration. Iterations must be idempotent: read file
  → advance one step → write file.
- A fixed-interval loop must have its exit condition written into the
  loop prompt itself, or it never terminates.

### GOAL-specific

- No natural boundary — safe points must be carved manually: after each
  completed sub-goal, and before any irreversible operation.
- `verify_cmd` is mandatory.

## Skill file structure

```
loop-goal/
├── skills/
│   └── loop-goal/
│       ├── SKILL.md          # mode detection + R1–R6 + triggers
│       └── templates/
│           └── state.json    # checkpoint skeleton, copied by R1
├── .claude-plugin/
│   ├── plugin.json           # Claude Code plugin manifest
│   └── marketplace.json      # single-plugin marketplace
├── AGENTS.md                 # thin always-on pointer (Codex/Copilot)
├── .github/
│   └── copilot-instructions.md  # thin always-on pointer (Copilot)
├── README.md                 # what / why + per-tool install matrix
├── DESIGN.md                 # this document
└── docs/
    └── i18n/                 # README translations (10 languages)
```

## Multi-platform distribution

loop-goal is pure prose, so it ships as native, checked-in files — no hosted
service. The single canonical `skills/loop-goal/SKILL.md` feeds:

- the `skills` CLI for every agent (`npx skills add lgqyhm2010/loop-goal -a <agent>`);
- the Claude Code **plugin** (auto-discovered under `skills/`), installable via
  `/plugin marketplace add lgqyhm2010/loop-goal` → `/plugin install loop-goal@lgqyhm2010`.

`AGENTS.md` and `.github/copilot-instructions.md` are thin always-on pointers to
the skill (Codex and Copilot); they never duplicate the rules.

The skill lives under `skills/loop-goal/` (not the repo root) because the `skills`
CLI copies only `SKILL.md` for a root-level skill but the whole folder — including
`templates/` — for a `skills/<name>/` skill.

**Caveats.** The CLI's Codex global path (`~/.codex/skills/`) may differ from where
Codex loads global skills; project-level install or `AGENTS.md` is recommended.
Copilot's auto-loading of `.agents/skills/` is unverified, so
`.github/copilot-instructions.md` is the recommended always-on path there.

## Non-goals

- Not a runtime harness — does not execute the loop itself.
- Not a replacement for `/loop` or `/schedule`.
- No multi-version checkpoint history — git provides that.
