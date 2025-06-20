from pydantic import BaseModel, Field
from typing import Annotated, Literal
from enum import Enum


class TargetLanguage(str, Enum):
    asm_Beng = "asm_Beng"
    ben_Beng = "ben_Beng"
    brx_Deva = "brx_Deva"
    doi_Deva = "doi_Deva"
    gom_Deva = "gom_Deva"
    guj_Gujr = "guj_Gujr"
    hin_Deva = "hin_Deva"
    kan_Knda = "kan_Knda"
    kas_Arab = "kas_Arab"
    kas_Deva = "kas_Deva"
    mai_Deva = "mai_Deva"
    mal_Mlym = "mal_Mlym"
    mar_Deva = "mar_Deva"
    mni_Beng = "mni_Beng"
    mni_Mtei = "mni_Mtei"
    npi_Deva = "npi_Deva"
    ory_Orya = "ory_Orya"
    pan_Guru = "pan_Guru"
    san_Deva = "san_Deva"
    sat_Olck = "sat_Olck"
    snd_Arab = "snd_Arab"
    snd_Deva = "snd_Deva"
    tam_Taml = "tam_Taml"
    tel_Telu = "tel_Telu"
    urd_Arab = "urd_Arab"


class TranslateRequest(BaseModel):
    input: Annotated[str, Field(..., description="Text to translate")]
    source_language_code: Annotated[Literal["eng_Latn"], Field(..., description="Must be 'eng_Latn'")]
    target_language_code: Annotated[TargetLanguage, Field(..., description="Target language code")]


class TranslateResponse(BaseModel):
    translated_text: Annotated[str, Field(..., description="Translated text")]
    source_language_code: Annotated[str, Field(..., description="Detected or source language")]
    request_id: str
