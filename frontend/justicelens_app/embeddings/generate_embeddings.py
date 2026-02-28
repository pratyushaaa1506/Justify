import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("legal_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = []

for chunk in chunks:
    text = chunk["text"]
    embedding = model.encode(text).tolist()

    embeddings.append({
        "id": chunk["id"],
        "topic": chunk["topic"],
        "text": text,
        "embedding": embedding
    })

with open("legal_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embeddings, f, indent=2)

print("✅ Embeddings generated successfully!")
