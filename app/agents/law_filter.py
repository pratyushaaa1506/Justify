from typing import List, Dict
from app.services.gemini_client import generate_raw_llm


class LawRelevanceFilter:

    @staticmethod
    def llm_prune_laws(user_query: str, laws: List[Dict]) -> List[Dict]:
        if not laws:
            return []

        law_text = "\n".join(
            [f"- {law['law']}: {law['text']}" for law in laws]
        )

        prompt = f"""
You are a legal relevance evaluator.

User Query:
{user_query}

Candidate Laws:
{law_text}

Task:
From the above list, return ONLY the names of laws that are clearly relevant to the user's query.

Rules:
- Exclude unrelated laws
- Be conservative (only keep relevant ones)
- Output one law name per line
"""

        response = generate_raw_llm(prompt)
        if not response:
            return laws

        # Parse law names from LLM output
        response_linenames = [line.strip() for line in response.splitlines() if line.strip()]
        law_names = set(law['law'].strip().lower() for law in laws)
        relevant = [law for law in laws if law['law'].strip().lower() in (name.lower() for name in response_linenames)]
        return relevant if relevant else laws
