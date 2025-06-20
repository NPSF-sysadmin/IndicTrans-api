from fastapi import Header, HTTPException

API_KEY = "CHANGE_ME_TO_SECURE_KEY"

def verify_api_key(api_key: str = Header(..., alias="api-subscription-key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
