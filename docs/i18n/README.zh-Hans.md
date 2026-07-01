[English](../../README.md) · **简体中文** · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

一个用于可靠运行**长任务**的纪律型技能——这类任务要么按计划重复执行（**循环，loops**），要么持续运行直到达成目标（**目标，goals**）。

## 安装

loop-goal 是位于 `skills/loop-goal/` 下的一个单一 `SKILL.md`。请在下方
选择你使用的工具——它可以安装到 Claude Code、Codex 和 GitHub Copilot 中。

### 快速安装（三者一次搞定）

[`skills`](https://github.com/vercel-labs/skills) CLI 会安装该技能——
无需克隆，也无需手动复制：

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

如果不需要某个目标，去掉对应的 `-a …` 即可。加上 `-g` 可以安装到
每一个项目，而不仅仅是当前项目。

### Claude Code

- **作为技能：** `npx skills add lgqyhm2010/loop-goal -a claude-code`（全局安装用 `-g`）
- **作为插件：** 在 Claude Code 中运行 `/plugin marketplace add lgqyhm2010/loop-goal`，
  然后运行 `/plugin install loop-goal@lgqyhm2010`
- **手动安装：** 把 `skills/loop-goal/` 复制到 `.claude/skills/`

### OpenAI Codex

- **作为技能：** `npx skills add lgqyhm2010/loop-goal -a codex`——会安装到
  `.agents/skills/loop-goal/`。推荐使用项目级安装。
- **始终启用：** 把 [`AGENTS.md`](AGENTS.md) 中的指针复制到你自己
  仓库的 `AGENTS.md`（或 `~/.codex/AGENTS.md`）中，这样该纪律会始终被加载。

### GitHub Copilot

- **作为技能：** `npx skills add lgqyhm2010/loop-goal -a github-copilot`——会安装
  到 `.agents/skills/loop-goal/`。
- **始终启用（推荐）：** 把
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md) 中的指针复制到你自己
  仓库的 `.github/copilot-instructions.md` 中。

> **说明。** 对于 Codex，优先选择项目级安装或 `AGENTS.md` 方式——
> CLI 的全局（`-g`）路径（`~/.codex/skills/`）可能与 Codex 实际读取
> 全局技能的位置不一致。对于 Copilot，`.github/copilot-instructions.md` 方式是保持
> 该纪律始终启用的最可靠方法。

安装完成后，只需描述一个循环或跑到完成为止的任务——该技能
会自行触发（参见 [何时触发](#何时触发)）。

## 问题所在

长时间运行的智能体任务通常会以三种不易察觉的方式失败：

1. **进度丢失**——对话上下文被压缩，智能体忘记了自己已经做过什么。
2. **上下文污染**——多次迭代中工具输出不断堆积，在长时间运行中拖累推理质量。
3. **无法退出**——一个没有写明停止条件的循环会永远运行下去。

这些问题的修复方法众所周知（把状态检查点写入文件、按迭代隔离上下文、把退出条件写下来）。麻烦在于它们依赖智能体*记得*去做——而在长时间运行中纪律会逐渐松懈。这个技能把这三种修复手段变成强制执行的规则。

## 它做什么

被调用时，该技能会：

1. **检测模式**——LOOP（时间驱动、重复执行）还是 GOAL（结果驱动、跑到完成为止）。
2. **强制要求一个检查点文件**——`.loopgoal/state.json` 保存唯一可恢复的状态；git 提交保存历史记录。
3. **强制执行六条规则**——用明确的退出条件初始化、在全新的子智能体中运行每一次迭代（上下文隔离）、按固定顺序写检查点、恢复时进行校验、记录决策、干净地退出。

它是**纯纪律**：不写任何代码、不运行任何命令，也不封装 `/loop` 或 `/schedule`——它约束的是你*如何*运行它们。

## 何时触发

诸如 "loop"、"goal"、"keep running"、"run in a loop"、"until X"、"run autonomously" 之类的短语——或其中文对应说法 "持续做"、"每隔"、"循环跑"、"直到…为止"、"自主跑"、"跑个 loop"——又或者明确的 "use the loop-goal skill"。

## 自成一体

可在任何项目中使用。它只依赖内置工具（`Agent`、git）和运行框架机制（`/loop`、`ScheduleWakeup`）。superpowers 插件是可选的搭档，绝非必需项。

## 文件

- `skills/loop-goal/SKILL.md`——技能本身：模式检测、检查点格式、六条规则。
- `skills/loop-goal/templates/state.json`——检查点骨架，由规则 R1 复制
  到项目中。
- `.claude-plugin/`——Claude Code 插件与市场（marketplace）清单文件。
- `AGENTS.md`、`.github/copilot-instructions.md`——供 Codex 和 Copilot
  使用的精简的始终启用指针文件。
- `DESIGN.md`——设计理念与决策。
