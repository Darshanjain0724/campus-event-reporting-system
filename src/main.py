from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import os
import time

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./campus_events.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class College(Base):
    __tablename__ = "colleges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    students = relationship("Student", back_populates="college")
    events = relationship("Event", back_populates="college")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    college = relationship("College", back_populates="students")
    registrations = relationship("Registration", back_populates="student")
    attendance = relationship("Attendance", back_populates="student")
    feedback = relationship("Feedback", back_populates="student")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    max_capacity = Column(Integer)
    is_cancelled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    college = relationship("College", back_populates="events")
    registrations = relationship("Registration", back_populates="event")
    attendance = relationship("Attendance", back_populates="event")
    feedback = relationship("Feedback", back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    registered_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    checked_in_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="attendance")
    event = relationship("Event", back_populates="attendance")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    rating = Column(Integer)  # 1-5 scale
    comment = Column(String, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="feedback")
    event = relationship("Event", back_populates="feedback")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class CollegeCreate(BaseModel):
    name: str
    location: str

class CollegeResponse(BaseModel):
    id: int
    name: str
    location: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    name: str
    email: str
    college_id: int

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    college_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    description: str
    college_id: int
    start_time: datetime
    end_time: datetime
    location: str
    max_capacity: int

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    college_id: int
    start_time: datetime
    end_time: datetime
    location: str
    max_capacity: int
    is_cancelled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    student_id: int
    event_id: int

class AttendanceCreate(BaseModel):
    student_id: int
    event_id: int

class FeedbackCreate(BaseModel):
    student_id: int
    event_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class EventReport(BaseModel):
    event_id: int
    event_title: str
    total_registrations: int
    total_attendance: int
    attendance_percentage: float
    average_feedback: Optional[float]
    total_feedback_count: int

class StudentReport(BaseModel):
    student_id: int
    student_name: str
    college_name: str
    total_events_attended: int
    average_feedback_given: Optional[float]

# SQL Query Models
class SQLQueryRequest(BaseModel):
    query: str

class SQLQueryResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    execution_time: float

