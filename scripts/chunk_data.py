import json

CHUNK_SIZE = 500  # larger chunks for structured data

def chunk_text(text, size=CHUNK_SIZE):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size
    return chunks

with open("shopify_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = []

for item in data:
    text_chunks = chunk_text(item["content"])
    for chunk in text_chunks:
        chunks.append({
            "title": item["title"],
            "type": item["type"],
            "content": chunk
        })

with open("rag_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print("Chunking complete. Total chunks:", len(chunks))
