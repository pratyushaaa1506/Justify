from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
from app.agents.vision_agent import VisionAgent

router = APIRouter()
vision_agent = VisionAgent()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/vision/analyze")
async def analyze_vision(file: UploadFile = File(...)):
    try:
        # READ RAW BYTES (CRITICAL FIX)
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        ext = os.path.splitext(file.filename)[1]
        temp_filename = f"vision_{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)

        # 🔥 WRITE BYTES MANUALLY
        with open(temp_path, "wb") as f:
            f.write(file_bytes)

        # HARD VERIFICATION
        file_size = os.path.getsize(temp_path)
        print("VISION FILE PATH:", temp_path)
        print("VISION FILE SIZE:", file_size)

        if file_size == 0:
            raise HTTPException(status_code=400, detail="Saved file is empty")

        # Call Vision Agent
        result = vision_agent.analyze_document(temp_path)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File processing error: {str(e)}"
        )

    finally:
        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
    