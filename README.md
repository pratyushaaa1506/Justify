# JusticeLens Backend

JusticeLens is an AI-powered legal assistant designed to help users navigate legal information and processes efficiently. This backend provides a robust API for interacting with the JusticeLens system.

## Tech Stack
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- python-multipart

## Folder Structure
```
backend/
├── app/
│   └── main.py
├── requirements.txt
└── README.md
```

## Steps to Run the Server
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoint Test
- **GET /ping**
  - Returns:
    ```json
    {
      "status": "alive",
      "message": "JusticeLens backend is running"
    }
    ```

## API Documentation
- Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
