# Project Structure

## Fynd AI Take-Home Assessment - Clean & Organized

### 📁 Directory Structure

```
fynd-ai-assessment/
│
├── 📂 src/                          # Source code
│   ├── backend/                     # Task 2 Backend
│   │   ├── main.py                  # FastAPI server
│   │   ├── database.py              # SQLite operations
│   │   └── llm_service.py           # Gemini API integration
│   ├── dashboards/                  # Task 2 Dashboards
│   │   ├── user_dashboard.py        # Public submission UI
│   │   └── admin_dashboard.py       # Internal analytics UI
│   └── extract_pdfs.py              # Utility: PDF text extraction
│
├── 📂 notebooks/                    # Task 1 Experiments
│   ├── run_prompt_experiments.py    # Prompting strategies script
│   └── task1_results/               # Output CSVs & metrics (gitignored)
│
├── 📂 data/                         # Datasets
│   └── yelp.csv                     # Sample Yelp data
│
├── 📂 docs/                         # Documentation & Assets
│   ├── Fynd AI Intern – Take Home Assessment.pdf
│   ├── Job Description.pdf
│   ├── extracted_text/              # Extracted PDF content
│   ├── SUMMARY.md                   # Project overview
│   ├── ROADMAP.md                   # Development timeline
│   ├── TASK_CHECKLIST.md            # Detailed breakdown
│   ├── DOCUMENTATION.md             # Technical specs
│   ├── DEPLOYMENT.md                # Cloud deployment guide
│   ├── GETTING_STARTED.md           # Quick start tutorial
│   └── SUBMISSION_CHECKLIST.md      # Final checklist
│
├── 📂 tests/                        # Test suite
│   └── test_backend.py              # Backend unit tests
│
├── 📂 venv/                         # Virtual environment (gitignored)
│
├── 📄 README.md                     # Main documentation
├── 📄 REPORT.md                     # Assessment report
├── 📄 requirements.txt              # Python dependencies
├── 📄 .gitignore                    # Git exclusions
├── 🚀 start_all.bat                 # Windows quick launcher
└── 🚀 start_all.sh                  # Linux/Mac quick launcher
```

### 🎯 Clean Organization Benefits

1. **Standard Python Structure**: Follows best practices (`src/`, `tests/`, `docs/`)
2. **Clear Separation**: Code, data, docs, and notebooks properly isolated
3. **Easy Navigation**: Logical grouping makes files easy to find
4. **Deployment Ready**: Clean structure for Docker/CI/CD if needed
5. **No Redundancy**: Removed duplicate files and empty directories

### 🗂️ File Purposes

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `src/` | Production code | Backend API, Dashboards, Utilities |
| `notebooks/` | Experiments & analysis | Task 1 prompting scripts |
| `data/` | Datasets | Yelp reviews CSV |
| `docs/` | Documentation | PDFs, guides, checklists |
| `tests/` | Test suite | Unit & integration tests |

### 🚀 Quick Commands

```bash
# Run Task 1
python notebooks/run_prompt_experiments.py

# Run Task 2 (all services)
./start_all.sh  # or start_all.bat on Windows

# Run tests
python tests/test_backend.py

# Extract PDFs
python src/extract_pdfs.py
```

### ✨ Changes Made

**Removed:**
- ❌ `tasks/` directory (reorganized into proper structure)
- ❌ `app/` directory (moved to `src/`)
- ❌ `dataset/` directory (consolidated to `data/`)
- ❌ Duplicate `requirements.txt` files
- ❌ Empty directories

**Reorganized:**
- ✅ All source code → `src/`
- ✅ Experiments → `notebooks/`
- ✅ Documentation → `docs/`
- ✅ Tests → `tests/`
- ✅ Datasets → `data/`

**Updated:**
- ✅ All file paths in scripts
- ✅ Documentation references
- ✅ Start scripts
- ✅ .gitignore patterns

### 📋 Next Steps

1. Run tests to verify nothing broke
2. Test quick launch scripts
3. Review documentation for accuracy
4. Ready for deployment!
