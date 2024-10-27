from fastapi import APIRouter
from app.core.ellipticCurve.point import PointType
from app.core.cryptoSystem import ecc
from pydantic import BaseModel

router = APIRouter()


class EncryptRequest(BaseModel):
    publicKey: ecc.PublicKey
    message: PointType


class DecryptRequest(BaseModel):
    privateKey: ecc.PrivateKey
    M1: PointType
    M2: PointType


@router.post("/ecc/generate_key")
async def ecc_generate_key(seed: ecc.Seed):
    private_key, public_key = ecc.generateKeyOnDomain(seed.curve_domain_name)
    return {
        "privateKey": private_key,
        "publicKey": public_key
    }


@router.post("/ecc/encrypt")
async def ecc_encrypt(req: EncryptRequest):
    return ecc.encrypt(req.publicKey, req.message)


@router.post("/ecc/decrypt")
async def ecc_decrypt(req: DecryptRequest):
    M1 = PointType(x=req.M1.x,
                   y=req.M1.y)
    M2 = PointType(x=req.M2.x,
                   y=req.M2.y)
    return ecc.decrypt(req.privateKey, (M1, M2))
