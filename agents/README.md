# CompliQ Agent Layer (Neuro-SAN)

This directory contains the Neuro-SAN configuration and coded tools for CompliQ.

## Goals

The agent network is designed to produce structured compliance output in a format consumable by the backend API:

- Coverage percent
- Risk score
- Findings list
- Task list
- Executive summary

## Agent Topology

CompliQ uses a frontman orchestration model with specialist sub-agents:

1. `ComplianceFrontman` — receives user/business inquiry and orchestrates the workflow.
2. `DocParserAgent` — extracts obligations and control-relevant statements.
3. `RuleMapperAgent` — maps extracted evidence to control categories.
4. `GapDetectorAgent` — identifies missing controls and policy gaps.
5. `RiskScorerAgent` — scores severity and computes normalized risk profile.
6. `ActionPlannerAgent` — converts findings into owner-based tasks.
7. `RiskScoringTool` — deterministic helper for baseline score normalization.
8. `ReportFormatterTool` — formats structured JSON output.

## Runtime Requirements

- `OPENAI_API_KEY` in environment.
- `AGENT_MANIFEST_FILE` pointing to `agents/registries/manifest.hocon`.
- `AGENT_TOOL_PATH` pointing to `agents/coded_tools`.

## Files

- `registries/manifest.hocon` — active agent manifest.
- `registries/llm_config.hocon` — shared model settings.
- `registries/compliq.hocon` — network definition.
- `coded_tools/compliq/risk_scoring.py` — deterministic score helper.
- `coded_tools/compliq/report_formatter.py` — output shaping tool.

## Expected Output Contract

The frontman returns JSON with this shape:

```json
{
  "coverage_percent": 72.5,
  "risk_score": 64.0,
  "summary": "...",
  "findings": [
    {
      "title": "...",
      "severity": "high",
      "evidence": "...",
      "recommendation": "..."
    }
  ],
  "tasks": [
    {
      "title": "...",
      "owner": "Compliance Owner",
      "priority": "P1",
      "due_in_days": 7
    }
  ]
}
```
