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
- **R2 — Context isolation.** Run each iteration/phase in a fresh subagent.
- **R3 — Checkpoint order.** Write state → `git commit` → then continue.
- **R4 — Resume.** Read the state file and run `verify_cmd` before each step.
- **R5 — Decision log.** Append every tradeoff to `decisions[]`.
- **R6 — Exit.** Stop cleanly when `exit_condition` is met; never spin silently.

Full rules, checkpoint format, and loop/goal specifics:
**[`skills/loop-goal/SKILL.md`](skills/loop-goal/SKILL.md)**.

*Copying this file into your own repo? Repoint the link above to wherever you
installed the skill (e.g. `.agents/skills/loop-goal/SKILL.md`), or drop it if you
rely on the skill's own auto-trigger.*
