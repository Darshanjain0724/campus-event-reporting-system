#!/usr/bin/env python3
"""
Web Interface Launcher for Campus Event Reporting System
This script will start both the FastAPI server and serve the web interface
"""

import subprocess
import webbrowser
import time
import os
import sys
from pathlib import Path

def check_fastapi_running():
    """Check if FastAPI server is already running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_fastapi_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        # Start FastAPI server in background
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server started successfully
        if check_fastapi_running():
            print("✅ FastAPI server started successfully on http://localhost:8000")
            return process
        else:
            print("❌ FastAPI server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {e}")
        return None

def start_web_server():
    """Start a simple HTTP server for the web interface"""
    print("🌐 Starting web server for interface...")
    try:
        # Start HTTP server in background
        process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)
        print("✅ Web server started on http://localhost:8080")
        return process
        
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        return None

def open_web_interface():
    """Open the web interface in browser"""
    web_url = "http://localhost:8080/sql_query_interface.html"
    api_url = "http://localhost:8000/docs"
    
    print(f"🌐 Opening web interface: {web_url}")
    print(f"📚 API documentation: {api_url}")
    
    try:
        webbrowser.open(web_url)
        time.sleep(1)
        webbrowser.open(api_url)
        print("✅ Web interface opened in browser")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print(f"Please manually open: {web_url}")

def main():
    print("🎓 Campus Event Reporting System - Web Interface Launcher")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Please run this script from the project directory.")
        return
    
    if not Path("sql_query_interface.html").exists():
        print("❌ sql_query_interface.html not found.")
        return
    
    # Check if FastAPI is already running
    if check_fastapi_running():
        print("✅ FastAPI server is already running")
        fastapi_process = None
    else:
        fastapi_process = start_fastapi_server()
        if not fastapi_process:
            print("❌ Cannot start FastAPI server. Please check your setup.")
            return
    
    # Start web server
    web_process = start_web_server()
    if not web_process:
        print("❌ Cannot start web server.")
        return
    
    # Open web interface
    open_web_interface()
    
    print("\n" + "=" * 60)
    print("🎉 Web interface is now running!")
    print("📱 Web Interface: http://localhost:8080/sql_query_interface.html")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop all servers")
    print("=" * 60)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down servers...")
        
        if fastapi_process:
            fastapi_process.terminate()
            print("✅ FastAPI server stopped")
        
        if web_process:
            web_process.terminate()
            print("✅ Web server stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
