from fastapi import APIRouter
from app.core.ellipticCurve.point import PointType
from app.core.cryptoSystem import ecc
from pydantic import BaseModel

router = APIRouter()


class GenerateKeyResponse(BaseModel):
    privateKey: ecc.PrivateKey
    publicKey: ecc.PublicKey


class EncryptRequest(BaseModel):
    publicKey: ecc.PublicKey
    message: PointType


class EncryptResponse(BaseModel):
    M1: PointType
    M2: PointType


class DecryptRequest(BaseModel):
    privateKey: ecc.PrivateKey
    M1: PointType
    M2: PointType


class DecryptResponse(BaseModel):
    M: PointType


@router.post("/ecc/generate_key", response_model=GenerateKeyResponse)
async def ecc_generate_key(seed: ecc.Seed):
    private_key, public_key = ecc.generateKeyOnDomain(seed.curve_domain_name)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


@router.post("/ecc/encrypt", response_model=EncryptResponse)
async def ecc_encrypt(req: EncryptRequest):
    M1, M2 = ecc.encrypt(req.publicKey, req.message)
    return EncryptResponse(M1=M1, M2=M2)


@router.post("/ecc/decrypt", response_model=DecryptResponse)
async def ecc_decrypt(req: DecryptRequest):
    M1 = PointType(x=req.M1.x,
                   y=req.M1.y)
    M2 = PointType(x=req.M2.x,
                   y=req.M2.y)
    return DecryptResponse(M=ecc.decrypt(req.privateKey, (M1, M2)))
