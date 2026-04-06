---
name: "insight-hypothesis"
description: "Use when: standalone generation of hypothesis-driven questions and chart ideas"
argument-hint: "Paste topic + columns + quality-check summary"
agent: "agent"
---

Use constraints from [Requirements](../../Requirements.md) and [Notes](../../Notes.md).

Input:
{{input}}

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided topic/columns/quality notes in 3-6 bullets.

## 2) Core analysis
- 8 hypotheses.
- For each: question, variables, chart, viva value, required evidence.

## 3) Priority actions
- Top 3 hypotheses to validate first + why.

## 4) Manual verification checklist
- Checklist items team must verify manually for each selected hypothesis.

## 5) Block dán vào `ai-trace.md`
- A concise markdown block ready to paste.

Important:
- Use hypothesis language only; no unverified final claims.
