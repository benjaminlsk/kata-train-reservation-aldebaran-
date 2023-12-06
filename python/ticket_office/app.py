from requests import Session
import json


from flask import Flask, request

class Session(Session):
    def request(self, method, url, *args, **kwargs):
        print(f"Request: {method} {url}")
        response = super().request(method, url, *args, **kwargs)
        print(f"Response: {response.status_code} {response.text}")
        return response


    
def reserve(seat_count, booking_reference, train_data):
    train_id = train_data["train_id"]

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
    
    return reservation_payload
    
