#!/usr/bin/env python3
"""
Setup script for YouTube Chapter Generator
Helps with initial project setup and dependency installation.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    if shutil.which('ffmpeg'):
        print("✅ FFmpeg is installed")
        return True
    else:
        print("❌ FFmpeg not found")
        print("   Install FFmpeg:")
        print("   - macOS: brew install ffmpeg")
        print("   - Windows: Download from https://ffmpeg.org/")
        print("   - Linux: sudo apt install ffmpeg")
        return False

def setup_venv():
    """Set up virtual environment."""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install Python dependencies."""
    config_dir = Path("config")
    requirements_file = config_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Requirements file not found")
        return False
    
    # Determine the correct pip path
    if sys.platform == "win32":
        pip_path = Path(".venv/Scripts/pip")
    else:
        pip_path = Path(".venv/bin/pip")
    
    try:
        print("📦 Installing dependencies...")
        subprocess.run([str(pip_path), "install", "-r", str(requirements_file)], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_config():
    """Set up configuration files."""
    config_dir = Path("config")
    example_file = config_dir / "config.env.example"
    config_file = config_dir / "config.env"
    
    if config_file.exists():
        print("✅ Configuration file already exists")
        return True
    
    if not example_file.exists():
        print("❌ Example configuration file not found")
        return False
    
    try:
        # Copy example to actual config
        shutil.copy(example_file, config_file)
        print("✅ Configuration file created")
        print("⚠️  Please edit config/config.env and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration file: {e}")
        return False

def main():
    print("🚀 YouTube Chapter Generator Setup")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Virtual Environment", setup_venv),
        ("Dependencies", install_dependencies),
        ("Configuration", setup_config),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit config/config.env and add your OpenAI API key")
        print("2. Test with: python generate_chapters.py <YouTube_URL> 100")
        print("\nUseful commands:")
        print("- python manage_chapters.py list    # View generated chapters")
        print("- python manage_chapters.py stats   # Show statistics")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
