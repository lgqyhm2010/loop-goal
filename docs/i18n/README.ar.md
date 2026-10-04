[English](../../README.md) · [简体中文](README.zh-Hans.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · **العربية** · [हिन्दी](README.hi.md) · [Português (BR)](README.pt-BR.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md)

# loop-goal

مهارة انضباط لتشغيل **المهام الطويلة** بموثوقية — المهام التي إمّا
تتكرّر وفق جدول زمني (**الحلقات**) أو تعمل حتى يتحقّق هدف معيّن
(**الأهداف**).

## التثبيت

loop-goal عبارة عن ملف `SKILL.md` واحد تحت `skills/loop-goal/`. اختر أداتك أدناه —
يتم تثبيتها في Claude Code وCodex وGitHub Copilot.

### تثبيت سريع (الثلاثة معاً)

تُثبِّت واجهة سطر الأوامر [`skills`](https://github.com/vercel-labs/skills) المهارة —
دون استنساخ ودون نسخ يدوي:

```bash
npx skills add lgqyhm2010/loop-goal -a claude-code -a codex -a github-copilot -y
```

احذف أي هدف `-a …` لا تحتاجه. أضِف `-g` للتثبيت في كل مشروع
بدلاً من المشروع الحالي فقط.

### Claude Code

- **كمهارة:** `npx skills add lgqyhm2010/loop-goal -a claude-code` (`-g` للتثبيت الشامل)
- **كإضافة (plugin):** داخل Claude Code، نفّذ `/plugin marketplace add lgqyhm2010/loop-goal`
  ثم `/plugin install loop-goal@lgqyhm2010`
- **يدوياً:** انسخ `skills/loop-goal/` إلى `.claude/skills/`

### OpenAI Codex

- **كمهارة:** `npx skills add lgqyhm2010/loop-goal -a codex` — يُثبَّت في
  `.agents/skills/loop-goal/`. يُنصح بالتثبيت على مستوى المشروع.
- **دائمة التفعيل:** انسخ المؤشر (pointer) من [`AGENTS.md`](AGENTS.md) إلى
  ملف `AGENTS.md` الخاص بمستودعك (أو `~/.codex/AGENTS.md`) حتى يُحمَّل الانضباط دائماً.

### GitHub Copilot

- **كمهارة:** `npx skills add lgqyhm2010/loop-goal -a github-copilot` — يُثبَّت
  في `.agents/skills/loop-goal/`.
- **دائمة التفعيل (موصى بها):** انسخ المؤشر من
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md) إلى ملف
  `.github/copilot-instructions.md` الخاص بمستودعك.

> **ملاحظات.** بالنسبة لـ Codex، يُفضَّل التثبيت على مستوى المشروع أو مسار
> `AGENTS.md` — فمسار الأداة الشامل (`-g`) (`~/.codex/skills/`) قد لا يطابق
> المكان الذي يقرأ منه Codex المهارات الشاملة. أما بالنسبة لـ Copilot، فمسار
> `.github/copilot-instructions.md` هو الطريقة الأكثر موثوقية لإبقاء الانضباط
> دائم التفعيل.

بمجرد التثبيت، اكتفِ بوصف مهمة حلقية أو تعمل حتى الإنجاز — تُفعَّل
المهارة من تلقاء نفسها (انظر [متى تُفعَّل](#متى-تُفعَّل)).

## المشكلة

تفشل مهام الوكيل طويلة الأمد بثلاث طرق خفيّة:

1. **فقدان التقدّم** — يجري ضغط سياق المحادثة فينسى
   الوكيل ما سبق أن أنجزه.
2. **تلوّث السياق** — تتراكم مخرجات الأدوات عبر التكرارات،
   مما يُضعف الاستدلال على مدى تشغيل طويل.
3. **غياب المخرج** — حلقة بلا شرط توقّف مكتوب تعمل إلى الأبد.

الحلول معروفة جيداً (حفظ نقطة مرجعية في ملف، عزل السياق لكل
تكرار، وكتابة شرط الخروج). المشكلة أنها تعتمد على *تذكّر* الوكيل
لتنفيذها — والانضباط ينحرف على مدى تشغيل طويل. تحوّل هذه المهارة
الحلول الثلاثة إلى قواعد مُلزَمة.

## ماذا تفعل

عند استدعائها، تقوم المهارة بما يلي:

1. **تكتشف الوضع** — LOOP (مدفوع بالوقت، متكرّر) مقابل GOAL
   (مدفوع بالنتيجة، يعمل حتى الإنجاز).
2. **تفرض ملف نقطة مرجعية** — يحمل `.loopgoal/state.json`
   الحالة القابلة للاستعادة الوحيدة؛ وتحمل التزامات git السجلّ التاريخي.
3. **تُنفِّذ ست قواعد** — التهيئة بشرط خروج صريح، وتشغيل
   كل تكرار في وكيل فرعي جديد (عزل السياق)، وحفظ نقطة مرجعية
   بترتيب ثابت، والتحقّق عند الاستئناف، وتسجيل القرارات، والخروج بنظافة.

إنها **انضباط خالص**: لا تكتب أي شيفرة، ولا تشغّل أي أوامر، ولا
تُغلّف `/loop` أو `/schedule` — بل تقيّد *كيفية* تشغيلها.

## متى تُفعَّل

عبارات مثل "loop" و"goal" و"keep running" و"run in a loop" و"until X"
و"run autonomously" — أو ما يكافئها بالصينية "持续做" و"每隔" و"循环跑"
و"直到…为止" و"自主跑" و"跑个 loop" — أو طلب صريح "use the loop-goal skill".

## قائمة بذاتها

تعمل في أي مشروع. تعتمد فقط على الأدوات المدمجة (`Agent` وgit)
وآليات البنية المضيفة (`/loop` و`ScheduleWakeup`). أما إضافة superpowers
فهي رفيق اختياري، وليست شرطاً على الإطلاق.

## الملفات

- `skills/loop-goal/SKILL.md` — المهارة نفسها: اكتشاف الوضع، وصيغة نقطة
  المرجعية، والقواعد الست.
- `skills/loop-goal/templates/state.json` — هيكل نقطة المرجعية، يُنسخ إلى
  المشروع بموجب القاعدة R1.
- `.claude-plugin/` — بيانات وصفية (manifests) لإضافة Claude Code والسوق (marketplace).
- `AGENTS.md`، `.github/copilot-instructions.md` — مؤشرات (pointers) رفيعة
  دائمة التفعيل لـ Codex وCopilot.
- `DESIGN.md` — الأساس المنطقي للتصميم والقرارات.


Host capability contract: [canonical skill](../../skills/loop-goal/SKILL.md#host-capabilities-and-permission-boundaries). Tool-specific examples require available host tools and authorization; use documented fallbacks for no subagent, no Git, read-only, or no shell.
