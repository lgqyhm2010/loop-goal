# Copilot instructions

For any **long-running task** — a recurring **loop** or a run-until-done
**goal** — follow the loop-goal discipline before starting.

**Triggers:** "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously".

**Seven rules:**

- **R1** — init `.loopgoal/state.json` with an explicit `exit_condition`.
- **R2** — run each iteration/phase in a fresh subagent (context isolation).
- **R3** — checkpoint order: write `.loopgoal/state.json` → `git commit` → continue.
- **R4** — verify on resume: read the state file, run `verify_cmd`, reconcile.
- **R5** — log every decision/tradeoff in `decisions[]`.
- **R6** — exit cleanly when `exit_condition` is met; never spin silently.
- **R7** — scale-out: when a phase splits into ≥4 independent, parallel units, fan out via the `Workflow` tool instead of serial R2 subagents.

Full rules: [`skills/loop-goal/SKILL.md`](../skills/loop-goal/SKILL.md).

*Copying this file into your own repo? Repoint the link above to wherever you
installed the skill (e.g. `.agents/skills/loop-goal/SKILL.md`).*
