# Campus Event Reporting System

A comprehensive web-based system for managing campus events, student registrations, attendance tracking, and feedback collection. Built with FastAPI and featuring an interactive SQL query interface.

## 🎯 Project Overview

This system was designed to solve the common problem of tracking and analyzing campus event participation. As someone who has worked with educational institutions, I noticed that most event management systems lack proper analytics and reporting capabilities. This project addresses that gap by providing both a robust API and a user-friendly web interface for data analysis.

## 🚀 Key Features

### Core Functionality
- **Event Management**: Create, manage, and cancel campus events with capacity limits
- **Student Registration**: Students can register for events with automatic duplicate prevention
- **Attendance Tracking**: Check-in system with time validation (±30 minutes from event start)
- **Feedback Collection**: Post-attendance rating system (1-5 scale) with optional comments
- **Comprehensive Reporting**: Real-time analytics on event popularity, attendance rates, and student engagement

### Web SQL Interface
- **Interactive Database Explorer**: Real-time schema display with clickable column names
- **Sample Query Navigation**: Horizontal browsing through pre-built analytical queries
- **Query Execution**: Direct SQL execution with formatted results and execution time tracking
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🏗️ Technical Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework with automatic API documentation
- **SQLAlchemy**: Robust ORM with relationship mapping and data validation
- **SQLite**: Lightweight database (easily portable to PostgreSQL/MySQL)
- **Pydantic**: Data validation and serialization with type hints

### Frontend
- **Pure HTML/CSS/JavaScript**: No framework dependencies for maximum compatibility
- **Responsive Design**: Mobile-first approach with modern CSS Grid and Flexbox
- **Interactive Elements**: Real-time schema updates and query result formatting

### Security Features
- **SQL Injection Protection**: Safe query execution with keyword filtering
- **Input Validation**: Comprehensive data validation with helpful error messages
- **Business Rule Enforcement**: Registration deadlines, capacity limits, and attendance validation

## 📊 Database Design

The system uses a well-normalized database schema with proper relationships:

```
Colleges (1) ──── (N) Students
Colleges (1) ──── (N) Events
Students (1) ──── (N) Registrations
Events (1) ──── (N) Registrations
Students (1) ──── (N) Attendance
Events (1) ──── (N) Attendance
Students (1) ──── (N) Feedback
Events (1) ──── (N) Feedback
```

This design ensures data integrity while allowing for complex analytical queries.

## 🎨 User Experience Design

### Web Interface Philosophy
I designed the web interface with the principle that data analysis should be accessible to non-technical users. The schema explorer allows users to understand the database structure without needing SQL knowledge, while the sample queries provide templates for common analytical tasks.

### Navigation Design
The horizontal query navigation was implemented to solve the problem of long scrolling lists. Users can now browse through analytical queries efficiently using both mouse clicks and keyboard shortcuts.

## 🔧 Development Process

### Problem-Solving Approach
1. **Identified Core Requirements**: Event management, registration, attendance, and feedback
2. **Designed Database Schema**: Focused on relationships and data integrity
3. **Built API First**: RESTful endpoints with comprehensive error handling
4. **Created Web Interface**: Interactive SQL interface for data analysis
5. **Added Sample Data**: Realistic test data for meaningful query results

### Code Organization
- **Separation of Concerns**: Clear separation between API logic, database models, and web interface
- **Modular Design**: Each component can be extended independently
- **Documentation**: Comprehensive inline documentation and setup guides

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/campus-event-reporting-system.git
cd campus-event-reporting-system

# Install dependencies
pip install -r requirements.txt

# Start the system
python launch_web_interface.py
```

### Access Points
- **Web SQL Interface**: http://localhost:8080/sql_query_interface.html
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## 📈 Sample Analytics

The system comes with pre-built analytical queries:

1. **Event Popularity**: Registration counts and trends
2. **Attendance Analysis**: Percentage calculations and patterns
3. **Student Engagement**: Most active participants
4. **Feedback Insights**: Rating distributions and comments
5. **College Performance**: Cross-institution comparisons

## 🔮 Future Enhancements

### Planned Features
- **User Authentication**: Role-based access control
- **Real-time Notifications**: Email/SMS alerts for events
- **Advanced Analytics**: Machine learning insights and predictions
- **Mobile App**: Native iOS/Android applications
- **Integration APIs**: Connect with existing campus systems

### Scalability Considerations
- **Database Migration**: Easy transition to PostgreSQL/MySQL
- **Caching Layer**: Redis integration for improved performance
- **Load Balancing**: Horizontal scaling capabilities
- **Microservices**: Service decomposition for large deployments

## 🤝 Contributing

This project welcomes contributions from the community. Please read the contributing guidelines and ensure your code follows the established patterns.

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive tests for new features
- Update documentation for any API changes
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Special thanks to the FastAPI community for the excellent framework, and to all the educational institutions that inspired this project's design.

---

**Built with passion for educational technology and data-driven insights.**
