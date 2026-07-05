[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · **日本語** · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

**長時間タスク** を確実に実行するための規律スキル。スケジュールに従って繰り返されるタスク（**loops**、ループ）と、目標が達成されるまで実行されるタスク（**goals**、ゴール）の両方を対象とします。

## インストール

loop-goal は `skills/loop-goal/` 配下にある単一の `SKILL.md` です。下記からお使いのツールを選んでください。
Claude Code、Codex、GitHub Copilot のいずれにもインストールできます。

### クイックインストール（3つ同時に）

[`skills`](https://github.com/vercel-labs/skills) CLI でスキルをインストールできます。
クローンも手動コピーも不要です。

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

不要な `-a …` ターゲットは削除してください。現在のプロジェクトだけでなく、すべての
プロジェクトへインストールするには `-g` を付けます。

### Claude Code

- **スキルとして:** `npx skills add lgqyhm2010/loop-goal -a claude-code`（グローバルには `-g`）
- **プラグインとして:** Claude Code 内で `/plugin marketplace add lgqyhm2010/loop-goal`
  を実行し、続けて `/plugin install loop-goal@lgqyhm2010` を実行します
- **手動で:** `skills/loop-goal/` を `.claude/skills/` へコピーしてください

### OpenAI Codex

- **スキルとして:** `npx skills add lgqyhm2010/loop-goal -a codex` — `.agents/skills/loop-goal/`
  にインストールされます。プロジェクト単位でのインストールを推奨します。
- **常時有効化:** [`AGENTS.md`](AGENTS.md) にあるポインターを、あなた自身のリポジトリの
  `AGENTS.md`（または `~/.codex/AGENTS.md`）にコピーすると、この規律が常に読み込まれます。

### GitHub Copilot

- **スキルとして:** `npx skills add lgqyhm2010/loop-goal -a github-copilot` —
  `.agents/skills/loop-goal/` にインストールされます。
- **常時有効化（推奨）:** [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
  にあるポインターを、あなた自身のリポジトリの `.github/copilot-instructions.md` にコピーしてください。

> **注意事項。** Codex では、プロジェクト単位のインストールか `AGENTS.md` 経由の方法を推奨します。
> CLI のグローバル（`-g`）パス（`~/.codex/skills/`）は、Codex がグローバルスキルを読み込む
> 場所と一致しない場合があります。Copilot では、`.github/copilot-instructions.md` 経由の方法が、
> この規律を常時有効に保つ最も確実な手段です。

インストールが済んだら、あとはループするタスクや完了まで実行するタスクを説明するだけです。スキルは自動的に発動します（[いつ発動するか](#いつ発動するか) を参照）。

## 課題

長時間実行されるエージェントタスクは、次の3つの目立たない形で失敗します。

1. **進捗の喪失** — 会話コンテキストが圧縮され、エージェントはすでに実行した内容を忘れてしまう。
2. **コンテキストの汚染** — 反復のたびにツール出力が積み重なり、長時間の実行にわたって推論の質が低下する。
3. **終了しない** — 停止条件が明文化されていないループは、永遠に実行され続ける。

これらの修正策はよく知られています（ファイルへのチェックポイント保存、反復ごとのコンテキスト分離、終了条件の明文化）。問題は、これらがエージェントが実行を *覚えている* ことに依存している点です。そして規律は長時間の実行にわたって薄れていきます。このスキルは、3つの修正策を強制されるルールへと変えます。

## 何をするのか

呼び出されると、このスキルは次を行います。

1. **モードを検出する** — LOOP（時間駆動、繰り返し）と GOAL（結果駆動、完了まで実行）を判別します。
2. **チェックポイントファイルを必須とする** — `.loopgoal/state.json` が唯一の復旧可能な状態を保持し、git コミットが履歴を保持します。
3. **7つのルールを強制する** — 明示的な終了条件を伴う初期化、各反復を新しいサブエージェントで実行（コンテキスト分離）、固定順序でのチェックポイント保存、再開時の検証、意思決定のログ記録、クリーンな終了、そしてフェーズが独立した並列ユニット ≥4 個に分岐する場合は、そのフェーズを `Workflow` ツールへスケールアウトする。

これは **純粋な規律** です。コードを書かず、コマンドを実行せず、`/loop` や `/schedule` をラップしません。あくまで、それらを *どのように* 実行するかを制約します。

## いつ発動するか

"loop"、"goal"、"keep running"、"run in a loop"、"until X"、"run autonomously" のようなフレーズ、あるいはそれらに対応する中国語の "持续做"、"每隔"、"循环跑"、"直到…为止"、"自主跑"、"跑个 loop"、または明示的な "use the loop-goal skill" です。

## 自己完結

あらゆるプロジェクトで動作します。依存するのは組み込みツール（`Agent`、git）とハーネスの仕組み（`/loop`、`ScheduleWakeup`）のみです。superpowers プラグインは任意のコンパニオンであり、必須ではありません。

## ファイル

- `skills/loop-goal/SKILL.md` — スキル本体。モード検出、チェックポイント形式、7つのルール。
- `skills/loop-goal/templates/state.json` — チェックポイントのひな形。ルール R1 によって
  プロジェクトへコピーされます。
- `.claude-plugin/` — Claude Code のプラグイン + マーケットプレイスのマニフェスト。
- `AGENTS.md`、`.github/copilot-instructions.md` — Codex と Copilot 向けの、常時有効化を
  行う簡潔なポインターファイル。
- `DESIGN.md` — 設計の根拠と決定事項。
