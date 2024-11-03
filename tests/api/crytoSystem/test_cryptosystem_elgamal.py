from fastapi.testclient import TestClient
import secrets


def test_pipeline(test_client: TestClient):
    response = test_client.post("/prime/generate", json={"bitLength": 8})
    assert response.status_code == 200
    p = response.json()
    a = secrets.randbits(8)

    response = test_client.post(
        "/crypto_system/elgamal/generate_key", json={"p": p, "a": a}
    )
    assert response.status_code == 200
    key = response.json()
    print(key)

    message = secrets.randbits(8)
    response = test_client.post(
        "/crypto_system/elgamal/encrypt",
        json={"publicKey": key["publicKey"], "message": message},
    )
    assert response.status_code == 200
    res = response.json()
    encrypted_message = res["encrypted_message"]

    response = test_client.post(
        "/crypto_system/elgamal/decrypt",
        json={"privateKey": key["privateKey"], "encrypted_message": encrypted_message},
    )
    assert response.status_code == 200
    res = response.json()
    decrypted_message = res["decrypted_message"]
    assert decrypted_message == message
