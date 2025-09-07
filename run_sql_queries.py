#!/usr/bin/env python3
"""
Script to execute sample SQL queries against the Campus Event Reporting System database
"""

import sqlite3
import pandas as pd
from datetime import datetime

def connect_to_db():
    """Connect to the SQLite database"""
    return sqlite3.connect("campus_events.db")

def execute_query(query, description):
    """Execute a SQL query and display results"""
    print(f"\n{'='*60}")
    print(f"📊 {description}")
    print(f"{'='*60}")
    
    try:
        conn = connect_to_db()
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            print("No data found.")
        else:
            print(df.to_string(index=False))
            print(f"\nTotal rows: {len(df)}")
        
    except Exception as e:
        print(f"❌ Error executing query: {e}")

def main():
    print("🎓 Campus Event Reporting System - SQL Query Executor")
    print("=" * 60)
    
    # Get college ID from user
    conn = connect_to_db()
    colleges = pd.read_sql_query("SELECT id, name FROM colleges", conn)
    conn.close()
    
    if colleges.empty:
        print("❌ No colleges found. Please run sample_data.py first.")
        return
    
    print("\nAvailable colleges:")
    print(colleges.to_string(index=False))
    
    college_id = input("\nEnter college ID to run queries for: ").strip()
    
    if not college_id.isdigit():
        print("❌ Please enter a valid college ID (number)")
        return
    
    # Sample SQL Queries (adapted for our schema)
    
    # 1. Total registrations per event
    query1 = f"""
    SELECT e.id, e.title, COUNT(r.id) AS registrations
    FROM events e
    LEFT JOIN registrations r ON r.event_id = e.id
    WHERE e.college_id = {college_id}
    GROUP BY e.id, e.title
    ORDER BY registrations DESC;
    """
    execute_query(query1, "Total Registrations per Event")
    
    # 2. Attendance percentage per event
    query2 = f"""
    SELECT e.id, e.title,
      COUNT(a.id) AS present,
      COUNT(r.id) AS registered,
      CASE WHEN COUNT(r.id)=0 THEN 0
           ELSE ROUND(100.0 * COUNT(a.id) / COUNT(r.id), 2) END AS attendance_pct
    FROM events e
    LEFT JOIN registrations r ON r.event_id = e.id
    LEFT JOIN attendance a ON a.event_id = e.id AND a.student_id = r.student_id
    WHERE e.college_id = {college_id}
    GROUP BY e.id, e.title
    ORDER BY attendance_pct DESC;
    """
    execute_query(query2, "Attendance Percentage per Event")
    
    # 3. Average feedback score
    query3 = f"""
    SELECT e.id, e.title, ROUND(AVG(f.rating), 2) AS avg_rating, COUNT(f.id) AS feedback_count
    FROM events e
    LEFT JOIN feedback f ON f.event_id = e.id
    WHERE e.college_id = {college_id}
    GROUP BY e.id, e.title
    ORDER BY avg_rating DESC;
    """
    execute_query(query3, "Average Feedback Score per Event")
    
    # 4. Top 3 most active students
    query4 = f"""
    SELECT s.id, s.name, s.email, COUNT(a.id) AS attended_events
    FROM students s
    JOIN attendance a ON a.student_id = s.id
    WHERE s.college_id = {college_id}
    GROUP BY s.id, s.name, s.email
    ORDER BY attended_events DESC
    LIMIT 3;
    """
    execute_query(query4, "Top 3 Most Active Students")
    
    # 5. Additional useful queries
    query5 = f"""
    SELECT 
        COUNT(DISTINCT e.id) AS total_events,
        COUNT(DISTINCT r.id) AS total_registrations,
        COUNT(DISTINCT a.id) AS total_attendance,
        COUNT(DISTINCT f.id) AS total_feedback
    FROM events e
    LEFT JOIN registrations r ON r.event_id = e.id
    LEFT JOIN attendance a ON a.event_id = e.id
    LEFT JOIN feedback f ON f.event_id = e.id
    WHERE e.college_id = {college_id};
    """
    execute_query(query5, "College Summary Statistics")
    
    print(f"\n{'='*60}")
    print("✅ All queries completed successfully!")
    print("💡 Tip: You can also run these queries directly in SQLite browser tools")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Query execution cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
