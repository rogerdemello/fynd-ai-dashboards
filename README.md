# Fynd AI Intern - Take Home Assessment

Complete implementation of the Fynd AI internship take-home assessment with two main tasks: rating prediction via prompting and a two-dashboard AI feedback system.

## 📋 Project Overview

This repository contains:
- **Task 1**: Rating prediction using multiple prompting approaches with Google Gemini
- **Task 2**: Full-stack web application with User and Admin dashboards
- Comprehensive documentation and deployment guides

## 🏗️ Project Structure

```
.
├── src/
│   ├── backend/
│   │   ├── main.py              # FastAPI backend server
│   │   ├── database.py          # SQLite database layer
│   │   ├── llm_service.py       # Gemini API integration
│   │   └── submissions.db       # SQLite database (auto-created)
│   ├── dashboards/
│   │   ├── user_dashboard.py    # Public review submission interface
│   │   └── admin_dashboard.py   # Internal analytics dashboard
│   └── extract_pdfs.py          # PDF text extraction utility
├── notebooks/
│   ├── run_prompt_experiments.py  # Task 1: Prompt testing script
│   └── task1_results/           # Experiment outputs (CSVs, JSON)
├── data/
│   └── yelp.csv                 # Dataset (optional)
├── docs/
│   ├── *.pdf                    # Assessment PDFs
│   ├── extracted_text/          # Extracted PDF content
│   ├── SUMMARY.md               # Project overview
│   ├── ROADMAP.md               # Timeline
│   ├── TASK_CHECKLIST.md        # Task breakdown
│   ├── DOCUMENTATION.md         # Technical details
│   ├── DEPLOYMENT.md            # Deploy guide
│   ├── GETTING_STARTED.md       # Quick start
│   └── SUBMISSION_CHECKLIST.md  # Final checklist
├── tests/
│   └── test_backend.py          # Backend tests
├── venv/                        # Python virtual environment
├── README.md                    # This file
├── REPORT.md                    # Assessment report
├── requirements.txt             # Dependencies
├── start_all.bat                # Windows launcher
└── start_all.sh                 # Linux/Mac launcher
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (3.12 recommended)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or navigate to the project:**
```bash
cd "e:/Fynd AI"
```

2. **Activate the virtual environment:**

Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

Windows (Command Prompt):
```cmd
venv\Scripts\activate.bat
```

Git Bash / WSL:
```bash
source venv/Scripts/activate
```

3. **Install dependencies** (already installed in venv):
```bash
pip install -r tasks/requirements.txt
```

4. **Set up API key:**

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

Windows Command Prompt:
```cmd
set GEMINI_API_KEY=your-api-key-here
```

Bash:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## 📊 Task 1: Rating Prediction via Prompting

### Running Experiments

```bash
python notebooks/run_prompt_experiments.py
```

This script:
- Tests 3 different prompting strategies (baseline, few-shot, chain-of-thought)
- Uses synthetic Yelp-like review data (200 samples)
- Outputs results to `notebooks/task1_results/`
- Generates comparison metrics (accuracy, JSON validity)

### Output Files

- `results_baseline.csv` - Direct classification results
- `results_few_shot.csv` - Few-shot learning results
- `results_chain_of_thought.csv` - Chain-of-thought reasoning results
- `summary.json` - Aggregated metrics

### Using Real Yelp Data

To use the actual Kaggle dataset:
1. Download from [Kaggle Yelp Reviews](https://www.kaggle.com/datasets/omkarsabnis/yelp-reviews-dataset)
2. Place in `data/yelp.csv`
3. Modify `run_prompt_experiments.py` to load from `data/yelp.csv`

## 🖥️ Task 2: Two-Dashboard AI Feedback System

### Architecture

- **Backend**: FastAPI REST API with SQLite storage
- **User Dashboard**: Streamlit public interface
- **Admin Dashboard**: Streamlit internal analytics view
- **LLM Integration**: Google Gemini for responses, summaries, and recommendations

### Running Locally

**Terminal 1 - Start Backend:**
```bash
cd src/backend
python main.py
```
Backend runs at: http://localhost:8000

**Terminal 2 - Start User Dashboard:**
```bash
streamlit run src/dashboards/user_dashboard.py --server.port 8501
```
User dashboard: http://localhost:8501

**Terminal 3 - Start Admin Dashboard:**
```bash
streamlit run src/dashboards/admin_dashboard.py --server.port 8502
```
Admin dashboard: http://localhost:8502

### API Endpoints

- `GET /` - Health check
- `POST /api/submit` - Submit new review
- `GET /api/submissions` - List all submissions
- `GET /api/analytics` - Get statistics

### Features

**User Dashboard:**
- ⭐ 1-5 star rating selection
- 📝 Review text submission
- 🤖 AI-generated personalized response
- ✅ Real-time feedback

**Admin Dashboard:**
- 📊 Live analytics (total submissions, average rating, distribution)
- 📋 All submission details with AI insights
- 🔍 AI-generated summaries for each review
- 💡 Recommended actions for business
- 🔄 Auto-refresh capability

## 🚢 Deployment

### Option 1: Hugging Face Spaces (Recommended for Streamlit)

**User Dashboard:**
1. Create new Space at huggingface.co
2. Upload `app/dashboards/user_dashboard.py` and `requirements.txt`
3. Set `GEMINI_API_KEY` in Space secrets
4. Set `API_URL` to your backend URL

**Admin Dashboard:**
1. Create separate Space
2. Upload `app/dashboards/admin_dashboard.py`
3. Configure same secrets

**Backend API:**
Deploy to Render, Railway, or similar:
1. Create web service from `app/backend/main.py`
2. Add `GEMINI_API_KEY` environment variable
3. Note the deployment URL for dashboards

### Option 2: Render / Railway

1. Create three services (backend, user dashboard, admin dashboard)
2. Configure environment variables
3. Link dashboards to backend API URL

### Environment Variables

- `GEMINI_API_KEY` - Required for AI functionality
- `API_URL` - Backend URL (for dashboards, default: http://localhost:8000)

## 🧪 Testing

Run the backend API:
```bash
# Test health endpoint
curl http://localhost:8000/

