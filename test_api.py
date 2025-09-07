#!/usr/bin/env python3
"""
Test script for Campus Event Reporting System API
This script demonstrates the API functionality with sample requests.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Testing Campus Event Reporting System API")
    print("=" * 50)
    
    # Test 1: Create a college
    print("\n1. Creating a test college...")
    college_data = {
        "name": "Test University",
        "location": "Test City"
    }
    response = requests.post(f"{BASE_URL}/colleges/", json=college_data)
    if response.status_code == 200:
        college = response.json()
        print(f"✅ College created: {college['name']} (ID: {college['id']})")
        college_id = college['id']
    else:
        print(f"❌ Failed to create college: {response.text}")
        return
    
    # Test 2: Create a student
    print("\n2. Creating a test student...")
    student_data = {
        "name": "John Doe",
        "email": "john.doe@testuniversity.edu",
        "college_id": college_id
    }
    response = requests.post(f"{BASE_URL}/students/", json=student_data)
    if response.status_code == 200:
        student = response.json()
        print(f"✅ Student created: {student['name']} (ID: {student['id']})")
        student_id = student['id']
    else:
        print(f"❌ Failed to create student: {response.text}")
        return
    
    # Test 3: Create an event
    print("\n3. Creating a test event...")
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    event_data = {
        "title": "Tech Conference 2024",
        "description": "Annual technology conference",
        "college_id": college_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "location": "Main Auditorium",
        "max_capacity": 50
    }
    response = requests.post(f"{BASE_URL}/events/", json=event_data)
    if response.status_code == 200:
        event = response.json()
        print(f"✅ Event created: {event['title']} (ID: {event['id']})")
        event_id = event['id']
    else:
        print(f"❌ Failed to create event: {response.text}")
        return
    
    # Test 4: Register for event
    print("\n4. Registering student for event...")
    registration_data = {
        "student_id": student_id,
        "event_id": event_id
    }
    response = requests.post(f"{BASE_URL}/registrations/", json=registration_data)
    if response.status_code == 200:
        print("✅ Student registered for event")
    else:
        print(f"❌ Failed to register: {response.text}")
        return
    
    # Test 5: Check in for attendance (simulate event time)
    print("\n5. Checking in for attendance...")
    attendance_data = {
        "student_id": student_id,
        "event_id": event_id
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=attendance_data)
    if response.status_code == 200:
        print("✅ Student checked in for attendance")
    else:
        print(f"❌ Failed to check in: {response.text}")
        print("Note: This might fail if event hasn't started yet")
    
    # Test 6: Submit feedback
    print("\n6. Submitting feedback...")
    feedback_data = {
        "student_id": student_id,
        "event_id": event_id,
        "rating": 4,
        "comment": "Great event! Learned a lot."
    }
    response = requests.post(f"{BASE_URL}/feedback/", json=feedback_data)
    if response.status_code == 200:
        print("✅ Feedback submitted successfully")
    else:
        print(f"❌ Failed to submit feedback: {response.text}")
    
    # Test 7: Get event report
    print("\n7. Getting event report...")
    response = requests.get(f"{BASE_URL}/reports/events/{event_id}")
    if response.status_code == 200:
        report = response.json()
        print(f"✅ Event Report:")
        print(f"   - Event: {report['event_title']}")
        print(f"   - Registrations: {report['total_registrations']}")
        print(f"   - Attendance: {report['total_attendance']}")
        print(f"   - Attendance %: {report['attendance_percentage']}%")
        print(f"   - Avg Feedback: {report['average_feedback']}")
        print(f"   - Feedback Count: {report['total_feedback_count']}")
    else:
        print(f"❌ Failed to get event report: {response.text}")
    
    # Test 8: Get student report
    print("\n8. Getting student report...")
    response = requests.get(f"{BASE_URL}/reports/students/{student_id}")
    if response.status_code == 200:
        report = response.json()
        print(f"✅ Student Report:")
        print(f"   - Student: {report['student_name']}")
        print(f"   - College: {report['college_name']}")
        print(f"   - Events Attended: {report['total_events_attended']}")
        print(f"   - Avg Feedback Given: {report['average_feedback_given']}")
    else:
        print(f"❌ Failed to get student report: {response.text}")
    
    # Test 9: Test edge cases
    print("\n9. Testing edge cases...")
    
    # Try duplicate registration
    print("   Testing duplicate registration...")
    response = requests.post(f"{BASE_URL}/registrations/", json=registration_data)
    if response.status_code == 400:
        print("   ✅ Duplicate registration properly rejected")
    else:
        print(f"   ❌ Duplicate registration not handled: {response.text}")
    
    # Try registering for cancelled event
    print("   Testing cancelled event registration...")
    requests.put(f"{BASE_URL}/events/{event_id}/cancel")
    response = requests.post(f"{BASE_URL}/registrations/", json={
        "student_id": student_id + 1,  # Different student
        "event_id": event_id
    })
    if response.status_code == 400:
        print("   ✅ Registration for cancelled event properly rejected")
    else:
        print(f"   ❌ Cancelled event registration not handled: {response.text}")
    
    print("\n🎉 API testing completed!")
    print("\nTo test the full system:")
    print("1. Run 'python sample_data.py' to populate with sample data")
    print("2. Visit http://localhost:8000/docs for interactive API documentation")
    print("3. Use Postman or similar tools to test all endpoints")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
