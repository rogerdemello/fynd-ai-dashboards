# Fynd AI Intern - Take Home Assessment

**Submission for AI Engineering Intern Position**

This repository contains the complete implementation of the Fynd AI take-home assessment, including:
- **Task 1**: Rating prediction via prompting (3 different approaches)
- **Task 2**: Two-dashboard AI feedback system (User + Admin interfaces)

---

## 🔗 Live Deployments

### Task 2 - Deployed Dashboards

- **User Dashboard**: https://fynd-ai-dashboards-user.streamlit.app
- **Admin Dashboard**: https://fynd-ai-dashboards-exec.streamlit.app  
- **Backend API**: https://fyndaidashboards.onrender.com

All dashboards are fully functional and connected to the backend.

---

## 📋 Repository Structure

```
fynd-ai-dashboards/
├── notebooks/
│   ├── run_prompt_experiments.py      # Task 1: Prompting experiments
│   └── task1_results/                  # Evaluation results & metrics
│       ├── results_baseline.csv
│       ├── results_few_shot.csv
│       ├── results_chain_of_thought.csv
│       └── summary.json
├── src/
│   ├── backend/                        # FastAPI backend server
│   │   ├── main.py                     # API endpoints
│   │   ├── database.py                 # SQLite database layer
│   │   └── llm_service.py              # Gemini LLM integration
│   └── dashboards/                     # Streamlit dashboards
│       ├── user_dashboard.py           # Public submission interface
│       └── admin_dashboard.py          # Internal analytics view
├── data/
│   └── yelp.csv                        # Sample dataset (200 reviews)
├── tests/
│   └── test_backend.py                 # Backend integration tests
├── docs/
│   ├── Fynd AI Intern – Take Home Assessment.pdf
│   └── DEPLOYMENT.md                   # Deployment instructions
├── requirements.txt                    # Python dependencies
├── Procfile                            # Render deployment config
├── REPORT.md                           # Detailed assessment report
└── README.md                           # This file
```

---

## 🚀 Task 1: Rating Prediction via Prompting

### Overview
Designed and evaluated **3 different prompting strategies** for classifying Yelp reviews into 1-5 star ratings using Google Gemini API.

### Prompting Approaches

1. **Baseline Prompt**: Direct classification with minimal context
2. **Few-Shot Learning**: Provided 3 example reviews with ratings
3. **Chain-of-Thought**: Encouraged step-by-step reasoning before prediction

### Key Results

| Approach | Accuracy | JSON Validity | Notes |
|----------|----------|---------------|-------|
| Baseline | 78% | 96% | Fast, simple, reliable |
| Few-Shot | 82% | 97% | Better calibration with examples |
| Chain-of-Thought | 80% | 95% | More detailed explanations |

**Best Performer**: Few-shot learning (82% accuracy, 97% JSON validity)

### Running Task 1

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (optional; runs in simulation mode without it)
export GEMINI_API_KEY="your-gemini-api-key"

# Run experiments
python notebooks/run_prompt_experiments.py

# Results saved to notebooks/task1_results/
```

**Simulation Mode**: The experiment runner includes synthetic data generation and runs without requiring an API key for quick testing.

---

## 🎯 Task 2: Two-Dashboard AI Feedback System

### Architecture

```
┌─────────────────┐
│  User Dashboard │ ──┐
└─────────────────┘   │
                      ▼
                ┌──────────────┐      ┌────────────┐
                │ FastAPI      │◄────►│  Gemini    │
                │ Backend      │      │  API       │
                └──────────────┘      └────────────┘
                      ▲
┌─────────────────┐   │
│ Admin Dashboard │ ──┘
└─────────────────┘
```

### Features

#### User Dashboard (Public)
- ⭐ 1-5 star rating selector
- 📝 Review text submission form
- 💬 AI-generated personalized response
- ✅ Submission confirmation with ID

#### Admin Dashboard (Internal)
- 📊 Live analytics (total submissions, average rating, distribution)
- 📋 Complete submission history with:
  - Customer review & rating
  - AI-generated response (what user sees)
  - Internal AI summary
  - Recommended action
- 🔄 Auto-refresh option
- 📈 Visual rating distribution chart

### Technology Stack

- **Backend**: FastAPI + uvicorn
- **Database**: SQLite (thread-safe)
- **LLM**: Google Gemini API
- **Frontend**: Streamlit
- **Hosting**: Render (backend) + Streamlit Community Cloud (dashboards)

### Running Locally

#### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your-gemini-api-key"  # Optional
export API_URL="http://localhost:8000"
```

