#!/usr/bin/env python3
"""
Refresh Sample Data Script
This script clears existing data and creates fresh sample data for testing
"""

from main import (
    College, Student, Event, Registration, Attendance, Feedback,
    SessionLocal, engine, Base
)
from datetime import datetime, timedelta
import random

def clear_existing_data():
    """Clear all existing data from the database"""
    db = SessionLocal()
    try:
        # Delete in reverse order of dependencies
        db.query(Feedback).delete()
        db.query(Attendance).delete()
        db.query(Registration).delete()
        db.query(Event).delete()
        db.query(Student).delete()
        db.query(College).delete()
        db.commit()
        print("✅ Cleared existing data")
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_data():
    """Create fresh sample data"""
    db = SessionLocal()
    
    try:
        # Create sample colleges
        colleges_data = [
            {"name": "University of Technology", "location": "Tech City"},
            {"name": "Business School of Excellence", "location": "Business District"},
            {"name": "Arts and Sciences College", "location": "Cultural Quarter"},
            {"name": "Engineering Institute", "location": "Innovation Hub"},
            {"name": "Medical University", "location": "Health Center"}
        ]
        
        colleges = []
        for college_data in colleges_data:
            college = College(**college_data)
            db.add(college)
            colleges.append(college)
        
        db.commit()
        print(f"✅ Created {len(colleges)} colleges")
        
        # Create sample students (50 per college)
        students = []
        for college in colleges:
            for i in range(50):
                student_data = {
                    "name": f"Student {i+1} from {college.name}",
                    "email": f"student{i+1}@{college.name.lower().replace(' ', '')}.edu",
                    "college_id": college.id
                }
                student = Student(**student_data)
                db.add(student)
                students.append(student)
        
        db.commit()
        print(f"✅ Created {len(students)} students")
        
        # Create sample events (20 per college)
        events = []
        for college in colleges:
            for i in range(20):
                # Create events spread over the next 3 months
                start_time = datetime.utcnow() + timedelta(days=random.randint(1, 90))
                end_time = start_time + timedelta(hours=random.randint(1, 4))
                
                event_data = {
                    "title": f"{college.name} Event {i+1}",
                    "description": f"Description for {college.name} Event {i+1}",
                    "college_id": college.id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "location": f"{college.location} - Room {i+1}",
                    "max_capacity": random.randint(20, 100)
                }
                event = Event(**event_data)
                db.add(event)
                events.append(event)
        
        db.commit()
        print(f"✅ Created {len(events)} events")
        
        # Create sample registrations (random students register for random events)
        registrations = []
        for event in events:
            # Randomly select students to register (60-80% of students per college)
            college_students = [s for s in students if s.college_id == event.college_id]
            num_registrations = random.randint(
                int(len(college_students) * 0.6),
                min(int(len(college_students) * 0.8), event.max_capacity)
            )
            
            selected_students = random.sample(college_students, num_registrations)
            
            for student in selected_students:
                registration = Registration(
                    student_id=student.id,
                    event_id=event.id,
                    registered_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.add(registration)
                registrations.append(registration)
        
        db.commit()
        print(f"✅ Created {len(registrations)} registrations")
        
        # Create sample attendance (for past events or events happening now)
        attendance_records = []
        for event in events:
            # Only create attendance for events that have started or are happening now
            if event.start_time <= datetime.utcnow():
                event_registrations = [r for r in registrations if r.event_id == event.id]
                
                # 70-90% of registered students actually attend
                attendance_rate = random.uniform(0.7, 0.9)
                num_attending = int(len(event_registrations) * attendance_rate)
                
                attending_students = random.sample(event_registrations, num_attending)
                
                for registration in attending_students:
                    # Check-in time within event duration or ±30 min
                    check_in_time = event.start_time + timedelta(
                        minutes=random.randint(-30, int((event.end_time - event.start_time).total_seconds() / 60))
                    )
                    
                    attendance = Attendance(
                        student_id=registration.student_id,
                        event_id=event.id,
                        checked_in_at=check_in_time
                    )
                    db.add(attendance)
                    attendance_records.append(attendance)
        
        db.commit()
        print(f"✅ Created {len(attendance_records)} attendance records")
        
        # Create sample feedback (for attended events)
        feedback_records = []
        for attendance in attendance_records:
            # 60-80% of attendees give feedback
            if random.random() < random.uniform(0.6, 0.8):
                feedback = Feedback(
                    student_id=attendance.student_id,
                    event_id=attendance.event_id,
                    rating=random.randint(1, 5),
                    comment=f"Sample feedback from student {attendance.student_id} for event {attendance.event_id}",
                    submitted_at=attendance.checked_in_at + timedelta(hours=random.randint(1, 24))
                )
                db.add(feedback)
                feedback_records.append(feedback)
        
        db.commit()
        print(f"✅ Created {len(feedback_records)} feedback records")
        
        print("\n🎉 Sample data created successfully!")
        print(f"📊 Summary:")
        print(f"   - {len(colleges)} colleges")
        print(f"   - {len(students)} students")
        print(f"   - {len(events)} events")
        print(f"   - {len(registrations)} registrations")
        print(f"   - {len(attendance_records)} attendance records")
        print(f"   - {len(feedback_records)} feedback records")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("🔄 Refreshing Campus Event Reporting System Sample Data")
    print("=" * 60)
    
    # Clear existing data
    clear_existing_data()
    
    # Create fresh sample data
    create_sample_data()
    
    print("\n✅ Database refreshed with new sample data!")
    print("🚀 You can now run queries and get real results!")

if __name__ == "__main__":
    main()
