# Quick Start Guide - Campus Event Reporting System

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the System
```bash
python start.py
```
This will:
- Check dependencies
- Ask if you want sample data
- Start the server at http://localhost:8000

### 3. Test the API
Visit http://localhost:8000/docs for interactive API documentation

## 📱 Simulating Mobile App Usage

Since this is a prototype, you'll simulate student mobile app actions using API calls:

### Student Workflow
1. **Register for Event**: `POST /registrations/`
2. **Check In**: `POST /attendance/` (during event time ±30 min)
3. **Give Feedback**: `POST /feedback/` (after attendance)

### Admin Workflow
1. **Create Event**: `POST /events/`
2. **View Reports**: `GET /reports/events/{event_id}`

## 🧪 Testing Examples

### Using Python requests:
```python
import requests

# Register for event
requests.post("http://localhost:8000/registrations/", json={
    "student_id": 1,
    "event_id": 1
})

# Check in for attendance
requests.post("http://localhost:8000/attendance/", json={
    "student_id": 1,
    "event_id": 1
})
```

### Using curl:
```bash
# Register for event
curl -X POST "http://localhost:8000/registrations/" \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "event_id": 1}'

# Check in for attendance
curl -X POST "http://localhost:8000/attendance/" \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "event_id": 1}'
```

## 📊 Sample Data

The system comes with sample data:
- 5 colleges
- 250 students (50 per college)
- 100 events (20 per college)
- Random registrations, attendance, and feedback

## 🔍 Key Features Demonstrated

### Business Rules
- ✅ No duplicate registrations
- ✅ Registration closes when event starts
- ✅ Attendance only during event time (±30 min)
- ✅ Feedback only after attendance
- ✅ Capacity limits enforced
- ✅ Cancelled events handled properly

### Reporting
- Event popularity (registration count)
- Attendance percentage
- Average feedback ratings
- Student participation statistics

## 🛠️ Development Notes

### Database
- SQLite for easy setup
- Easily portable to PostgreSQL/MySQL
- All relationships properly defined

### API Design
- RESTful endpoints
- Proper HTTP status codes
- Comprehensive error handling
- Input validation with Pydantic

### Scalability
- Designed for ~50 colleges × ~500 students × ~20 events
- Efficient queries with proper indexing
- Async FastAPI for performance

## 🎯 Next Steps

1. **Test all endpoints** using the interactive docs
2. **Try edge cases** (duplicates, late check-ins, etc.)
3. **Generate reports** for different events and students
4. **Modify sample data** to test different scenarios

## 📞 Support

- Check the main README.md for detailed documentation
- Use the interactive API docs at /docs
- Run test_api.py for automated testing
