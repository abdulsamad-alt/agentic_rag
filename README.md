# 🤖 Agentic RAG System (Hybrid)

This project implements a **Hybrid Agentic Retrieval-Augmented Generation (RAG)** system using Python.

It combines:
- A **Router (cost optimization layer)**
- A **Retriever (FAISS vector search)**
- A **Tool-calling LLM Agent (Gemini)**
- Optional **Image Tool (multimodal)**
- **Short-term Memory (chat history)**

---

## 🧠 Architecture

### 🔹 Ingestion Pipeline
1. Load PDF using PyMuPDF
2. Extract raw text (page-wise)
3. Preprocess text (cleaning, normalization)
4. Chunk text (500 size, 100 overlap)
5. Generate embeddings using SentenceTransformers
6. Store vectors in FAISS index
7. Store metadata in `chunks.pkl`

---

### 🔹 Runtime Flow

User Query  
→ Router (cheap decision)  
→ Either:
- Greeting / invalid → direct response  
- Retrieval → FAISS + LLM  
- Complex → LLM Agent (tool-calling)

---

### 🔹 Agentic Behavior

The LLM agent:
- Decides whether to use tools
- Calls:
  - `RetrieverTool`
  - `ImageTool`
- Combines results to generate answers

---

## ⚙️ Features

- Hybrid routing (cost-efficient)
- Semantic search using FAISS
- Tool-calling agent (prompt-based)
- Multimodal support (images)
- Chat memory (last 5 interactions)
- Streamlit UI

---

## 📁 Project Structure

agentic_rag_project/
│
├── app/
│ └── main.py
│
├── core/
│ ├── agent.py
│ ├── router.py
│ └── config.py
│
├── tools/
│ ├── retriever_tool.py
│ └── image_tool.py
│
├── ingestion/
│ ├── loader.py
│ ├── chunking.py
│ ├── embeddings.py
│ ├── vector_store.py
│ └── image_extractor.py
│
├── data/
│ ├── raw/
│ ├── vector_db/
│ └── images/
│
├── utils/
│ └── helpers.py
│
├── build_index.py
├── extract_images.py
├── run_agent.py
├── requirements.txt
└── README.md


---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

2. Add API key

Create .env file:
GEMINI_API_KEY=your_api_key_here

3. Run ingestion (one-time)

python build_index.py
python extract_images.py

4. Run application
streamlit run app/main.py

💬 Example Queries
"What is revenue growth?"
"Explain the financial performance"
"Describe the chart on page 5"
"Explain diagram and related text"

🎯 Key Concept

This project demonstrates:

A hybrid agentic RAG system where a router optimizes cost and an LLM agent dynamically decides tool usage.

📌 Technologies Used
Python
Streamlit
FAISS
SentenceTransformers
Google Gemini API
PyMuPDF

🧠 Author Note

This project was built with a focus on:

Explainability
Modular design
Cost optimization
Agentic behavior without heavy frameworks