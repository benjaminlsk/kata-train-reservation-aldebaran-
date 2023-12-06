import json
import httpx


def get_train_data(train_id):
    client = httpx.Client()
    response = client.get(f"http://127.0.0.1:8081/data_for_train/{train_id}")
    response.raise_for_status()
    return response.json()


def reset_train(train_id):
    client = httpx.Client()
    response = client.post(f"http://127.0.0.1:8081/reset/{train_id}")
    response.raise_for_status()


def test_reserve_seats_from_empty_train():
    train_id = "express_2000"
    reset_train(train_id)

    client = httpx.Client()
    response = client.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 4}
    )
    assert response.status_code == 200, response.text
    reservation = response.json()
    assert reservation["train_id"] == "express_2000"
    assert len(reservation["seats"]) == 4
    assert reservation["seats"] == ["1A", "2A", "3A", "4A"]


def test_reserve_four_additional_seats():
    train_id = "express_2000"
    reset_train(train_id)

    client = httpx.Client()
    response = client.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 4}
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 4}
    )
    assert response.status_code == 200, response.text
    reservation = response.json()
    assert reservation["train_id"] == "express_2000"
    assert len(reservation["seats"]) == 4
    assert reservation["seats"] == ["5A", "6A", "7A", "8A"]


# Additional tests based on the provided context and rules


def test_overall_train_capacity_limit():
    train_id = "express_2000"
    reset_train(train_id)

    client = httpx.Client()
    # Assuming the train has 100 seats for simplicity
    response = client.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 71}
    )
    assert response.status_code == 400


def test_individual_coach_capacity_limit():
    train_id = "express_2000"
    reset_train(train_id)

    client = httpx.Client()
    # Assuming each coach has 20 seats, trying to reserve 15 seats in one coach
    response = client.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 15}
    )
    assert response.status_code == 200
    reservation = response.json()
    # Check if all reserved seats are in the same coach
    coach = reservation["seats"][0][-1]  # Extract coach letter
    assert all(seat[-1] == coach for seat in reservation["seats"])


def test_impossible_reservation_request():
    train_id = "express_2000"
    reset_train(train_id)

    client = httpx.Client()
    # Assuming the train is almost fully booked and only 3 seats are available
    # Try to reserve 4 seats
    response = client.post(
        "http://127.0.0.1:8083/reserve", json={"train_id": train_id, "count": 4}
    )
    assert response.status_code == 400
