import os
import sys

project_dir = os.path.abspath(os.path.dirname("../.."))
sys.path.append(project_dir)

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from backend.image_lookup import ImageFetcher
from backend.chatter import ChatProcessor
from backend.definition import DefinitionFetcher
from backend.loader import DictionaryLoader
from backend.ml_models.translation import Translator
from backend.models import ChatResponse, ChatRequest

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


loader = DictionaryLoader()
translator = Translator()
fetcher = DefinitionFetcher(loader, translator)
image_fetcher = ImageFetcher()
processor = ChatProcessor(fetcher, image_fetcher)


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    result = processor.detect_translation_request(req.message)
    output_result = result or processor.process_message(req.message)
    print(output_result)
    return output_result


# Mount the frontend
frontend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/dist")
)
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


@app.get("/{full_path:path}")
def serve_vue_app(full_path: str):
    return FileResponse(os.path.join(frontend_path, "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
