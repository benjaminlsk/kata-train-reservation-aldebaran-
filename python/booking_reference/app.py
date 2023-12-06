from flask import Flask


class BookingReference:
    def __init__(self):
        self._count = 123456789

    def increment(self):
        self._count += 1

    def value(self):
        return str(hex(self._count))[2:]

    def get_booking_reference(self):
        self.increment()
        return self.value()


