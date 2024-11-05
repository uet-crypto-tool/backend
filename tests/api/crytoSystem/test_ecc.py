import random
import secrets
from fastapi.testclient import TestClient
from app.core.ellipticCurve.domain import CurveDomainParamter


def test_pipeline_plain_text(test_client: TestClient):
    curve_name = random.choice(CurveDomainParamter.list())
    print(f"Testing Ecc on Curve Domain {curve_name}")
    secret_number = secrets.randbits(1024)
    response = test_client.post(
        "/crypto_system/ecc/generate_key",
        json={"curve_name": curve_name, "secret_number": str(secret_number)},
    )
    assert response.status_code == 200
    key = response.json()

    message = "hello world"
    response = test_client.post(
        "/crypto_system/ecc/encrypt",
        json={"publicKey": key["publicKey"], "message": message},
    )
    assert response.status_code == 200
    res = response.json()

    response = test_client.post(
        "/crypto_system/ecc/decrypt",
        json={
            "privateKey": key["privateKey"],
            "encrypted_message": res["encrypted_message"],
        },
    )
    assert response.status_code == 200

    res = response.json()
    assert message == res["decrypted_message"]
