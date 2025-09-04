# 📊 RAG Finance – Smarter Q&A on Annual Filings

**A Retrieval-Augmented Generation (RAG) system that reads through long financial filings and answers questions like “What was Microsoft’s total revenue in 2024?” in structured JSON.**

---

## ✨ Overview

Instead of searching line by line, this system:

- Splits, embeds, and indexes documents with **FAISS** and **Sentence Transformers**
- Quickly retrieves relevant chunks when you ask a question
- Extracts numbers and returns answers with sources in **JSON format**

Basically: **you ask → it searches → extracts numbers → gives an answer with references**.

---

## 🔧 Features

✅ Reads raw 10-K style filings (Google, Microsoft, Nvidia)  
✅ Splits each filing into chunks so even large docs can be handled  
✅ Creates embeddings using **MiniLM sentence transformer**  
✅ Stores everything in a **FAISS index** for fast semantic search  
✅ Returns answers + financial numbers with sources in **JSON format**

---

## 📂 Folder Layout

rag-finance/
│
├── data/ # input text filings (2022–2024 for 3 companies)
├── outputs/ # generated FAISS index + metadata + results
├── main.py # main pipeline script
├── requirements.txt # dependencies
└── README.md # this file

yaml
Copy code

---

## ⚡ Quick Start

### 1️⃣ Install Requirements

```bash
pip install -r requirements.txt
2️⃣ Build the Index (First Run)
bash
Copy code
python main.py
This will:

Chunk the files

Create embeddings

Save an index

Files created:

outputs/index.faiss → FAISS index

outputs/meta.json → metadata for chunks

outputs/results.json → saved answers

3️⃣ Ask Questions Interactively
Once the index exists, you can query without rebuilding:

bash
Copy code
python main.py
Example:

rust
Copy code
Enter your query (or 'exit'): What was Microsoft's total revenue in 2024?
JSON Output:

json
Copy code
{
  "query": "What was Microsoft's total revenue in 2024?",
  "answer_numbers": ["$211 billion"],
  "sources": ["msft_2024.txt"]
}
🧠 Notes & Tips
Speed: Keep only 2024 filings (3 files) → lighter, faster

Full coverage: Include all 9 files (2022–2024 for each company)

Index only needs to be rebuilt if files change

📌 Sample Queries
What was Microsoft’s revenue in 2022?

How much revenue did Google report in 2023?

What risks did Nvidia highlight in 2024?

How much did Microsoft spend on R&D in 2024?

✅ Deliverables
main.py → the main code

requirements.txt → install list

data/ → text filings

outputs/ → FAISS index, metadata, sample results

README.md → this guide

✨ Built with Python, FAISS, and Sentence Transformers
📌 Demonstrates how RAG can unlock insights from massi