#### 2. Start Backend

```bash
cd src/backend
uvicorn main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

#### 3. Start Dashboards

```bash
# User Dashboard
streamlit run src/dashboards/user_dashboard.py --server.port 8501

# Admin Dashboard (in separate terminal)
streamlit run src/dashboards/admin_dashboard.py --server.port 8502
```

- User Dashboard: http://localhost:8501
- Admin Dashboard: http://localhost:8502

### API Endpoints

- `GET /` - Health check
- `POST /api/submit` - Submit review (returns AI response)
- `GET /api/submissions` - Get all submissions (admin)
- `GET /api/analytics` - Get analytics summary

### Testing

```bash
# Run backend tests
python tests/test_backend.py

# Test backend API
curl http://localhost:8000/
curl http://localhost:8000/api/analytics

# Submit test review
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "review": "Excellent service!"}'
```

---

## 🔑 Environment Variables

### Backend (Required for deployment)
```bash
GEMINI_API_KEY=your-gemini-api-key  # Optional; uses fallback responses without it
```

### Dashboards (Streamlit Cloud Secrets)
```toml
API_URL = "https://fyndaidashboards.onrender.com"
GEMINI_API_KEY = "your-gemini-api-key"  # Optional
```

---

## 📦 Deployment Guide

### Backend (Render)
1. Connect GitHub repository
2. Set start command: `cd src/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add environment variable: `GEMINI_API_KEY`
4. Deploy

### Dashboards (Streamlit Community Cloud)
1. New app → Select repository
2. Main file: `src/dashboards/user_dashboard.py` (or `admin_dashboard.py`)
3. Add secrets in Settings → Secrets
4. Deploy

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

---

## 📊 Evaluation & Results

### Task 1 Highlights
- **200 sample reviews** evaluated across 3 prompting strategies
- **97% JSON validity** achieved with schema enforcement
- **82% accuracy** (best: few-shot learning)
- **Simulation mode** for quick testing without API costs

### Task 2 Highlights
- ✅ Both dashboards deployed and publicly accessible
- ✅ Full CRUD operations with SQLite persistence
- ✅ AI-powered response generation and summarization
- ✅ Real-time analytics and visualization
- ✅ Production-ready with error handling and CORS

---

## 📄 Documentation

- **[REPORT.md](REPORT.md)**: Detailed technical report with:
  - Prompt engineering iterations
  - Evaluation methodology & results
  - Architecture decisions
  - Deployment strategy
  
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**: Step-by-step deployment guide for:
  - Streamlit Community Cloud
  - Render
  - Hugging Face Spaces
  - Railway

---

## 🛠️ Dependencies

Key packages (see [requirements.txt](requirements.txt) for full list):
- `fastapi` - Backend API framework
- `uvicorn` - ASGI server
- `streamlit` - Dashboard framework
- `google-generativeai` - Gemini API client
- `pandas` - Data manipulation
- `pydantic` - Data validation

---

## 🔍 Assessment Deliverables Checklist

- ✅ **GitHub Repository** with all code
- ✅ **Python notebook** for Task 1 (`notebooks/run_prompt_experiments.py`)
- ✅ **Application code** for Task 2 (`src/backend/`, `src/dashboards/`)
- ✅ **Deployed User Dashboard** (public URL provided)
- ✅ **Deployed Admin Dashboard** (public URL provided)
- ✅ **Short Report** ([REPORT.md](REPORT.md))
- ✅ **3+ Prompting Approaches** with evaluation
- ✅ **Comparison Table** and discussion
- ✅ **LLM Integration** for responses, summaries, and recommendations

---

## 📧 Contact

For questions or clarifications about this submission, please contact via GitHub issues or the email provided in the application.

---

## 📝 License

This project was created as part of the Fynd AI Intern take-home assessment.
