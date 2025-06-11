Flask Facility Booking API
This is a Flask-based RESTful API that allows users to register, log in, view facilities, book them, and manage both facilities and bookings. It uses Flask-Login for session handling and SQLite as the database via SQLAlchemy.

Features
- User Registration & Login (Session-based)
- Facility Management (Add, View, Edit, Delete)
- Booking System with Start/End Times
- Route Protection (Booking requires login)
- SQLite Database

Tech Stack
- Python 
- Flask
- Flask-Login
- SQLAlchemy
- SQLite (default database)

Facility Management
- View All Facilities
- GET /api/facility

- View Single Facility
- GET /api/facility_single/<facility_id>

- Add a New Facility
- POST /api/update_facility

Booking Management
- View All Bookings
- GET /api/booking

- View Single Booking
- GET /api/booking_single/<booking_id>

- Create a Booking (Login Required)
- POST /api/update_booking

Sample Test Sequence
- Register user → /api/register
- Login → /api/login
- Add facility → /api/update_facility
- View facilities → /api/facility
- Book facility → /api/update_booking
- View bookings → /api/booking

