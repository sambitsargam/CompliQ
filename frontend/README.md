# CompliQ Frontend

The frontend provides two user-facing experiences:
- A landing page for storytelling and product value communication.
- A dashboard for running the complete analysis flow.

## Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS

## Routes

- `/` : Landing page
- `/dashboard` : Interactive compliance workspace

## What the Dashboard Supports

1. Backend health verification
2. Document upload
3. Multi-document selection
4. Analysis execution
5. Findings and tasks rendering
6. Report content rendering
7. Inline error visibility

## Folder Structure

```text
frontend/
├── app/
│   ├── dashboard/page.tsx     # main workspace flow
│   ├── page.tsx               # landing page
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── section-card.tsx
│   └── stat-card.tsx
├── lib/
│   └── api.ts                 # API helper wrappers
├── package.json
└── tailwind.config.ts
```

## Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Environment Configuration

The frontend uses:
- `NEXT_PUBLIC_API_BASE_URL`

Default expected local value:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## API Integration Details

The UI calls:
- `GET /health`
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{analysis_id}`
- `GET /api/v1/tasks`
- `GET /api/v1/reports/{analysis_id}/content`

Helper methods in `lib/api.ts`:
- `fetchJson`
- `postJson`
- `postFile`
- `fetchText`

## UX Behavior Notes

- Dashboard loads health, documents, and tasks in parallel for faster render.
- Upload control accepts a single file at a time.
- Users must select at least one document before analysis.
- API failures are shown in an inline warning block.
- Analysis output cards and report panel render only after a successful run.

## Styling Direction

The UI intentionally avoids generic defaults and uses:
- clear spacing with card-based layout
- soft enterprise-safe color palette
- high readability for demo and judge walkthrough

## Demo Tips

For a smooth live demo:
1. Start backend first and verify `/health`.
2. Keep one short sample policy text ready.
3. Upload, select, run analysis in under 60 seconds.
4. Explain findings and task priorities.
5. Show generated report content as proof artifact.

## Troubleshooting

1. Frontend starts but data does not load:
- Verify backend is running.
- Check `NEXT_PUBLIC_API_BASE_URL`.

2. Upload fails:
- Verify backend `/api/v1/documents/upload` is reachable.

3. Analysis button returns error:
- Ensure at least one document checkbox is selected.
- Verify selected IDs still exist in backend response.

## Planned Frontend Enhancements

- Better severity visualization (badges/charts)
- Download report button
- Sorting and filtering for findings/tasks
- Inline framework selector
- Loading skeletons and improved empty states
