from flask import Flask, jsonify, request

from booking_reference import BookingReference
from train_data import TrainDataManager, ensure_train_exists, ensure_field_in_body, SeatNotInTrain, SeatAlreadyReserved


def create_app():
    app = Flask("train_reservation")
    
    booking_reference = BookingReference()
    train_data_manager = TrainDataManager()
    
    @app.get("/booking_reference")
    def get_booking_reference():
        booking_reference.increment()
        return booking_reference.value()
    
    @app.get("/data_for_train/<train_id>")
    @ensure_train_exists(train_data_manager)
    def data_for_train(train_id):
        train = train_data_manager.data_for_train(train_id)
        return jsonify(train)

    @app.post("/reset/<train_id>")
    @ensure_train_exists(train_data_manager)
    def reset(train_id):
        train_data_manager.reset(train_id)
        return jsonify({"reset": train_id})

    @app.post("/reserve")
    @ensure_field_in_body("train_id")
    @ensure_field_in_body("booking_reference")
    @ensure_field_in_body("seats")
    def reserve():
        payload = request.json
        try:
            train = train_data_manager.reserve(payload)
            
        except SeatNotInTrain as e:
            return str(e), 404
        
        except SeatAlreadyReserved as e:
            return str(e), 409
        
        return jsonify(train)

    return app




if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)
