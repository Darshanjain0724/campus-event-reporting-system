# SQL Queries Guide - Campus Event Reporting System

## 🎯 Ways to Execute SQL Queries

### Method 1: Automated Query Runner (Recommended)
Run the pre-configured queries with formatted output:

```bash
python run_sql_queries.py
```

This script will:
- Show available colleges
- Let you select a college ID
- Execute all sample queries with formatted results
- Display statistics in a readable format

### Method 2: Interactive SQL Console
Run custom SQL queries interactively:

```bash
python sql_console.py
```

This gives you a SQL prompt where you can:
- Run any custom SQL query
- See sample queries for reference
- Get formatted results

### Method 3: Direct SQLite Access
Access the database directly using SQLite command line:

```bash
sqlite3 campus_events.db
```

Then run queries directly:
```sql
SELECT * FROM events LIMIT 5;
.exit
```

### Method 4: SQLite Browser Tools
Use GUI tools like:
- **DB Browser for SQLite** (free, cross-platform)
- **SQLiteStudio** (free, cross-platform)
- **DBeaver** (free, supports multiple databases)

## 📊 Sample Queries (Adapted for Our Schema)

### 1. Total Registrations per Event
```sql
SELECT e.id, e.title, COUNT(r.id) AS registrations
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
WHERE e.college_id = 1  -- Replace with your college ID
GROUP BY e.id, e.title
ORDER BY registrations DESC;
```

### 2. Attendance Percentage per Event
```sql
SELECT e.id, e.title,
  COUNT(a.id) AS present,
  COUNT(r.id) AS registered,
  CASE WHEN COUNT(r.id)=0 THEN 0
       ELSE ROUND(100.0 * COUNT(a.id) / COUNT(r.id), 2) END AS attendance_pct
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
LEFT JOIN attendance a ON a.event_id = e.id AND a.student_id = r.student_id
WHERE e.college_id = 1  -- Replace with your college ID
GROUP BY e.id, e.title
ORDER BY attendance_pct DESC;
```

### 3. Average Feedback Score
```sql
SELECT e.id, e.title, ROUND(AVG(f.rating), 2) AS avg_rating, COUNT(f.id) AS feedback_count
FROM events e
LEFT JOIN feedback f ON f.event_id = e.id
WHERE e.college_id = 1  -- Replace with your college ID
GROUP BY e.id, e.title
ORDER BY avg_rating DESC;
```

### 4. Top 3 Most Active Students
```sql
SELECT s.id, s.name, s.email, COUNT(a.id) AS attended_events
FROM students s
JOIN attendance a ON a.student_id = s.id
WHERE s.college_id = 1  -- Replace with your college ID
GROUP BY s.id, s.name, s.email
ORDER BY attended_events DESC
LIMIT 3;
```

## 🔍 Additional Useful Queries

### College Summary Statistics
```sql
SELECT 
    COUNT(DISTINCT e.id) AS total_events,
    COUNT(DISTINCT r.id) AS total_registrations,
    COUNT(DISTINCT a.id) AS total_attendance,
    COUNT(DISTINCT f.id) AS total_feedback
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
LEFT JOIN attendance a ON a.event_id = e.id
LEFT JOIN feedback f ON f.event_id = e.id
WHERE e.college_id = 1;
```

### Events with Low Attendance
```sql
SELECT e.title, 
       COUNT(r.id) as registered,
       COUNT(a.id) as attended,
       ROUND(100.0 * COUNT(a.id) / COUNT(r.id), 2) as attendance_pct
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
LEFT JOIN attendance a ON a.event_id = e.id AND a.student_id = r.student_id
WHERE e.college_id = 1
GROUP BY e.id, e.title
HAVING attendance_pct < 50
ORDER BY attendance_pct ASC;
```

### Student Participation by College
```sql
SELECT c.name as college_name,
       COUNT(DISTINCT s.id) as total_students,
       COUNT(DISTINCT r.id) as total_registrations,
       COUNT(DISTINCT a.id) as total_attendance
FROM colleges c
LEFT JOIN students s ON s.college_id = c.id
LEFT JOIN registrations r ON r.student_id = s.id
LEFT JOIN attendance a ON a.student_id = s.id
GROUP BY c.id, c.name
ORDER BY total_attendance DESC;
```

### Recent Events (Last 30 days)
```sql
SELECT e.title, e.start_time, e.location,
       COUNT(r.id) as registrations,
       COUNT(a.id) as attendance
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
LEFT JOIN attendance a ON a.event_id = e.id
WHERE e.start_time >= datetime('now', '-30 days')
GROUP BY e.id, e.title, e.start_time, e.location
ORDER BY e.start_time DESC;
```

## 🛠️ Schema Reference

### Tables and Key Columns
- **colleges**: id, name, location
- **students**: id, name, email, college_id
- **events**: id, title, description, college_id, start_time, end_time, location, max_capacity
- **registrations**: id, student_id, event_id, registered_at
- **attendance**: id, student_id, event_id, checked_in_at
- **feedback**: id, student_id, event_id, rating, comment, submitted_at

### Key Relationships
- Students belong to one college (college_id)
- Events belong to one college (college_id)
- Registrations link students to events
- Attendance links students to events (after registration)
- Feedback links students to events (after attendance)

## 💡 Tips for Query Writing

1. **Use LEFT JOIN** for optional relationships (events might have no registrations)
2. **Always filter by college_id** for college-specific reports
3. **Use COUNT(DISTINCT ...)** when you want unique counts
4. **Handle NULL values** with CASE statements for percentages
5. **Order results** by relevant metrics (DESC for counts, ASC for dates)

## 🚀 Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Populate sample data**: `python sample_data.py`
3. **Run automated queries**: `python run_sql_queries.py`
4. **Or use interactive console**: `python sql_console.py`

The automated script will show you all available colleges and let you select which one to run reports for!
