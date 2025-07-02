#!/usr/bin/env python3
"""
AI Tutor Setup Script
This script sets up the AI Tutor application by installing dependencies
and downloading required models.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🤖 AI Tutor Setup Script")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies. Please check your internet connection.")
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("⚠️  spaCy model download failed. The app will still work but with limited NLP features.")
    
    # Create necessary directories if they don't exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo start the AI Tutor:")
    print("  python app.py")
    print("\nThen open your browser to: http://localhost:5000")

if __name__ == "__main__":
    main()
