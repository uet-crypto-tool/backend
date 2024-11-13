from fastapi import APIRouter
from app.api.routes.cryptoSystem.main import router as cryptoSytemRouter
from app.api.routes.signatureScheme.main import router as signatureSchemeRouter
from app.api.routes.ellipticeCurve.main import router as ellipticCurveRouter
from app.api.routes.prime.main import router as primeRouter

router = APIRouter()


@router.get("/api/healthchecker", tags=["Health"])
def health_checker():
    return {"connected": True}


router.include_router(
    primeRouter,
    prefix="/prime",
    tags=["Prime"],
)

router.include_router(
    cryptoSytemRouter,
    prefix="/crypto_system",
)

router.include_router(
    signatureSchemeRouter,
    prefix="/signature_scheme",
    tags=["Signature Scheme"],
)

router.include_router(
    ellipticCurveRouter,
    prefix="/elliptice_curve",
    tags=["Elliptic Curve"],
)
