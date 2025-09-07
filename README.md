# Campus Event Reporting System

A comprehensive FastAPI-based system for managing campus events, student registrations, attendance tracking, and feedback collection.

## Overview

This system is designed to handle campus event management with two main user types:
- **Admins** (college event coordinators): Create events and view reports
- **Students**: Register for events, check in for attendance, and provide feedback

## Key Features

- Event creation and management (Admin only)
- Student registration for events
- Attendance tracking with check-in functionality
- Feedback collection (1-5 rating scale)
- Comprehensive reporting system
- College-based organization
- Edge case handling (duplicates, cancellations, late check-ins)

## Architecture

### Technology Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite (easily portable to PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic models

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Admin Users   │    │  Student Users  │    │   API Client    │
│ (Event Creators)│    │ (Mobile App)    │    │   (Postman)     │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     FastAPI Server        │
                    │   (REST API Endpoints)   │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │    SQLAlchemy ORM        │
                    │   (Data Validation)      │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     SQLite Database      │
                    │  (Colleges, Students,    │
                    │   Events, Attendance)    │
                    └───────────────────────────┘
```

### Database Schema

The system uses the following entities:
- **Colleges**: Educational institutions
- **Students**: Belong to exactly one college
- **Events**: Created by colleges with time, location, and capacity constraints
- **Registrations**: Student sign-ups for events
- **Attendance**: Check-in records during event time
- **Feedback**: Post-attendance ratings and comments

### Entity Relationships
```
College (1) ──── (N) Student
College (1) ──── (N) Event
Student (1) ──── (N) Registration
Event (1) ──── (N) Registration
Student (1) ──── (N) Attendance
Event (1) ──── (N) Attendance
Student (1) ──── (N) Feedback
Event (1) ──── (N) Feedback
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

4. **Populate with sample data** (optional):
   ```bash
   python sample_data.py
   ```

5. **View API documentation**:
   - Interactive docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### College Management
- `POST /colleges/` - Create a new college
- `GET /colleges/` - List all colleges

### Student Management
- `POST /students/` - Create a new student
- `GET /students/` - List all students
- `GET /students/{student_id}` - Get student details

### Event Management (Admin)
- `POST /events/` - Create a new event
- `GET /events/` - List all events
- `GET /events/{event_id}` - Get event details
- `PUT /events/{event_id}/cancel` - Cancel an event

### Student Actions
- `POST /registrations/` - Register for an event
- `GET /registrations/student/{student_id}` - Get student's registrations
- `POST /attendance/` - Check in for attendance
- `POST /feedback/` - Submit event feedback

### Reporting
- `GET /reports/events/{event_id}` - Get event analytics
- `GET /reports/students/{student_id}` - Get student statistics
- `GET /reports/colleges/{college_id}/events` - Get college event reports

## Business Rules

### Registration Rules
- Registration closes when the event starts
- No duplicate registrations allowed
- Capacity limits enforced
- Cannot register for cancelled events

### Attendance Rules
- Must be registered to check in
- Check-in allowed within ±30 minutes of event time
- One attendance record per student per event
- Cannot check in for cancelled events

### Feedback Rules
- Only allowed after attendance is marked
- Rating scale: 1-5 (required)
- Comments are optional
- One feedback per student per event

## Sample Data

The `sample_data.py` script creates:
- 5 colleges
- 250 students (50 per college)
- 100 events (20 per college)
- Random registrations, attendance, and feedback

## Testing with Postman/API Client

### Example API Calls

1. **Create a College**:
   ```json
   POST /colleges/
   {
     "name": "Test University",
     "location": "Test City"
   }
   ```

2. **Create a Student**:
   ```json
   POST /students/
   {
     "name": "John Doe",
     "email": "john.doe@testuniversity.edu",
     "college_id": 1
   }
   ```

3. **Create an Event**:
   ```json
   POST /events/
   {
     "title": "Tech Conference 2024",
     "description": "Annual technology conference",
     "college_id": 1,
     "start_time": "2024-02-15T10:00:00",
     "end_time": "2024-02-15T16:00:00",
     "location": "Main Auditorium",
     "max_capacity": 100
   }
   ```

4. **Register for Event**:
   ```json
   POST /registrations/
   {
     "student_id": 1,
     "event_id": 1
   }
   ```

5. **Check In for Attendance**:
   ```json
   POST /attendance/
   {
     "student_id": 1,
     "event_id": 1
   }
   ```

6. **Submit Feedback**:
   ```json
   POST /feedback/
   {
     "student_id": 1,
     "event_id": 1,
     "rating": 4,
     "comment": "Great event!"
   }
   ```

## Edge Cases Handled

1. **Duplicate Registrations**: Prevented with unique constraints
2. **Event Cancellation**: Disables new registrations and attendance
3. **Late Check-ins**: Rejected if outside ±30 minute window
4. **Capacity Limits**: Enforced during registration
5. **Missing Dependencies**: Proper error handling for non-existent students/events
6. **Empty Reports**: Graceful handling of events with no participation

## Performance Considerations

- Designed for ~50 colleges × ~500 students × ~20 events/semester
- SQLite suitable for prototype; easily migrates to PostgreSQL/MySQL
- Indexed foreign keys for efficient queries
- Optimized reporting queries

## Future Enhancements

- Authentication and authorization system
- Real-time notifications
- Mobile app integration
- Advanced analytics and dashboards
- Email/SMS notifications
- Event categories and tags
- Waitlist functionality

## Database Migration

To migrate from SQLite to PostgreSQL/MySQL:

1. Update `SQLALCHEMY_DATABASE_URL` in `main.py`
2. Install appropriate database driver
3. Update connection parameters
4. Schema remains compatible

## Troubleshooting

### Common Issues

1. **Port already in use**: Change port in `uvicorn.run()` call
2. **Database locked**: Ensure no other processes are using the database
3. **Import errors**: Verify all dependencies are installed
4. **Date/time issues**: Ensure system clock is accurate for attendance validation

### Logs

The application logs errors and important events. Check console output for debugging information.

## License

This project is for educational and prototyping purposes.
