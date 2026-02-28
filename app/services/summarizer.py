from typing import List, Dict

def generate_summary(user_query: str, category: str, rag_results: List[Dict[str, str]]) -> Dict:
    # Short description of the issue
    issue = f"This issue relates to: {user_query.strip()}"

    # List applicable laws
    applicable_laws = [law.get("law", "Unknown Law") for law in rag_results]

    # Simple guidance based on category
    guidance_map = {
        "Cyber Crime": "Consider collecting evidence and contacting cyber crime authorities.",
        "Domestic Violence": "Seek immediate help from local protection officers or helplines.",
        "Labour Dispute": "Document your employment details and approach the labour department.",
        "Consumer Complaint": "Keep all receipts and file a complaint with consumer forums.",
        "Property Dispute": "Gather property documents and consult a property lawyer.",
        "General Legal Issue": "Describe your issue in detail to get more specific guidance."
    }
    guidance = guidance_map.get(category, guidance_map["General Legal Issue"])

    return {
        "issue": issue,
        "category": category,
        "applicable_laws": applicable_laws,
        "guidance": guidance
    }