# FastAPI app
app = FastAPI(title="Campus Event Reporting System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def is_event_active(event: Event) -> bool:
    """Check if event is currently active (within ±30 min of event time)"""
    now = datetime.utcnow()
    return (event.start_time - timedelta(minutes=30) <= now <= event.end_time + timedelta(minutes=30))

def is_registration_open(event: Event) -> bool:
    """Check if registration is still open (before event starts)"""
    return datetime.utcnow() < event.start_time

# API Endpoints

@app.get("/")
async def root():
    return {"message": "Campus Event Reporting System API"}

# College endpoints
@app.post("/colleges/", response_model=CollegeResponse)
async def create_college(college: CollegeCreate, db: Session = Depends(get_db)):
    db_college = College(**college.dict())
    db.add(db_college)
    db.commit()
    db.refresh(db_college)
    return db_college

@app.get("/colleges/", response_model=List[CollegeResponse])
async def get_colleges(db: Session = Depends(get_db)):
    return db.query(College).all()

# Student endpoints
@app.post("/students/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if college exists
    college = db.query(College).filter(College.id == student.college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    # Check if email already exists
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[StudentResponse])
async def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Event endpoints (Admin only)
@app.post("/events/", response_model=EventResponse)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    # Check if college exists
    college = db.query(College).filter(College.id == event.college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    # Validate event times
    if event.start_time >= event.end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time")
    
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events/", response_model=List[EventResponse])
async def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@app.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.put("/events/{event_id}/cancel")
async def cancel_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.is_cancelled = True
    db.commit()
    return {"message": "Event cancelled successfully"}

# Registration endpoints
@app.post("/registrations/")
async def register_for_event(registration: RegistrationCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.id == registration.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if event exists
    event = db.query(Event).filter(Event.id == registration.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if event is cancelled
    if event.is_cancelled:
        raise HTTPException(status_code=400, detail="Cannot register for cancelled event")
    
    # Check if registration is still open
    if not is_registration_open(event):
        raise HTTPException(status_code=400, detail="Registration closed - event has started")
    
    # Check for duplicate registration
    existing_registration = db.query(Registration).filter(
        Registration.student_id == registration.student_id,
        Registration.event_id == registration.event_id
    ).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail="Already registered for this event")
    
    # Check capacity
    current_registrations = db.query(Registration).filter(
        Registration.event_id == registration.event_id
    ).count()
    if current_registrations >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is at full capacity")
    
    db_registration = Registration(**registration.dict())
    db.add(db_registration)
    db.commit()
    return {"message": "Successfully registered for event"}

@app.get("/registrations/student/{student_id}")
async def get_student_registrations(student_id: int, db: Session = Depends(get_db)):
    registrations = db.query(Registration).filter(Registration.student_id == student_id).all()
    return registrations

# Attendance endpoints
@app.post("/attendance/")
async def check_in_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.id == attendance.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if event exists
    event = db.query(Event).filter(Event.id == attendance.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if event is cancelled
    if event.is_cancelled:
        raise HTTPException(status_code=400, detail="Cannot check in for cancelled event")
    
    # Check if student is registered
    registration = db.query(Registration).filter(
        Registration.student_id == attendance.student_id,
        Registration.event_id == attendance.event_id
    ).first()
    if not registration:
        raise HTTPException(status_code=400, detail="Student not registered for this event")
    
    # Check if already attended
    existing_attendance = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.event_id == attendance.event_id
    ).first()
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Already checked in for this event")
    
    # Check if event is active (within ±30 min)
    if not is_event_active(event):
        raise HTTPException(status_code=400, detail="Cannot check in - event is not active")
    
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    return {"message": "Successfully checked in for event"}

# Feedback endpoints
@app.post("/feedback/")
async def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.id == feedback.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if event exists
    event = db.query(Event).filter(Event.id == feedback.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if event is cancelled
    if event.is_cancelled:
        raise HTTPException(status_code=400, detail="Cannot submit feedback for cancelled event")
    
    # Check if student attended the event
    attendance = db.query(Attendance).filter(
        Attendance.student_id == feedback.student_id,
        Attendance.event_id == feedback.event_id
    ).first()
    if not attendance:
        raise HTTPException(status_code=400, detail="Must attend event before submitting feedback")
    
    # Check for duplicate feedback
    existing_feedback = db.query(Feedback).filter(
        Feedback.student_id == feedback.student_id,
        Feedback.event_id == feedback.event_id
    ).first()
    if existing_feedback:
        raise HTTPException(status_code=400, detail="Already submitted feedback for this event")
    
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    return {"message": "Feedback submitted successfully"}

# Reporting endpoints
@app.get("/reports/events/{event_id}", response_model=EventReport)
async def get_event_report(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get registration count
    total_registrations = db.query(Registration).filter(Registration.event_id == event_id).count()
    
    # Get attendance count
    total_attendance = db.query(Attendance).filter(Attendance.event_id == event_id).count()
    
    # Calculate attendance percentage
    attendance_percentage = (total_attendance / total_registrations * 100) if total_registrations > 0 else 0
    
    # Get average feedback
    feedback_query = db.query(Feedback).filter(Feedback.event_id == event_id)
    feedback_count = feedback_query.count()
    avg_feedback = None
    if feedback_count > 0:
        avg_feedback = db.query(Feedback.rating).filter(Feedback.event_id == event_id).all()
        avg_feedback = sum([f[0] for f in avg_feedback]) / feedback_count
    
    return EventReport(
        event_id=event.id,
        event_title=event.title,
        total_registrations=total_registrations,
        total_attendance=total_attendance,
        attendance_percentage=round(attendance_percentage, 2),
        average_feedback=round(avg_feedback, 2) if avg_feedback else None,
        total_feedback_count=feedback_count
    )

@app.get("/reports/students/{student_id}", response_model=StudentReport)
async def get_student_report(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get total events attended
    total_events_attended = db.query(Attendance).filter(Attendance.student_id == student_id).count()
    
    # Get average feedback given
    feedback_query = db.query(Feedback).filter(Feedback.student_id == student_id)
    feedback_count = feedback_query.count()
    avg_feedback = None
    if feedback_count > 0:
        avg_feedback = db.query(Feedback.rating).filter(Feedback.student_id == student_id).all()
        avg_feedback = sum([f[0] for f in avg_feedback]) / feedback_count
    
    return StudentReport(
        student_id=student.id,
        student_name=student.name,
        college_name=student.college.name,
        total_events_attended=total_events_attended,
        average_feedback_given=round(avg_feedback, 2) if avg_feedback else None
    )

@app.get("/reports/colleges/{college_id}/events")
async def get_college_events_report(college_id: int, db: Session = Depends(get_db)):
    college = db.query(College).filter(College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    events = db.query(Event).filter(Event.college_id == college_id).all()
    reports = []
    
    for event in events:
        total_registrations = db.query(Registration).filter(Registration.event_id == event.id).count()
        total_attendance = db.query(Attendance).filter(Attendance.event_id == event.id).count()
        attendance_percentage = (total_attendance / total_registrations * 100) if total_registrations > 0 else 0
        
        feedback_query = db.query(Feedback).filter(Feedback.event_id == event.id)
        feedback_count = feedback_query.count()
        avg_feedback = None
        if feedback_count > 0:
            avg_feedback = db.query(Feedback.rating).filter(Feedback.event_id == event.id).all()
            avg_feedback = sum([f[0] for f in avg_feedback]) / feedback_count
        
        reports.append(EventReport(
            event_id=event.id,
            event_title=event.title,
            total_registrations=total_registrations,
            total_attendance=total_attendance,
            attendance_percentage=round(attendance_percentage, 2),
            average_feedback=round(avg_feedback, 2) if avg_feedback else None,
            total_feedback_count=feedback_count
        ))
    
    return reports

# SQL Query Endpoints
@app.post("/execute-sql", response_model=SQLQueryResponse)
async def execute_sql_endpoint(
    request: SQLQueryRequest, 
    db: Session = Depends(get_db)
):
    """
    Execute a SQL query and return results
    Only SELECT queries are allowed for security
    """
    start_time = time.time()
    
    # Basic security checks
    query_lower = request.query.lower().strip()
    
    # Block dangerous operations
    dangerous_keywords = [
        'drop', 'delete', 'update', 'insert', 'alter', 'create', 'truncate',
        'grant', 'revoke', 'exec', 'execute', 'sp_', 'xp_', '--', '/*', '*/'
    ]
    
    for keyword in dangerous_keywords:
        if keyword in query_lower:
            raise HTTPException(
                status_code=400, 
                detail=f"Query contains potentially dangerous keyword: {keyword}"
            )
    
    # Only allow SELECT queries for safety
    if not query_lower.startswith('select'):
        raise HTTPException(
            status_code=400,
            detail="Only SELECT queries are allowed for security reasons"
        )
    
    try:
        # Execute the query
        result = db.execute(text(request.query))
        
        # Convert to list of rows
        rows = result.fetchall()
        
        # Get column names
        columns = list(result.keys()) if rows else []
        
        # Convert rows to list of lists
        row_data = [list(row) for row in rows]
        
        execution_time = time.time() - start_time
        
        return SQLQueryResponse(
            columns=columns,
            rows=row_data,
            row_count=len(row_data),
            execution_time=round(execution_time, 4)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"SQL execution error: {str(e)}"
        )

@app.get("/sql/schema")
async def get_database_schema(db: Session = Depends(get_db)):
    """
    Get database schema information
    """
    try:
        # Get table names
        tables_query = """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
        """
        tables_result = db.execute(text(tables_query))
        tables = [row[0] for row in tables_result.fetchall()]
        
        schema_info = {}
        
        for table in tables:
            # Get column information
            columns_query = f"PRAGMA table_info({table});"
            columns_result = db.execute(text(columns_query))
            columns = [
                {
                    "name": row[1],
                    "type": row[2],
                    "not_null": bool(row[3]),
                    "primary_key": bool(row[5])
                }
                for row in columns_result.fetchall()
            ]
            
            schema_info[table] = {
                "columns": columns,
                "column_count": len(columns)
            }
        
        return {
            "tables": tables,
            "schema": schema_info
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting schema: {str(e)}"
        )

@app.get("/sql/sample/{table_name}")
async def get_sample_data(table_name: str, limit: int = 5, db: Session = Depends(get_db)):
    """
    Get sample data from a specific table
    """
    # Validate table name (basic security)
    if not table_name.replace('_', '').replace('-', '').isalnum():
        raise HTTPException(
            status_code=400,
            detail="Invalid table name"
        )
    
    try:
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        result = db.execute(text(query))
        
        rows = result.fetchall()
        columns = list(result.keys()) if rows else []
        row_data = [list(row) for row in rows]
        
        return {
            "table": table_name,
            "columns": columns,
            "rows": row_data,
            "row_count": len(row_data)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error getting sample data: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
