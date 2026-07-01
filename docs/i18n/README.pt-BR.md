[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · **Português (BR)** · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

Uma skill de disciplina para executar **tarefas longas** de forma
confiável — tarefas que ou se repetem em uma programação (**loops**) ou
rodam até uma meta ser atingida (**goals**).

## O problema

Tarefas de agente de longa duração falham de três formas silenciosas:

1. **Progresso perdido** — o contexto da conversa é compactado e o
   agente esquece o que já fez.
2. **Contexto poluído** — a saída das ferramentas se acumula ao longo
   das iterações, degradando o raciocínio em uma execução longa.
3. **Sem saída** — um loop sem condição de parada escrita roda para
   sempre.

As correções são bem conhecidas (fazer checkpoint em um arquivo, isolar
o contexto por iteração, escrever a condição de saída). O problema é que
elas dependem de o agente *lembrar* de fazê-las — e a disciplina se
dissolve ao longo de uma execução longa. Esta skill transforma as três
correções em regras impostas.

## O que ela faz

Quando invocada, a skill:

1. **Detecta o modo** — LOOP (orientado ao tempo, recorrente) vs GOAL
   (orientado ao resultado, roda-até-concluir).
2. **Exige um arquivo de checkpoint** — `.loopgoal/state.json` guarda o
   único estado recuperável; os commits do git guardam o histórico.
3. **Impõe seis regras** — inicializar com uma condição de saída
   explícita, executar cada iteração em um subagente novo (isolamento de
   contexto), fazer checkpoint em uma ordem fixa, verificar ao retomar,
   registrar decisões, sair de forma limpa.

Ela é **pura disciplina**: não escreve código, não roda comandos e não
envolve `/loop` ou `/schedule` — ela restringe *como* você os executa.

## Quando ela é acionada

Frases como "loop", "goal", "keep running", "run in a loop", "until X",
"run autonomously" — ou seus equivalentes em chinês "持续做", "每隔", "循环跑",
"直到…为止", "自主跑", "跑个 loop" — ou um explícito "use the loop-goal skill".

## Autossuficiente

Funciona em qualquer projeto. Depende apenas de ferramentas nativas
(`Agent`, git) e de mecanismos do harness (`/loop`, `ScheduleWakeup`). O
plugin superpowers é um complemento opcional, nunca um requisito.

## Arquivos

- `SKILL.md` — a própria skill: detecção de modo, o formato do
  checkpoint, as seis regras.
- `DESIGN.md` — a justificativa e as decisões de design.
- `templates/state.json` — o esqueleto do checkpoint, copiado para um
  projeto pela regra R1.
