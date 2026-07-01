[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · **Português (BR)** · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

Uma skill de disciplina para executar **tarefas longas** de forma
confiável — tarefas que ou se repetem em uma programação (**loops**) ou
rodam até uma meta ser atingida (**goals**).

## Instalação

loop-goal é um único `SKILL.md` em `skills/loop-goal/`. Escolha sua
ferramenta abaixo — ela instala no Claude Code, no Codex e no GitHub Copilot.

### Instalação rápida (as três de uma vez)

A CLI [`skills`](https://github.com/vercel-labs/skills) instala a skill —
sem clone, sem cópia manual:

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

Remova qualquer alvo `-a …` que você não precise. Adicione `-g` para
instalar em todos os projetos em vez de apenas no atual.

### Claude Code

- **Como skill:** `npx skills add lgqyhm2010/loop-goal -a claude-code` (`-g` para global)
- **Como plugin:** no Claude Code, rode `/plugin marketplace add lgqyhm2010/loop-goal`
  e depois `/plugin install loop-goal@lgqyhm2010`
- **Manualmente:** copie `skills/loop-goal/` para `.claude/skills/`

### OpenAI Codex

- **Como skill:** `npx skills add lgqyhm2010/loop-goal -a codex` — instala em
  `.agents/skills/loop-goal/`. A instalação em nível de projeto é recomendada.
- **Sempre ativo:** copie o ponteiro de [`AGENTS.md`](AGENTS.md) para o
  `AGENTS.md` do seu próprio repositório (ou `~/.codex/AGENTS.md`) para que a
  disciplina esteja sempre carregada.

### GitHub Copilot

- **Como skill:** `npx skills add lgqyhm2010/loop-goal -a github-copilot` — instala
  em `.agents/skills/loop-goal/`.
- **Sempre ativo (recomendado):** copie o ponteiro de
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md) para o
  `.github/copilot-instructions.md` do seu próprio repositório.

> **Notas.** Para o Codex, prefira uma instalação em nível de projeto ou o
> caminho via `AGENTS.md` — o caminho global (`-g`) da CLI (`~/.codex/skills/`)
> pode não corresponder ao local de onde o Codex lê as skills globais. Para o
> Copilot, o caminho `.github/copilot-instructions.md` é a forma mais
> confiável de manter a disciplina sempre ativa.

Uma vez instalada, basta descrever uma tarefa em loop ou de rodar-até-concluir
— a skill é acionada por conta própria (veja [Quando ela é acionada](#quando-ela-é-acionada)).

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

- `skills/loop-goal/SKILL.md` — a própria skill: detecção de modo, o formato
  do checkpoint, as seis regras.
- `skills/loop-goal/templates/state.json` — o esqueleto do checkpoint,
  copiado para um projeto pela regra R1.
- `.claude-plugin/` — manifestos do plugin do Claude Code + do marketplace.
- `AGENTS.md`, `.github/copilot-instructions.md` — ponteiros enxutos e
  sempre ativos para o Codex e o Copilot.
- `DESIGN.md` — a justificativa e as decisões de design.
