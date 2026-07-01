[English](../../README.md) · [简体中文](README.zh-Hans.md) · **繁體中文** · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

一個用於可靠執行**長時間任務**的紀律技能——這類任務要麼依排程重複執行（**loops**，循環），要麼持續執行直到目標達成（**goals**，目標）。

## 安裝

loop-goal 是位於 `skills/loop-goal/` 下的單一 `SKILL.md`。請在下方挑選你使用的工具——
它可以安裝進 Claude Code、Codex 與 GitHub Copilot。

### 快速安裝（三者一次搞定）

[`skills`](https://github.com/vercel-labs/skills) CLI 會直接安裝這個技能——
無需 clone、無需手動複製：

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

不需要的 `-a …` 目標可以直接省略。加上 `-g` 即可安裝到每個專案，而不只是目前這一個。

### Claude Code

- **以技能形式：**`npx skills add lgqyhm2010/loop-goal -a claude-code`（全域安裝請加 `-g`）
- **以外掛形式：**在 Claude Code 中執行 `/plugin marketplace add lgqyhm2010/loop-goal`，
  接著執行 `/plugin install loop-goal@lgqyhm2010`
- **手動安裝：**把 `skills/loop-goal/` 複製到 `.claude/skills/`

### OpenAI Codex

- **以技能形式：**`npx skills add lgqyhm2010/loop-goal -a codex`——會安裝到
  `.agents/skills/loop-goal/`。建議採用專案層級安裝。
- **常駐啟用：**把 [`AGENTS.md`](AGENTS.md) 中的指標複製到你自己
  repo 的 `AGENTS.md`（或 `~/.codex/AGENTS.md`），讓這項紀律隨時載入。

### GitHub Copilot

- **以技能形式：**`npx skills add lgqyhm2010/loop-goal -a github-copilot`——會安裝
  到 `.agents/skills/loop-goal/`。
- **常駐啟用（建議）：**把
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md) 中的指標複製到你自己
  repo 的 `.github/copilot-instructions.md`。

> **注意事項。** 對於 Codex，建議採用專案層級安裝或 `AGENTS.md` 這條路徑——
> CLI 的全域（`-g`）路徑（`~/.codex/skills/`）可能與 Codex 讀取全域技能的位置不一致。
> 對於 Copilot，`.github/copilot-instructions.md` 這條路徑是讓這項紀律保持常駐啟用最可靠的方式。

安裝完成後，只要描述一個循環或執行到完成為止的任務——技能就會自動觸發（見[何時觸發](#何時觸發)）。

## 問題所在

長時間執行的 agent 任務會以三種難以察覺的方式失敗：

1. **進度遺失**——對話脈絡被壓縮，agent 忘記自己已經做過的事。
2. **脈絡污染**——工具輸出在多次迭代間不斷堆積，使長時間執行下的推理逐漸退化。
3. **沒有出口**——一個沒有寫下停止條件的循環會永遠執行下去。

這些問題的修正方法眾所周知（把狀態檢查點寫入檔案、為每次迭代隔離脈絡、把出口條件寫下來）。麻煩在於它們依賴 agent *記得*去做——而在長時間執行下，紀律會漸漸鬆懈。這個技能把這三項修正轉化為強制執行的規則。

## 它做什麼

被呼叫時，這個技能會：

1. **偵測模式**——LOOP（時間驅動、重複執行）對比 GOAL（結果驅動、執行到完成為止）。
2. **強制要求一個檢查點檔案**——`.loopgoal/state.json` 保存唯一可復原的狀態；git commits 保存歷史。
3. **強制執行六條規則**——以明確的出口條件初始化、在全新的 subagent 中執行每次迭代（脈絡隔離）、以固定順序寫入檢查點、復原時驗證、記錄決策、乾淨地退出。

它是**純粹的紀律**：它不寫任何程式碼、不執行任何命令，也不包裝 `/loop` 或 `/schedule`——它約束的是你*如何*執行它們。

## 何時觸發

像是 "loop"、"goal"、"keep running"、"run in a loop"、"until X"、"run autonomously" 這類語句——或其中文對應 "持续做"、"每隔"、"循环跑"、"直到…为止"、"自主跑"、"跑个 loop"——或明確的 "use the loop-goal skill"。

## 自我完備

可在任何專案中運作。它僅依賴內建工具（`Agent`、git）與 harness 機制（`/loop`、`ScheduleWakeup`）。superpowers 外掛是一個可選的搭配，絕非必要條件。

## 檔案

- `skills/loop-goal/SKILL.md`——技能本身：模式偵測、檢查點格式、六條規則。
- `skills/loop-goal/templates/state.json`——檢查點骨架，由規則 R1 複製進專案。
- `.claude-plugin/`——Claude Code 外掛與 marketplace 的清單檔。
- `AGENTS.md`、`.github/copilot-instructions.md`——供 Codex 與 Copilot 使用的精簡常駐指標檔。
- `DESIGN.md`——設計理據與決策。
