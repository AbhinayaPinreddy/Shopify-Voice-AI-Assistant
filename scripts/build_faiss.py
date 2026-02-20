import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRIPT_DIR, "rag_chunks.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["content"] for item in data]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, os.path.join(SCRIPT_DIR, "faiss.index"))

print("FAISS index built successfully.")
