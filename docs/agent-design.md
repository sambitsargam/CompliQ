# CompliQ Agent Design (Neuro-SAN)

## 1. Purpose

The Neuro-SAN layer gives CompliQ an agentic reasoning path that can:
- interpret policy language semantically
- produce structured compliance findings
- generate actionable remediation tasks
- stay aligned to a strict backend contract

## 2. Design Principles

1. Contract-first output
- Agent network must return JSON matching backend schema.

2. Specialist decomposition
- Separate parsing, mapping, detection, scoring, and planning concerns.

3. Deterministic support tools
- Use coded tools where numeric normalization/format guarantees are required.

4. Fail-safe integration
- Any agent failure triggers deterministic backend fallback.

## 3. Agent Network Topology

### `ComplianceFrontman`

Role:
- orchestrates the full reasoning chain
- enforces JSON-only final output
- coordinates specialist tools/agents

Input:
- merged policy text from backend

Output:
- strict JSON payload compatible with `AnalysisResult`

### `DocParserAgent`

Role:
- extract obligations and signals related to control domains

Expected extraction domains:
- policy ownership
- review cadence
- incident response
- data retention
- access governance

### `RuleMapperAgent`

Role:
- normalize extracted evidence into control buckets for consistent scoring and gap reasoning

### `GapDetectorAgent`

Role:
- identify missing, weak, or ambiguous controls
- generate concise finding candidates

### `RiskScorerAgent`

Role:
- transform findings into normalized coverage/risk outputs
- optionally delegate to deterministic scoring tool

### `ActionPlannerAgent`

Role:
- generate one or more remediation tasks per finding
- assign owner, priority, and due window

## 4. Coded Tools

### `RiskScoringTool`

Purpose:
- deterministic normalization from severity counts

Input:
- high, medium, low counts
- total_controls

Output:
- `coverage_percent`
- `risk_score`

### `ReportFormatterTool`

Purpose:
- produce final output object with required key set and value types

## 5. Manifest and Registry Files

- `agents/registries/manifest.hocon` selects active network files
- `agents/registries/compliq.hocon` defines agents, instructions, and tool wiring
- `agents/registries/llm_config.hocon` central runtime model settings

## 6. Backend Integration Contract

The backend expects this shape from Neuro-SAN:

```json
{
  "coverage_percent": 0,
  "risk_score": 0,
  "summary": "",
  "findings": [
    {
      "title": "",
      "severity": "high",
      "evidence": "",
      "recommendation": ""
    }
  ],
  "tasks": [
    {
      "title": "",
      "owner": "",
      "priority": "P1",
      "due_in_days": 7
    }
  ]
}
```

Any invalid or unparseable output causes backend fallback.

## 7. Runtime Lifecycle

1. Backend prepares merged text.
2. Adapter creates direct Neuro-SAN session (`agent_name=compliq`).
3. Adapter reads streamed messages until done.
4. Adapter extracts JSON from text output.
5. Adapter maps payload to backend schemas.
6. If any step fails, adapter returns `None`.
7. Backend executes deterministic analysis path.

## 8. Quality and Guardrails

Current safeguards:
- strict prompt instructions for JSON-only response
- deterministic formatter tool
- schema mapping in backend before persistence

Recommended additions:
- JSON schema validation before acceptance
- finding/task count sanity checks
- confidence scoring per finding
- explicit control coverage explanation array

## 9. Extensibility Strategy

Short-term enhancements:
- framework-conditioned prompts (SOC2-lite, ISO-like, HIPAA-lite)
- region-based compliance heuristics
- stronger evidence extraction and quoting

Long-term enhancements:
- retrieval-augmented regulatory references
- human review loop for finding approval
- longitudinal trend analysis across runs

## 10. Known Constraints

- Agent output quality depends on source text quality.
- Current MVP parsing is text-first and not optimized for complex binary documents.
- Frontman instruction discipline is required to avoid markdown/prose leakage.

## 11. Why This Design Works for Hackathon

- Demonstrates clear agentic architecture (multi-agent + tools).
- Maintains reliability for live judging.
- Produces business-friendly outputs judges can score quickly.
