"""FastAPI server for Whisper transcription"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from faster_whisper import WhisperModel

app = FastAPI()

model = WhisperModel("large", device="auto", compute_type="default")
# Enable in case you want to run on CPU, but it's much slower
#model = WhisperModel("medium", device="cpu", compute_type="int8")

class TranscribeRequest(BaseModel):
    file_path: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/transcribe/")
async def transcribe(request: TranscribeRequest):
    segments, info = model.transcribe(request.file_path)
    text = " ".join([segment.text.strip() for segment in segments])
    return {"text": text}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=4242)

if __name__ == "__main__":
    run_server()
