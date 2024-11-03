from fastapi.testclient import TestClient
import secrets


def test_pipeline(test_client: TestClient):
    response = test_client.post("/prime/generate", json={"bitLength": 8})
    assert response.status_code == 200
    p = response.json()
    a = secrets.randbits(8)

    response = test_client.post(
        "/signature_scheme/elgamal/generate_key", json={"p": p, "a": a}
    )
    assert response.status_code == 200
    key = response.json()

    message = secrets.randbits(8)
    response = test_client.post(
        "/signature_scheme/elgamal/sign",
        json={"privateKey": key["privateKey"], "message": message},
    )
    assert response.status_code == 200
    res = response.json()
    signature = res["signature"]

    response = test_client.post(
        "/signature_scheme/elgamal/verify",
        json={
            "publicKey": key["publicKey"],
            "message": message,
            "signature": signature,
        },
    )
    assert response.status_code == 200
    res = response.json()
    is_valid = res["is_valid"]
    assert is_valid == True
