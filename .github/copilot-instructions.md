# Copilot instructions

For any **long-running task** — a recurring **loop** or a run-until-done
**goal** — follow the loop-goal discipline before starting.

**Triggers:** "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously".

**Six rules:**

- **R1** — init `.loopgoal/state.json` with an explicit `exit_condition`.
- **R2** — run each iteration/phase in a fresh subagent (context isolation).
- **R3** — checkpoint order: write `.loopgoal/state.json` → `git commit` → continue.
- **R4** — verify on resume: read the state file, run `verify_cmd`, reconcile.
- **R5** — log every decision/tradeoff in `decisions[]`.
- **R6** — exit cleanly when `exit_condition` is met; never spin silently.

Full rules: [`skills/loop-goal/SKILL.md`](../skills/loop-goal/SKILL.md).
