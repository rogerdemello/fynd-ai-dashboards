# Detailed Task Checklist & Implementation Plan

## Overview
This checklist breaks down the two assessment tasks into actionable subtasks, priorities, estimated effort, and deliverables so you can implement them efficiently.

---

## Priority & timeline (recommended)
- Priority A (core, 0–3 days): Task 1 experiments, minimal User Dashboard, data storage, short report draft.
- Priority B (3–7 days): Admin Dashboard, deployment, tests, polishing, README and report finalisation.
- Priority C (7+ days): CI, analytics, extra UX polish.

---

## Task 1 — Rating Prediction via Prompting
Goal: design 3+ prompt strategies to classify Yelp reviews (1–5 stars), return JSON with `predicted_stars` and `explanation`.

Subtasks:
- 1.1 Dataset acquisition & sample (~200 rows): download or sample from Kaggle dataset. (1–2 hrs)
- 1.2 Baseline prompt (direct ask): craft simple prompt asking for 1–5 stars and short explanation. (1 hr)
- 1.3 Contextual prompt (include few-shot examples): prepare 3–5 labeled examples in prompt. (2–3 hrs)
- 1.4 Chain-of-thought / explanation-first prompt: ask LLM to reason then output JSON. (2–3 hrs)
- 1.5 Prompt engineering iterations: refine for JSON-valid outputs and stability. (2–4 hrs)
- 1.6 Evaluation harness: run prompts on sampled set, compute accuracy (rounded to nearest star), JSON validity rate, and consistency (repeatability). (2–3 hrs)
- 1.7 Document results: table comparing prompts, example outputs, short discussion. (1–2 hrs)

Deliverables:
- `notebooks/task1_prompting.ipynb` with prompt code, evaluation, and result tables.
- A `task1_results.csv` (or embed in notebook) and short writeup in report.

Recommended tools/stacks:
- Python + `openai` / OpenRouter / other LLM bindings; use `requests` if using other APIs.
- `pandas` for data handling; `pytest` for any small test harness.

Notes:
- If output JSON is malformed, wrap prompt with strict JSON schema and add post-processing/repair.

---

## Task 2 — Two-Dashboard AI Feedback System
Goal: Web app with User Dashboard (public) and Admin Dashboard (internal). Both must be deployed and share a data store.

Subtasks:
- 2.1 Data model & storage (shared): choose a file-backed store (CSV/JSON) or lightweight DB (SQLite). (1–2 hrs)
- 2.2 Backend API: simple FastAPI/Flask service to read/write submissions and expose endpoints for dashboards. (2–4 hrs)
- 2.3 LLM integration: endpoint to call LLM for summarisation, recommended actions, and user response. (2–4 hrs)
- 2.4 User Dashboard: implement quick UI (Streamlit/Gradio/React) to submit rating + review and display AI response. (2–4 hrs)
- 2.5 Admin Dashboard: implement UI to list submissions live, show LLM outputs, and simple analytics (counts, avg rating). (3–5 hrs)
- 2.6 Persistence & concurrency: ensure read/write atomicity for shared store (file locks or DB). (1–2 hrs)
- 2.7 Deployment: choose platform(s) — Hugging Face Spaces for Streamlit/Gradio, Vercel/Render for Node/React or FastAPI. (2–4 hrs)
- 2.8 Testing & polish: manual checks, small unit tests for API. (2–3 hrs)

Deliverables:
- Source code in `app/` or `dashboard/` folders, README with run/deploy steps.
- Deployed URLs for both dashboards.

Recommended minimal stack for fast delivery:
- Backend: `FastAPI` + `uvicorn`, store data in `submissions.db` (SQLite).
- Dashboards: `Streamlit` for both dashboards (fast to build + deploy on Spaces) OR Streamlit user + lightweight admin React if preferred.
- LLM: any accessible API; keep API key in env var.

---

## Cross-cutting tasks
- A. Repository structure: root README, `notebooks/`, `app/`, `tasks/text/`, `scripts/`. (done/partial)
- B. Report: short PDF describing approach + prompt iterations + evaluation. (ongoing)
- C. Tests: smoke tests for API and end-to-end submission flow. (optional but recommended)
- D. Deployment checklist: env vars, secrets, scaling notes, and public URLs.

---

## Branching & workflow suggestions
- `main` — final submission-ready code.
- `task1/experiment-*` — prompt experiments per approach.
- `task2/backend`, `task2/user-dashboard`, `task2/admin-dashboard` — feature branches.

---

## Immediate next steps (I can do next)
1. Run Task 1 experiments on 200 samples and produce `notebooks/task1_prompting.ipynb`. 
2. Scaffold `FastAPI` backend + simple `Streamlit` User dashboard and demo data store.

If you want, I can start with step 1 (Task 1 experiments) now — run a set of 3 prompt strategies on 200 sample reviews and produce results.
