from fastapi import APIRouter
from . import primality, generator

router = APIRouter()

router.include_router(primality.router)
router.include_router(generator.router)
