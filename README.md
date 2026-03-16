# Pharma_GenAI_Project_2026

# Pharma GenAI Project 2026
### Clinical Trial Document Q&A — An AI assistant built with RAG

---

## The problem

Clinical operations teams spend hours manually searching through trial documents to answer questions like:

- *"What are the inclusion criteria for this protocol?"*
- *"Which sites had enrollment below 50% of target?"*
- *"What adverse events were flagged in the interim report?"*

These answers exist in the documents. Finding them shouldn't take hours.

---

## The solution

Upload clinical trial PDFs. Ask questions in plain English. Get accurate answers with the exact source passage cited — in seconds.

This app uses **Retrieval Augmented Generation (RAG)**: it finds the most relevant passages from your documents, then uses an LLM to generate a clear, cited answer. If the answer isn't in the documents, it says so — no hallucinations.

---

## How it works

```
Your PDFs
    ↓
Text is split into ~500 character chunks
    ↓
Each chunk is converted to a vector (embedding)
    ↓
Vectors are stored in ChromaDB (local, free)
    ↓
You ask a question
    ↓
ChromaDB finds the 4 most similar chunks
    ↓
LLM reads those chunks + your question → generates answer
    ↓
Answer shown with source citations
```

---

## Tech stack

| Layer | Tool |
|---|---|
| Document loading | LangChain PyPDFLoader |
| Text splitting | RecursiveCharacterTextSplitter |
| Embeddings | OpenAI text-embedding-3-small |
| Vector store | ChromaDB (local, free) |
| LLM | GPT-3.5-turbo |
| UI | Streamlit |

---

## Run locally

```bash
# 1. Clone
git clone https://github.com/PradeepChandarPc/Pharma_GenAI_Project_2026.git
cd Pharma_GenAI_Project_2026

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your OpenAI API key
cp .env.example .env
# Edit .env and paste your key from platform.openai.com

# 4. Add your PDF documents
# Drop files into data/sample_docs/

# 5. Build the knowledge base
python rag_pipeline.py

# 6. Launch the app
streamlit run app.py
```

---

## Project structure

```
Pharma_GenAI_Project_2026/
├── app.py               # Streamlit chat UI
├── rag_pipeline.py      # Ingestion, chunking, embedding, retrieval
├── requirements.txt     # All dependencies
├── .env.example         # API key template (never commit your real key)
└── data/
    └── sample_docs/     # Drop your PDFs here
```

---

## Why this project

I have 3 years of real pharma analytics experience — clinical trial site feasibility, HCP/KOL identification, and Real-World Evidence analysis at Mu Sigma. This project is a direct extension of that domain knowledge into Gen AI.

Clinical teams I've worked alongside actually face this problem. This is my attempt to solve it.

---

## Build log

| Week | What I built |
|---|---|
| Week 1 | Learned RAG fundamentals, set up Python environment |
| Week 3 | PDF ingestion pipeline + ChromaDB vector storage |
| Week 4 | Retrieval chain + LLM integration with pharma-specific prompt |
| Week 5 | Streamlit chat UI + deployed to Streamlit Cloud |

---

## What's next

- [ ] Add RAGAS evaluation metrics (answer relevancy, faithfulness)
- [ ] Support multi-document comparison queries
- [ ] Add confidence score to each answer
- [ ] Experiment with open-source LLMs (Mistral, LLaMA)

---

## Author

**Pradeep Chandar** — Data Scientist & Analyst, Pharma & Healthcare Analytics

Learning Gen AI in public — follow along on [LinkedIn](https://www.linkedin.com/in/pradeep-chandar/)
