[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [Español](README.es.md) · **Français** · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

Une compétence de discipline pour exécuter de manière fiable des **tâches longues** — des tâches qui,
soit se répètent selon une planification (**boucles**), soit s'exécutent jusqu'à ce qu'un objectif soit atteint
(**objectifs**).

## Installation

Ajoutez-la avec la CLI [`skills`](https://github.com/vercel-labs/skills) —
sans clonage, sans copie manuelle :

```bash
# Dans le projet courant → .claude/skills/
npx skills add lgqyhm2010/loop-goal

# Pour chaque projet → ~/.claude/skills/
npx skills add lgqyhm2010/loop-goal -g
```

`skills` trouve le `SKILL.md` à la racine du dépôt et le dépose (avec
`templates/`) dans votre répertoire de compétences. Ajoutez `-a claude-code -y`
pour une installation non interactive.

Vous préférez le faire à la main ? Copiez `SKILL.md` et `templates/` dans
`.claude/skills/loop-goal/`.

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

- `SKILL.md` — la compétence elle-même : détection du mode, le format du point de contrôle,
  les six règles.
- `DESIGN.md` — justification et décisions de conception.
- `templates/state.json` — le squelette du point de contrôle, copié dans un
  projet par la règle R1.
