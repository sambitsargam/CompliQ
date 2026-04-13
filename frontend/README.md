# CompliQ Frontend

The frontend includes a landing page and an interactive dashboard for running end-to-end compliance analysis.

## 1. Views

### Landing (`/`)

- Hero section with value proposition
- Product output snapshot
- Feature highlights
- CTA to dashboard

### Dashboard (`/dashboard`)

- Backend health indicator
- Document upload widget
- Document multi-select list
- Analysis trigger button
- Findings and tasks view
- Report content viewer

## 2. Stack

- Next.js App Router
- TypeScript
- Tailwind CSS

## 3. Local Run

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## 4. API Integration

The dashboard reads/writes to backend endpoints:

- `GET /health`
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{analysis_id}`
- `GET /api/v1/tasks`
- `GET /api/v1/reports/{analysis_id}/content`

Base URL is configured via:

- `NEXT_PUBLIC_API_BASE_URL`
