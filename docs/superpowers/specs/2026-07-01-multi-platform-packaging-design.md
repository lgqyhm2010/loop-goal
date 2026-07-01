# loop-goal — Multi-Platform Packaging Design Spec

**Date:** 2026-07-01
**Status:** Approved (design) — pending spec review, then implementation plan
**Branch:** `feat/multi-platform-packaging`
**Repo:** `lgqyhm2010/loop-goal` (`https://github.com/lgqyhm2010/loop-goal.git`)

---

## Goal

Make the `loop-goal` discipline skill a first-class, installable citizen of the
extension/"plugin" systems of **Claude Code**, **OpenAI Codex**, and **GitHub
Copilot** — using each tool's native, checked-in-files mechanism (no hosted
services). Along the way, fix a latent distribution bug where the skill's
`templates/` folder is not delivered by the `skills` CLI.

loop-goal is pure prose (no code, no MCP server, no app). The right altitude is
therefore native files committed to the repo, not marketplace/hosted packaging.

## Background: where we are today

- The skill ships as a single root `SKILL.md` + `templates/state.json`.
- It is distributed via the `vercel-labs/skills` CLI: `npx skills add lgqyhm2010/loop-goal`.
- Research (2026-07-01) confirmed all three target tools are already first-class
  `-a` targets of that CLI: `claude-code`, `codex`, `github-copilot`.

### Latent bug discovered during research

The `skills` CLI treats a **root-level** `SKILL.md` specially: it copies **only
`SKILL.md`**, deliberately excluding sibling files, to avoid dumping unrelated
repo files. For a skill placed in a **subdirectory** (`skills/<name>/`), it
copies the **whole folder** (including `templates/`).

Consequence: `npx skills add lgqyhm2010/loop-goal` today installs `SKILL.md`
**without** `templates/state.json`, yet rule R1 instructs the installed skill to
"copy the skeleton from `templates/state.json`." The current README's claim that
the CLI drops the skill "(plus `templates/`)" is inaccurate for the root layout.

**Fix:** move the skill into `skills/loop-goal/`, so the CLI copies the whole
folder — which also happens to be the standard Claude Code plugin skills layout.

## Scope

