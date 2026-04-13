# CompliQ Agent Design (Neuro-SAN)

## 1. Objective

The CompliQ agent network transforms unstructured policy text into structured compliance artifacts with explainable findings and actionable tasks.

## 2. Why Multi-Agent

Compliance checks involve multiple reasoning modes:

- extraction (what is written)
- mapping (which control it belongs to)
- diagnosis (what is missing)
- scoring (how risky is it)
- planning (what to do next)

Splitting these into specialist agents improves explainability and keeps prompts focused.

## 3. Agent Roles

### ComplianceFrontman

- Main orchestrator
- Enforces strict JSON contract
- Combines specialist outputs

### DocParserAgent

- Extracts obligations and evidence phrases

### RuleMapperAgent

- Aligns text to control categories

### GapDetectorAgent

- Produces gap/finding candidates

### RiskScorerAgent

- Computes normalized risk and coverage
- Can call deterministic scoring tool

### ActionPlannerAgent

- Converts findings into remediation tasks

## 4. Coded Tools

### RiskScoringTool

- Input: severity counts + control baseline
- Output: normalized coverage and risk

### ReportFormatterTool

- Ensures final output shape remains backend compatible

## 5. Output Contract

The network must return strict JSON with these keys:

- `coverage_percent`
- `risk_score`
- `summary`
- `findings[]`
- `tasks[]`

This design ensures backend APIs remain stable whether output is from deterministic fallback logic or Neuro-SAN LLM orchestration.
