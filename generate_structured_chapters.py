#!/usr/bin/env python3
"""
Specialized YouTube Chapter Generator for structured content like Q&A videos.
Allows custom chapter structures (e.g., Introduction + Questions + Closing).
"""

import argparse
import yt_dlp
import os
import re
import openai
import json
import whisper
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv('config/config.env')

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def get_video_info(video_id):
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'writeautomaticsub': True,
        'outtmpl': f'{video_id}.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=True)
        return info

def download_audio(video_id):
    """Download audio from YouTube video for Whisper processing"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{video_id}_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio for video {video_id}...")
        info = ydl.extract_info(video_id, download=True)
        audio_file = f"{video_id}_audio.mp3"
        return audio_file, info.get('duration', 0)

def transcribe_with_whisper(audio_file):
    """Use Whisper to transcribe audio file"""
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    print("Transcribing audio with Whisper...")
    result = model.transcribe(audio_file)
    
    # Convert Whisper output to our transcript format
    transcript = []
    for segment in result["segments"]:
        transcript.append({
            'start': segment['start'],
            'text': segment['text'].strip()
        })
    
    return transcript

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def analyze_structured_transcript(transcript, structure, api_key):
    """Use AI to analyze transcript and create structured chapters"""
    client = openai.OpenAI(api_key=api_key)
    
    # Create a text version of the transcript with timestamps
    total_entries = len(transcript)
    sample_size = min(300, total_entries)  # Larger sample for better question detection
    step = max(1, total_entries // sample_size)
    
    transcript_text = ""
    sampled_entries = transcript[::step]
    
    for entry in sampled_entries:
        timestamp = format_time(entry['start'])
        transcript_text += f"[{timestamp}] {entry['text']}\n"
    
    # Get video duration
    if transcript:
        duration = transcript[-1]['start']
        duration_minutes = duration / 60
    else:
        duration_minutes = 30  # Default fallback
    
    prompt = f"""Analyze this educational video transcript and create EXACTLY {structure['total']} chapters with the specified structure.

This is a {duration_minutes:.1f}-minute educational video. I need you to identify:

REQUIRED STRUCTURE:
- 1 Introduction chapter
- {structure['questions']} Question chapters (Q1, Q2, etc.) - each covering a specific topic/question
- 1 Closing remarks chapter

Total: {structure['total']} chapters exactly.

VIDEO TRANSCRIPT:
{transcript_text}

INSTRUCTIONS:
1. Find the introduction section (usually at the beginning)
2. Identify {structure['questions']} distinct questions/topics being covered
3. Find the closing/conclusion section
4. Create meaningful titles for each question based on the actual content
5. Ensure timestamps cover the ENTIRE video duration

EXAMPLE FORMAT for questions:
- "Q1: Oxaloacetate vs Acetyl CoA Metabolism"
- "Q2: Enzyme Kinetics and Inhibition"
- etc.

Return your response as a JSON object with exactly {structure['total']} chapters:
{{
    "chapters": [
        {{"timestamp": "00:00:00", "title": "Introduction"}},
        {{"timestamp": "00:02:30", "title": "Q1: [Specific Topic from Content]"}},
        {{"timestamp": "00:05:15", "title": "Q2: [Specific Topic from Content]"}},
        ...
        {{"timestamp": "{format_time(duration-60)}", "title": "Closing Remarks"}}
    ]
}}

