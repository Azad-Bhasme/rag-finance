📊 RAG Finance – Smarter Q&A on Annual Filings

I built this project as a Retrieval Augmented Generation (RAG) system that can read through long financial filings and answer questions like “What was Microsoft’s total revenue in 2024?” in a structured JSON format.

Instead of searching line by line, the system splits, embeds, and indexes documents with FAISS and Sentence Transformers, then quickly retrieves relevant chunks when you ask a question.

✨ What this does

✅ Reads raw 10-K style filings (Google, Microsoft, Nvidia).

✅ Splits each filing into chunks so even large docs can be handled.

✅ Creates embeddings using MiniLM sentence transformer.

✅ Stores everything in a FAISS index for fast semantic search.

✅ Returns answers + financial numbers with sources in JSON format.

Basically: you ask → it searches → extracts numbers → gives an answer with references.

📂 Folder Layout
rag-finance/
│
├── data/            # input text filings (2022–2024 for 3 companies)
├── outputs/         # generated FAISS index + metadata + results
├── main.py          # main pipeline script
├── requirements.txt # dependencies
└── README.md        # this file

⚡ Quick Start
1️⃣ Install the requirements
pip install -r requirements.txt

2️⃣ Build the index

On first run, the script will chunk the files, create embeddings, and save an index.

python main.py


This will create:

outputs/index.faiss → FAISS index

outputs/meta.json → metadata for chunks

outputs/results.json → saved answers

3️⃣ Ask questions interactively

Once the index exists, you can query without rebuilding:

python main.py


Example:

Enter your query (or 'exit'): What was Microsoft's total revenue in 2024?

JSON Output:
{
  "query": "What was Microsoft's total revenue in 2024?",
  "answer_numbers": ["$211 billion"],
  "sources": ["msft_2024.txt"]
}

🧠 Notes & Tips

If you’re short on time → keep only 2024 filings in data/ (3 files). Faster, lighter.

If you want full coverage → use all 9 files (2022–2024 for each company).

Once index is built, you don’t need to rebuild unless files change.

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