# Copilot instructions

For any **long-running task** — a recurring **loop** or a run-until-done
**goal** — follow the loop-goal discipline before starting.

**Triggers:** "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously".

**Six rules:**

- **R1** — init `.loopgoal/state.json` with an explicit `exit_condition`.
- **R2** — use a host-native subagent when available; otherwise checkpoint short serial phases.
- **R3** — checkpoint order: write state → commit only task-owned paths when Git/permissions allow → then continue.
- **R4** — verify on resume: read the state file, run `verify_cmd` or `verify_observation`, reconcile.
- **R5** — log every decision/tradeoff in `decisions[]`.
- **R6** — exit cleanly when `exit_condition` is met; never spin silently.

Full rules: [`skills/loop-goal/SKILL.md`](../skills/loop-goal/SKILL.md).

*Copying this file into your own repo? Repoint the link above to wherever you
installed the skill (e.g. `.agents/skills/loop-goal/SKILL.md`).*

The host-capability and permission boundaries in the full skill take precedence over tool-specific examples. Missing Git, shell, or subagents must be recorded; never broaden permissions or include unrelated staged changes.
