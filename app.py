from flask import Flask, jsonify, request
from Facility.models import User, Facility, Booking, db
from flask_login import LoginManager, login_user, logout_user, current_user
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'iyke'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facility.db'


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))



@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'message': 'Please fill in all to register'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'You have successfully registered. Now login!'}), 200


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Invalid Login.. Try again!'}), 400

    user = User.query.filter_by(username=username, password=password).first()
    if user and user.password == password:
        login_user(user)
        return jsonify({'message': 'You have logged in!!'}), 200
    return jsonify({'message': 'Please Login again'}), 400


@app.route('/api/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify({'message': 'You have been logged out!!'}), 200


@app.route('/api/facility', methods=['GET'])
def facility():
    facility_all = Facility.query.all()
    facilities_list = [
        {"id": f.id, "name": f.name, "description": f.description, "price": f.price}
        for f in facility_all
    ]
    return jsonify({'facilities': facilities_list}), 200


@app.route('/api/facility_single/<int:facility_id>', methods=['GET'])
def facility_single(facility_id):
    facility_one = Facility.query.get(facility_id)
    return jsonify({'facility_one': facility_one.to_dict()}), 200


@app.route('/api/update_facility', methods=['POST'])
def update_facility():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not name or not description or not price:
        return jsonify({'message': 'Please fill in all'}), 400

    new_facility = Facility(name=name, description=description, price=price)
    db.session.add(new_facility)
    db.session.commit()
    return jsonify({'message': 'You have successfully updated the Facility'}), 200


@app.route('/api/edit_facility/<int:facility_id>', methods=['PUT'])
def edit_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    data = request.get_json()
    facility.name = data.get('name', facility.name)
    facility.description = data.get('description', facility.description)
    facility.price = data.get('price', facility.price)
    db.session.commit()
    return jsonify({'message': 'Your facility has been edited. Thank you!'}), 200


@app.route('/api/delete/<int:facility_id>', methods=['DELETE'])
def delete_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    db.session.delete(facility)
    db.session.commit()
    return jsonify({'message': 'This Facility has been removed'}), 200


@app.route('/api/booking', methods=['GET'])
def booking():
    book_all = Booking.query.all()
    book_list = [
        {
            "id": b.id,
            "user_id": b.user_id,
            'facility_id': b.facility_id,
            'start_time': b.start_time,
            'end_time': b.end_time
        }
        for b in book_all
    ]
    return jsonify({'book_list': book_list}), 200


@app.route('/api/booking_single/<int:booking_id>', methods=['GET'])
def booking_single(booking_id):
    booking_one = Booking.query.get(booking_id)
    return jsonify({'booking_one': booking_one}), 200


@app.route('/api/update_booking', methods=['POST'])
def update_booking():
    data = request.get_json()
    facility_id = data.get('facility_id')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid date format. Use ISO 8601 like 2025-04-18T10:00:00'}), 400

    if not current_user.is_authenticated:
        return jsonify({'error': 'You must be logged in to make a booking'}), 401

    new_booking = Booking(user_id=current_user.id, facility_id=facility_id,
                          start_time=start_time, end_time=end_time)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Your Booking has been updated'}), 200


@app.route('/api/edit_booking/<int:booking_id>', methods=['PUT'])
def edit_booking(booking_id):
    try:
        book = Booking.query.get_or_404(booking_id)
        data = request.get_json()
        book.user_id = data.get('user_id', book.user_id)
        book.facility_id = data.get('facility_id', book.facility_id)
        book.start_time = datetime.fromisoformat(data['start_time'])
        book.end_time = datetime.fromisoformat(data['end_time'])
        db.session.commit()
        return jsonify({'message': 'Successfully edited'}), 200
    except Exception as e:
        return jsonify({'message': "Please fill in all", 'error': str(e)}), 500


@app.route('/api/delete_booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'This booking has been deleted'}), 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
