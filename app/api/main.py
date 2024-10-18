from fastapi import APIRouter

from app.api.routes.cryptoSystem.classic import shift
from app.api.routes.cryptoSystem.modern import rsa
from app.api.routes.ellipticCurve import ellipticCurve

api_router = APIRouter()

api_router.include_router(
    shift.router, prefix="/cryptoSystem/classic/shift", tags=["Classic CryptoSystem"])
api_router.include_router(
    rsa.router, prefix="/cryptoSystem/modern/rsa", tags=["Modern CryptoSystem"])
api_router.include_router(
    ellipticCurve.router, prefix="/cryptosys/ecc", tags=["Elliptic Curve"])