# Submit a test review
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "review": "Great experience!"}'

# Get analytics
curl http://localhost:8000/api/analytics
```

## 📝 Documentation

Additional documentation files in `tasks/`:
- `SUMMARY.md` - Project overview
- `ROADMAP.md` - Development timeline
- `TASK_CHECKLIST.md` - Detailed task breakdown
- `DOCUMENTATION.md` - Technical details
- `REQ.txt` - Setup notes

## 🛠️ Development

### Adding New Prompting Strategies (Task 1)

Edit `notebooks/run_prompt_experiments.py`:
```python
def my_new_prompt(review: str) -> str:
    return f"Your prompt here: {review}"

# Add to strategies list in main()
strategies.append(("my_strategy", my_new_prompt))
```

### Extending the Backend (Task 2)

Add new endpoints in `src/backend/main.py`:
```python
@app.get("/api/my-endpoint")
def my_endpoint():
    return {"data": "value"}
```

## 📦 Deliverables

- ✅ GitHub Repository with all code
- ✅ Python notebook/scripts for Task 1
- ✅ Complete web application for Task 2
- ✅ Comprehensive README and documentation
- 🚧 Deployed dashboard URLs (deploy to get URLs)
- 🚧 Short report PDF (to be created)

## 🔍 Key Technologies

- **LLM**: Google Gemini (gemini-1.5-flash)
- **Backend**: FastAPI + SQLite
- **Frontend**: Streamlit
- **Data**: Pandas, JSON
- **Deployment**: Hugging Face Spaces / Render

## 📄 License

This project is submitted as part of the Fynd AI internship assessment.

## 👤 Author

Submitted for Fynd AI Engineering Intern position

---

**Need Help?**
- Ensure `GEMINI_API_KEY` is set before running
- Check all services are running on different ports
- Review logs for detailed error messages
