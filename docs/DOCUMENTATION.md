# Documentation for `tasks/`

## Purpose
This document explains the current contents of `tasks/`, how to extract and interpret the PDFs, and recommended next steps to produce a full submission.

## File descriptions
- `Fynd AI Intern – Take Home Assessment.pdf` — contains the assessment prompt and instructions; extract text to identify deliverables.
- `Job Description.pdf` — contains role expectations and may clarify scoring criteria.
- `SUMMARY.md` — brief overview and actionable next steps.
- `ROADMAP.md` — proposed timeline and priorities.
- `REQ.txt` — environment and package setup notes.

## How to extract PDF text (quick example using PyPDF2)

```python
from PyPDF2 import PdfReader
reader = PdfReader('tasks/Fynd AI Intern – Take Home Assessment.pdf')
text = []
for p in reader.pages:
    text.append(p.extract_text() or '')
full_text = '\n'.join(text)
print(full_text[:2000])  # preview
```

If `extract_text()` returns empty strings (scanned pages), use OCR (pytesseract) after converting pages to images.

## Contribution / next actions
1. Run the extraction script and save plain-text copies under `tasks/text/`.
2. From extracted text, produce a detailed checklist and assign priorities/timelines.
3. Implement the assessment solutions in a separate branch; include tests and a `README.md` for reviewers.

## Contact / handoff
If you want, I can extract the PDFs' text now and produce a detailed tasks checklist and implementation plan.
