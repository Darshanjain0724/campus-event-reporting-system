# Web-Based SQL Query Interface Guide

## 🎯 Overview

You now have a beautiful web-based SQL query interface that allows you to write and execute SQL queries directly in your browser! This provides a user-friendly way to interact with your Campus Event Reporting System database.

## 🚀 Setup Instructions

### 1. Add SQL Endpoint to Your FastAPI App

Add the following code to your `main.py` file (after the existing imports and before the app definition):

```python
# Add these imports at the top
import time
from typing import List, Dict, Any

# Add these Pydantic models
class SQLQueryRequest(BaseModel):
    query: str

class SQLQueryResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    execution_time: float

# Add these endpoints to your FastAPI app
@app.post("/execute-sql", response_model=SQLQueryResponse)
async def execute_sql_endpoint(
    request: SQLQueryRequest, 
    db: Session = Depends(get_db)
):
    """
    Execute a SQL query and return results
    Only SELECT queries are allowed for security
    """
    import time
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
```

### 2. Start Your FastAPI Server

```bash
python main.py
```

### 3. Open the Web Interface

Open `sql_query_interface.html` in your web browser, or serve it using a simple HTTP server:

```bash
# Option 1: Direct file opening
# Just double-click sql_query_interface.html

# Option 2: Using Python HTTP server
python -m http.server 8080
# Then visit http://localhost:8080/sql_query_interface.html
```

## 🎨 Features

### ✨ Beautiful Interface
- Modern, responsive design
- Real-time API status indicator
- Syntax highlighting for SQL queries
- Formatted query results in tables

### 🔒 Security Features
- Only SELECT queries allowed
- Dangerous keywords blocked
- Input validation and sanitization
- Error handling with helpful messages

### 📊 Query Features
- Pre-built sample queries (click to use)
- Query formatting tool
- Execution time tracking
- Row count and column statistics
- Keyboard shortcuts (Ctrl+Enter to execute)

### 🎯 Sample Queries Included
1. **Total Registrations per Event**
2. **Attendance Percentage per Event**
3. **Average Feedback Score**
4. **Top 3 Most Active Students**
5. **College Summary Statistics**

## 🛠️ Usage

### Writing Queries
1. Type your SQL query in the text area
2. Use sample queries as templates (click to load)
3. Format your query with the "Format Query" button
4. Execute with "Execute Query" button or Ctrl+Enter

### Viewing Results
- Results display in a formatted table
- Shows execution time and row count
- Handles NULL values gracefully
- Responsive design for mobile devices

### Error Handling
- Clear error messages for invalid queries
- Security warnings for blocked operations
- Connection status indicator

## 🔧 Customization

### Adding More Sample Queries
Edit the `sampleQueries` array in the HTML file:

```javascript
const sampleQueries = [
    `SELECT * FROM events LIMIT 5;`,
    `SELECT COUNT(*) FROM students;`,
    // Add your custom queries here
];
```

### Changing API URL
Update the `API_BASE_URL` constant:

```javascript
const API_BASE_URL = 'http://your-server:8000';
```

### Styling Changes
Modify the CSS in the `<style>` section to match your brand colors and preferences.

## 🚀 Advanced Features

### Schema Explorer
The interface can be extended to include:
- Database schema viewer
- Table relationship diagrams
- Column type information
- Sample data from each table

### Query History
Add functionality to:
- Save frequently used queries
- View query execution history
- Export results to CSV/Excel

### User Authentication
For production use, add:
- User login system
- Role-based query permissions
- Query logging and auditing

## 🎯 Benefits

1. **No Command Line Required**: Easy-to-use web interface
2. **Real-time Results**: Instant query execution and results
3. **Beautiful Output**: Formatted tables with statistics
4. **Secure**: Only read-only queries allowed
5. **Mobile Friendly**: Works on all devices
6. **Sample Queries**: Pre-built templates for common reports

## 🔍 Troubleshooting

### API Connection Issues
- Ensure FastAPI server is running on port 8000
- Check browser console for CORS errors
- Verify the API_BASE_URL is correct

### Query Errors
- Only SELECT queries are allowed
- Check SQL syntax carefully
- Use sample queries as templates

### Performance Issues
- Large result sets may take time to load
- Consider adding LIMIT clauses to queries
- Monitor execution times in the results

## 🎉 Ready to Use!

Your web-based SQL query interface is now ready! You can:
- Write custom queries for your campus event data
- Use pre-built sample queries for common reports
- View results in beautiful, formatted tables
- Track query performance and statistics

This provides a much more user-friendly way to interact with your database compared to command-line tools!
