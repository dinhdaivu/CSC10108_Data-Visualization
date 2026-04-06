---
name: "dashboard-critic"
description: "Use when: standalone dashboard critique for clarity, analysis depth, and viva readiness"
argument-hint: "Paste goal + chart list + filters + screenshot summary"
agent: "agent"
---

Use constraints from [Requirements](../../Requirements.md) and [Notes](../../Notes.md).

Input:
{{input}}

Behavior:
- If screenshot/layout details are missing, ask for them briefly before final review.

Review criteria:
- clarity/readability
- chart appropriateness
- linkage among visuals
- interaction/navigation
- color usage
- analysis depth (not only presentation)

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided goal/charts/filters/layout details in 3-6 bullets.

## 2) Core analysis
- 3 strongest points.
- 5 urgent fixes (priority order).
- Concrete improvements.

## 3) Priority actions
- Immediate next 5 dashboard edits in execution order.

## 4) Manual verification checklist
- Checklist items team must verify manually.

## 5) Block dán vào `ai-trace.md`
- Include the 60-90 second Vietnamese viva explanation draft and key review notes.
