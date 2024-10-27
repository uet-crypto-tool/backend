from app.core.ellipticCurve import ellipticCurve, domain
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()


@router.get("/domains")
async def elliptic_curve_domain_params():
    return domain.CurveDomainParamter.list()


@router.get("/domains/{name}")
async def elliptice_curve_domain_param(name: str):
    return domain.CurveDomainParamter[name]
