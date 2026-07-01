# Multi-Platform Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package the `loop-goal` discipline skill as a native, checked-in-files extension for Claude Code (skill + plugin marketplace), OpenAI Codex, and GitHub Copilot, and fix the `templates/` delivery bug by relocating the skill under `skills/loop-goal/`.

**Architecture:** One canonical `skills/loop-goal/SKILL.md` (+ `templates/`) feeds the `skills` CLI (all agents) and the Claude Code plugin (auto-discovered under `skills/`). Thin always-on pointer files (`AGENTS.md`, `.github/copilot-instructions.md`) reference the skill without duplicating its rules. Docs are rewritten into a per-tool install matrix, in English and all 11 i18n READMEs.

**Tech Stack:** Markdown, JSON (plugin manifests), git. No code, no build step, no test framework — verification is JSON parsing + `grep` path checks + link resolution.

## Global Constraints

- Branch: `feat/multi-platform-packaging`. Commit per task. Do NOT push or open a PR unless the user asks.
- Repo slug is `lgqyhm2010/loop-goal` (`https://github.com/lgqyhm2010/loop-goal.git`) — use it verbatim in every install command and manifest.
- `skills/loop-goal/SKILL.md` frontmatter MUST keep `name: loop-goal` and the existing `description:` (spec-compliant for both the CLI and the plugin).
- Do NOT change the skill's actual rules (R1–R6), mode detection, or checkpoint format. This is packaging only.
- Marketplace name = `lgqyhm2010`; plugin name = `loop-goal`; install reads `loop-goal@lgqyhm2010`.
- Pointer files (`AGENTS.md`, `.github/copilot-instructions.md`) are THIN: trigger phrases + six rule names + "full rules → `skills/loop-goal/SKILL.md`". Never copy the full ruleset into them.
- The 11 i18n locales (per `docs/i18n/`): `zh-Hans, zh-Hant, ja, es, fr, ar, hi, pt-BR, ru, bn` (plus the English root `README.md`).
- `plugin.json` declares `license: MIT` — a root `LICENSE` file must exist to match.

---

### Task 1: Relocate the skill to `skills/loop-goal/`

Moves `SKILL.md` and `templates/` off the repo root so the `skills` CLI copies the whole folder (fixing `templates/` delivery) and the Claude Code plugin auto-discovers it under `skills/`.

**Files:**
- Move: `SKILL.md` → `skills/loop-goal/SKILL.md`
- Move: `templates/state.json` → `skills/loop-goal/templates/state.json`
- Verify only (no content edits): `skills/loop-goal/SKILL.md`

**Interfaces:**
- Consumes: nothing (first task).
- Produces: canonical path `skills/loop-goal/SKILL.md` and `skills/loop-goal/templates/state.json` that Tasks 2–5 reference.

- [ ] **Step 1: Move the files with git (preserve history)**

```bash
mkdir -p skills/loop-goal
git mv SKILL.md skills/loop-goal/SKILL.md
git mv templates skills/loop-goal/templates
```

- [ ] **Step 2: Verify the new layout and that the root is clean**

```bash
ls skills/loop-goal skills/loop-goal/templates
test ! -e SKILL.md && test ! -e templates && echo "root clean OK"
```
Expected: lists `SKILL.md` and `templates/` under `skills/loop-goal/`; prints `root clean OK`.

- [ ] **Step 3: Verify the skill frontmatter is intact (name + description)**

```bash
head -4 skills/loop-goal/SKILL.md
```
Expected: shows `---`, `name: loop-goal`, a `description:` line, `---`. Do NOT edit the body.

- [ ] **Step 4: Confirm what still references the old root paths (fixed later, not here)**

```bash
grep -rn --exclude-dir=.git -E '(^|[^/])SKILL\.md|(^|[^/])templates/' README.md DESIGN.md docs/i18n || true
```
Expected: matches will appear (README/DESIGN/i18n still point at old paths). These are fixed in Tasks 4–5 — note them, do not fix here.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "refactor: move skill into skills/loop-goal/ so templates/ ships via the skills CLI

Root-level SKILL.md caused the skills CLI to copy only SKILL.md (not
templates/). Relocating under skills/loop-goal/ makes the CLI copy the whole
folder and matches the Claude Code plugin skills layout.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Add Claude Code plugin manifests + LICENSE

Makes the repo installable as a one-plugin Claude Code marketplace and adds the MIT license that `plugin.json` declares.

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `LICENSE`

**Interfaces:**
- Consumes: `skills/loop-goal/SKILL.md` (auto-discovered by the plugin; no `skills` field needed in `plugin.json`).
- Produces: install flow `/plugin marketplace add lgqyhm2010/loop-goal` → `/plugin install loop-goal@lgqyhm2010`.

