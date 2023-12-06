from requests import Session
import json


from flask import Flask, request

from train_data import ensure_field_in_body

class Session(Session):
    def request(self, method, url, *args, **kwargs):
        print(f"Request: {method} {url}")
        response = super().request(method, url, *args, **kwargs)
        print(f"Response: {response.status_code} {response.text}")
        return response
    
def create_app():
    app = Flask("ticket_office")

    @app.post("/reserve")
    @ensure_field_in_body("count")
    @ensure_field_in_body("train_id")
    def reserve():
        payload = request.json
        seat_count = payload["count"]
        train_id = payload["train_id"]

        session = Session()

        booking_reference = session.get("http://localhost:8080/booking_reference").text

        train_data = session.get(
            f"http://localhost:8080/data_for_train/" + train_id
        ).json()
        available_seats = (
            s
            for s in train_data["seats"].values()
            if s["coach"] == "A" and not s["booking_reference"]
        )
        to_reserve = []
        for i in range(seat_count):
            to_reserve.append(next(available_seats))

        seat_ids = [s["seat_number"] + s["coach"] for s in to_reserve]
        reservation = {
            "train_id": train_id,
            "booking_reference": booking_reference,
            "seats": seat_ids,
        }

        reservation_payload = {
            "train_id": reservation["train_id"],
            "seats": reservation["seats"],
            "booking_reference": reservation["booking_reference"],
        }

        response = session.post(
            "http://localhost:8080/reserve",
            json=reservation_payload,
        )
        assert response.status_code == 200, response.text
        response = response.json()

        return json.dumps(reservation)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8083)
