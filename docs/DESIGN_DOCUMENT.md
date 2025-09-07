# Campus Event Reporting System - Design Document

## 1. System Overview

### 1.1 Purpose
The Campus Event Reporting System is designed to provide comprehensive event management and analytics capabilities for educational institutions. The system addresses the need for efficient tracking of student participation, event performance, and institutional engagement metrics.

### 1.2 Scope
- Event creation and management
- Student registration and attendance tracking
- Feedback collection and analysis
- Real-time reporting and analytics
- Interactive SQL query interface for data exploration

### 1.3 Key Stakeholders
- **Administrators**: College event coordinators who create and manage events
- **Students**: Event participants who register, attend, and provide feedback
- **Analysts**: Data users who need to extract insights from event data
- **IT Staff**: System administrators responsible for deployment and maintenance

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Admin Users   │    │  Student Users  │    │   Data Analysts │
│ (Event Creators)│    │ (Mobile App)    │    │   (Web Interface)│
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

### 2.2 Technology Stack

#### Backend Technologies
- **FastAPI**: Modern Python web framework
  - Automatic API documentation generation
  - Built-in data validation with Pydantic
  - Async support for high performance
  - Type hints for better code quality

- **SQLAlchemy**: Object-Relational Mapping
  - Declarative base for clean model definitions
  - Relationship mapping for data integrity
  - Query optimization and lazy loading
  - Database-agnostic design

- **SQLite**: Database Engine
  - Zero-configuration setup
  - ACID compliance for data integrity
  - Easy backup and portability
  - Suitable for prototype and small-medium deployments

#### Frontend Technologies
- **HTML5**: Semantic markup and modern features
- **CSS3**: Flexbox, Grid, and responsive design
- **Vanilla JavaScript**: No framework dependencies
- **Fetch API**: Modern HTTP client for API communication

## 3. Database Design

### 3.1 Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Colleges  │    │   Students  │    │    Events   │
│             │    │             │    │             │
│ - id (PK)   │◄───┤ - college_id│    │ - college_id│◄───┐
│ - name      │    │ - name      │    │ - title     │    │
│ - location  │    │ - email     │    │ - start_time│    │
│ - created_at│    │ - created_at│    │ - end_time  │    │
└─────────────┘    └─────────────┘    │ - location  │    │
                                      │ - capacity  │    │
┌─────────────┐    ┌─────────────┐    │ - cancelled │    │
│Registrations│    │ Attendance  │    └─────────────┘    │
│             │    │             │                       │
│ - student_id│◄───┤ - student_id│                       │
│ - event_id │◄───┤ - event_id  │                       │
│ - registered│    │ - checked_in│                       │
└─────────────┘    └─────────────┘                       │
                                                          │
