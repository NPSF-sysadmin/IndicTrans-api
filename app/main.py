from fastapi import FastAPI, Depends
from uuid import uuid4
from .schema import TranslateRequest, TranslateResponse
from .model import translate
from .auth import verify_api_key
from .model import safe_translate 

app = FastAPI()

@app.post("/translate", response_model=TranslateResponse)
async def translate_text(req: TranslateRequest, api_key: str = Depends(verify_api_key)):
    translated, detected_lang = await safe_translate(
        req.input,
        req.source_language_code.value if hasattr(req.source_language_code, "value") else req.source_language_code,
        req.target_language_code.value if hasattr(req.target_language_code, "value") else req.target_language_code
    )
    return TranslateResponse(
        translated_text=translated,
        source_language_code=detected_lang,
        request_id=str(uuid4())
    )