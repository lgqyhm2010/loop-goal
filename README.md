**English** · [简体中文](docs/i18n/README.zh-Hans.md) · [繁體中文](docs/i18n/README.zh-Hant.md) · [日本語](docs/i18n/README.ja.md) · [Español](docs/i18n/README.es.md) · [Français](docs/i18n/README.fr.md) · [العربية](docs/i18n/README.ar.md) · [हिन्दी](docs/i18n/README.hi.md) · [Português (BR)](docs/i18n/README.pt-BR.md) · [Русский](docs/i18n/README.ru.md) · [বাংলা](docs/i18n/README.bn.md)

# loop-goal

A discipline skill for running **long tasks** reliably — tasks that
either repeat on a schedule (**loops**) or run until a goal is met
(**goals**).

## Install

loop-goal is a single `SKILL.md` under `skills/loop-goal/`. Pick your tool below —
it installs into Claude Code, Codex, and GitHub Copilot.

### Quick install (all three at once)

The [`skills`](https://github.com/vercel-labs/skills) CLI installs the skill —
no clone, no manual copy:

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

Drop any `-a …` target you don't need. Add `-g` to install for every project
instead of just the current one.

### Claude Code

- **As a skill:** `npx skills add lgqyhm2010/loop-goal -a claude-code` (`-g` for global)
- **As a plugin:** in Claude Code, run `/plugin marketplace add lgqyhm2010/loop-goal`
  then `/plugin install loop-goal@lgqyhm2010`
- **Manually:** copy `skills/loop-goal/` into `.claude/skills/`

### OpenAI Codex

- **As a skill:** `npx skills add lgqyhm2010/loop-goal -a codex` — installs into
  `.agents/skills/loop-goal/`. Project-level install is recommended.
- **Always-on:** copy the pointer from [`AGENTS.md`](AGENTS.md) into your own
  repo's `AGENTS.md` (or `~/.codex/AGENTS.md`) so the discipline is always loaded.

### GitHub Copilot

- **As a skill:** `npx skills add lgqyhm2010/loop-goal -a github-copilot` — installs
  into `.agents/skills/loop-goal/`.
- **Always-on (recommended):** copy the pointer from
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md) into your own
  repo's `.github/copilot-instructions.md`.

> **Notes.** For Codex, prefer a project-level install or the `AGENTS.md` route —
> the CLI's global (`-g`) path (`~/.codex/skills/`) may not match where Codex reads
> global skills. For Copilot, the `.github/copilot-instructions.md` route is the most
> reliable way to keep the discipline always-on.

Once installed, just describe a looping or run-until-done task — the skill
triggers on its own (see [When it triggers](#when-it-triggers)).

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

Works across hosts with the capability adaptations in the [skill](skills/loop-goal/SKILL.md). Subagents and Git are used when available and authorized; read-only observations can replace shell verification. It does not require a specific tool name or scheduler. The superpowers plugin is an optional companion, never a requirement.

## Files

- `skills/loop-goal/SKILL.md` — the skill itself: mode detection, the checkpoint
  format, the six rules.
- `skills/loop-goal/templates/state.json` — the checkpoint skeleton, copied into
  a project by rule R1.
- `.claude-plugin/` — Claude Code plugin + marketplace manifests.
- `AGENTS.md`, `.github/copilot-instructions.md` — thin always-on pointers for
  Codex and Copilot.
- `DESIGN.md` — design rationale and decisions.