┌─────────────┐                                          │
│   Feedback  │                                          │
│             │                                          │
│ - student_id│◄─────────────────────────────────────────┘
│ - event_id │
│ - rating   │
│ - comment  │
│ - submitted│
└─────────────┘
```

### 3.2 Table Specifications

#### Colleges Table
- **Purpose**: Store institutional information
- **Key Fields**: name (unique), location
- **Relationships**: One-to-many with Students and Events

#### Students Table
- **Purpose**: Store student information and college affiliation
- **Key Fields**: email (unique), college_id (foreign key)
- **Relationships**: Many-to-one with College, One-to-many with Registrations/Attendance/Feedback

#### Events Table
- **Purpose**: Store event details and scheduling information
- **Key Fields**: title, start_time, end_time, max_capacity, is_cancelled
- **Relationships**: Many-to-one with College, One-to-many with Registrations/Attendance/Feedback

#### Registrations Table
- **Purpose**: Track student event registrations
- **Key Fields**: student_id, event_id (composite unique constraint)
- **Business Rules**: No duplicate registrations, registration closes when event starts

#### Attendance Table
- **Purpose**: Track actual event attendance
- **Key Fields**: student_id, event_id, checked_in_at
- **Business Rules**: Must be registered, check-in within ±30 minutes of event time

#### Feedback Table
- **Purpose**: Store post-event feedback and ratings
- **Key Fields**: student_id, event_id, rating (1-5), comment
- **Business Rules**: Must have attended event, one feedback per student per event

## 4. API Design

### 4.1 RESTful Endpoints

#### College Management
- `POST /colleges/` - Create new college
- `GET /colleges/` - List all colleges

#### Student Management
- `POST /students/` - Create new student
- `GET /students/` - List all students
- `GET /students/{student_id}` - Get student details

#### Event Management
- `POST /events/` - Create new event
- `GET /events/` - List all events
- `GET /events/{event_id}` - Get event details
- `PUT /events/{event_id}/cancel` - Cancel event

#### Student Actions
- `POST /registrations/` - Register for event
- `GET /registrations/student/{student_id}` - Get student registrations
- `POST /attendance/` - Check in for attendance
- `POST /feedback/` - Submit feedback

#### Reporting
- `GET /reports/events/{event_id}` - Event analytics
- `GET /reports/students/{student_id}` - Student statistics
- `GET /reports/colleges/{college_id}/events` - College event reports

#### SQL Interface
- `POST /execute-sql` - Execute SQL queries safely
- `GET /sql/schema` - Get database schema
- `GET /sql/sample/{table_name}` - Get sample data

### 4.2 Data Models

#### Request/Response Models
- **CollegeCreate**: name, location
- **StudentCreate**: name, email, college_id
- **EventCreate**: title, description, college_id, start_time, end_time, location, max_capacity
- **SQLQueryRequest**: query
- **SQLQueryResponse**: columns, rows, row_count, execution_time

#### Business Logic Models
- **EventReport**: event_id, event_title, total_registrations, total_attendance, attendance_percentage, average_feedback, total_feedback_count
- **StudentReport**: student_id, student_name, college_name, total_events_attended, average_feedback_given

## 5. Security Design

### 5.1 Input Validation
- **Pydantic Models**: Automatic data validation and type checking
- **SQL Injection Prevention**: Parameterized queries and keyword filtering
- **Business Rule Validation**: Registration deadlines, capacity limits, attendance windows

### 5.2 SQL Query Security
- **Read-Only Queries**: Only SELECT statements allowed
- **Dangerous Keyword Filtering**: Block DROP, DELETE, UPDATE, INSERT, etc.
- **Query Timeout**: Prevent long-running queries
- **Result Limiting**: Prevent excessive data exposure

### 5.3 Error Handling
- **Graceful Degradation**: Meaningful error messages without system details
- **Input Sanitization**: Clean user input before processing
- **Logging**: Comprehensive error logging for debugging

## 6. User Interface Design

### 6.1 Web SQL Interface

#### Design Principles
- **Accessibility**: Clear navigation and intuitive controls
- **Responsiveness**: Mobile-first design approach
- **Performance**: Fast query execution and result display
- **Usability**: Schema exploration and sample query templates

#### Key Components
- **Query Input Area**: Large text area with syntax highlighting
- **Schema Explorer**: Interactive database structure display
- **Sample Query Navigation**: Horizontal browsing with keyboard shortcuts
- **Results Display**: Formatted tables with execution statistics
- **Status Indicators**: Real-time API connection status

#### User Experience Flow
1. **Schema Exploration**: Users can browse database structure
2. **Query Writing**: Assisted by schema panel and sample queries
3. **Execution**: One-click query execution with progress indicators
4. **Results Analysis**: Formatted results with metadata
5. **Iteration**: Easy modification and re-execution

### 6.2 Responsive Design
- **Mobile Breakpoints**: Optimized for phones, tablets, and desktops
- **Touch-Friendly**: Large buttons and touch targets
- **Flexible Layout**: CSS Grid and Flexbox for adaptive design
- **Performance**: Optimized assets and lazy loading

## 7. Performance Considerations

### 7.1 Database Optimization
- **Indexing Strategy**: Primary keys, foreign keys, and frequently queried columns
- **Query Optimization**: Efficient JOIN operations and WHERE clauses
- **Connection Pooling**: SQLAlchemy connection management
- **Lazy Loading**: On-demand relationship loading

### 7.2 API Performance
- **Async Operations**: FastAPI async support for concurrent requests
- **Response Caching**: HTTP caching headers for static data
- **Pagination**: Large result set handling
- **Compression**: Gzip compression for API responses

### 7.3 Frontend Performance
- **Asset Optimization**: Minified CSS and JavaScript
- **Lazy Loading**: On-demand resource loading
- **Caching Strategy**: Browser caching for static assets
- **Progressive Enhancement**: Core functionality without JavaScript

## 8. Deployment Architecture

### 8.1 Development Environment
- **Local SQLite**: Easy setup and testing
- **Hot Reloading**: FastAPI development server
- **Debug Mode**: Detailed error messages and logging

### 8.2 Production Considerations
- **Database Migration**: SQLite to PostgreSQL/MySQL
- **Web Server**: Nginx reverse proxy
- **Process Management**: Gunicorn or uWSGI
- **Monitoring**: Application performance monitoring
- **Backup Strategy**: Regular database backups

### 8.3 Scalability Planning
- **Horizontal Scaling**: Multiple application instances
- **Database Scaling**: Read replicas and connection pooling
- **Caching Layer**: Redis for session and query caching
- **Load Balancing**: Distribution of incoming requests

## 9. Testing Strategy

### 9.1 Unit Testing
- **Model Testing**: Database model validation
- **API Testing**: Endpoint functionality and error handling
- **Business Logic**: Registration, attendance, and feedback rules

### 9.2 Integration Testing
- **Database Integration**: SQLAlchemy ORM testing
- **API Integration**: End-to-end request/response testing
- **Frontend Integration**: JavaScript functionality testing

### 9.3 Performance Testing
- **Load Testing**: Concurrent user simulation
- **Query Performance**: SQL query optimization testing
- **Response Time**: API endpoint performance measurement

## 10. Future Enhancements

### 10.1 Short-term Improvements
- **User Authentication**: JWT-based authentication system
- **Role-based Access**: Admin, student, and analyst roles
- **Email Notifications**: Event reminders and updates
- **Advanced Filtering**: Query result filtering and sorting

### 10.2 Long-term Vision
- **Machine Learning**: Predictive analytics for event success
- **Mobile Applications**: Native iOS and Android apps
- **Integration APIs**: Connect with existing campus systems
- **Real-time Analytics**: Live dashboards and reporting
- **Multi-tenant Architecture**: Support for multiple institutions

---

*This design document serves as the foundation for the Campus Event Reporting System and will be updated as the system evolves.*
