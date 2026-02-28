
def generate_raw_llm(prompt: str) -> str:
    """
    Directly call Gemini with a custom prompt and return the raw text output.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, "text") else str(response)
import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted, NotFound

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Stable, supported model
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_llm_response(user_query: str, rag_context: list) -> str:

    # Build legal context for reference (plain text, not structured)
    context_str = "\n".join(
        [
            f"{item.get('law', '')}: {item.get('text', '')}".strip()
            for item in rag_context if item.get('law') or item.get('text')
        ]
    )

    prompt = f"""
You are JusticeLens, a professional and friendly AI legal assistant.

Your job is to help users understand their legal situation in simple terms.

IMPORTANT:
- Do not show your internal reasoning.
- Do not list laws mechanically.
- Do not explain classifications or confidence scores.
- Speak naturally, like a human legal advisor.

User's situation:
{user_query}

Relevant legal information (for your reference only):
{context_str}

Write a clear, well-structured response that explains:
1. What the issue likely is
2. Whether any law may apply (if relevant)
3. What the user should do next

Respond in clean paragraphs.
Do not mention analysis, context, or uncertainty explicitly.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except ResourceExhausted:
        return (
            "The AI reasoning service is temporarily unavailable due to usage limits. "
            "Based on the retrieved legal information above, this issue may relate to the listed laws. "
            "Please try again later for a detailed explanation."
        )

    except NotFound:
        return (
            "The AI model is currently unavailable. "
            "Relevant legal information was retrieved, but detailed reasoning cannot be generated at this moment."
        )
