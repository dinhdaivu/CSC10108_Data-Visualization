---
name: "source-reliability"
description: "Use when: standalone source trust and citation audit for viva/report"
argument-hint: "Paste source link, publisher, date accessed, metadata"
agent: "agent"
---

Use constraints from [Requirements](../../Final (v2)/Requirements.md) and [Notes](../../Final (v2)/Notes.md).

Input:
{{input}}

Behavior:
- If source evidence is incomplete, explicitly mark confidence as limited.
- Do not claim high trust without justification.

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided source evidence in 3-6 bullets.

## 2) Core analysis
- Trust level: High/Medium/Low + reason.
- Strengths vs weaknesses table.
- Bias risks + mitigations.

## 3) Priority actions
- Missing citations/metadata to add, prioritized.

## 4) Manual verification checklist
- Checklist items team must verify manually.

## 5) Block dán vào `ai-trace.md`
- A concise markdown block ready to paste.
