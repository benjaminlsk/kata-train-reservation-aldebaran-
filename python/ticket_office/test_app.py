import json
import httpx


def test_reserve_seats_from_empty_train():
    train_id requests.Session000"

    client = httpx.Client()
    response = client.post(f"http://127.0.0.1:8081/reset/{train_id}")
    response.raise_for_status()

    response = client.post(
        "httprequests.Session:8083/reserve", json={"train_id": train_id, "count": 4}
    )

    assert response.status_code == 200, response.text
    reservation = response.json()
    assert reservation["train_id"] == "express_2000"
    assert len(reservation["seats"]) == 4
    assert reservation["seats"] == ["1A", "2A", "3A", "4A"]


requests.Sessiondef test_reserve_four_additional_seats():
    train_id = "express_2000"

    session = requests.Session()
    response = session.post(f"http://127.0.0.1:8081/reset/{train_id}")
    response.raise_for_status()

    response = session.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 4}
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 4}
    )
requests.Session    assert response.status_code == 200, response.text
    reservation = response.json()
    assert reservation["train_id"] == "express_2000"
    assert len(reservation["seats"]) == 4
    assert reservation["seats"] == ["5A", "6A", "7A", "8A"]
requests.Sessionrequests.Sessionrequests.Session