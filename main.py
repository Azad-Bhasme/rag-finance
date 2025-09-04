import os
import re
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ------------------------------
# CONFIGURATION (can be tuned)
# ------------------------------
DATA_DIR = "data"               # folder with filings .txt
INDEX_FILE = "outputs/index.faiss"
META_FILE = "outputs/meta.json"
RESULTS_FILE = "outputs/results.json"
CHUNK_SIZE = 1000
BATCH_SIZE = 32
TOP_K = 5   # how many chunks to fetch per query

# ------------------------------
# Load embedding model
# ------------------------------
print("⚡ loading embedding model ...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ------------------------------
# Helper functions
# ------------------------------
def load_files():
    """read all filings from data/ and break into chunks"""
    docs, metas = [], []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".txt"):   # recruiter asked for 9 files
            path = os.path.join(DATA_DIR, fname)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            # chunking the text
            for i in range(0, len(text), CHUNK_SIZE):
                chunk = text[i:i+CHUNK_SIZE]
                docs.append(chunk)
                metas.append(fname)
            print(f"✅ loaded {fname} with {len(text)//CHUNK_SIZE} chunks")
    return docs, metas

def embed_texts(texts):
    """get sentence embeddings"""
    emb = model.encode(texts, show_progress_bar=True, batch_size=BATCH_SIZE)
    return np.array(emb).astype("float32")

def build_index():
    """create new FAISS index"""
    docs, metas = load_files()
    embeddings = embed_texts(docs)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"docs": docs, "metas": metas}, f)

    print("✅ index saved")
    return index, docs, metas

def load_index():
    """reload FAISS + metadata"""
    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta["docs"], meta["metas"]

def search(query, index, docs, metas, top_k=TOP_K):
    """semantic search for query"""
    q_emb = model.encode([query]).astype("float32")
    D, I = index.search(q_emb, top_k)
    results = [docs[i] for i in I[0]]
    sources = [metas[i] for i in I[0]]
    return results, sources

# ------------------------------
# Regex number extractor (with filter)
# ------------------------------
def extract_numbers(text):
    # regex to capture $123, 200 billion, 50.2 million etc
    matches = re.findall(r"\$?\d[\d,\.]*\s?(?:billion|million|thousand|trillion)?", 
                         text, flags=re.IGNORECASE)

    clean = []
    for m in matches:
        m = m.strip()
        # skip silly stuff like "0", "9" unless they hv $ sign
        if len(m) <= 2 and not m.startswith("$"):
            continue
        clean.append(m)

    # remove duplicates, keep top 3
    clean = list(dict.fromkeys(clean))
    return clean[:3] if clean else ["No clear number found"]

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)

    # build new index if not already present
    if not os.path.exists(INDEX_FILE):
        print("🛠️ building new index ...")
        index, docs, metas = build_index()
    else:
        print("🔄 loading saved index ...")
        index, docs, metas = load_index()

    # demo queries for recruiter proof
    demo_qs = [
        "What was Microsoft's total revenue in 2024?",
        "How much revenue did Google report in 2023?",
        "How much did Nvidia spend on Research and Development in 2022?",
        "What risks did Microsoft highlight in 2024?",
        "What did Google mention about AI strategy in 2024?"
    ]

    results = []
    for q in demo_qs:
        chunks, sources = search(q, index, docs, metas)
        combined = " ".join(chunks)
        numbers = extract_numbers(combined)

        out = {
            "query": q,
            "answer_numbers": numbers,
            "sources": sources
        }
        print("\nJSON Output:")
        print(json.dumps(out, indent=2))
        results.append(out)

    # save demo answers
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Saved demo answers to {RESULTS_FILE}")

    # interactive loop
    while True:
        q = input("\nEnter your query (or 'exit'): ")
        if q.lower() == "exit":
            break
        chunks, sources = search(q, index, docs, metas)
        combined = " ".join(chunks)
        numbers = extract_numbers(combined)
        out = {
            "query": q,
            "answer_numbers": numbers,
            "sources": sources
        }
        print("\nJSON Output:")
        print(json.dumps(out, indent=2))
