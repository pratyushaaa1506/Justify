from typing import List, Dict
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

COLLECTION_NAME = "legal_knowledge"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333


class RAGEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(
            host=QDRANT_HOST,
            port=QDRANT_PORT
        )

    def search_legal_knowledge(self, query: str) -> List[Dict[str, str]]:
        # Safety: Check if collection exists and is not empty
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == COLLECTION_NAME for c in collections)
            if not exists:
                return []
            info = self.client.get_collection(COLLECTION_NAME)
            if hasattr(info, 'points_count') and getattr(info, 'points_count', 0) == 0:
                return []
        except Exception:
            return []

        # Convert query to embedding
        query_vector = self.model.encode(query).tolist()

        # Query Qdrant (correct API)
        response = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=3
        )

        results = []

        for point in response.points:
            results.append(
                {
                    "law": point.payload.get("law", point.payload.get("name", "Unknown")),
                    "text": point.payload.get("text", "")
                }
            )

        return results
