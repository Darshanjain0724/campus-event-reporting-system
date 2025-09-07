#!/usr/bin/env python3
"""
FastAPI endpoint for executing SQL queries safely
This should be added to your main.py file
"""

from fastapi import HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
from typing import List, Dict, Any

# Add this to your main.py file after the existing imports and before the app definition

class SQLQueryRequest(BaseModel):
    query: str

class SQLQueryResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    execution_time: float

def execute_sql_query(query: str, db: Session = Depends(get_db)) -> SQLQueryResponse:
    """
    Execute a SQL query safely and return results
    """
    import time
    start_time = time.time()
    
    # Basic security checks
    query_lower = query.lower().strip()
    
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
        result = db.execute(text(query))
        
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

# Add this endpoint to your FastAPI app
@app.post("/execute-sql", response_model=SQLQueryResponse)
async def execute_sql_endpoint(
    request: SQLQueryRequest, 
    db: Session = Depends(get_db)
):
    """
    Execute a SQL query and return results
    Only SELECT queries are allowed for security
    """
    return execute_sql_query(request.query, db)

# Add this endpoint to get available tables and their schemas
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

# Add this endpoint to get sample data from tables
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
