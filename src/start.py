#!/usr/bin/env python3
"""
Startup script for Campus Event Reporting System
This script starts the FastAPI server and optionally populates sample data.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Campus Event Reporting System...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the server
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
    except FileNotFoundError:
        print("❌ main.py not found. Make sure you're in the correct directory.")

def populate_sample_data():
    """Ask user if they want to populate sample data"""
    response = input("\n📊 Would you like to populate the database with sample data? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        print("📊 Populating database with sample data...")
        try:
            subprocess.run([sys.executable, "sample_data.py"], check=True)
            print("✅ Sample data created successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating sample data: {e}")
        except FileNotFoundError:
            print("❌ sample_data.py not found")

def main():
    print("🎓 Campus Event Reporting System")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Please run this script from the project directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Ask about sample data
    populate_sample_data()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
