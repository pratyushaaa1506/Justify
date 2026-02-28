import sys
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

COLLECTION_NAME = "legal_knowledge"
VECTOR_SIZE = 384


def main():
    client = QdrantClient(host="localhost", port=6333)
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    if exists:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        return
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )
    print(f"Collection '{COLLECTION_NAME}' created with vector size {VECTOR_SIZE} and cosine distance.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
