#!/usr/bin/env python3
"""
YouTube Chapter Generator Web Interface
Flask web app for generating YouTube chapters with AI
"""

import os
import json
import subprocess
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/config.env')

app = Flask(__name__)

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def validate_youtube_url(url):
    """Validate YouTube URL format"""
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        if re.match(pattern, url):
            return True
    return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_chapters():
    """API endpoint to generate chapters"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        chapters = data.get('chapters', 10)
        questions_mode = data.get('questions', False)
        
        # Validation
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not validate_youtube_url(url):
            return jsonify({'error': 'Invalid YouTube URL format'}), 400
        
        if not isinstance(chapters, int) or chapters < 1 or chapters > 200:
            return jsonify({'error': 'Chapters must be between 1 and 200'}), 400
        
        # Check if API key exists
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        video_id = get_video_id(url)
        if not video_id:
            return jsonify({'error': 'Could not extract video ID'}), 400
        
        # Build command
        cmd = [
            'python', 'generate_youtube_chapters.py',
            url, str(chapters)
        ]
        
        if questions_mode:
            cmd.append('--questions')
        
        # Execute chapter generation
        result = subprocess.run(
            cmd,
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )
        
        if result.returncode != 0:
            return jsonify({
                'error': f'Chapter generation failed: {result.stderr}'
            }), 500
        
        # Find generated chapter file
        chapters_dir = Path('chapters')
        chapter_files = list(chapters_dir.glob(f'{video_id}_*chapters.txt'))
        
        if not chapter_files:
            return jsonify({'error': 'No chapter file generated'}), 500
        
        # Read the generated chapters
        chapter_file = chapter_files[0]
        with open(chapter_file, 'r') as f:
            full_content = f.read().strip()
        
        # Split content into sections
        titles = None
        chapters_content = full_content
        tags = None
        
        # Extract titles if present
        if full_content.startswith('SUGGESTED TITLES:\n'):
            if '\n\nCHAPTERS:\n' in full_content:
                title_section, rest = full_content.split('\n\nCHAPTERS:\n', 1)
                title_lines = title_section.replace('SUGGESTED TITLES:\n', '').strip().split('\n')
                titles = [line.strip() for line in title_lines if line.strip()]
                chapters_content = rest
            
        # Extract tags if present
        if '\n\nYOUTUBE TAGS:\n' in chapters_content:
            chapters_content, tags = chapters_content.split('\n\nYOUTUBE TAGS:\n', 1)
            tags = tags.strip()
        
        # Remove "CHAPTERS:" header if present
        if chapters_content.startswith('CHAPTERS:\n'):
            chapters_content = chapters_content.replace('CHAPTERS:\n', '', 1)
        
        # Parse chapters into structured format
        chapter_lines = chapters_content.split('\n')
        parsed_chapters = []
        for line in chapter_lines:
            if line.strip():
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    timestamp, title = parts
                    parsed_chapters.append({
                        'timestamp': timestamp,
                        'title': title
                    })
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'chapters': parsed_chapters,
            'total_chapters': len(parsed_chapters),
            'titles': titles,
            'tags': tags,
            'raw_content': full_content
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Generation timed out (max 30 minutes)'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/download/<video_id>')
def download_chapters(video_id):
    """Download generated chapters file"""
    try:
        chapters_dir = Path('chapters')
        chapter_files = list(chapters_dir.glob(f'{video_id}_*chapters.txt'))
        
        if not chapter_files:
            return jsonify({'error': 'Chapter file not found'}), 404
        
        return send_file(
            chapter_files[0],
            as_attachment=True,
            download_name=f'{video_id}_chapters.txt'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure chapters directory exists
    Path('chapters').mkdir(exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
