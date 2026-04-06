---
name: "gatekeeper"
description: "Use when: standalone requirement check for final project dataset (rows, variables, Vietnam ratio, source)"
argument-hint: "Paste dataset summary: rows, columns, source, Vietnam relevance"
agent: "agent"
---

Use constraints from [Requirements](../../Requirements.md) and [Notes](../../Notes.md).

Input:
{{input}}

Behavior:
- If critical inputs are missing, ask up to 5 concise clarification questions first.
- Never assume unknown values.

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided inputs in 3-6 bullets.

## 2) Core analysis
- PASS/FAIL table for each requirement.
- Missing information.

## 3) Priority actions
- Top 5 next actions in priority order.

## 4) Manual verification checklist
- Checklist items team must verify manually.

## 5) Block dán vào `ai-trace.md`
- A concise markdown block ready to paste.
