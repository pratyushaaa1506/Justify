
from typing import Dict, Any
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Legal categories
CATEGORIES = [
    "Cyber Crime",
    "Domestic Violence",
    "Labour Dispute",
    "Consumer Complaint",
    "Property Dispute",
    "General Legal Issue"
]

# Rule-based fallback classifier
def rule_based_classify(text: str) -> Dict[str, Any]:
    keywords = {
        "Cyber Crime": ["cyber", "hacking", "phishing", "online fraud", "identity theft", "ransomware", "malware", "internet crime"],
        "Domestic Violence": ["domestic violence", "abuse", "spouse", "partner", "family violence", "physical assault", "emotional abuse"],
        "Labour Dispute": ["labour", "employment", "worker", "salary", "wages", "job", "workplace", "union", "layoff", "termination", "company", "employer"],
        "Consumer Complaint": ["consumer", "complaint", "refund", "product", "service", "warranty", "customer", "purchase", "seller"],
        "Property Dispute": ["property", "land", "ownership", "title", "real estate", "boundary", "encroachment", "tenant", "lease"]
    }
    text_lower = text.lower()
    best_category = "General Legal Issue"
    best_match_count = 0
    best_total_keywords = 1
    for category, kw_list in keywords.items():
        match_count = sum(1 for kw in kw_list if re.search(r"\b" + re.escape(kw) + r"\b", text_lower))
        if match_count > best_match_count:
            best_category = category
            best_match_count = match_count
            best_total_keywords = len(kw_list)
    confidence = best_match_count / best_total_keywords if best_match_count > 0 else 0.0
    return {"category": best_category, "confidence": round(confidence, 2)}

# Load LegalBERT model and tokenizer globally
_tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
_model = AutoModelForSequenceClassification.from_pretrained("nlpaueb/legal-bert-base-uncased", num_labels=len(CATEGORIES))

class LegalIssueClassifier:
    @staticmethod
    def classify(text: str) -> Dict[str, Any]:
        # Tokenize
        inputs = _tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = _model(**inputs).logits
            probs = F.softmax(logits, dim=1).squeeze().cpu().numpy()
        max_idx = int(probs.argmax())
        max_prob = float(probs[max_idx])
        category = CATEGORIES[max_idx]
        # Fallback to rule-based if confidence < 0.4
        if max_prob < 0.4:
            return rule_based_classify(text)
        return {"category": category, "confidence": round(max_prob, 2)}
