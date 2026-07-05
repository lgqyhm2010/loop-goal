[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · **Español** · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

Una skill de disciplina para ejecutar **tareas largas** de forma fiable — tareas que
o bien se repiten según una planificación (**loops**) o bien se ejecutan hasta cumplir
un objetivo (**goals**).

## Instalación

loop-goal es un único `SKILL.md` bajo `skills/loop-goal/`. Elige tu herramienta a continuación —
se instala en Claude Code, Codex y GitHub Copilot.

### Instalación rápida (las tres a la vez)

La CLI [`skills`](https://github.com/vercel-labs/skills) instala la skill —
sin clonar, sin copiar a mano:

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

Elimina cualquier destino `-a …` que no necesites. Añade `-g` para instalarla
en todos los proyectos en lugar de solo el actual.

### Claude Code

- **Como skill:** `npx skills add lgqyhm2010/loop-goal -a claude-code` (`-g` para instalación global)
- **Como plugin:** en Claude Code, ejecuta `/plugin marketplace add lgqyhm2010/loop-goal`
  y luego `/plugin install loop-goal@lgqyhm2010`
- **De forma manual:** copia `skills/loop-goal/` en `.claude/skills/`

### OpenAI Codex

- **Como skill:** `npx skills add lgqyhm2010/loop-goal -a codex` — se instala en
  `.agents/skills/loop-goal/`. Se recomienda la instalación a nivel de proyecto.
- **Siempre activa:** copia el puntero de [`AGENTS.md`](AGENTS.md) en el `AGENTS.md`
  de tu propio repositorio (o en `~/.codex/AGENTS.md`) para que la disciplina se cargue siempre.

### GitHub Copilot

- **Como skill:** `npx skills add lgqyhm2010/loop-goal -a github-copilot` — se instala
  en `.agents/skills/loop-goal/`.
- **Siempre activa (recomendado):** copia el puntero de
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md) en el
  `.github/copilot-instructions.md` de tu propio repositorio.

> **Notas.** Para Codex, prefiere una instalación a nivel de proyecto o la vía `AGENTS.md` —
> la ruta global (`-g`) de la CLI (`~/.codex/skills/`) puede no coincidir con dónde lee Codex
> las skills globales. Para Copilot, la vía `.github/copilot-instructions.md` es la forma más
> fiable de mantener la disciplina siempre activa.

Una vez instalada, basta con describir una tarea en loop o de ejecución hasta terminar — la
skill se activa por sí sola (consulta [Cuándo se activa](#cuándo-se-activa)).

## El problema

Las tareas de agente de larga duración fallan de tres formas silenciosas:

1. **Progreso perdido** — el contexto de la conversación se compacta y el
   agente olvida lo que ya hizo.
2. **Contexto contaminado** — la salida de las herramientas se acumula a lo largo de las iteraciones,
   degradando el razonamiento durante una ejecución larga.
3. **Sin salida** — un loop sin una condición de parada escrita se ejecuta para siempre.

Las soluciones son bien conocidas (hacer checkpoint a un archivo, aislar el contexto por
iteración, dejar por escrito la condición de salida). El problema es que dependen de que
el agente *recuerde* hacerlas — y la disciplina se relaja a lo largo de una ejecución
larga. Esta skill convierte las tres soluciones en reglas impuestas.

## Qué hace

Al invocarse, la skill:

1. **Detecta el modo** — LOOP (impulsado por el tiempo, recurrente) frente a GOAL
   (impulsado por el resultado, se ejecuta hasta terminar).
2. **Exige un archivo de checkpoint** — `.loopgoal/state.json` contiene el
   único estado recuperable; los commits de git contienen el historial.
3. **Impone siete reglas** — inicializar con una condición de salida explícita, ejecutar
   cada iteración en un subagente nuevo (aislamiento de contexto), hacer checkpoint
   en un orden fijo, verificar al reanudar, registrar decisiones, salir limpiamente y
   escalar una fase hacia la herramienta `Workflow` cuando se ramifica en ≥4 unidades
   independientes y paralelas.

Es **pura disciplina**: no escribe código, no ejecuta comandos y
no envuelve `/loop` ni `/schedule` — restringe *cómo* los ejecutas.

## Cuándo se activa

Frases como "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously" — o sus equivalentes en chino "持续做", "每隔", "循环跑",
"直到…为止", "自主跑", "跑个 loop" — o un explícito "use the loop-goal skill".

## Autónoma

Funciona en cualquier proyecto. Depende únicamente de herramientas integradas (`Agent`, git)
y mecanismos del harness (`/loop`, `ScheduleWakeup`). El plugin superpowers
es un compañero opcional, nunca un requisito.

## Archivos

- `skills/loop-goal/SKILL.md` — la skill en sí: detección de modo, el formato de
  checkpoint, las siete reglas.
- `skills/loop-goal/templates/state.json` — el esqueleto del checkpoint, copiado a
  un proyecto por la regla R1.
- `.claude-plugin/` — manifiestos del plugin y del marketplace de Claude Code.
- `AGENTS.md`, `.github/copilot-instructions.md` — punteros mínimos siempre activos
  para Codex y Copilot.
- `DESIGN.md` — justificación y decisiones de diseño.
