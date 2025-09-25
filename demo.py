#!/usr/bin/env python3
"""
Demo script to test the YouTube Chapter Generator Web Interface
"""

import subprocess
import time
import webbrowser
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if config exists
    config_path = Path('config/config.env')
    if not config_path.exists():
        print("❌ config/config.env not found")
        print("📝 Please copy config/config.env.example to config/config.env and add your OpenAI API key")
        return False
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv('config/config.env')
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.strip() == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured")
        print("📝 Please add your actual OpenAI API key to config/config.env")
        return False
    
    print("✅ Configuration looks good!")
    return True

def start_web_interface():
    """Start the web interface"""
    print("\n🚀 Starting web interface...")
    print("📱 The interface will be available at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        # Start Flask app
        subprocess.run(['python', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting web interface: {e}")

def main():
    print("🎬 YouTube Chapter Generator Demo")
    print("=" * 50)
    
    if not check_requirements():
        print("\n🛠️  Please fix the requirements above and run the demo again.")
        return
    
    print("\n🌟 Ready to generate chapters!")
    print("\nOptions:")
    print("1. Start Web Interface (Recommended)")
    print("2. Command Line Example")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            # Try to open browser automatically
            try:
                print("\n🌐 Opening browser...")
                webbrowser.open('http://localhost:5000')
                time.sleep(2)
            except:
                pass
            start_web_interface()
            break
        elif choice == '2':
            print("\n📋 Command Line Examples:")
            print("# Medical education video (100 chapters)")
            print("python generate_youtube_chapters.py https://youtu.be/iKEcax0auH0 100")
            print("\n# Q&A video (12 chapters: intro + 10 questions + song)")
            print("python generate_youtube_chapters.py https://youtu.be/vXpvPSYmI4I 12 --questions")
            break
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
