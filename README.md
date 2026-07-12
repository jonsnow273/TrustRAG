# TrustRAG

**A RAG system that thinks before it retrieves, and checks itself before it answers.**

TrustRAG is a Retrieval-Augmented Generation (RAG) pipeline that goes beyond the standard "fixed pipeline" approach in two key ways:

1. **Adaptive Configuration Selection** — instead of using one static retrieval setup (chunk size, top-k, retriever type) for every question, TrustRAG uses a trained classifier to automatically pick the best configuration based on the question's type and features.
2. **Self-Verification via NLI** — after generating an answer, TrustRAG doesn't just trust it. It breaks the answer into individual claims and checks each one against the retrieved documents using a Natural Language Inference (NLI) model, flagging any claim that isn't actually supported — i.e., catching hallucinations before the user sees them.

This project addresses two of the most common real-world weaknesses in typical RAG systems: **poor configuration tuning** and **unchecked hallucination**.

---

## Why This Project Exists

Most RAG demos are a thin wrapper around an LLM API — a vector store, a fixed prompt, and a call to a language model. That's integration, not engineering.

TrustRAG was built to demonstrate two things:
- The ability to design and train a real ML component (the config selector) using labeled data derived from experimentation, not just prompt engineering.
- An understanding of a genuine open problem in RAG systems — hallucination — and a concrete, testable approach to detecting it, rather than just hoping the LLM behaves.

---

## How It Works

```
Question
   │
   ▼
[Config Selector] ──► picks chunk size, retriever type, top-k
   │                   based on question features (type, length, etc.)
   ▼
[Retriever] ──► fetches top-k relevant chunks using the selected config
   │
   ▼
[Generator] ──► LLM generates an answer using the question + retrieved chunks
   │
   ▼
[Verifier]
   ├─ Claim Splitter ──► breaks the answer into individual factual claims
   └─ NLI Checker ──► checks each claim against retrieved chunks
                        labels each as: Supported / Contradicted / Unverifiable
   │
   ▼
Final Answer + Trust Report
```

---

## Features

- 🔀 **Adaptive retrieval configuration** — a trained scikit-learn classifier routes each question to its optimal RAG settings instead of using one-size-fits-all defaults.
- 🔍 **Claim-level hallucination detection** — answers are decomposed into atomic claims and each is independently verified via NLI entailment against the source documents.
- 📊 **Transparent trust scoring** — every answer ships with a breakdown showing which claims are grounded and which aren't.
- ⚡ **FastAPI backend** — clean REST API exposing the full pipeline.
- 🎨 **React + Tailwind frontend** — simple interface to ask questions and visually inspect the config chosen and the claim-by-claim trust report.
- 💸 **Free LLM inference** — uses Groq's free API tier (Llama models) instead of paid providers.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Retrieval | `sentence-transformers`, `faiss-cpu` |
| Config Selector | `scikit-learn` |
| Generation | Groq API (Llama models) |
| Hallucination Detection | Hugging Face `transformers` (NLI model) |
| Backend | FastAPI, Pydantic |
| Frontend | React, Vite, Tailwind CSS |
| Experimentation | Jupyter Notebooks |

---

## Project Structure

```
trust-rag/
├── data/
│   ├── raw_docs/              # source documents for retrieval
│   ├── questions.csv          # question dataset with type/config labels
│   └── eval_set.csv           # held-out questions for evaluation
│
├── src/
│   ├── ingestion/              # document chunking + embedding
│   ├── retriever/              # top-k retrieval given a config
│   ├── config_selector/        # question feature extraction + classifier
│   ├── generator/               # LLM answer generation
│   ├── verifier/                # claim splitting + NLI-based checking
│   └── pipeline.py             # orchestrates the full flow
│
├── notebooks/                  # experimentation & label generation
├── api/                        # FastAPI app
├── frontend/                   # React + Tailwind UI
├── tests/                      # unit tests
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/trust-rag.git
cd trust-rag
```

### 2. Set up the backend
```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file in the root:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

### 4. Run the backend
```bash
uvicorn api.main:app --reload
```

### 5. Set up the frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Evaluation

TrustRAG is evaluated on two fronts:

- **Config Selector Accuracy** — how often the selector's chosen configuration matches (or outperforms) the best config found via brute-force search on the eval set.
- **Hallucination Detection Performance** — precision/recall/F1 of the NLI-based verifier against a set of answers with known supported and unsupported claims.

*(Results to be added as evaluation is completed.)*

| Metric | Score |
|---|---|
| Config Selector Accuracy | TBD |
| Claim Verification Precision | TBD |
| Claim Verification Recall | TBD |

---

## Roadmap

- [ ] Document ingestion + chunking
- [ ] Retriever with configurable top-k / chunk size
- [ ] Label generation for config selector training
- [ ] Train and evaluate config selector
- [ ] Claim splitter
- [ ] NLI-based claim verifier
- [ ] Full pipeline integration
- [ ] FastAPI backend
- [ ] React + Tailwind frontend
- [ ] Evaluation report + metrics

---

LICENSE -- MIT

---

made by -- pranit bharat more 🐐
