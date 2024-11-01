from fastapi import APIRouter
from app.core.ellipticCurve.point import PointType
from app.core.cryptoSystem import ecc
from pydantic import BaseModel
from typing import Tuple

router = APIRouter()


class GenerateKeyResponse(BaseModel):
    privateKey: ecc.PrivateKey
    publicKey: ecc.PublicKey


class EncryptRequest(BaseModel):
    publicKey: ecc.PublicKey
    message: str


class EncryptResponse(BaseModel):
    encrypted_pairs: Tuple[Tuple[PointType, PointType], ...]


class DecryptRequest(BaseModel):
    privateKey: ecc.PrivateKey
    encrypted_pairs: Tuple[Tuple[PointType, PointType], ...]


class DecryptResponse(BaseModel):
    decrypted_message: str


@router.post("/ecc/generate_key", response_model=GenerateKeyResponse)
async def ecc_generate_key(seed: ecc.Seed):
    private_key, public_key = ecc.generateKeyOnDomain(seed.curve_domain_name)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


@router.post("/ecc/encrypt", response_model=EncryptResponse)
async def ecc_encrypt(req: EncryptRequest):
    encrypted_pairs = ecc.encryptPlainText(
        req.publicKey, req.message)
    print(encrypted_pairs)
    return EncryptResponse(encrypted_pairs=encrypted_pairs)


@router.post("/ecc/decrypt", response_model=DecryptResponse)
async def ecc_decrypt(req: DecryptRequest):
    decrypted_message = ecc.decryptPlainText(
        req.privateKey, req.encrypted_pairs)
    return DecryptResponse(decrypted_message=decrypted_message)
