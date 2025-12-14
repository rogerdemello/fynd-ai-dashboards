#!/usr/bin/env python3
from pathlib import Path
from PyPDF2 import PdfReader
import sys

def extract_pdf(path: Path, outdir: Path) -> bool:
    try:
        reader = PdfReader(str(path))
    except Exception as e:
        print(f"Failed to open {path}: {e}")
        return False
    texts = []
    for p in reader.pages:
        try:
            t = p.extract_text()
        except Exception:
            t = None
        if t:
            texts.append(t)
    out = "\n".join(texts)
    out_file = outdir / (path.stem + ".txt")
    out_file.write_text(out, encoding="utf-8", errors="replace")
    return bool(out.strip())

def main():
    base = Path(__file__).resolve().parents[1]  # e:/Fynd AI
    docs_dir = base / "docs"
    pdfs = list(docs_dir.glob("*.pdf"))
    outdir = docs_dir / "extracted_text"
    outdir.mkdir(exist_ok=True)
    if not pdfs:
        print("No PDF files found in", tasks_dir)
        return
    results = {}
    for p in pdfs:
        ok = extract_pdf(p, outdir)
        results[p.name] = ok
    print("Extraction results:")
    for k, v in results.items():
        print(f"- {k}: {'text' if v else 'no text (scanned)'}")

if __name__ == '__main__':
    main()
