# Campus Event Reporting System - Project Structure

## Repository Organization

```
campus-event-reporting-system/
├── README.md                           # Main project documentation
├── PROJECT_STRUCTURE.md               # This file - project organization
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
│
├── src/                               # Source code directory
│   ├── main.py                       # FastAPI application
│   ├── sample_data.py                # Sample data generator
│   ├── refresh_sample_data.py        # Data refresh script
│   ├── test_api.py                   # API testing script
│   ├── run_sql_queries.py            # SQL query runner
│   ├── sql_console.py                # Interactive SQL console
│   ├── sql_endpoint.py               # SQL endpoint definitions
│   ├── start.py                      # Startup script
│   ├── launch_web_interface.py       # Web interface launcher
│   ├── launch_web_interface.bat     # Windows batch launcher
│   └── sql_query_interface.html      # Web SQL interface
│
├── docs/                             # Documentation directory
│   └── DESIGN_DOCUMENT.md            # Comprehensive design document
│
├── reports/                          # Reports and outputs directory
│   └── SAMPLE_QUERY_RESULTS.md       # Sample query results and analytics
│
├── ai_conversation_log/              # AI development conversation log
│   └── CONVERSATION_LOG.md           # Complete development conversation
│
└── Additional Documentation Files:
    ├── QUICK_START.md                # Quick start guide
    ├── SQL_QUERIES_GUIDE.md          # SQL query examples and guide
    └── WEB_SQL_INTERFACE_GUIDE.md    # Web interface documentation
```

## File Descriptions

### Core Application Files (`src/`)
- **`main.py`**: Complete FastAPI application with all endpoints
- **`sql_query_interface.html`**: Web-based SQL query interface
- **`sample_data.py`**: Generates realistic test data
- **`refresh_sample_data.py`**: Clears and repopulates database
- **`launch_web_interface.py`**: Starts both API and web servers

### Testing and Utilities (`src/`)
- **`test_api.py`**: Automated API testing
- **`run_sql_queries.py`**: Executes sample SQL queries
- **`sql_console.py`**: Interactive SQL command line interface
- **`start.py`**: Simple startup script

### Documentation (`docs/`)
- **`DESIGN_DOCUMENT.md`**: Comprehensive system design and architecture

### Reports (`reports/`)
- **`SAMPLE_QUERY_RESULTS.md`**: Sample outputs and analytics results

### Development Log (`ai_conversation_log/`)
- **`CONVERSATION_LOG.md`**: Complete AI-assisted development conversation

## Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Start the system**: `python src/launch_web_interface.py`
3. **Access web interface**: `http://localhost:8080/sql_query_interface.html`
4. **View API docs**: `http://localhost:8000/docs`

## Key Features

- **FastAPI Backend**: Modern Python web framework
- **SQLite Database**: Lightweight, portable database
- **Web SQL Interface**: Interactive query execution
- **Sample Data**: Realistic test data for meaningful results
- **Comprehensive Documentation**: Complete setup and usage guides
- **Professional Repository Structure**: Organized for easy navigation

## Development Notes

- All Python files are in the `src/` directory for better organization
- Documentation is separated into logical categories
- Sample data and reports demonstrate system capabilities
- AI conversation log provides complete development history
- Repository follows professional software development practices
