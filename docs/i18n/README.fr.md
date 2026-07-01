[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [Español](README.es.md) · **Français** · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

Une compétence de discipline pour exécuter de manière fiable des **tâches longues** — des tâches qui,
soit se répètent selon une planification (**boucles**), soit s'exécutent jusqu'à ce qu'un objectif soit atteint
(**objectifs**).

## Installation

loop-goal est un unique `SKILL.md` sous `skills/loop-goal/`. Choisissez votre outil
ci-dessous — l'installation se fait dans Claude Code, Codex et GitHub Copilot.

### Installation rapide (les trois à la fois)

La CLI [`skills`](https://github.com/vercel-labs/skills) installe la compétence —
sans clonage, sans copie manuelle :

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

Retirez toute cible `-a …` dont vous n'avez pas besoin. Ajoutez `-g` pour l'installer
pour chaque projet plutôt que pour le projet courant uniquement.

### Claude Code

- **En tant que compétence :** `npx skills add lgqyhm2010/loop-goal -a claude-code` (`-g` pour une installation globale)
- **En tant que plugin :** dans Claude Code, exécutez `/plugin marketplace add lgqyhm2010/loop-goal`
  puis `/plugin install loop-goal@lgqyhm2010`
- **Manuellement :** copiez `skills/loop-goal/` dans `.claude/skills/`

### OpenAI Codex

- **En tant que compétence :** `npx skills add lgqyhm2010/loop-goal -a codex` — s'installe dans
  `.agents/skills/loop-goal/`. L'installation au niveau du projet est recommandée.
- **Toujours actif :** copiez le pointeur depuis [`AGENTS.md`](AGENTS.md) dans le fichier
  `AGENTS.md` de votre propre dépôt (ou `~/.codex/AGENTS.md`) afin que la discipline soit
  toujours chargée.

### GitHub Copilot

- **En tant que compétence :** `npx skills add lgqyhm2010/loop-goal -a github-copilot` — s'installe
  dans `.agents/skills/loop-goal/`.
- **Toujours actif (recommandé) :** copiez le pointeur depuis
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md) dans le fichier
  `.github/copilot-instructions.md` de votre propre dépôt.

> **Remarques.** Pour Codex, préférez une installation au niveau du projet ou la voie `AGENTS.md` —
> le chemin global (`-g`) de la CLI (`~/.codex/skills/`) peut ne pas correspondre à l'endroit où Codex
> lit les compétences globales. Pour Copilot, la voie `.github/copilot-instructions.md` est le moyen
> le plus fiable de garder la discipline toujours active.

Une fois installée, décrivez simplement une tâche en boucle ou à exécuter
jusqu'à l'achèvement — la compétence se déclenche d'elle-même (voir
[Quand elle se déclenche](#quand-elle-se-déclenche)).

## Le problème

Les tâches d'agent de longue durée échouent de trois manières discrètes :

1. **Progression perdue** — le contexte de la conversation est compacté et
   l'agent oublie ce qu'il a déjà fait.
2. **Contexte pollué** — la sortie des outils s'accumule au fil des itérations,
   dégradant le raisonnement sur une longue exécution.
3. **Aucune sortie** — une boucle sans condition d'arrêt écrite s'exécute indéfiniment.

Les correctifs sont bien connus (créer un point de contrôle dans un fichier, isoler le contexte à chaque
itération, écrire la condition de sortie). Le hic, c'est qu'ils reposent sur le fait que
l'agent *se souvienne* de les appliquer — et la discipline se relâche sur une longue
exécution. Cette compétence transforme les trois correctifs en règles imposées.

## Ce qu'elle fait

Lorsqu'elle est invoquée, la compétence :

1. **Détecte le mode** — LOOP (piloté par le temps, récurrent) vs GOAL
   (piloté par le résultat, exécuté jusqu'à l'achèvement).
2. **Impose un fichier de point de contrôle** — `.loopgoal/state.json` détient
   l'unique état récupérable ; les commits git détiennent l'historique.
3. **Applique six règles** — initialiser avec une condition de sortie explicite, exécuter
   chaque itération dans un sous-agent frais (isolation du contexte), créer un point de contrôle
   dans un ordre fixe, vérifier à la reprise, journaliser les décisions, sortir proprement.

C'est de la **pure discipline** : elle n'écrit aucun code, n'exécute aucune commande et
n'enveloppe pas `/loop` ni `/schedule` — elle contraint *la manière dont* vous les exécutez.

## Quand elle se déclenche

Des expressions comme "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously" — ou leurs équivalents chinois "持续做", "每隔", "循环跑",
"直到…为止", "自主跑", "跑个 loop" — ou un "use the loop-goal skill" explicite.

## Autonome

Fonctionne dans n'importe quel projet. Elle ne dépend que d'outils intégrés (`Agent`, git)
et de mécanismes du harnais (`/loop`, `ScheduleWakeup`). Le plugin superpowers
est un compagnon optionnel, jamais une exigence.

## Fichiers

- `skills/loop-goal/SKILL.md` — la compétence elle-même : détection du mode, le format du
  point de contrôle, les six règles.
- `skills/loop-goal/templates/state.json` — le squelette du point de contrôle, copié dans
  un projet par la règle R1.
- `.claude-plugin/` — manifestes du plugin Claude Code et du marketplace.
- `AGENTS.md`, `.github/copilot-instructions.md` — pointeurs légers toujours actifs pour
  Codex et Copilot.
- `DESIGN.md` — justification et décisions de conception.
