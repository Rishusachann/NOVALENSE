# NOVALENSE

**NOVALENSE: Hybrid Transformer-Based Research Originality and Semantic Forensics Framework**

NOVALENSE is a deployable research prototype for originality assessment of academic documents. It combines semantic retrieval, sentence-level similarity analysis, paraphrase-aware evidence extraction, and explainable AI-likelihood estimation to generate a reviewer-friendly originality report.

This repository is aligned with the core pipeline described in the NOVALENSE paper: contextual embedding, semantic similarity analysis, paraphrase detection, AI-generated text estimation, and weighted originality scoring.

## Core Features

- Upload and analyze **PDF, DOCX, or TXT** documents
- Extract text and split it into analyzable sentence units
- Retrieve **Top-K similar papers** from a scholarly corpus using **Sentence Transformers + FAISS**
- Perform **sentence-level semantic matching**
- Estimate **paraphrase probability** for matched sentences
- Estimate **AI-likelihood** using stylometric features
- Compute a final **originality score** with weighted fusion
- Generate **JSON and HTML reports**
- Includes a **FastAPI backend** and a **Streamlit demo frontend**

## Project Architecture

```text
Input Document
   ↓
Text Extraction + Normalization
   ↓
Sentence Segmentation
   ↓
Contextual Embedding Generation
   ↓
Top-K Corpus Retrieval (FAISS)
   ↓
Sentence-Level Similarity Matching
   ↓
Paraphrase Probability Estimation
   ↓
Stylometric AI-Likelihood Analysis
   ↓
Weighted Fusion Scoring
   ↓
JSON + HTML Forensic Report
```

## Mathematical Formulation

The current MVP computes originality as:

```math
Originality = 100 × (1 - (λ1·S_sem + λ2·P_para + λ3·P_ai))
```

Where:

- `S_sem` = aggregated semantic similarity score
- `P_para` = aggregated paraphrase score
- `P_ai` = AI-likelihood score
- `λ1 + λ2 + λ3 = 1`

Default weights are configured in `app/core/config.py`.

## Folder Structure

```text
NOVALENSE/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── frontend/
│   └── streamlit_app.py
├── data/
│   ├── corpus_metadata.csv
│   ├── raw_papers/
│   └── sample_inputs/
├── index/
├── outputs/
│   ├── logs/
│   └── reports/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.sh
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/NOVALENSE.git
cd NOVALENSE
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Backend

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

## Run the Frontend

Open another terminal and run:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend will run at:

```text
http://127.0.0.1:8501
```

## API Endpoints

### Health Check

```http
GET /health
```

### Upload Document

```http
POST /api/v1/upload
```

### Analyze Document

```http
POST /api/v1/analyze
```

Example request body:

```json
{
  "file_path": "data/sample_inputs/sample_paper.txt",
  "top_k": 5,
  "semantic_threshold": 0.72
}
```

### Report Lookup

```http
GET /api/v1/report?path=<absolute_or_relative_report_path>
```

## Quick Test with Sample File

You can test immediately using the included sample file:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "data/sample_inputs/sample_paper.txt",
    "top_k": 5,
    "semantic_threshold": 0.72
  }'
```

## Docker Deployment

### Build and run backend

```bash
docker build -t novalense .
docker run -p 8000:8000 novalense
```

### Run backend + frontend using compose

```bash
docker compose up --build
```

## What This MVP Does Well

- Provides a **real working prototype** suitable for GitHub, demos, and academic project presentation
- Shows a clear bridge from research paper concepts to deployable software
- Produces evidence-based originality analysis rather than a single percentage only

## Current Limitations

- AI-likelihood detection is **heuristic and probabilistic**, not a final forensic truth
- Corpus quality directly affects retrieval quality
- Sentence-level matching currently uses abstract-based references from the included corpus metadata
- This is a **research prototype**, not a complete institutional plagiarism platform

## Future Improvements

- Replace CSV corpus with full paper store and metadata database
- Add full-text corpus indexing instead of abstract-only retrieval
- Add SHAP visualizations in the frontend
- Add PDF report export
- Add citation graph analysis
- Add multilingual and cross-lingual similarity support
- Add user authentication and persistent job tracking

## Recommended GitHub Additions

Before publishing, add these items:

- 3–4 screenshots of the Streamlit UI
- One architecture image matching your paper
- One sample output report in `outputs/reports/`
- A short demo GIF

## Citation Note

If you use this repository in an academic submission or project demonstration, cite your NOVALENSE paper and clearly mark this codebase as the prototype implementation.
