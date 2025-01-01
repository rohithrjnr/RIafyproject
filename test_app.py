import unittest
from flask import Flask, jsonify
from app import app, db, Appointment  

class FlaskAppTest(unittest.TestCase):


    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()


        with app.app_context():
            db.create_all()


    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


    def test_get_available_slots(self):

        response = self.client.get('/api/slots?date=2025-01-01')
        self.assertEqual(response.status_code, 200)
        available_slots = response.json
        self.assertIn("10:00", available_slots)
        self.assertIn("16:30", available_slots)


    def test_get_appointments(self):

        appointment = Appointment(name="John Doe", phonenumber="1234567890", date="2025-01-01", timeslot="10:00")
        db.session.add(appointment)
        db.session.commit()

        response = self.client.get('/api/appointments')
        self.assertEqual(response.status_code, 200)
        appointments = response.json
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0]['name'], "John Doe")
        self.assertEqual(appointments[0]['timeslot'], "10:00")


    def test_book_appointment(self):
        appointment_data = {
            "name": "Jane Doe",
            "phonenumber": "9876543210",
            "date": "2025-01-01",
            "timeslot": "11:00"
        }

        response = self.client.post('/api/book', json=appointment_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['success'], "Appointment booked successfully")


        appointment = Appointment.query.filter_by(name="Jane Doe").first()
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.name, "Jane Doe")
        self.assertEqual(appointment.timeslot, "11:00")


    def test_book_appointment_slot_already_booked(self):
        # First, book a slot
        appointment_data = {
            "name": "John Smith",
            "phonenumber": "1112233445",
            "date": "2025-01-01",
            "timeslot": "12:00"
        }
        self.client.post('/api/book', json=appointment_data)


        duplicate_appointment_data = {
            "name": "Alice",
            "phonenumber": "9876543210",
            "date": "2025-01-01",
            "timeslot": "12:00"
        }

        response = self.client.post('/api/book', json=duplicate_appointment_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Time slot already booked')


    def test_get_available_slots_no_slots(self):

        slots = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]
        for slot in slots:
            appointment = Appointment(name="Test", phonenumber="1234567890", date="2025-01-01", timeslot=slot)
            db.session.add(appointment)
        db.session.commit()

        response = self.client.get('/api/slots?date=2025-01-01')
        self.assertEqual(response.status_code, 200)
        available_slots = response.json
        self.assertEqual(available_slots, [])

if __name__ == '__main__':
    unittest.main()
