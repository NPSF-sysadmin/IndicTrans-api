import asyncio
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor

semaphore = asyncio.Semaphore(2)  # Or more depending on memory/GPU

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
#MODEL_NAME = "ai4bharat/indictrans2-en-indic-1B"
MODEL_NAME = "prajdabre/rotary-indictrans2-en-indic-1B"



tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.float16,
    attn_implementation="flash_attention_2"
).to(DEVICE)

# Simplified lang map; adjust as needed
LANG_CODE_MAP = {
    "auto": "eng_Latn",
    "hi-IN": "hin_Deva",
    "bn-IN": "ben_Beng",
}

def translate(text: str, src_lang: str, tgt_lang: str):
    ip = IndicProcessor(inference=True)  # safer to keep per request
    src = LANG_CODE_MAP.get(src_lang, src_lang)
    tgt = LANG_CODE_MAP.get(tgt_lang, tgt_lang)

    batch = ip.preprocess_batch([text], src_lang=src, tgt_lang=tgt)
    inputs = tokenizer(batch, padding="longest", truncation=True,  return_tensors="pt", max_length=2048,).to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            num_return_sequences=1,
            length_penalty=1.5,
            repetition_penalty=2.0,
            max_new_tokens=2048,
            num_beams=10,
            early_stopping=True)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    translated = ip.postprocess_batch(decoded, lang=tgt)[0]
    return translated, src

async def safe_translate(text: str, src_lang: str, tgt_lang: str):
    async with semaphore:
        return await asyncio.to_thread(translate, text, src_lang, tgt_lang)
