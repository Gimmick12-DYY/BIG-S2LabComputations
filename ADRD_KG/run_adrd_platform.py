#!/usr/bin/env python3
"""
ADRD Metadata Analysis Platform - Startup Script

This script provides an easy way to start the ADRD Metadata Analysis Platform
using the local ADRD_Metadata_YuyangD.xlsx dataset.

Usage:
    python run_adrd_platform.py

The application will be available at: http://localhost:5000
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_data_file():
    """Check if the ADRD metadata file exists."""
    data_file = 'templates/ADRD_Metadata_YuyangD.xlsx'
    if os.path.exists(data_file):
        print(f"✅ ADRD metadata file found: {data_file}")
        return True
    else:
        print(f"❌ ADRD metadata file not found: {data_file}")
        print("Please ensure the file is in the templates directory")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'flask', 'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories for the application."""
    directories = ['uploads', 'datasets', 'templates']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Application directories created/verified")

def main():
    """Main function to start the ADRD Metadata Analysis Platform."""
    print("="*80)
    print("🧠 ADRD METADATA ANALYSIS PLATFORM")
    print("="*80)
    print("Starting web application for ADRD metadata analysis...")
    print()
    
    # Check data file
    print("🔍 Checking ADRD metadata file...")
    if not check_data_file():
        sys.exit(1)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies are installed")
    
    # Create directories
    print("📁 Setting up directories...")
    create_directories()
    
    # Start the application
    print("🚀 Starting Flask application...")
    print("📍 Application will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the application")
    print("="*80)
    
    try:
        from adrd_web_app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        print("Make sure adrd_web_app.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting the application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
