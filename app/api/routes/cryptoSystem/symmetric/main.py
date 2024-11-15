from fastapi import APIRouter
from . import shiftcipher, affine, vigenere

router = APIRouter()

router.include_router(shiftcipher.router)
router.include_router(affine.router)
router.include_router(vigenere.router)
