# CompliQ Agent Layer (Neuro-SAN)

This directory defines the Neuro-SAN multi-agent network used by CompliQ.

The backend can invoke this network to generate structured compliance output. If agent execution fails, backend falls back to deterministic analysis for reliability.

## Agentic Purpose

The Neuro-SAN path is used to:
1. Parse policy text semantically.
2. Map evidence to compliance control buckets.
3. Detect control gaps.
4. Score risk and coverage.
5. Create actionable remediation tasks.
6. Return strict JSON that backend persists and serves.

## Topology

CompliQ currently uses a frontman + specialist design:

1. `ComplianceFrontman`
- Orchestrator entrypoint.
- Enforces strict output contract.
- Delegates to specialist agents and formatter tool.

2. `DocParserAgent`
- Extracts obligations, ownership, cadence, incident, retention, and access-related evidence.

3. `RuleMapperAgent`
- Maps extracted evidence into normalized control categories.

4. `GapDetectorAgent`
- Produces gap candidates with severity and recommendations.

5. `RiskScorerAgent`
- Computes normalized coverage/risk.
- Can use `RiskScoringTool` for deterministic weighting.

6. `ActionPlannerAgent`
- Converts findings into execution-ready tasks with owner, priority, and due windows.

7. `ReportFormatterTool`
- Ensures strict JSON structure for backend ingestion.

## Required Output Contract

The final frontman output must be valid JSON with keys:
- `coverage_percent`
- `risk_score`
- `summary`
- `findings`
- `tasks`

Expected shape:

```json
{
  "coverage_percent": 72.5,
  "risk_score": 64.0,
  "summary": "CompliQ scanned policy artifacts...",
  "findings": [
    {
      "title": "Policy ownership missing",
      "severity": "high",
      "evidence": "No clear owner keyword found...",
      "recommendation": "Assign a compliance owner..."
    }
  ],
  "tasks": [
    {
      "title": "Resolve: Policy ownership missing",
      "owner": "Compliance Owner",
      "priority": "P1",
      "due_in_days": 7
    }
  ]
}
```

## Directory Contents

```text
agents/
├── registries/
│   ├── manifest.hocon         # selects active network files
│   ├── llm_config.hocon       # shared model/runtime config
│   └── compliq.hocon          # network definition and prompts
└── coded_tools/
    └── compliq/
        ├── risk_scoring.py    # deterministic scoring helper
        └── report_formatter.py# output normalization helper
```

## Environment Variables

These values must be available when backend analysis runs:
- `OPENAI_API_KEY`
- `AGENT_MANIFEST_FILE`
- `AGENT_TOOL_PATH`
- `USE_NEURO_SAN`

Recommended local values (from `backend/` execution context):

```env
USE_NEURO_SAN=true
AGENT_MANIFEST_FILE=../agents/registries/manifest.hocon
AGENT_TOOL_PATH=../agents/coded_tools
```

## How Backend Uses It

The backend service `run_neuro_san_analysis`:
1. Resolves default manifest/tool paths if env is missing.
2. Extends `PYTHONPATH` to include tool modules.
3. Creates direct Neuro-SAN session with agent `compliq`.
4. Streams responses until done.
5. Extracts JSON payload from plain text response.
6. Converts payload into backend `AnalysisResult` schema.

If any step fails, `None` is returned and fallback logic executes.

## Reliability Strategy

To keep live demos safe:
- Agent path is optional at runtime.
- Deterministic path always exists.
- API contracts are identical for both paths.

This prevents frontend breakage even during external model/runtime instability.

## Extension Guidance

To improve the network after hackathon:
1. Add framework-specific mapping prompts (SOC2-lite, ISO27001-lite).
2. Add confidence score per finding.
3. Add citation extraction (line-level evidence links).
4. Add region-aware compliance packs.
5. Add post-processing guardrail for schema validation before persistence.

## Debugging Notes

1. If Neuro-SAN output is empty:
- Verify API key and manifest path.
- Check tool imports under `coded_tools/compliq`.

2. If JSON parse fails:
- Ensure frontman instruction is strict JSON only.
- Keep formatter tool in frontman tool list.

3. If backend always falls back:
- Temporarily log adapter exceptions in `backend/app/services/neuro_san_adapter.py`.
- Confirm `USE_NEURO_SAN=true` in effective environment.
