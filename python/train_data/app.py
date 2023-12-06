import json
from flask import request

class SeatNotInTrain(Exception):
    pass

class SeatAlreadyReserved(Exception):
    pass

def get_trains():
    with open("trains.json", "r") as f:
        data = json.load(f)
        trains = {}
        for train_id, train_data in data.items():
            seats = {}
            raw_seat_data = train_data["seats"]
            for seat_id, seat_data in raw_seat_data.items():
                seats[seat_id] = Seat(seat_data["coach"], seat_data["seat_number"], seat_data["booking_reference"])
            trains[train_data] = Train(train_id, seats)
        return trains


class Train:
    def __init__(self, train_id, seats):
        self.train_id = train_id
        self.seats = seats

class Seat:
    def __init__(self, coach, seat_number, booking_reference):
        self.coach = coach
        self.seat_number = seat_number
        self.booking_reference = booking_reference


class TrainDataManager:
    def __init__(self):
        self.trains = get_trains()
    
    def data_for_train(self, train_id):
        return self.trains.get(train_id)
    
    def reset(self, train_id):
        train = self.trains.get(train_id)

        for seat_id, seat in train.seats.items():
            seat.booking_reference = ""
    
    def reserve(self, payload):
        train_id = payload.get("train_id")
        train = self.trains.get(train_id)

        seats = payload.get("seats")

        booking_reference = payload.get("booking_reference")

        for seat in seats:
            if not seat in train.seats:
                raise SeatNotInTrain(f"No seat found with number {seat}")
                
            existing_reservation = train.seats[seat].booking_reference
            if existing_reservation and existing_reservation != booking_reference:
                raise SeatAlreadyReserved(
                    f"Cannot book seat {seat} with {booking_reference} - "
                    + f"already booked with {existing_reservation}"
                )
                

        for seat in seats:
            train.seats[seat].booking_reference = booking_reference

        return train

    
