#  Shopify Voice AI Assistant

An AI-powered Voice Assistant that answers questions about Shopify store products using Retrieval-Augmented Generation (RAG).

This assistant can:

- Listen to voice queries  
-  Retrieve relevant product information using FAISS  
-  Understand user intent (price, size, description, policies)  
-  Respond with natural voice  

---

#  Features

- Voice-based interaction (Speech-to-Text using Faster-Whisper)
- Semantic search using Sentence Transformers
- FAISS vector indexing for fast and accurate retrieval
- Intent-aware response handling (Price, Size, Description)
- Text-to-Speech using pyttsx3
- Clean and modular architecture
- Fully compatible with Python 3.14

---
#  Project Objective

To build a voice-enabled AI assistant that can accurately answer product-related queries from a Shopify store using semantic search and retrieval-augmented generation.

#  System Architecture

User Voice
   ↓
Speech-to-Text (Faster-Whisper)
   ↓
Sentence Transformer Embedding
   ↓
FAISS Vector Search
   ↓
Intent Detection & Answer Extraction
   ↓
Text-to-Speech Response


##  Project Structure

```
shopify_voice_ai/
│
├── scripts/
│   ├── rag_query.py
│   ├── hf_stt.py
│   ├── hf_tts.py
│   └── chunk_data.py
│
├── build_faiss.py
├── shopify_data.json   # example file
├── requirements.txt
├── README.md
└── .gitignore
```


---

#  Technologies Used

- Python 3.14
- Sentence-Transformers
- FAISS (Vector Search)
- Faster-Whisper (Speech-to-Text)
- pyttsx3 (Text-to-Speech)
- NumPy & Scikit-learn

---

#  Installation Guide
##  Requirements

- Python 3.14
- Microphone enabled
- Windows OS (recommended)


## 1️⃣ Clone the Repository

git clone <your-repository-url>
cd shopify_voice_ai

---

## 2️⃣ Install Dependencies

pip install -r requirements.txt

Make sure Python 3.14 is installed.

---

# ▶️ How to Run the Project

## Step 1 — Generate Chunks

python scripts/chunk_data.py

## Step 2 — Build FAISS Index

python scripts/build_faiss.py

## Step 3 — Start Voice Assistant

python scripts/rag_query.py

---

# 🔄 Workflow (When Data Changes)

If you update `shopify_data.json`, run:

python scripts/chunk_data.py
python scripts/build_faiss.py
python scripts/rag_query.py

---

#  Example Voice Queries

You can ask:

- What is the price of cotton kurta?
- What sizes are available for denim jacket?
- Describe silk saree.
- What is your shipping policy?
- What is your return policy?
- How can I contact you?
- Exit

---

# 📌 How It Works

1. The assistant records user voice input.
2. Converts speech to text using Faster-Whisper.
3. Generates embeddings using Sentence-Transformers.
4. Performs semantic search using FAISS.
5. Detects user intent (price, size, description).
6. Extracts accurate information.
7. Responds using Text-to-Speech.

---

---

#  Author

Developed as an AI-based Shopify Voice Assistant project using Retrieval-Augmented Generation (RAG).

---

