import random
from fastapi.testclient import TestClient
from app.core.ellipticCurve.domain import CurveDomainParamter


def test_pipeline(test_client: TestClient):
    curve_domain_name = random.choice(CurveDomainParamter.list())
    print(f"Testing Ecc on Curve Domain {curve_domain_name}")
    response = test_client.post(
        "/crypto_system/ecc/generate_key",
        json={"curve_domain_name": curve_domain_name}
    )
    assert response.status_code == 200
    key = response.json()

    curve_params = CurveDomainParamter[curve_domain_name].value

    message_point = curve_params["g"]
    response = test_client.post(
        "/crypto_system/ecc/encrypt", json={
            "publicKey": key["publicKey"],
            "message": {
                "x": message_point[0],
                "y": message_point[1],
            }
        }
    )
    assert response.status_code == 200
    res = response.json()

    response = test_client.post(
        "/crypto_system/ecc/decrypt", json={
            "privateKey": key["privateKey"],
            "M1": res["M1"],
            "M2": res["M2"],
        }
    )
    assert response.status_code == 200

    res = response.json()
    decrypted_point = res["M"]
    assert decrypted_point["x"] == message_point[0]
    assert decrypted_point["y"] == message_point[1]
