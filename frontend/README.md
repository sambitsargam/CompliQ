# CompliQ Frontend

## Purpose

The frontend provides:

1. A polished landing page with value proposition and feature overview.
2. A dashboard that reads backend APIs for health, documents, and tasks.

## Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS

## Run

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Views

### Landing (`/`)

- Brand intro and tagline
- CTA to open dashboard
- Feature cards
- Snapshot panel

### Dashboard (`/dashboard`)

- Service health card
- Documents count card
- Open tasks card
- API base reference
- Recent documents panel
- Action queue panel

## API Assumptions

Frontend expects backend at:

- `NEXT_PUBLIC_API_BASE_URL` (default `http://localhost:8000`)

Read endpoints:

- `GET /health`
- `GET /api/v1/documents`
- `GET /api/v1/tasks`
