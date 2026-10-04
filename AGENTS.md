# AGENTS.md

This repository IS the `loop-goal` skill. When you (any agent) are about to run a
**long-running task** — one that repeats on an interval (a **loop**) or runs
until a completion criterion is met (a **goal**) — follow the loop-goal
discipline before you start.

**Triggers:** "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously" — or the Chinese equivalents "持续做", "每隔", "循环跑",
"直到…为止", "自主跑", "跑个 loop".

**The six rules (summary):**

- **R1 — Init.** Create `.loopgoal/state.json` with an explicit `exit_condition`.
- **R2 — Context isolation.** Use a host-native subagent when available; otherwise checkpoint short serial phases.
- **R3 — Checkpoint order.** Write state → commit only task-owned paths when Git/permissions allow → then continue.
- **R4 — Resume.** Read state and run `verify_cmd` or `verify_observation` before each step.
- **R5 — Decision log.** Append every tradeoff to `decisions[]`.
- **R6 — Exit.** Stop cleanly when `exit_condition` is met; never spin silently.

Full rules, checkpoint format, and loop/goal specifics:
**[`skills/loop-goal/SKILL.md`](skills/loop-goal/SKILL.md)**.

*Copying this file into your own repo? Repoint the link above to wherever you
installed the skill (e.g. `.agents/skills/loop-goal/SKILL.md`), or drop it if you
rely on the skill's own auto-trigger.*

The host-capability and permission boundaries in the full skill take precedence over tool-specific examples. Missing Git, shell, or subagents must be recorded; never broaden permissions or include unrelated staged changes.
