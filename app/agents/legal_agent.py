
from app.services.classifier import LegalIssueClassifier
from app.services.rag_engine import RAGEngine
from app.services.gemini_client import generate_llm_response
from app.agents.law_filter import LawRelevanceFilter
from app.agents.memory_store import MemoryStore



class LegalAgent:
    def __init__(self):
        self.classifier = LegalIssueClassifier()
        self.rag = RAGEngine()
        self.memory = MemoryStore(max_messages=10)

    def decide_and_act(self, user_query: str, session_id: str, vision_context: dict = None) -> dict:
        # Step 1: Soft classification (signal only)
        classification = self.classifier.classify(user_query)

        # Step 2: Retrieve candidate laws, optionally using vision_context
        rag_query = user_query
        if vision_context:
            # Inject vision context into RAG query for richer retrieval
            rag_query = f"{user_query}\n\n[Vision Evidence]\n{vision_context}"
        raw_sources = self.rag.search_legal_knowledge(rag_query)

        if not raw_sources:
            self.memory.add_message(session_id, "user", user_query)
            self.memory.add_message(session_id, "assistant", "I couldn't find any relevant legal information. Please provide more details.")
            return {
                "response": (
                    "I couldn't find any relevant legal information. "
                    "Please provide more details."
                ),
                "classification": classification,
                "sources": []
            }

        # Step 3: LLM-assisted relevance pruning
        filtered_sources = LawRelevanceFilter.llm_prune_laws(
            user_query=rag_query,
            laws=raw_sources
        )

        if not filtered_sources:
            self.memory.add_message(session_id, "user", user_query)
            self.memory.add_message(session_id, "assistant", "I couldn't find any relevant legal information after filtering. Please provide more details.")
            return {
                "response": (
                    "I couldn't find any relevant legal information after filtering. "
                    "Please provide more details."
                ),
                "classification": classification,
                "sources": []
            }

        # Step 4: Inject memory context and vision context into LLM reasoning
        memory_context = self.memory.get_memory(session_id)
        memory_str = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in memory_context
        ])
        if memory_str:
            memory_str = f"Conversation history:\n{memory_str}\n---\n"

        # Compose vision context string for LLM prompt
        vision_str = ""
        if vision_context:
            import json
            try:
                vision_str = f"\n[Vision Evidence]:\n{json.dumps(vision_context, ensure_ascii=False, indent=2)}\n---\n"
            except Exception:
                vision_str = f"\n[Vision Evidence]:\n{str(vision_context)}\n---\n"

        # Step 5: Final reasoning (hybrid prompt)
        llm_response = generate_llm_response(
            user_query=memory_str + vision_str + user_query,
            rag_context=filtered_sources
        )

        # Step 6: Store messages in memory
        self.memory.add_message(session_id, "user", user_query)
        self.memory.add_message(session_id, "assistant", llm_response)

        return {
            "response": llm_response,
            "classification": classification,
            "sources": filtered_sources,
            "vision_context": vision_context if vision_context else None
        }
