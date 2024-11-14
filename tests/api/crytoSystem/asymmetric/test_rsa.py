from fastapi.testclient import TestClient
import secrets


def test_pipeline(test_client: TestClient):
    response = test_client.post("/prime/generate", json={"bit_length": 100})
    assert response.status_code == 200
    p = response.json()

    response = test_client.post("/prime/generate", json={"bit_length": 100})
    assert response.status_code == 200
    q = response.json()

    response = test_client.post(
        "/crypto_system/asymmetric/rsa/generate_key", json={"p": str(p), "q": str(q)}
    )
    assert response.status_code == 200
    key = response.json()

    message = str(secrets.randbits(8))
    response = test_client.post(
        "/crypto_system/asymmetric/rsa/encrypt",
        json={"publicKey": key["publicKey"], "message": message},
    )
    assert response.status_code == 200
    res = response.json()

    response = test_client.post(
        "/crypto_system/asymmetric/rsa/decrypt",
        json={
            "privateKey": key["privateKey"],
            "encrypted_message": res["encrypted_message"],
        },
    )
    assert response.status_code == 200
    res = response.json()
    decrypted_message = res["decrypted_message"]
    assert decrypted_message == message
