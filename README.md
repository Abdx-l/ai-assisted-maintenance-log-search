# AI-Assisted Maintenance Log Search

PostgreSQL pgvector and full-text hybrid ranking with equipment/severity/date filters, synthetic seed generation, a FastAPI endpoint, and a React search view.

## Run

Run schema.sql in PostgreSQL with pgvector. Set DATABASE_URL, install requirements.txt, run `python seed.py` and `uvicorn app:app`. UI: `cd web && npm install && npm run dev`.
