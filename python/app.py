import json

from flask import Flask, jsonify, request

from booking_reference.app import BookingReference
from train_data.app import TrainDataManager, SeatNotInTrain, SeatAlreadyReserved
from ticket_office.app import reserve as make_reservation, Session


app = Flask("train_reservation")

booking_reference = BookingReference()
train_data_manager = TrainDataManager()

@app.get("/booking_reference")
def get_booking_reference():
    booking_reference.increment()
    return booking_reference.value()

@app.get("/data_for_train/<train_id>")
def data_for_train(train_id):
    train = train_data_manager.data_for_train(train_id)
    return jsonify(train)

@app.post("/reset/<train_id>")
def reset(train_id):
    train_data_manager.reset(train_id)
    return jsonify({"reset": train_id})

@app.post("/reserve")
def reserve():
    payload = request.json
    try:
        train = train_data_manager.reserve(payload)
        
    except SeatNotInTrain as e:
        return str(e), 404
    
    except SeatAlreadyReserved as e:
        return str(e), 409
    
    return jsonify(train)

@app.post("/reserve_seats")
def reserve_seats():
    payload = request.json
    seat_count = payload["count"]
    train_id = payload["train_id"]
    
    session = Session()

    train_data = session.get(
        f"http://localhost:8080/data_for_train/" + train_id
    ).json()
    booking_reference = session.get("http://localhost:8080/booking_reference").text
    
    reservation_payload = make_reservation(seat_count, booking_reference, train_data)
    
    response = session.post(
        "http://localhost:8080/reserve",
        json=reservation_payload
    )

    assert response.status_code == 200, response.text 
    return json.dumps(response.json())


if __name__ == "__main__":
    app.run(debug=True, port=8000)
