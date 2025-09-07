# 🎓 Campus Event Reporting System

A comprehensive FastAPI-based system for managing campus events, student registrations, attendance tracking, and feedback collection with a beautiful web-based SQL query interface.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### 🎯 Core Functionality
- **Event Management**: Create, manage, and cancel campus events
- **Student Registration**: Students can register for events with capacity limits
- **Attendance Tracking**: Check-in system with time validation (±30 minutes)
- **Feedback Collection**: Post-attendance rating system (1-5 scale)
- **Comprehensive Reporting**: Event analytics, attendance percentages, and student statistics

### 🎨 Web Interface
- **Beautiful SQL Query Interface**: Write and execute SQL queries directly in your browser
- **Interactive Database Schema**: Real-time schema explorer with clickable column names
- **Sample Queries**: Pre-built queries for common reports
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 🔒 Security & Validation
- **Input Validation**: Comprehensive data validation with Pydantic models
- **SQL Injection Protection**: Safe SQL query execution with keyword filtering
- **Business Rules**: Enforced registration deadlines, capacity limits, and attendance validation
- **Error Handling**: Graceful error handling with helpful messages

## 🏗️ Architecture

### Technology Stack
- **Backend**: FastAPI (Python) with async support
- **Database**: SQLite (easily portable to PostgreSQL/MySQL)
- **ORM**: SQLAlchemy with relationship mapping
- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks needed)
- **Validation**: Pydantic models for request/response validation

### Database Schema
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Colleges  │    │   Students  │    │    Events   │
│             │    │             │    │             │
│ - id        │◄───┤ - college_id│    │ - college_id│◄───┐
│ - name      │    │ - name      │    │ - title     │    │
│ - location  │    │ - email     │    │ - start_time│    │
└─────────────┘    └─────────────┘    │ - end_time  │    │
                                      │ - location  │    │
┌─────────────┐    ┌─────────────┐    │ - capacity  │    │
│Registrations│    │ Attendance  │    └─────────────┘    │
│             │    │             │                       │
│ - student_id│◄───┤ - student_id│                       │
│ - event_id  │◄───┤ - event_id  │                       │
│ - registered│    │ - checked_in│                       │
└─────────────┘    └─────────────┘                       │
                                                          │
┌─────────────┐                                          │
│   Feedback  │                                          │
│             │                                          │
│ - student_id│◄─────────────────────────────────────────┘
│ - event_id  │
│ - rating    │
│ - comment   │
└─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/campus-event-reporting-system.git
   cd campus-event-reporting-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the system**
   ```bash
   python launch_web_interface.py
   ```

4. **Access the interfaces**
   - **Web SQL Interface**: http://localhost:8080/sql_query_interface.html
   - **API Documentation**: http://localhost:8000/docs
   - **Interactive API**: http://localhost:8000/redoc

### Alternative Setup

1. **Start FastAPI server**
   ```bash
   python main.py
   ```

2. **Start web server** (in another terminal)
   ```bash
   python -m http.server 8080
   ```

3. **Populate with sample data** (optional)
   ```bash
   python sample_data.py
   ```

## 📱 Usage

### Web SQL Interface

1. **Open the web interface**: http://localhost:8080/sql_query_interface.html
2. **Explore the schema**: Click table names in the right panel to see columns
3. **Write queries**: Use the schema panel to avoid typos
4. **Execute queries**: Click "Execute Query" or press Ctrl+Enter
5. **View results**: Results display in formatted tables with execution time

### API Endpoints

#### College Management
- `POST /colleges/` - Create a new college
- `GET /colleges/` - List all colleges

#### Student Management
- `POST /students/` - Create a new student
- `GET /students/` - List all students
- `GET /students/{student_id}` - Get student details

#### Event Management
- `POST /events/` - Create a new event
- `GET /events/` - List all events
- `GET /events/{event_id}` - Get event details
- `PUT /events/{event_id}/cancel` - Cancel an event

#### Student Actions
- `POST /registrations/` - Register for an event
- `POST /attendance/` - Check in for attendance
- `POST /feedback/` - Submit event feedback

#### Reporting
- `GET /reports/events/{event_id}` - Get event analytics
- `GET /reports/students/{student_id}` - Get student statistics
- `GET /reports/colleges/{college_id}/events` - Get college event reports

#### SQL Query Interface
- `POST /execute-sql` - Execute SQL queries safely
- `GET /sql/schema` - Get database schema information
- `GET /sql/sample/{table_name}` - Get sample data from tables

## 📊 Sample Queries

### Event Analytics
```sql
-- Total registrations per event
SELECT e.id, e.title, COUNT(r.id) AS registrations
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
WHERE e.college_id = 1
GROUP BY e.id, e.title
ORDER BY registrations DESC;

-- Attendance percentage per event
SELECT e.id, e.title,
  COUNT(a.id) AS present,
  COUNT(r.id) AS registered,
  CASE WHEN COUNT(r.id)=0 THEN 0
       ELSE ROUND(100.0 * COUNT(a.id) / COUNT(r.id), 2) END AS attendance_pct
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
LEFT JOIN attendance a ON a.event_id = e.id AND a.student_id = r.student_id
WHERE e.college_id = 1
GROUP BY e.id, e.title
ORDER BY attendance_pct DESC;
```

### Student Statistics
```sql
-- Top 3 most active students
SELECT s.id, s.name, s.email, COUNT(a.id) AS attended_events
FROM students s
JOIN attendance a ON a.student_id = s.id
WHERE s.college_id = 1
GROUP BY s.id, s.name, s.email
ORDER BY attended_events DESC
LIMIT 3;
```

## 🛠️ Development

### Project Structure
```
campus-event-reporting-system/
├── main.py                      # FastAPI application
├── sql_query_interface.html     # Web SQL interface
├── sample_data.py              # Sample data generator
├── launch_web_interface.py     # Web interface launcher
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── .gitignore                 # Git ignore rules
└── docs/                      # Additional documentation
```

### Running Tests
```bash
# Test the API
python test_api.py

# Run SQL queries
python run_sql_queries.py

# Interactive SQL console
python sql_console.py
```

### Database Migration
To migrate from SQLite to PostgreSQL/MySQL:

1. Update `SQLALCHEMY_DATABASE_URL` in `main.py`
2. Install appropriate database driver
3. Update connection parameters
4. Schema remains compatible

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
DATABASE_URL=sqlite:///./campus_events.db
API_HOST=0.0.0.0
API_PORT=8000
WEB_PORT=8080
```

### Customization
- **Branding**: Modify colors and styling in the HTML file
- **Sample Queries**: Add custom queries to the interface
- **API Endpoints**: Extend with additional functionality
- **Database Schema**: Add new tables and relationships

## 📈 Performance

### Scalability
- Designed for ~50 colleges × ~500 students × ~20 events/semester
- Efficient queries with proper indexing
- Async FastAPI for high performance
- SQLite suitable for prototype; easily migrates to production databases

### Optimization
- Database indexes on foreign keys
- Optimized reporting queries
- Efficient data validation
- Minimal memory footprint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure backward compatibility

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for robust ORM capabilities
- SQLite for the lightweight database engine
- The open-source community for inspiration and tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/campus-event-reporting-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/campus-event-reporting-system/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/campus-event-reporting-system/wiki)

## 🎯 Roadmap

- [ ] User authentication and authorization
- [ ] Real-time notifications
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Email/SMS notifications
- [ ] Event categories and tags
- [ ] Waitlist functionality
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Database backup and restore

---

**Made with ❤️ for educational institutions**
