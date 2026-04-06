---
name: "data-quality"
description: "Use when: standalone data quality audit (missing, duplicates, invalid formats, outliers)"
argument-hint: "Paste schema + 5-20 sample rows + domain notes"
agent: "agent"
---

Use constraints from [Requirements](../../Final (v2)/Requirements.md) and [Notes](../../Final (v2)/Notes.md).

Input:
{{input}}

Behavior:
- If sample is insufficient, request additional sample rows or column examples.
- Prioritize issues by impact on analysis.

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided schema/sample/domain notes in 3-6 bullets.

## 2) Core analysis
- Issue list with severity (High/Medium/Low).
- Potential anomaly-driven insights.

## 3) Priority actions
- Prioritized remediation steps.

## 4) Manual verification checklist
- Checklist items team must verify manually.

## 5) Block dán vào `ai-trace.md`
- A concise markdown block ready to paste.
