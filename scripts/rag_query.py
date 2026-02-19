import json
import faiss
import numpy as np
import time
from sentence_transformers import SentenceTransformer
from hf_stt import listen
from hf_tts import speak

# Load chunked data
with open("rag_chunks.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["content"] for item in data]

# Load FAISS
index = faiss.read_index("faiss.index")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

welcome = "Shopify Voice Assistant started. Ask your question."
print(welcome)
speak(welcome)

while True:
    question = listen()

    if not question:
        continue

    question = question.lower()
    print("User:", question)

    if "exit" in question:
        speak("Goodbye.")
        break

    is_price = "price" in question
    is_size = "size" in question or "sizes" in question
    is_description = any(w in question for w in ["describe", "about", "details"])

    query_embedding = model.encode([question])
    D, I = index.search(np.array(query_embedding), k=5)

    answer = ""

    for idx in I[0]:
        chunk = texts[idx]
        lines = chunk.splitlines()

        if is_price:
            for line in lines:
                if "price" in line.lower():
                    answer = line.strip()
                    break
        elif is_size:
            for line in lines:
                if "size" in line.lower():
                    answer = line.strip()
                    break
        elif is_description:
            for line in lines:
                if "description" in line.lower():
                    answer = line.strip()
                    break

        if answer:
            break

    if not answer:
        answer = texts[I[0][0]]

    print("Answer:", answer)
    speak(answer)
    time.sleep(0.5)
