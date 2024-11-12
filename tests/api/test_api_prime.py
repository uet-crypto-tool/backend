from fastapi.testclient import TestClient


def test_primality(test_client: TestClient):
    response = test_client.post("/prime/check", json={"number": 3})
    assert response.status_code == 200
    assert response.json() == {"isPrime": True}

    response = test_client.post("/prime/check", json={"number": 4})
    assert response.status_code == 200
    assert response.json() == {"isPrime": False}

    response = test_client.post("/prime/aks/check", json={"number": 3})
    assert response.status_code == 200
    assert response.json() == {"isPrime": True}

    response = test_client.post("/prime/aks/check", json={"number": 4})
    assert response.status_code == 200
    assert response.json() == {"isPrime": False}

    response = test_client.post("/prime/miller_rabbin/check", json={"number": 3})
    assert response.status_code == 200
    assert response.json() == {"isPrime": True}

    response = test_client.post("/prime/miller_rabbin/check", json={"number": 6})
    assert response.status_code == 200
    assert response.json() == {"isPrime": False}


def test_generator_prime(test_client: TestClient):
    response = test_client.post("/prime/generate", json={"bit_length": 8})
    assert response.status_code == 200
    prime = response.json()

    response = test_client.post("/prime/check", json={"number": prime})
    assert response.status_code == 200
    assert response.json() == {"isPrime": True}
