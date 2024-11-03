from app.core.ellipticCurve.domain import CurveDomainParamter
from fastapi import APIRouter

router = APIRouter()


@router.get("/domains")
async def elliptic_curve_domain_params():
    return CurveDomainParamter.list()


@router.get("/domains/{name}")
async def elliptice_curve_domain_param(name: str):
    return CurveDomainParamter[name].value.to_json()
