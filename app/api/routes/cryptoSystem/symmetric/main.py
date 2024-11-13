from fastapi import APIRouter
from . import shift, affine, vigenere

router = APIRouter()

router.include_router(shift.router)
router.include_router(affine.router)
router.include_router(vigenere.router)
