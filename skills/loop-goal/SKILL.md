---
name: loop-goal
description: Discipline rules for long-running agent tasks — recurring loops and run-until-done goals. Use when about to run a task that repeats on an interval or runs until a completion criterion is met. Trigger phrases (English or Chinese) — "loop", "goal", "keep running", "run in a loop", "until X", "run autonomously", "持续做", "每隔", "循环跑", "直到…为止", "自主跑", "跑个 loop", or an explicit "use the loop-goal skill". Enforces three things that otherwise rely on agent self-discipline: (1) checkpointing recoverable state to a single `.loopgoal/state.json` file plus git commits, (2) running each iteration/phase in a fresh subagent so the main session's context never accumulates, (3) an explicit, written exit condition. Auto-detects LOOP mode (time-driven, recurring, no intrinsic end) vs GOAL mode (result-driven, has a completion criterion). Pure discipline — writes no code, runs no commands, does not wrap /loop or /schedule.
---

# loop-goal

Discipline for running long tasks without losing progress or polluting context.

A long-running task — one that repeats, or one that runs until done —
has three failure modes that quietly ruin it:

- **Progress is lost** when conversation context is compacted.
- **Context is polluted** by accumulated tool output across iterations.
- **The loop never ends** because no exit condition was written down.

This skill turns the three fixes into rules you MUST follow, instead of
habits you might forget halfway through a long run.

## Step 1 — Detect the mode

Decide LOOP or GOAL before anything else.

| Mode | Signals | End condition |
|------|---------|---------------|
| **LOOP** | time-driven, recurring — "every N…" / "每隔…", "keep monitoring" / "持续监控", an interval given, `/loop` | none intrinsic — you MUST write one |
| **GOAL** | result-driven, run-until-done — "turn all tests green" / "把所有测试修绿", "until X" / "直到 X 为止" | a completion criterion already exists |

State the detected mode out loud, then proceed.

## Step 2 — The checkpoint file

`.loopgoal/state.json` is the single recoverable source of truth. Git
commits hold history. Copy the skeleton from `templates/state.json`.

```json
{
  "mode": "goal",
  "objective": "one line — what this task achieves",
  "exit_condition": "the explicit, testable condition that ends the task",
  "status": "in_progress",
  "iteration": 0,
  "phases": [{"name": "...", "status": "todo"}],
  "current": {"focus": "...", "next_action": "...", "blockers": ""},
  "decisions": [],
  "verify_cmd": "command that checks the current state is real",
  "updated_at": "2026-05-17T15:00:00"
}
```

`decisions[]` is not optional bookkeeping — it is the field context
compaction is most likely to silently drop. Record tradeoffs there as
you make them.

## Host capabilities and permission boundaries

Before a phase, inspect the host's available capabilities and record them in the checkpoint.
Use the host-native subagent tool (for example `Agent` or `spawn_agent`), never assume one name exists.
If subagents are unavailable, use short serial phases and persist a checkpoint between them; record this degraded mode.
If the workspace is not a Git repository, is read-only, or commits are not authorized, skip commits and retain the checkpoint in an authorized writable location. If no such location exists, stop and request a supported checkpoint destination.
For Git checkpoints, stage and commit only task-owned paths. Never run a blanket `git add .` or include pre-existing staged changes; isolate the checkpoint commit or stop if the index cannot be safely separated.
If shell commands are unavailable or the task is read-only, use a named, repeatable read-only observation in `verify_observation` instead of `verify_cmd`. Stop when neither verification route is available. Missing capabilities never justify expanded permissions, external actions, or fabricated success.
The invariants are explicit exit criteria, recoverable state, verified progress, and bounded context; the capability adaptations above take precedence over tool-specific examples below.

## The six rules

Follow all six invariants, using the capability adaptations above.

- **R1 — Init.** Before starting, create `.loopgoal/state.json` from the
  template and write `exit_condition` explicitly. If you cannot state
  the exit condition, stop and ask the user — a loop without one never
  ends.

- **R2 — Context isolation.** Run each unit of work — a LOOP iteration
  or a GOAL phase — in a **fresh subagent** using the host-native tool when available. The
  subagent reads the checkpoint, advances **one step**, writes the
  checkpoint, and returns a one-line summary. This is equivalent to
  clearing context every iteration: the main session stays a thin
  coordinator and never accumulates.
  - *Exception:* if a single iteration is genuinely lightweight — no
    file reads, no long command output (e.g. one `curl` for a status
    code) — run it in the main session directly. Subagent overhead is
    not worth it for trivial work.

- **R3 — Checkpoint order.** At every safe point, in this exact order:
  1. write `.loopgoal/state.json`
  2. commit only task-owned paths when authorized and Git is available; otherwise record why the checkpoint is uncommitted
  3. then continue, or schedule the next iteration
  Never reorder. The file must be current before the commit, and both
  before you move on — so a context loss right after still recovers.

- **R4 — Resume.** At the start of every iteration/step: read
  `.loopgoal/state.json`, run `verify_cmd` or perform `verify_observation`, and reconcile it against
  reality. The file is "what I last believed", not fact. If they
  disagree, reality wins — fix the file first, then proceed.

- **R5 — Decision log.** The moment you make a meaningful tradeoff,
  append it to `decisions[]` with its reason. Do not rely on
  conversation memory to carry decisions across iterations.

- **R6 — Exit.** When `exit_condition` is met: set `status` to `done`,
  write the file, commit, and **stop scheduling**. If you hit a blocker
  you cannot resolve: set `status` to `blocked`, record it in
  `current.blockers`, and stop to ask the user. Never spin silently.

## LOOP-specific

- A safe point is **each iteration**. Iterations must be idempotent:
  read file → advance one step → write file. Never depend on "I
  remember what I did last round."
- A **fixed-interval** loop (cron / `/loop 5m`) does not stop itself.
  Its `exit_condition` MUST also be written into the loop prompt, or it
  runs forever.
- A **dynamic** loop (`ScheduleWakeup`, self-paced) ends naturally: when
  `exit_condition` is met, simply do not schedule the next wakeup.

## GOAL-specific

- A goal has **no natural boundary**. You MUST carve safe points
  manually: after each completed sub-goal, and before any irreversible
  operation (bulk writes, long jobs, commits to shared branches).
- A nonempty `verify_cmd` or `verify_observation` is **mandatory** — a goal must have a repeatable check.
- Break the goal into `phases[]` up front. Each phase is one R2 unit of
  work.

## Optional companions

These improve results but are NOT required — this skill is fully
self-contained:

- `superpowers:subagent-driven-development` — a heavier per-task
  subagent + review workflow, compatible with R2.
- `/loop`, `/schedule` — harness mechanisms for actually scheduling the
  iterations this skill disciplines.
