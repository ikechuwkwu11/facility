from flask import Flask,jsonify,request
from Facility.models import User,Facility,Booking,db
from flask_login import LoginManager,login_user,logout_user
from datetime import datetime
from flask_login import current_user

app= Flask(__name__)
app.config['SECRET_KEY'] = 'iyke'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facility.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

# This is the first stage where a user has to register before getting access into the website
@app.route('/api/register',methods =['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'message':'Please fill in all to register'}),400

    new_user = User(username=username,email=email,password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'You have successfully registered. Now login!'}),200


# After you are done registering, now you will have to Log in into the website, if you put in a wrong details. it will flag and error and ask you to try again
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message':'Invalid Login.. Try again!'}),400

    user = User.query.filter_by(username=username,password=password).first()
    if user.password == password:
        login_user(user)
        return jsonify({'message':'You have logged in!!'}),200
    return jsonify({'message':'please Login again'}),400


# When you want to log out from the website
@app.route('/api/logout',methods=['GET'])
def logout():
    logout_user()
    return jsonify({'message':'You have been logged out!!'}),200


# Now you are inside the website, and you want to see all the facilities in the website
@app.route('/api/facility',methods=['GET'])
def facility():
    facility_all = Facility.query.all()
    facilities_List = [
        {
            "id": f.id,
            "name": f.name,
            "description" : f.description,
            "price" : f.price
        }
        for f in facility_all
    ]
    return jsonify({'facilities': facilities_List}),200


# This is when you want to get a particular facility from the website
@app.route('/api/facility_single/<int:facility_id>',methods=['GET'])
def facility_single(facility_id):
    facility_one = Facility.query.get(facility_id)
    return jsonify({'facility_one':facility_one.to_dict()}),200

# Now you want to update your facility and add in new facilities in the website
@app.route('/api/update_facility',methods = ['POST'])
def update_facility():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not name or not description or not price:
        return jsonify({'message':'Please fill in all'}),400

    new_user= Facility(name=name,description=description,price=price)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'You have successfully updated the Facility'}),200


# You made a mistake when you were adding things to the facility, and you want to edit it and put in the correct details
@app.route('/api/edit_facility/<int:facility_id>',methods =['PUT'])
def edit_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    data = request.get_json()
    facility.name = data.get('name',facility.name)
    facility.description = data.get('description', facility.description)
    facility.price = data.get('price',facility.price)
    db.session.commit()
    return jsonify({'message':'Your facility has been edited. Thank you!'}),200


# When you no longer want to be using a facility again then here is where you will delete it
@app.route('/api/delete/<int:facility_id>',methods=['DELETE'])
def delete(facility_id):
    user = Facility.query.get_or_404(facility_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'This Facility has been removed'}),200


# This is the booking area where you can book facilities that yiu want to use which has a start_time and an end_time
@app.route('/api/booking',methods=['GET'])
def booking():
    book_all = Booking.query.all()
    book_list = [
        {
            "id": b.id,
            "user_id": b.user_id,
            'facility_id' : b.facility_id,
            'start_time' :b.start_time,
            'end_time':b.end_time
        }
        for b in book_all
    ]
    return jsonify({'book_list':book_list}),200



# This is when you want to single out a particular booking which you made for you to see
@app.route('/api/booking_single/<int:booking_id>',methods=['GET'])
def booking_single(booking_id):
    booking_one = Booking.query.get(booking_id)
    return jsonify({'booking_one':booking_one})

# This is when you update you booking or add more bookings to the already existing one
@app.route('/api/update_booking',methods=['POST'])
def update_booking():
    data = request.get_json()
    # user_id = data.get('user')
    facility_id = data.get('facility_id')
    start_time_str =data.get('start_time')
    end_time_str = data.get('end_time')


    try:
        # Convert to Python datetime objects
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except (ValueError,TypeError) as e:
        print("Error parsing date:", str(e))
        return jsonify({'error': 'Invalid date format. Use ISO 8601 like 2025-04-18T10:00:00'}), 400

    if not current_user.is_authenticated:
        return jsonify({'error': 'You must be logged in to make a booking'}), 401



    new_user = Booking(user_id = current_user.id,facility_id=facility_id,start_time=start_time,end_time=end_time)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'Your Booking has been updated'}),200


# When you make a mistake when you were booking a facility, and you want to edit it and put in the correct details
@app.route('/api/edit_booking/<int:booking_id>',methods = ['PUT'])
def edit_booking(booking_id):
    try:
        book = Booking.query.get_or_404(booking_id)
        data = request.get_json()
        book.user_id = data.get('user_id',book.user_id)
        book.facility_id = data.get('facility_id',book.facility_id)
        book.start_time = datetime.fromisoformat(data['start_time'])
        book.end_time = datetime.fromisoformat(data['end_time'])
        db.session.commit()
        return jsonify({'message':'successfully edited'}),200
    except Exception as e:
        return jsonify({'message':"please fill in all"},str(e)),500





# When the facilities are all booked up, or you found a better facility and want to do a change then you delete the booking
@app.route('/api/delete_booking/<int:booking_id>',methods=['DELETE'])
def delete_booking(booking_id):
    user = Booking.query.get_or_404(booking_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'This user has been deleted'}),200



if __name__=='__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)