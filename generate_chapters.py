#!/usr/bin/env python3
"""
Convenient launcher script for the YouTube Chapter Generator.
This script allows you to run the chapter generator from the root directory
without worrying about the internal folder structure.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the enhanced script
    enhanced_script = script_dir / "src" / "main_enhanced.py"
    
    # Check if the enhanced script exists
    if not enhanced_script.exists():
        print(f"Error: Could not find {enhanced_script}")
        print("Please make sure the project structure is intact.")
        return 1
    
    # Pass all command line arguments to the enhanced script
    cmd = [sys.executable, str(enhanced_script)] + sys.argv[1:]
    
    # Change to the script directory so relative paths work
    original_cwd = os.getcwd()
    os.chdir(script_dir)
    
    try:
        # Run the enhanced script
        result = subprocess.run(cmd, cwd=script_dir)
        return result.returncode
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("YouTube Chapter Generator")
        print("=" * 50)
        print()
        print("Usage:")
        print("  python generate_chapters.py <YouTube_URL> <suggested_chapters>")
        print()
        print("Examples:")
        print('  python generate_chapters.py "https://www.youtube.com/watch?v=VIDEO_ID" 100')
        print('  python generate_chapters.py "https://youtu.be/VIDEO_ID" 50 --use-whisper')
        print()
        print("Options:")
        print("  --use-whisper    Force use of Whisper even if subtitles exist")
        print("  --api-key KEY    Use custom OpenAI API key")
        print()
        print("Output:")
        print("  Chapter files are saved in the chapters/ directory")
        print("  Files are automatically organized by content type")
        sys.exit(1)
    
    sys.exit(main())
