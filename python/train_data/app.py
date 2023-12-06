import json
from flask import request

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

    
