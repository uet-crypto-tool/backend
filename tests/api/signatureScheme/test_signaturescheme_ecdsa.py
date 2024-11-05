import random
from fastapi.testclient import TestClient
from app.core.ellipticCurve.domain import CurveDomainParamter
import secrets


def test_pipeline(test_client: TestClient):
    curve_name = random.choice(CurveDomainParamter.list())
    print(f"Testing ECDSA on Curve Domain {curve_name}")
    response = test_client.post(
        "/signature_scheme/ecdsa/generate_key", json={"curve_name": curve_name}
    )
    assert response.status_code == 200
    key = response.json()

    message = str(secrets.randbits(8))
    response = test_client.post(
        "/signature_scheme/ecdsa/sign",
        json={"privateKey": key["privateKey"], "message": message},
    )
    assert response.status_code == 200
    res = response.json()

    response = test_client.post(
        "/signature_scheme/ecdsa/verify",
        json={
            "publicKey": key["publicKey"],
            "message": message,
            "signature": res["signature"],
        },
    )
    assert response.status_code == 200
    res = response.json()

    is_valid = res["is_valid"]
    assert is_valid == True
