# IndicTrans API

A lightweight FastAPI-based wrapper for deploying AI4Bharat's IndicTrans2 models as an OpenAI-compatible translation API. This service wraps around a custom IndicTrans2 model and provides endpoints for translation in a format compatible with OpenAI's `chat/completions` interface.

## 🌐 API Overview

- **GET** `/v1/models`\
  Returns available translation model information.

- **POST** `/v1/chat/completions`\
  Accepts OpenAI-style message format and returns translation from English to Indian languages (e.g., Hindi, Gujarati).

### Example Input

```json
{
  "model": "ai4bharat/indictrans2-en-indic-1B",
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ]
}
```

### Example Output

```json
{
  "id": "uuid",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "indictrans-1b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "હેલ્લો, તમે કેમ છો?"
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
```

---

## 🚀 Run Locally with Docker

```bash
docker build -t indictrans-api .
docker run -p 8088:8088 indictrans-api
```

Access the service at `http://localhost:8088/v1/chat/completions`.

---

## 🧠 Model Info

This API uses models from [Hugging Face](https://huggingface.co/prajdabre/rotary-indictrans2-en-indic-1B) and the [IndicTransToolkit](https://github.com/VarunGumma/IndicTransToolkit).

---

## 🧰 Tech Stack

- Python 3.10
- FastAPI
- HuggingFace Transformers
- Docker
- FlashAttention (for GPU acceleration)

---