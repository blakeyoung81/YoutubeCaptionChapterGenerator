import argparse
import yt_dlp
import math
import os
import re
import openai
import json
import whisper
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../config/config.env')

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
    model = whisper.load_model("base")  # You can use "tiny", "base", "small", "medium", "large"
    
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

def analyze_transcript_with_ai(transcript, suggested_chapters, api_key):
    """Use AI to analyze transcript and create intelligent chapters"""
    client = openai.OpenAI(api_key=api_key)
    
    # Create a text version of the transcript with timestamps
    # Reduce sample size to stay within token limits
    total_entries = len(transcript)
    sample_size = min(200, total_entries)  # Reduced from 500 to stay within limits
    step = max(1, total_entries // sample_size)
    
    transcript_text = ""
    sampled_entries = transcript[::step]  # Sample evenly across the entire video
    
    for entry in sampled_entries:
        timestamp = format_time(entry['start'])
        transcript_text += f"[{timestamp}] {entry['text']}\n"
    
    # Get video duration for better chapter distribution
    if transcript:
        duration = transcript[-1]['start']
        duration_hours = duration / 3600
    else:
        duration_hours = 1  # Default fallback
    
    # Calculate appropriate number of chapters based on duration
    target_chapters = min(100, max(5, int(duration / 180)))  # 1 chapter per 3 minutes, max 100
    
    prompt = f"""Analyze this video transcript and create exactly {target_chapters} intelligent chapter divisions. 

This video is approximately {duration_hours:.1f} hours long. Create exactly {target_chapters} chapters that cover the entire content.

Transcript sample:
{transcript_text}

Create exactly {target_chapters} chapters that:
1. Cover the ENTIRE video duration with evenly distributed timestamps
2. Have meaningful, professional titles that describe specific topics
3. Are evenly spaced across the video timeline
4. Focus on specific topics, not broad overviews
5. Use clear, descriptive titles

IMPORTANT: You must return exactly {target_chapters} chapters, no more, no less.

Return your response as a JSON object with exactly {target_chapters} chapters:
{{
    "chapters": [
        {{"timestamp": "00:00:00", "title": "Introduction"}},
        {{"timestamp": "00:03:43", "title": "Topic 1"}},
        ... (continue with exactly {target_chapters} chapters)
    ]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert educator who creates clear, professional chapter divisions for educational videos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,  # Reduced from 4000 to stay within limits
            temperature=0.2
        )
        
        # Parse the JSON response
        response_text = response.choices[0].message.content
        # Extract JSON from the response (in case there's extra text)
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_text = response_text[json_start:json_end]
        
        chapters_data = json.loads(json_text)
        return chapters_data['chapters']
        
    except Exception as e:
        print(f"AI analysis failed: {e}")
        print("Falling back to time-based chapters...")
        return None

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
            
            # More robust time parsing
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
            # Clean up HTML-like tags from the text
            text = re.sub(r'<[^>]+>', '', text)
            transcript.append({'start': seconds, 'text': text})
            
    return transcript

def main():
    parser = argparse.ArgumentParser(description="Generate intelligent YouTube chapters from transcript or audio using AI.")
    parser.add_argument("url", help="The YouTube video URL.")
    parser.add_argument("chapters", type=int, help="Suggested number of chapters (AI will determine optimal number).")
    parser.add_argument("--api-key", help="OpenAI API key for AI analysis (optional if set in config.env).")
    parser.add_argument("--use-whisper", action="store_true", help="Force use of Whisper even if subtitles exist.")
    args = parser.parse_args()
    
    # Get API key from environment variable or command line argument
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Error: OpenAI API key not found!")
        print("Please either:")
        print("1. Set OPENAI_API_KEY in config.env file, or")
        print("2. Use --api-key argument")
        print("\nTo set up config.env:")
        print("1. Copy config.env.example to config.env")
        print("2. Add your OpenAI API key to config.env")
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
        
        # Clean the title for filename use
        clean_title = re.sub(r'[<>:"/\\|?*]', '', video_title)  # Remove invalid filename characters
        clean_title = clean_title.replace(' ', '_')  # Replace spaces with underscores
        clean_title = clean_title[:50]  # Limit length to 50 characters
        
        # Try to get transcript from subtitles first
        if not args.use_whisper and os.path.exists(subtitle_file):
            print("Found subtitles, parsing transcript...")
            transcript = parse_vtt(subtitle_file)
        
        # If no subtitles or forced Whisper, download audio and transcribe
        if not transcript or args.use_whisper:
            print("No subtitles found or Whisper forced. Downloading audio and using Whisper...")
            audio_file, audio_duration = download_audio(video_id)
            
            if os.path.exists(audio_file):
                transcript = transcribe_with_whisper(audio_file)
                
                # Clean up audio file
                os.remove(audio_file)
            else:
                print("Failed to download audio file.")
                return
        
        if not transcript:
            print("Could not generate transcript.")
            return

        print(f"Analyzing transcript for '{video_title}' with AI to create intelligent chapters...")
        
        # Use AI to analyze transcript and create intelligent chapters
        ai_chapters = analyze_transcript_with_ai(transcript, args.chapters, api_key)
        
        if ai_chapters:
            chapters = []
            for chapter in ai_chapters:
                chapters.append(f"{chapter['timestamp']} {chapter['title']}")
        else:
            # Fallback to time-based chapters if AI fails
            print("Using fallback time-based chapters...")
            print(f"Video duration: {duration} seconds ({duration/3600:.2f} hours)")
            
            # Create time-based chapters
            target_chapters = min(100, max(10, int(duration / 180)))  # 1 chapter per 3 minutes, max 100
            chapter_length = duration / target_chapters
            
            chapters = []
            chapters.append("00:00:00 Introduction")

            for i in range(1, target_chapters):
                chapter_time = i * chapter_length
                closest_entry = min(transcript, key=lambda x: abs(x['start'] - chapter_time))
                timestamp = format_time(closest_entry['start'])
                text = closest_entry['text'].strip()[:100]  # Get more text for better context
                chapters.append(f"{timestamp} {text}")
            
            print(f"Generated {len(chapters)} time-based chapters")

        # Generate output filename with video title
        output_file = f"{clean_title}_chapters.txt"
        
        # Write chapters to file
        with open(output_file, 'w') as f:
            for chapter in chapters:
                f.write(chapter + '\n')
        
        print(f"Generated {len(chapters)} intelligent chapters and saved to: {output_file}")
        print("\nPreview of chapters:")
        for chapter in chapters:
            print(chapter)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up subtitle file if it exists
        if os.path.exists(subtitle_file):
            os.remove(subtitle_file)

if __name__ == "__main__":
    main()
