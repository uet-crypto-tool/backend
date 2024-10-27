from fastapi import APIRouter
from . import rsa, elgamal, ecdsa

router = APIRouter()

router.include_router(rsa.router)
router.include_router(elgamal.router)
router.include_router(ecdsa.router)