- [ ] **Step 1: Create `.claude-plugin/plugin.json`**

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

- [ ] **Step 2: Create `.claude-plugin/marketplace.json`**

```json
{
  "name": "lgqyhm2010",
  "owner": { "name": "lgqyhm2010" },
  "plugins": [
    { "name": "loop-goal", "source": "./" }
  ]
}
```

- [ ] **Step 3: Create `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2026 lgqyhm2010

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Validate both JSON manifests parse**

```bash
python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('json OK')"
```
Expected: `json OK`.

- [ ] **Step 5: Verify no skill files leaked into `.claude-plugin/`**

```bash
ls .claude-plugin
test ! -e .claude-plugin/skills && test ! -e .claude-plugin/SKILL.md && echo "manifest dir clean OK"
```
Expected: lists only `plugin.json` and `marketplace.json`; prints `manifest dir clean OK`. (Claude Code requires only `plugin.json` to live inside `.claude-plugin/`; skills stay at repo-root `skills/`.)

- [ ] **Step 6: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json LICENSE
git commit -m "feat: add Claude Code plugin manifests and MIT LICENSE

.claude-plugin/{plugin,marketplace}.json make the repo installable via
/plugin marketplace add lgqyhm2010/loop-goal → /plugin install loop-goal@lgqyhm2010.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Add always-on pointer files (Codex + Copilot)

Thin pointer files that make the discipline always-on where a user wants it, and dogfood the skill on this repo.

**Files:**
- Create: `AGENTS.md`
- Create: `.github/copilot-instructions.md`

**Interfaces:**
- Consumes: `skills/loop-goal/SKILL.md` (both files link to it as the full-rules source).
- Produces: copy-paste-ready pointer blocks referenced by the README install matrix (Task 4).

- [ ] **Step 1: Create `AGENTS.md`**

```markdown
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
```

- [ ] **Step 2: Create `.github/copilot-instructions.md`**

```markdown
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
```

- [ ] **Step 3: Verify both pointers resolve to the skill and stay short**

```bash
test -f skills/loop-goal/SKILL.md && echo "skill target exists"
grep -q "skills/loop-goal/SKILL.md" AGENTS.md && grep -q "skills/loop-goal/SKILL.md" .github/copilot-instructions.md && echo "pointers link to skill"
awk 'END{print FILENAME, NR}' AGENTS.md; awk 'END{print FILENAME, NR}' .github/copilot-instructions.md
```
Expected: `skill target exists`; `pointers link to skill`; each file well under ~35 lines (thin).

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md .github/copilot-instructions.md
git commit -m "feat: add always-on pointer files for Codex and Copilot

Thin AGENTS.md (Codex/Copilot/other AGENTS.md-aware tools) and
.github/copilot-instructions.md (Copilot's documented always-on path) point to
skills/loop-goal/SKILL.md without duplicating the rules.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Rewrite `README.md` install matrix + update `DESIGN.md`

Replaces the single Claude-Code-only install block with a per-tool matrix, fixes the inaccurate "(plus templates/)" claim and old root paths, and updates the design doc's layout.

**Files:**
- Modify: `README.md` (Install section, lines ~9–27; Files section, lines ~74–80)
- Modify: `DESIGN.md` (Skill file structure section; add distribution section)

**Interfaces:**
- Consumes: install commands + pointer files from Tasks 1–3.
- Produces: the English install matrix that Task 5 translates into the 11 i18n READMEs.

- [ ] **Step 1: Replace the README `## Install` section**

Find the current block (from `## Install` through the manual-copy line ending `.claude/skills/loop-goal/`) and replace it with:

````markdown
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
````

- [ ] **Step 2: Update the README `## Files` section**

Replace the current Files list with:

```markdown
## Files

- `skills/loop-goal/SKILL.md` — the skill itself: mode detection, the checkpoint
  format, the six rules.
- `skills/loop-goal/templates/state.json` — the checkpoint skeleton, copied into
  a project by rule R1.
- `.claude-plugin/` — Claude Code plugin + marketplace manifests.
- `AGENTS.md`, `.github/copilot-instructions.md` — thin always-on pointers for
  Codex and Copilot.
- `DESIGN.md` — design rationale and decisions.
```

- [ ] **Step 3: Update `DESIGN.md` — Skill file structure tree**

Replace the `## Skill file structure` code block with the new layout:

````markdown
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
````

- [ ] **Step 4: Add a distribution section to `DESIGN.md`**

Append after the file-structure section:

````markdown
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
````

- [ ] **Step 5: Verify no stale root paths and links resolve**

