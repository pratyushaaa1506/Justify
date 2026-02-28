
from app.services.ocr_engine import OCREngine
from app.services.gemini_client import generate_raw_llm
import re

class VisionAgent:

    def analyze_document(self, image_path: str) -> dict:
        extracted_text = OCREngine.extract_text(image_path)

        if not extracted_text:
            return {
                "error": "OCR failed or no text found in document.",
                "document_type": "unknown",
                "fraud_risk": "unknown",
                "confidence_score": 0.0,
                "detected_entities": {},
                "agent_flags": [],
                "summary": ""
            }

        # --- 1. Entity Extraction (Rule-based) ---
        detected_entities = self._extract_entities(extracted_text)

        # --- 2. Fraud Risk Scoring (Agent Logic) ---
        fraud_risk, risk_score = self._score_fraud(detected_entities)

        # --- 3. Confidence Score ---
        confidence_score = self._compute_confidence(detected_entities, risk_score)

        # --- 4. Agent Flags ---
        agent_flags = []
        if fraud_risk == "high":
            agent_flags.append("needs_human_review")

        # --- 5. LLM Summary (Hybrid) ---
        prompt = f"""
You are a legal document analysis assistant.\n\nExtracted Text:\n{extracted_text}\n\nTasks:\n1. Identify document type (receipt, invoice, FIR, ID, agreement, unknown)\n2. Provide a short summary\n\nRespond STRICTLY in JSON format with keys: document_type, summary\n"""
        try:
            response = generate_raw_llm(prompt)
            # Fallbacks if LLM fails
            document_type = "unknown"
            summary = ""
            if response:
                # Try to parse JSON keys from LLM output
                import json
                try:
                    parsed = json.loads(response)
                    document_type = parsed.get("document_type", "unknown")
                    summary = parsed.get("summary", response.strip())
                except Exception:
                    summary = response.strip()

            return {
                "document_type": document_type,
                "fraud_risk": fraud_risk,
                "confidence_score": confidence_score,
                "detected_entities": detected_entities,
                "agent_flags": agent_flags,
                "summary": summary
            }
        except Exception as e:
            print("VISION AGENT ERROR:", e)
            return {
                "error": "Document analysis failed.",
                "document_type": "unknown",
                "fraud_risk": "unknown",
                "confidence_score": 0.0,
                "detected_entities": {},
                "agent_flags": [],
                "summary": ""
            }

    def _extract_entities(self, text: str) -> dict:
        # Amounts: ₹, Rs, numbers
        amounts = re.findall(r"(?:₹|Rs\.?|INR)?\s?([0-9,]+\.?[0-9]*)", text, re.IGNORECASE)
        # Dates: dd-mm-yyyy, dd/mm/yyyy, yyyy-mm-dd, etc.
        dates = re.findall(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b", text)
        # UPI IDs: pattern like name@bank
        upi_ids = re.findall(r"[\w.]+@[\w]+", text)
        # Transaction IDs: alphanumeric, 8+ chars
        txn_ids = re.findall(r"\b[A-Z0-9]{8,}\b", text)
        return {
            "amounts": amounts,
            "dates": dates,
            "upi_ids": upi_ids,
            "transaction_ids": txn_ids
        }

    def _score_fraud(self, entities: dict):
        # Simple rule-based scoring
        score = 0
        if not entities.get("amounts"):
            score += 1
        if not entities.get("upi_ids") and not entities.get("transaction_ids"):
            score += 1
        # Map to risk
        if score == 0:
            risk = "low"
        elif score == 1:
            risk = "medium"
        else:
            risk = "high"
        return risk, score

    def _compute_confidence(self, entities: dict, risk_score: int) -> float:
        # Confidence is higher if more entities are found and risk is low
        num_signals = 0
        if entities.get("amounts"):
            num_signals += 1
        if entities.get("upi_ids") or entities.get("transaction_ids"):
            num_signals += 1
        if entities.get("dates"):
            num_signals += 1
        # Base confidence
        confidence = 0.4 + 0.2 * num_signals
        # Penalty for high risk
        if risk_score == 2:
            confidence -= 0.2
        return min(max(confidence, 0.0), 1.0)
    