# 🏢 Flask Facility Booking API
A simple and secure RESTful API built with Flask for managing facilities and user bookings. This app supports user registration/login, facility creation, and session-protected booking features.

Ideal for systems that manage:
- Gym or studio reservations
- Meeting room bookings
- Event or venue scheduling

## ✅ Features
- User Authentication
-Register new users
-Login with session support using Flask-Login

## 🏢 Facility Management
- Add new facilities
- View all or individual facilities
- Edit or delete facility data

## 📅 Booking System
- Create bookings with start/end times
- View all bookings or a specific booking
- Login required to book

🔒 Protected Routes
- Only authenticated users can create bookings

🗃️ Database
- Data persisted via SQLite and SQLAlchemy ORM

## 🧰 Tech Stack
| Component     | Tool/Technology  |
| ------------- | ---------------- |
| Language      | Python           |
| Web Framework | Flask            |
| Auth Handling | Flask-Login      |
| ORM           | SQLAlchemy       |
| Database      | SQLite (default) |


## 🔧 API Endpoints
| Method | Route                       | Description            |
| ------ | --------------------------- | ---------------------- |
| GET    | `/api/facility`             | View all facilities    |
| GET    | `/api/facility_single/<id>` | View one facility      |
| POST   | `/api/update_facility`      | Add or update facility |


## 📝 Booking Management
| Method | Route                      | Description                                |
| ------ | -------------------------- | ------------------------------------------ |
| GET    | `/api/booking`             | View all bookings                          |
| GET    | `/api/booking_single/<id>` | View one booking                           |
| POST   | `/api/update_booking`      | Create a new booking 🛑 *(requires login)* |


- Note: /api/update_booking requires the user to be logged in.

## 👥 User Authentication
| Method | Route           | Description              |
| ------ | --------------- | ------------------------ |
| POST   | `/api/register` | Register new user        |
| POST   | `/api/login`    | Log in and start session |


## 🧪 Sample Test Flow
- Register a user: POST /api/register
- Log in as the user: POST /api/login
- Add a facility: POST /api/update_facility
- View all facilities: GET /api/facility
- Book a facility :POST /api/update_booking
- View bookings: GET /api/booking

## 🛡️ To-Do & Improvements
- Add admin interface for managing facilities and bookings
- Implement booking conflict validation
- Add logout route
- Switch to JWT or OAuth2 for token-based auth
- Add date filtering and availability checking