CRITICAL: You must return exactly {structure['total']} chapters. Base question titles on the actual content discussed in the transcript."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using more capable model for better analysis
            messages=[
                {"role": "system", "content": "You are an expert educational content analyzer who creates precise chapter divisions for structured educational videos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.1  # Lower temperature for more consistent results
        )
        
        # Parse the JSON response
        response_text = response.choices[0].message.content
        print(f"AI Response: {response_text[:200]}...")  # Debug output
        
        # Extract JSON from the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON found in response")
        
        json_text = response_text[json_start:json_end]
        chapters_data = json.loads(json_text)
        
        if 'chapters' not in chapters_data:
            raise ValueError("No 'chapters' key found in response")
        
        chapters = chapters_data['chapters']
        if len(chapters) != structure['total']:
            print(f"Warning: Expected {structure['total']} chapters, got {len(chapters)}")
        
        return chapters
        
    except Exception as e:
        print(f"AI analysis failed: {e}")
        print("Falling back to structured time-based chapters...")
        return create_fallback_structured_chapters(transcript, structure)

def create_fallback_structured_chapters(transcript, structure):
    """Create fallback structured chapters if AI fails"""
    if not transcript:
        return []
    
    duration = transcript[-1]['start']
    chapters = []
    
    # Introduction (first 5% or 2 minutes, whichever is smaller)
    intro_end = min(duration * 0.05, 120)
    chapters.append({"timestamp": "00:00:00", "title": "Introduction"})
    
    # Questions (distribute remaining time minus closing)
    closing_start = max(duration - 60, duration * 0.95)  # Last minute or 5%
    question_duration = closing_start - intro_end
    question_length = question_duration / structure['questions']
    
    for i in range(structure['questions']):
        q_start = intro_end + (i * question_length)
        timestamp = format_time(q_start)
        chapters.append({"timestamp": timestamp, "title": f"Q{i+1}: Topic {i+1}"})
    
    # Closing remarks
    chapters.append({"timestamp": format_time(closing_start), "title": "Closing Remarks"})
    
    return chapters

def parse_vtt(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    transcript = []
    cues = re.split(r'\n\n', content.strip())
    
    for cue in cues:
        lines = cue.strip().split('\n')
        if len(lines) >= 2 and '-->' in lines[0]:
            time_line = lines[0]
            text_lines = lines[1:]
            
            start_time_str = time_line.split(' --> ')[0]
            
            # Parse time
            parts = start_time_str.split(':')
            if len(parts) == 3:
                h, m, s_ms = parts
                s, ms = s_ms.split('.')
                seconds = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
            elif len(parts) == 2:
                m, s_ms = parts
                s, ms = s_ms.split('.')
                seconds = int(m) * 60 + int(s) + int(ms) / 1000
            else:
                continue

            text = ' '.join(text_lines)
            text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
            transcript.append({'start': seconds, 'text': text})
            
    return transcript

def main():
    parser = argparse.ArgumentParser(description="Generate structured YouTube chapters (Introduction + Questions + Closing)")
    parser.add_argument("url", help="The YouTube video URL")
    parser.add_argument("questions", type=int, help="Number of questions/topics to identify")
    parser.add_argument("--api-key", help="OpenAI API key (optional if set in config.env)")
    parser.add_argument("--use-whisper", action="store_true", help="Force use of Whisper")
    
    args = parser.parse_args()
    
    # Calculate structure
    structure = {
        'questions': args.questions,
        'total': args.questions + 2  # +1 for intro, +1 for closing
    }
    
    # Get API key
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OpenAI API key not found!")
        print("Set OPENAI_API_KEY in config/config.env or use --api-key")
        return

    video_id = get_video_id(args.url)
    if not video_id:
        print("Invalid YouTube URL.")
        return

    subtitle_file = f"{video_id}.en.vtt"
    transcript = None

    try:
        info = get_video_info(video_id)
        duration = info.get('duration', 0)
        video_title = info.get('title', video_id)
        
        # Clean title for filename
        clean_title = re.sub(r'[<>:"/\\|?*]', '', video_title)
        clean_title = clean_title.replace(' ', '_')[:50]
        
        # Try subtitles first
        if not args.use_whisper and os.path.exists(subtitle_file):
            print("Found subtitles, parsing transcript...")
            transcript = parse_vtt(subtitle_file)
        
        # Fallback to Whisper
        if not transcript or args.use_whisper:
            print("Using Whisper for transcription...")
            audio_file, audio_duration = download_audio(video_id)
            
            if os.path.exists(audio_file):
                transcript = transcribe_with_whisper(audio_file)
                os.remove(audio_file)  # Cleanup
            else:
                print("Failed to download audio.")
                return
        
        if not transcript:
            print("Could not generate transcript.")
            return

        print(f"Analyzing '{video_title}' for structured chapters...")
        print(f"Structure: Introduction + {structure['questions']} Questions + Closing = {structure['total']} chapters")
        
        # Analyze with AI
        chapters = analyze_structured_transcript(transcript, structure, api_key)
        
        if chapters:
            # Format chapters for output
            chapter_lines = []
            for chapter in chapters:
                chapter_lines.append(f"{chapter['timestamp']} {chapter['title']}")
            
            # Save to file
            output_file = f"chapters/{clean_title}_structured_chapters.txt"
            
            # Ensure chapters directory exists
            Path("chapters").mkdir(exist_ok=True)
            
            with open(output_file, 'w') as f:
                for line in chapter_lines:
                    f.write(line + '\n')
            
            print(f"\n✅ Generated {len(chapters)} structured chapters!")
            print(f"💾 Saved to: {output_file}")
            print("\n📋 Chapter Preview:")
            for line in chapter_lines:
                print(f"   {line}")
        else:
            print("Failed to generate structured chapters.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup
        if os.path.exists(subtitle_file):
            os.remove(subtitle_file)

if __name__ == "__main__":
    main()
