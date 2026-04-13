# CompliQ Backend

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Key Endpoints

- `GET /health`
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{analysis_id}`
- `GET /api/v1/tasks`
- `GET /api/v1/reports/{analysis_id}`
