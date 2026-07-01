[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · **Español** · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

Una skill de disciplina para ejecutar **tareas largas** de forma fiable — tareas que
o bien se repiten según una planificación (**loops**) o bien se ejecutan hasta cumplir
un objetivo (**goals**).

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
3. **Impone seis reglas** — inicializar con una condición de salida explícita, ejecutar
   cada iteración en un subagente nuevo (aislamiento de contexto), hacer checkpoint
   en un orden fijo, verificar al reanudar, registrar decisiones, salir limpiamente.

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

- `SKILL.md` — la skill en sí: detección de modo, el formato de checkpoint,
  las seis reglas.
- `DESIGN.md` — justificación y decisiones de diseño.
- `templates/state.json` — el esqueleto del checkpoint, copiado a un
  proyecto por la regla R1.
