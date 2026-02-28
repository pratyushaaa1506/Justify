import sys
import json
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
import uuid

COLLECTION_NAME = "legal_knowledge"
VECTOR_SIZE = 384
MODEL_NAME = "all-MiniLM-L6-v2"

# Path to your sample legal data (adjust as needed)
SAMPLE_DATA_PATH = "data/laws/sample_laws.json"

def load_sample_laws():
    with open(SAMPLE_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    client = QdrantClient(host="localhost", port=6333)
    model = SentenceTransformer(MODEL_NAME)
    docs = load_sample_laws()
    points = []
    for i, law in enumerate(docs):
        law_name = law.get("name") or law.get("title") or f"Law {i+1}"
        law_text = law.get("text") or law.get("content") or ""
        if not law_text:
            continue
        vector = model.encode(law_text).tolist()
        payload = {"name": law_name, "text": law_text}
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=payload
        )
        points.append(point)
    if not points:
        print("No valid legal documents found to insert.")
        return
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Inserted {len(points)} legal documents into '{COLLECTION_NAME}'.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
