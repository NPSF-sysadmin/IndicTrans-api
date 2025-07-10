from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import json
import time
import asyncio

from .model import safe_translate 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/v1/models")
def get_models():
    return {
        "data": [
            {
                "id": "ai4bharat/indictrans2-en-indic-1B",
                "object": "model",
                "created": 0,
                "owned_by": "you"
            }
        ]
    }

@app.post("/v1/chat/completions")
async def chat_completion(request: Request):
    try:
        req_json = await request.json()
        print(f"\n=== Incoming Chat Completion Request ===\n{json.dumps(req_json, indent=2)}\n")

        messages = req_json.get("messages", [])
        if not messages:
            return JSONResponse({"error": "No messages provided"}, status_code=400)

        last_user_msg = [m for m in messages if m["role"] == "user"]
        if not last_user_msg:
            return JSONResponse({"error": "No user message provided"}, status_code=400)

        text = last_user_msg[-1]["content"]
        translated_text, src_lang = await safe_translate(text, "eng_Latn", "mar_Deva")

        # Streaming
        if req_json.get("stream", False):
            def event_stream():
                data = {
                    "id": str(uuid4()),
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "indictrans-1b",
                    "choices": [
                        {
                            "delta": {
                                "role": "assistant",
                                "content": translated_text
                            },
                            "index": 0,
                            "finish_reason": None
                        }
                    ]
                }
                yield f"data: {json.dumps(data)}\n\n"
                time.sleep(0.1)
                yield "data: [DONE]\n\n"

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        # Regular (non-streaming) response
        return {
            "id": str(uuid4()),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "indictrans-1b",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": translated_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
    except Exception as e:
        print(f"❌ Exception in /v1/chat/completions: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=400)
