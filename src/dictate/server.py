"""FastAPI server for Whisper transcription"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import mlx_whisper

app = FastAPI()

# MLX Whisper automatically uses Apple Silicon optimization  
model_name = "mlx-community/whisper-large-v3-mlx"

class TranscribeRequest(BaseModel):
    file_path: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/transcribe/")
async def transcribe(request: TranscribeRequest):
    result = mlx_whisper.transcribe(request.file_path, path_or_hf_repo=model_name)
    text = result["text"].strip()
    return {"text": text}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=4242)

if __name__ == "__main__":
    run_server()
