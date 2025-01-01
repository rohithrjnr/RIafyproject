from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from models import db, Appointment


app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)


@app.route('/api/slots', methods=['GET'])
def available_slots():
    date = request.args.get('date')
    booked_slots = [a.timeslot for a in Appointment.query.filter_by(date=date).all()]
    slots = gettimeslots()
    available_slots = [slot for slot in slots if slot not in booked_slots]
    return jsonify(available_slots)

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    try:
        appointments = Appointment.query.all()
        appointment_list = []
        for appointment in appointments:
            appointment_list.append({
                'name': appointment.name,
                'phonenumber': appointment.phonenumber,
                'date': appointment.date,
                'timeslot': appointment.timeslot
            })
        return jsonify(appointment_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/book', methods=['OPTIONS', 'POST'])
def book_appointment():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return response, 200

    data = request.json
    date = data.get('date')
    timeslot = data.get('timeslot')

    if Appointment.query.filter_by(date=date, timeslot=timeslot).first():
        return jsonify({'error': 'Time slot already booked'}), 400

    new_appointment = Appointment(
        name=data.get('name'),
        phonenumber=data.get('phonenumber'),
        date=date,
        timeslot=timeslot
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'success': 'Appointment booked successfully'}), 201

# Helper function
def gettimeslots():
    timeslots = []
    for hour in range(10, 17):
        for minute in [0, 30]:
            slot = f"{hour:02}:{minute:02}"
            if slot not in ["13:00", "13:30"]:
                timeslots.append(slot)
    return timeslots

if __name__ == '__main__':
    app.run(debug=True)
