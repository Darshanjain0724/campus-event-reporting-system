#!/usr/bin/env python3
"""
Interactive SQL console for Campus Event Reporting System
Allows you to run custom SQL queries directly against the database
"""

import sqlite3
import pandas as pd

def connect_to_db():
    """Connect to the SQLite database"""
    return sqlite3.connect("campus_events.db")

def execute_custom_query():
    """Interactive SQL console"""
    print("🎓 Campus Event Reporting System - SQL Console")
    print("=" * 50)
    print("💡 Type your SQL queries here. Type 'exit' to quit.")
    print("📚 Available tables: colleges, students, events, registrations, attendance, feedback")
    print("🔍 Example: SELECT * FROM events LIMIT 5;")
    print("-" * 50)
    
    conn = connect_to_db()
    
    try:
        while True:
            query = input("\nSQL> ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            if not query.endswith(';'):
                query += ';'
            
            try:
                df = pd.read_sql_query(query, conn)
                
                if df.empty:
                    print("✅ Query executed successfully (no results)")
                else:
                    print(f"\n📊 Results ({len(df)} rows):")
                    print("-" * 50)
                    print(df.to_string(index=False))
                    
            except Exception as e:
                print(f"❌ SQL Error: {e}")
                
    except KeyboardInterrupt:
        print("\n👋 Console closed by user")
    finally:
        conn.close()

def show_sample_queries():
    """Display sample queries for reference"""
    print("\n📚 Sample Queries for Reference:")
    print("=" * 50)
    
    samples = [
        ("List all colleges", "SELECT * FROM colleges;"),
        ("List all students", "SELECT * FROM students LIMIT 10;"),
        ("List all events", "SELECT * FROM events LIMIT 10;"),
        ("Event registrations", "SELECT e.title, COUNT(r.id) as registrations FROM events e LEFT JOIN registrations r ON e.id = r.event_id GROUP BY e.id, e.title;"),
        ("Attendance stats", "SELECT e.title, COUNT(a.id) as attendance FROM events e LEFT JOIN attendance a ON e.id = a.event_id GROUP BY e.id, e.title;"),
        ("Feedback summary", "SELECT e.title, AVG(f.rating) as avg_rating FROM events e LEFT JOIN feedback f ON e.id = f.event_id GROUP BY e.id, e.title;")
    ]
    
    for i, (desc, query) in enumerate(samples, 1):
        print(f"\n{i}. {desc}:")
        print(f"   {query}")

if __name__ == "__main__":
    try:
        show_sample_queries()
        execute_custom_query()
    except Exception as e:
        print(f"❌ Error: {e}")
