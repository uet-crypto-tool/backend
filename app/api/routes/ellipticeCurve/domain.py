from app.core.ellipticCurve.domain import CurveDomainParamter
from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/domains", summary="Get a list of available elliptic curve domain parameters"
)
async def elliptic_curve_domain_params():
    return CurveDomainParamter.list()


@router.get(
    "/domains/{name}", summary="Get specific elliptic curve domain parameter by name"
)
async def elliptic_curve_domain_param(name: str):
    return CurveDomainParamter[name].value.to_json()
