from fastapi import APIRouter
from . import domain

router = APIRouter()

router.include_router(domain.router)
