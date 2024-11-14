from fastapi.testclient import TestClient
import secrets


def test_pipeline(test_client: TestClient):
    response = test_client.post("/prime/generate", json={"bit_length": 100})
    assert response.status_code == 200
    p = response.json()
    a = secrets.randbits(8)

    response = test_client.post(
        "/crypto_system/asymmetric/elgamal/generate_key",
        json={"p": str(p), "a": str(a)},
    )
    assert response.status_code == 200
    key = response.json()
    print(key)

    message = str(secrets.randbits(8))
    response = test_client.post(
        "/crypto_system/asymmetric/elgamal/encrypt",
        json={"publicKey": key["publicKey"], "message": message},
    )
    assert response.status_code == 200
    res = response.json()

    response = test_client.post(
        "/crypto_system/asymmetric/elgamal/decrypt",
        json={
            "privateKey": key["privateKey"],
            "encrypted_message": res["encrypted_message"],
        },
    )
    assert response.status_code == 200
    res = response.json()
    assert res["decrypted_message"] == message
