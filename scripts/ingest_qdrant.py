import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, PointStruct
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'laws', 'sample_laws.json')
COLLECTION_NAME = "legal_knowledge"
VECTOR_SIZE = 384
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# Load Sentence-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read legal data
with open(DATA_PATH, "r", encoding="utf-8") as f:
    laws = json.load(f)

# Connect to Qdrant
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Create collection if not exists
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance="Cosine")
)

points = []
for idx, law in enumerate(laws):
    text = law["text"]
    law_name = law["law"]
    embedding = model.encode(text).tolist()
    payload = {"law": law_name, "text": text}
    points.append(PointStruct(id=idx, vector=embedding, payload=payload))

# Insert points
client.upsert(collection_name=COLLECTION_NAME, points=points)

print(f"Inserted {len(points)} laws into Qdrant collection '{COLLECTION_NAME}'.")
