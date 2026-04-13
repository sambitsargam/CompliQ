# CompliQ Frontend Design

## 1. UX Goals

- Communicate product value in under 10 seconds.
- Provide immediate confidence with visible system health.
- Make analysis artifacts easy to skim for non-technical users.

## 2. Information Architecture

### Landing Page

- Hero (brand, tagline, CTA)
- Product snapshot (coverage/risk mock values)
- Feature highlights (3 cards)

### Dashboard

- KPI cards for health/documents/open tasks
- Recent document list
- Action queue list
- API connection visibility for debugging/demo

## 3. Visual Direction

- Color palette avoids generic purple templates.
- Uses mint/sky/ink for clarity and trust.
- Soft shadows and rounded containers for enterprise polish.
- Dot-grid background and layered gradients for depth.

## 4. Component Strategy

Reusable components:

- `StatCard`
- `SectionCard`

These keep styling consistent and simplify future expansion.

## 5. Data Flow

- `fetchJson()` utility reads from backend base URL.
- Dashboard loads health, documents, and tasks in parallel.
- API errors surface in an inline warning block.
