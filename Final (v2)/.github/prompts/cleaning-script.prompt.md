---
name: "cleaning-script"
description: "Use when: standalone generation of safe Python starter cleaning script"
argument-hint: "Paste input file, schema, quality issues, cleaning rules"
agent: "agent"
---

Use constraints from [Requirements](../../Requirements.md) and [Notes](../../Notes.md).

Input:
{{input}}

Constraints:
- Do not delete records unless rule is explicitly provided.
- Include before/after logging.
- If cleaning rules are ambiguous, ask up to 5 concise questions first.

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided file/schema/issues/rules in 3-6 bullets.

## 2) Core analysis
- Complete Python starter script.
- Human edits required before production.

## 3) Priority actions
- Step-by-step run order and quick cautions.

## 4) Manual verification checklist
- Post-run verification checklist.

## 5) Block dán vào `ai-trace.md`
- A concise markdown block ready to paste.
