[English](../../README.md) · [简体中文](README.zh-Hans.md) · **繁體中文** · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

一個用於可靠執行**長時間任務**的紀律技能——這類任務要麼依排程重複執行（**loops**，循環），要麼持續執行直到目標達成（**goals**，目標）。

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

- `SKILL.md`——技能本身：模式偵測、檢查點格式、六條規則。
- `DESIGN.md`——設計理據與決策。
- `templates/state.json`——檢查點骨架，由規則 R1 複製進專案。
