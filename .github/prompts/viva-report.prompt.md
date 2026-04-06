---
name: "viva-report"
description: "Use when: standalone viva prep and AI usage summary with required evidence chain"
argument-hint: "Paste team list + verified insights + AI usage notes"
agent: "agent"
---

Use reporting chain requirement from [Notes](../../Final (v2)/Notes.md):
Prompt -> AI-generated script -> Human-edited script -> Verified result.

Input:
{{input}}

Behavior:
- If member list is missing, ask for names first.
- Keep outputs concise and in Vietnamese.

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided team/insights/AI-usage notes in 3-6 bullets.

## 2) Core analysis
- At least 2 viva questions per member + concise Vietnamese answers.
- 1 harder follow-up per question.
- Which evidence/file to open for each answer.
- Final Vietnamese AI-usage summary paragraph with required chain.

## 3) Priority actions
- Practice plan by member (short, prioritized).

## 4) Manual verification checklist
- Checklist items team must verify manually.

## 5) Block dán vào `ai-trace.md`
- A concise markdown block ready to paste.