**In scope**
- Relocate the canonical skill to `skills/loop-goal/` (single source of truth).
- Claude Code **plugin** packaging: `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`.
- Always-on pointer files: root `AGENTS.md` (Codex + Copilot + other AGENTS.md-aware tools) and `.github/copilot-instructions.md` (Copilot's documented path).
- Docs: rewrite `README.md` install section as a per-tool matrix; update all 11 i18n READMEs; update `DESIGN.md`.

**Out of scope** (explicitly declined)
- Codex Plugin Directory publishing.
- A hosted GitHub Copilot Extension (GitHub App + HTTPS backend).
- Any MCP server, hook, or code — loop-goal remains pure prose.

## Final repository layout

```
loop-goal/
├── .claude-plugin/
│   ├── plugin.json                 # Claude Code plugin manifest
│   └── marketplace.json            # single-plugin marketplace (repo = marketplace)
├── skills/
│   └── loop-goal/
│       ├── SKILL.md                # CANONICAL skill (moved from repo root)
│       └── templates/
│           └── state.json          # moved from repo root; now travels with the skill
├── AGENTS.md                       # thin always-on pointer (Codex/Copilot/others)
├── .github/
│   ├── copilot-instructions.md     # thin always-on pointer (Copilot documented path)
│   └── workflows/                  # unchanged
│       ├── claude.yml
│       └── claude-code-review.yml
├── README.md                       # per-tool install matrix (rewritten)
├── DESIGN.md                       # updated file-structure + distribution section
└── docs/
    ├── i18n/                       # 11 translated READMEs (install sections updated)
    └── superpowers/specs/          # this spec
```

One `SKILL.md` feeds every consumer:
- `skills` CLI for all agents (`skills/loop-goal/` → whole folder copied, templates included).
- Claude Code plugin (auto-discovered under `skills/`).
- The single source of the *full* rule text that the pointer files reference.

## Single source of truth & drift avoidance

- `skills/loop-goal/SKILL.md` holds the **complete** rules (mode detection,
  checkpoint format, R1–R6, loop/goal specifics).
- `AGENTS.md` and `.github/copilot-instructions.md` are **thin pointers** (~15–25
  lines): trigger phrases, one-paragraph gist, the six rule names, and an
  explicit "full rules → `skills/loop-goal/SKILL.md`". They intentionally do NOT
  duplicate the full skill. Rationale: (a) always-on instruction files should be
  short to keep every request's context lean; (b) short + stable pointers rarely
  drift; (c) the skill stays the one place to edit the actual rules.

## Per-tool packaging detail

### Claude Code
Three install paths, all documented:
1. **Skill via CLI:** `npx skills add lgqyhm2010/loop-goal -a claude-code` (`-g` global, `-y` non-interactive).
2. **Plugin via marketplace:** `/plugin marketplace add lgqyhm2010/loop-goal` then `/plugin install loop-goal@lgqyhm2010`.
3. **Manual:** copy `skills/loop-goal/` into `.claude/skills/`.

### OpenAI Codex
1. **Skill via CLI:** `npx skills add lgqyhm2010/loop-goal -a codex` → installs to
   `.agents/skills/loop-goal/` (project). Recommend **project-level** install.
2. **Always-on:** paste the `AGENTS.md` pointer into the user's own
   `AGENTS.md` (repo root) or `~/.codex/AGENTS.md`.

### GitHub Copilot
1. **Skill via CLI:** `npx skills add lgqyhm2010/loop-goal -a github-copilot` →
   `.agents/skills/loop-goal/` (project).
2. **Always-on (recommended):** paste into `.github/copilot-instructions.md`
   (Copilot's guaranteed auto-load path) or `AGENTS.md`.

### One-liner for all three
`npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y`

## Known caveats (documented honestly)

- **Codex global (`-g`):** the CLI writes global skills to `~/.codex/skills/`,
  but Codex may load global skills from `~/.agents/skills/`. Docs will recommend
  project-level install (or the `AGENTS.md` route) for Codex and note the
  global-path uncertainty rather than assert `-g` works.
- **Copilot skill auto-fire:** whether Copilot reliably auto-triggers a
  `.agents/skills/…/SKILL.md` as a discipline rule set is not documented. That is
  why `.github/copilot-instructions.md` is presented as the recommended Copilot
  path for guaranteed always-on behavior.
- **Preview/churn:** Codex Skills + Plugin Directory and Copilot nested AGENTS.md
  are young/preview features; we rely only on the GA mechanisms above.

## Manifest & pointer file contents (implementation reference)

### `.claude-plugin/plugin.json`
```json
{
  "name": "loop-goal",
  "description": "Discipline rules for long-running agent tasks — recurring loops and run-until-done goals. Checkpoint to .loopgoal/state.json, isolate each iteration in a fresh subagent, and write an explicit exit condition.",
  "version": "1.0.0",
  "author": { "name": "lgqyhm2010" },
  "homepage": "https://github.com/lgqyhm2010/loop-goal",
  "license": "MIT"
}
```
Skills are auto-discovered from `skills/loop-goal/SKILL.md`; no `skills` field needed.

### `.claude-plugin/marketplace.json`
```json
{
  "name": "lgqyhm2010",
  "owner": { "name": "lgqyhm2010" },
  "plugins": [
    { "name": "loop-goal", "source": "./" }
  ]
}
```
Install flow: `/plugin marketplace add lgqyhm2010/loop-goal` → `/plugin install loop-goal@lgqyhm2010`.

### `AGENTS.md` (thin pointer, draft)
```markdown
# AGENTS.md

This repository IS the `loop-goal` skill. When you (any agent) are about to run a
**long-running task** — one that repeats on an interval (a **loop**) or runs
until a completion criterion is met (a **goal**) — follow the loop-goal
discipline.

Triggers: "loop", "goal", "keep running", "until X", "run autonomously" — or
Chinese equivalents "持续做", "每隔", "循环跑", "直到…为止", "自主跑".

The six rules (summary): R1 init an explicit exit condition, R2 run each unit of
work in a fresh subagent, R3 fixed checkpoint order (write state → commit →
continue), R4 verify on resume, R5 log decisions, R6 exit cleanly.

Full rules, checkpoint format, and loop/goal specifics:
**`skills/loop-goal/SKILL.md`**.
```

### `.github/copilot-instructions.md` (thin pointer, draft)
```markdown
# Copilot instructions

For any **long-running task** — recurring **loop** or run-until-done **goal** —
follow the loop-goal discipline before starting.

Triggers: "loop", "goal", "keep running", "until X", "run autonomously".

Six rules: R1 explicit exit condition, R2 fresh subagent per iteration/phase,
R3 checkpoint order (write `.loopgoal/state.json` → commit → continue),
R4 verify on resume, R5 log decisions, R6 exit cleanly.

Full rules: `skills/loop-goal/SKILL.md`.
```

## Documentation plan

- **`README.md`** — replace the single "Install" block with a per-tool matrix
  (Claude Code skill/plugin/manual, Codex skill/AGENTS.md, Copilot
  skill/copilot-instructions.md), the all-three one-liner, and the caveats note.
  Keep the language-switcher header and everything else.
- **11 i18n READMEs** (`docs/i18n/README.*.md`) — update their Install sections to
  match the new matrix. Executed via a parallel workflow (same approach used for
  the original 11-language translation).
- **`DESIGN.md`** — update the "Skill file structure" tree to the new layout and
  add a short "Multi-platform distribution" section recording these decisions
  (relocation rationale, plugin manifest, thin always-on pointers, caveats).

## Commit plan (on `feat/multi-platform-packaging`)

1. `git mv` `SKILL.md` → `skills/loop-goal/SKILL.md` and `templates/` →
   `skills/loop-goal/templates/` (preserve history; fixes templates delivery).
2. Add `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`.
3. Add `AGENTS.md` + `.github/copilot-instructions.md`.
4. Rewrite `README.md` install matrix + update `DESIGN.md`.
5. Update all 11 i18n README install sections.

No push or PR unless the user asks.

## Verification

- `git mv` preserves history; `skills/loop-goal/SKILL.md` frontmatter still has
  `name` + `description` (spec-compliant).
- JSON manifests parse (validate `plugin.json`, `marketplace.json`).
- Internal links in README/DESIGN/pointers resolve to `skills/loop-goal/SKILL.md`.
- Spot-check that no doc still references the old root `SKILL.md`/`templates/` path.
- (Manual, optional) dry-run `npx skills add . -a codex -y` against a temp dir to
  confirm the whole folder (incl. `templates/`) is delivered.

## Non-goals

- Not a runtime harness; does not execute loops.
- No hosted marketplace/extension.
- No change to the skill's actual rules (R1–R6) or checkpoint format.
