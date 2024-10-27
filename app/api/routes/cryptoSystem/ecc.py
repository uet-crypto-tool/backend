from fastapi import APIRouter
from app.core.cryptoSystem import ecc
from pydantic import BaseModel

router = APIRouter()


@router.post("/ecc/generate_key")
async def ecc_generate_key(curve_name: str):
    private_key, public_key = ecc.generateKey(curve_name)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


class ecc_EncryptRequest(BaseModel):
    pass


@router.post("/ecc/encrypt")
async def ecc_encrypt(req: ecc_EncryptRequest):
    return "ecc_encrypt"


class ecc_DecryptRequest(BaseModel):
    pass


@router.post("/ecc/decrypt")
async def ecc_decrypt(req: ecc_EncryptRequest):
    return "ecc_decrypt"