```bash
grep -n "the repo root" README.md || echo "no 'repo root' claim OK"
grep -nE '`SKILL\.md`|`templates/' README.md DESIGN.md | grep -v 'skills/loop-goal' || echo "no bare root SKILL.md/templates refs OK"
grep -q "skills/loop-goal/SKILL.md" README.md && echo "README points to new path"
```
Expected: the old "at the repo root" claim is gone; no bare `SKILL.md`/`templates/` refs remain outside `skills/loop-goal/`; README points to the new path.

- [ ] **Step 6: Commit**

```bash
git add README.md DESIGN.md
git commit -m "docs: rewrite README install as a per-tool matrix; update DESIGN layout

Per-tool install (Claude Code skill/plugin/manual, Codex skill/AGENTS.md, Copilot
skill/copilot-instructions.md) + all-three one-liner. Fixes the inaccurate
'(plus templates/)' claim and old root paths. DESIGN gets the new file tree and a
multi-platform distribution section.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Update the 11 i18n README install sections

Bring every translated README's Install (and Files) section in line with the new English matrix, preserving each file's language and the rest of its content. Done with a parallel workflow because it's 10 near-identical translation edits.

**Files:**
- Modify: `docs/i18n/README.zh-Hans.md`, `README.zh-Hant.md`, `README.ja.md`, `README.es.md`, `README.fr.md`, `README.ar.md`, `README.hi.md`, `README.pt-BR.md`, `README.ru.md`, `README.bn.md` (10 files)

**Interfaces:**
- Consumes: the English Install + Files sections from Task 4 as the translation source.
- Produces: nothing downstream (final task).

- [ ] **Step 1: Confirm the current i18n install sections and their structure**

```bash
for f in docs/i18n/README.*.md; do echo "=== $f ==="; grep -niE 'install|npx skills|SKILL\.md|templates/' "$f" | head -20; done
```
Expected: each file has an Install-equivalent heading + the old `npx skills add lgqyhm2010/loop-goal` block and root-path references. Note each locale's heading wording.

- [ ] **Step 2: Run a translation workflow to rewrite each locale's Install + Files section**

Dispatch one agent per locale (10 total) via a Workflow. Each agent:
1. Reads its `docs/i18n/README.<locale>.md`.
2. Replaces the Install section with a translation of the English matrix from Task 4 (headings translated; commands, code blocks, flags, paths, and identifiers like `npx skills add lgqyhm2010/loop-goal`, `AGENTS.md`, `.github/copilot-instructions.md`, `loop-goal@lgqyhm2010` kept verbatim in English).
3. Replaces the Files list with a translation of the new English Files list (paths verbatim).
4. Leaves every other section, the language-switcher header, and the file's tone unchanged.
5. Writes the file back.

Use the English `README.md` Install + Files sections (post-Task-4) as the exact source text handed to each agent.

- [ ] **Step 3: Verify every locale updated and no stale root paths remain**

```bash
for f in docs/i18n/README.*.md; do
  grep -q "skills/loop-goal" "$f" && grep -q "a claude-code\|a codex\|a github-copilot\|loop-goal@lgqyhm2010" "$f" \
    && echo "OK  $f" || echo "MISS $f"
done
grep -rnE '`SKILL\.md`|`templates/' docs/i18n | grep -v 'skills/loop-goal' || echo "no bare root refs in i18n OK"
```
Expected: `OK` for all 10 files; no bare root `SKILL.md`/`templates/` references remain.

- [ ] **Step 4: Commit**

```bash
git add docs/i18n
git commit -m "docs(i18n): update all 11 README install sections for multi-platform packaging

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage** — every spec section maps to a task:
- Relocate skill → Task 1. Plugin manifests → Task 2. LICENSE → Task 2. Pointer files → Task 3. README matrix + DESIGN → Task 4. 11 i18n → Task 5. Known caveats → documented in README (Task 4 Step 1 Notes) + DESIGN (Task 4 Step 4). Templates-bug fix → Task 1. Out-of-scope items (Plugin Directory, Copilot Extension) → not implemented, by design.

**Placeholder scan** — no TBD/TODO; every file's full content is inline (manifests, LICENSE, both pointers, README/DESIGN replacements). Task 5's per-locale translations are delegated (10 near-identical edits) with an exact source and a mechanical verify step — not a placeholder.

**Type/path consistency** — one canonical path `skills/loop-goal/SKILL.md` and `skills/loop-goal/templates/state.json` used identically across Tasks 1–5; marketplace `lgqyhm2010` / plugin `loop-goal` / install `loop-goal@lgqyhm2010` consistent between Task 2 and Task 4; pointer link targets consistent between Task 3 and the READMEs.
