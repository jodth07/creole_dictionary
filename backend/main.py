import os
import re

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from back_translation import get_creole_definition
from models import ChatResponse, ChatRequest

app = FastAPI(title="Diksyonè Kreyòl API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    return {"message": "pong"}

def extract_words(text: str):
    patterns = [
        r"kisa\s+(\w+)\s+vle\s+di",
        r"kisa\s+yon\s+(\w+)\s+ye",
        r"kisa\s+(\w+)\s+ye",
        r"ki\s+siyifikasyon\s+(\w+)",
        r"sa\s+vle\s+di\s+(\w+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return [match.group(1)]  # return the captured keyword

    # Fallback: tokenize all words if no match
    return re.findall(r"\b\w+\b", text.lower())

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    words = extract_words(req.message)
    seen = set()
    definitions = []

    for word in words:
        if word not in seen:
            defn, source = get_creole_definition(word)
            definitions.append({
                "word": word,
                "definition": defn,
                "source": source
            })
            seen.add(word)

    if not definitions:
        return {"reply": "Mwen pa jwenn okenn definisyon.", "definitions": []}

    reply = "\n".join([f"*{d['word']}*: vle di {d['definition']} sous: {d['source']}" for d in definitions])
    return {"reply": reply, "definitions": definitions}


# Mount the frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/dist'))
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


@app.get("/{full_path:path}")
def serve_vue_app(full_path: str):
    return FileResponse(os.path.join(frontend_path, "index.html"))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)