from fastapi.testclient import TestClient
import secrets


def test_pipeline(test_client: TestClient):
    response = test_client.post("/prime/generate", json={"bitLength": 8})
    assert response.status_code == 200
    p = response.json()

    response = test_client.post("/prime/generate", json={"bitLength": 8})
    assert response.status_code == 200
    q = response.json()

    response = test_client.post(
        "/signature_scheme/rsa/generate_key", json={"p": p, "q": q})
    assert response.status_code == 200
    key = response.json()

    message = secrets.randbits(8)
    response = test_client.post(
        "/signature_scheme/rsa/sign", json={
            "privateKey": key["privateKey"],
            "message": message})
    assert response.status_code == 200
    signature = response.json()

    response = test_client.post(
        "/signature_scheme/rsa/verify", json={
            "publicKey": key["publicKey"],
            "message": message,
            "signature": signature})
    assert response.status_code == 200
    assert response.json() == True
