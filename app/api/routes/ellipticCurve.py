from app.core.ellipticCurve import ellipticCurve, registry
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()


@router.get("/registries")
async def elliptic_curve_registries():
    return registry.EC_CURVE_REGISTRY


@router.get("/registrie/{name}")
async def elliptic_curve_registries(name: str):
    return registry.EC_CURVE_REGISTRY[name]
