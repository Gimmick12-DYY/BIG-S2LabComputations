#!/usr/bin/env python3
"""
Simple script to run the Disease Type Matrix Web Application

This script provides an easy way to start the Flask web application
for the disease type matrix visualization.

Usage:
    python run_web_app.py

The application will be available at: http://localhost:5000
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from web_app import app
    
    if __name__ == '__main__':
        print("="*60)
        print("Disease Type Matrix Web Application")
        print("="*60)
        print("Starting Flask application...")
        print("Application will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop the application")
        print("="*60)
        
        # Run the Flask application
        app.run(debug=True, host='0.0.0.0', port=5000)
        
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure you have installed all required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting the application: {e}")
    sys.exit(1)
