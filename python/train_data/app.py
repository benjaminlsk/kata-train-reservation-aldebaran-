import json
from flask import Flask, jsonify, request

class SeatNotInTrain(Exception):
    pass

class SeatAlreadyReserved(Exception):
    pass

class TrainDataManager:
    def __init__(self):
        with open("trains.json", "r") as f:
            self.trains = json.load(f)
    
    def data_for_train(self, train_id):
        return self.trains.get(train_id)
    
    def reset(self, train_id):
        train = self.trains.get(train_id)

        for seat_id, seat in train["seats"].items():
            seat["booking_reference"] = ""
    
    def reserve(self, payload):
        train_id = payload.get("train_id")
        train = self.trains.get(train_id)

        seats = payload.get("seats")

        booking_reference = payload.get("booking_reference")

        for seat in seats:
            if not seat in train["seats"]:
                raise SeatNotInTrain(f"No seat found with number {seat}")
                
            existing_reservation = train["seats"][seat]["booking_reference"]
            if existing_reservation and existing_reservation != booking_reference:
                raise SeatAlreadyReserved(
                    f"Cannot book seat {seat} with {booking_reference} - "
                    + f"already booked with {existing_reservation}"
                )

        for seat in seats:
            train["seats"][seat]["booking_reference"] = booking_reference

        return train
    
# decorator for ensuring that a train exists
def ensure_train_exists(train_data_manager):
    def decorator(f):
        def wrapper(*args, **kwargs):
            train_id = kwargs.get("train_id")
            if not train_id:
                return "Missing 'train_id' in path", 400
            if not train_data_manager.data_for_train(train_id):
                return f"No train with id '{train_id}'", 404
            return f(*args, **kwargs)
        return wrapper
    return decorator

def ensure_field_in_body(fieldname):
    def decorator(f):
        def wrapper(*args, **kwargs):
            payload = request.json
            if not payload:
                return "Missing body", 400
            if not fieldname in payload:
                return f"Missing '{fieldname}' in body", 400
            return f(*args, **kwargs)
        return wrapper
    
