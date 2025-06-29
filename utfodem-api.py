from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import random

# --- Your codex logic ---
RANGE_1 = (0x4E00, 0x9FFF)
RANGE_2 = (0x3400, 0x4DBF)
RANGE_3 = (0xAC00, 0xD7AF)
CODEX = (
    [chr(i) for i in range(RANGE_1[0], RANGE_1[1] + 1)] +
    [chr(i) for i in range(RANGE_2[0], RANGE_2[1] + 1)] +
    [chr(i) for i in range(RANGE_3[0], RANGE_3[1] + 1)]
)
CODEX_SIZE = len(CODEX)

def get_shuffled_codex(seed_char):
    random.seed(ord(seed_char))
    shuffled = CODEX.copy()
    random.shuffle(shuffled)
    return shuffled

def encode(text):
    data = text.encode('utf-8')
    num = int.from_bytes(data, 'big') if data else 0
    seed_char = random.choice(CODEX)
    codex = get_shuffled_codex(seed_char)
    chars = []
    base = CODEX_SIZE
    if num == 0:
        chars.append(codex[0])
    else:
        while num > 0:
            chars.append(codex[num % base])
            num //= base
    return seed_char + ''.join(reversed(chars))

def decode(encoded):
    if not encoded:
        return ""
    seed_char = encoded[0]
    codex = get_shuffled_codex(seed_char)
    base = CODEX_SIZE
    num = 0
    for c in encoded[1:]:
        idx = codex.index(c)
        num = num * base + idx
    if num == 0:
        return ""
    byte_length = (num.bit_length() + 7) // 8
    data = num.to_bytes(byte_length, 'big')
    return data.decode('utf-8')

# --- FastAPI setup ---
app = FastAPI()

class EncodeRequest(BaseModel):
    text: str

class EncodeResponse(BaseModel):
    encoded: str

class DecodeRequest(BaseModel):
    encoded: str

class DecodeResponse(BaseModel):
    text: str

@app.post("/encode", response_model=EncodeResponse)
def api_encode(req: EncodeRequest):
    try:
        result = encode(req.text)
        return {"encoded": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/decode", response_model=DecodeResponse)
def api_decode(req: DecodeRequest):
    try:
        result = decode(req.encoded)
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
