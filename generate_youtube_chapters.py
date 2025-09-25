#!/usr/bin/env python3
"""
YouTube Chapter Generator
Generates AI-powered chapters for YouTube videos using Whisper transcription.
"""

import argparse
import json
import os
import re
import pathlib
import bisect
import whisper
import openai
import yt_dlp
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/config.env')

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def format_time(seconds):
    """Convert seconds to HH:MM:SS format"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def get_video_info(url):
    """Get video information including title"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiesfrombrowser': ('chrome',),
        'skip_download': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                'id': info.get('id', ''),
                'title': info.get('title', 'Unknown Video'),
                'duration': info.get('duration', 0)
            }
        except Exception as e:
            print(f"Failed to extract video info: {e}")
            # Fallback: use video ID as title
            video_id = get_video_id(url)
            return {
                'id': video_id,
                'title': f"Video_{video_id}",
                'duration': 0
            }

def sanitize_filename(title):
    """Convert video title to safe filename"""
    # Remove invalid filename characters
    import re
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = title.replace(' ', '_')
    # Limit length
    if len(title) > 100:
        title = title[:100]
    return title

def download_audio(video_id, url, video_title=""):
    """Download audio from YouTube video"""
    ydl_opts = {
        'format': 'worst[ext=mp4][acodec!=none]/worst[ext=webm][acodec!=none]/worst',
        'outtmpl': f'{video_id}_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'noplaylist': True,
        'cookiesfrombrowser': ('chrome',),
        'retries': 1,
        'fragment_retries': 1,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio for video {video_id}...")
        ydl.extract_info(url, download=True)
        return f"{video_id}_audio.mp3"

def transcribe_with_whisper(audio_file):
    """Use Whisper to transcribe audio file"""
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    print("Transcribing audio...")
    result = model.transcribe(audio_file)
    
    # Convert Whisper output to our transcript format
    transcript = []
    for segment in result["segments"]:
        transcript.append({
            'start': segment['start'],
            'text': segment['text'].strip()
        })
    
    return transcript

def generate_youtube_titles(transcript, chapters, api_key):
    """Generate optimized YouTube titles based on transcript and chapters"""
    client = openai.OpenAI(api_key=api_key)
    
    # Sample transcript to stay within token limits
    sample_size = min(150, len(transcript))
    step = max(1, len(transcript) // sample_size)
    sampled = transcript[::step]
    
    transcript_text = ""
    for entry in sampled:
        timestamp = format_time(entry['start'])
        transcript_text += f"[{timestamp}] {entry['text']}\n"
    
    # Convert chapters to text
    chapters_text = "\n".join([f"{ch['timestamp']} {ch['title']}" for ch in chapters])
    
    prompt = f"""
Analyze this educational video content and generate 5 high-performing YouTube titles optimized for maximum views and SEO.

CHAPTERS:
{chapters_text}

TRANSCRIPT SAMPLE:
{transcript_text}

Create titles that are:
1. Start with "Step 1 Prep -" for medical content (or "Study Guide -" for other educational content)
2. List the main topics covered, separated by commas
3. Include at least 5 specific topics from the chapters
4. Keep total length under 100 characters for YouTube optimization
5. Use medical terminology when appropriate
6. Make topics sound comprehensive and high-yield

Examples of desired format:
- "Step 1 Prep - Cardiology, Nephrology, Pulmonology, GI, Neurology"
- "Step 1 Prep - Diabetes, Hypertension, Heart Failure, COPD, Stroke"

Focus on listing the actual medical topics/conditions covered in the video. Extract specific topics from the chapter titles.

Output exactly 5 titles, one per line:
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate YouTube titles optimized for educational content engagement and SEO."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.3
        )
        
        titles = response.choices[0].message.content.strip().split('\n')
        # Clean up and limit to 5 titles
        clean_titles = []
        for title in titles:
            title = title.strip()
            if title and not title.startswith('#') and len(title) > 10:
                # Remove numbering if present
                if title.startswith(('1.', '2.', '3.', '4.', '5.')):
                    title = title[2:].strip()
                clean_titles.append(title)
        
        return clean_titles[:5] if clean_titles else ["Complete Guide to [Topic]", "Everything You Need to Know", "Master [Subject] Fast", "Essential [Topic] Review", "Ultimate [Subject] Prep"]
    except Exception as e:
        print(f"Title generation failed: {e}")
        return ["Complete Educational Guide", "Everything You Need to Know", "Master the Basics", "Essential Review", "Ultimate Study Guide"]

def generate_youtube_tags(transcript, chapters, api_key):
    """Generate optimized YouTube tags based on transcript and chapters"""
    client = openai.OpenAI(api_key=api_key)
    
    # Sample transcript to stay within token limits
    sample_size = min(200, len(transcript))
    step = max(1, len(transcript) // sample_size)
    sampled = transcript[::step]
    
    transcript_text = ""
    for entry in sampled:
        timestamp = format_time(entry['start'])
        transcript_text += f"[{timestamp}] {entry['text']}\n"
    
    # Convert chapters to text
    chapters_text = "\n".join([f"{ch['timestamp']} {ch['title']}" for ch in chapters])
    
    prompt = f"""
Analyze this video content and generate 15-20 optimized YouTube tags for maximum SEO discovery.

CHAPTERS:
{chapters_text}

TRANSCRIPT SAMPLE:
{transcript_text}

Generate hashtags that are:
1. Highly relevant to the content
2. Mix of broad and specific terms  
3. Include educational keywords if applicable
4. Optimized for search discovery
5. Include popular exam/study terms if medical/academic content

Output format: #tag1 #tag2 #tag3 (space-separated hashtags)
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate YouTube hashtags optimized for SEO discovery."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Tag generation failed: {e}")
        return "#EducationalContent #Tutorial #Learning"

def generate_ai_chapters(transcript, num_chapters, api_key, structure_type="general"):
    """Use AI to analyze transcript and create intelligent chapters"""
    client = openai.OpenAI(api_key=api_key)
    
    # Sample transcript to stay within token limits
    sample_size = min(400, len(transcript))
    step = max(1, len(transcript) // sample_size)
    sampled = transcript[::step]
    
    transcript_text = ""
    for entry in sampled:
        timestamp = format_time(entry['start'])
        transcript_text += f"[{timestamp}] {entry['text']}\n"
    
    # Get video duration
    duration = transcript[-1]['start'] if transcript else 0
    duration_minutes = duration / 60
    
    if structure_type == "questions":
        prompt = f"""
Create YouTube chapters for a video with {num_chapters-2} questions plus introduction and song.
Output EXACTLY {num_chapters} chapters: Introduction, Questions (use topic names, not "Q1"), Song.
Output strict JSON: {{"chapters":[{{"timestamp":"HH:MM:SS","title":"..."}}, ...]}}
Titles must be concise, <=4 words.
Base timestamps on when topics are first mentioned.

TRANSCRIPT SAMPLE:\n{transcript_text}
"""
    else:
        prompt = f"""
Analyze this educational video transcript and create exactly {num_chapters} chapters.
Rules:
- Each chapter marks when a NEW topic is first introduced
- Timestamps must correspond to when topics are first mentioned
- Titles must be 4 words or less
- Output strict JSON only: {{"chapters":[{{"timestamp":"HH:MM:SS","title":"..."}}, ...]}}
- Start with 00:00:00 Introduction

TRANSCRIPT SAMPLE:\n{transcript_text}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return strict JSON only with the requested number of chapters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.1
        )
        
        response_text = response.choices[0].message.content
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_text = response_text[json_start:json_end]
        chapters_data = json.loads(json_text)
        
        return chapters_data['chapters']
        
    except Exception as e:
        print(f"AI analysis failed: {e}")
        return None

def snap_timestamps_to_transcript(chapters, transcript):
    """Snap chapter timestamps to nearest transcript segment starts"""
    starts = [seg['start'] for seg in transcript]
    aligned = []
    
    for ch in chapters:
        ts = ch.get('timestamp', '00:00:00')
        title = ' '.join(re.findall(r"[A-Za-z0-9'\-]+", ch.get('title', 'Chapter')))[:120].strip()
        
        try:
            h, m, s = map(int, ts.split(':'))
            t = h * 3600 + m * 60 + s
        except:
            t = 0
            
        idx = bisect.bisect_right(starts, t) - 1
        if idx < 0:
            idx = 0
        snap = starts[idx]
        aligned.append((snap, title))
    
    # Remove duplicates and sort
    seen = set()
    unique = []
    for t, title in aligned:
        if t in seen:
            continue
        seen.add(t)
        unique.append((t, title))
    
    unique.sort(key=lambda x: x[0])
    return unique

def main():
    parser = argparse.ArgumentParser(description="Generate YouTube chapters using AI and Whisper")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("chapters", type=int, help="Number of chapters to generate")
    parser.add_argument("--questions", action="store_true", help="Structure for Q&A videos (intro + questions + song)")
    parser.add_argument("--api-key", help="OpenAI API key (optional if set in config.env)")
    
    args = parser.parse_args()
    
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
    
    # Get video information first
    print("Getting video information...")
    video_info = get_video_info(args.url)
    if video_info:
        video_title = video_info['title']
        sanitized_title = sanitize_filename(video_title)
        print(f"Video title: {video_title}")
    else:
        # Fallback to video ID if title extraction fails
        video_title = f"Video_{video_id}"
        sanitized_title = video_id
        print(f"Using video ID as title: {video_title}")
    
    try:
        # Download audio
        audio_file = download_audio(video_id, args.url, video_title)
        
        # Transcribe
        transcript = transcribe_with_whisper(audio_file)
        
        if not transcript:
            print("Failed to generate transcript.")
            return
        
        print(f"Generated transcript with {len(transcript)} segments")
        print(f"Video duration: {format_time(transcript[-1]['start'])}")
        
        # Save transcript
        transcript_file = f"{video_id}_transcript.json"
        with open(transcript_file, 'w') as f:
            json.dump(transcript, f, indent=2)
        print(f"Transcript saved to {transcript_file}")
        
        # Generate chapters with AI
        structure_type = "questions" if args.questions else "general"
        chapters = generate_ai_chapters(transcript, args.chapters, api_key, structure_type)
        
        if chapters:
            # Snap timestamps to transcript segments
            aligned_chapters = snap_timestamps_to_transcript(chapters, transcript)
            
            # Convert to format needed for optimization
            chapters_for_optimization = [{'timestamp': format_time(t), 'title': title} for t, title in aligned_chapters[:args.chapters]]
            
            # Generate YouTube optimizations
            print("🏷️  Generating YouTube tags...")
            youtube_tags = generate_youtube_tags(transcript, chapters_for_optimization, api_key)
            
            print("📝 Generating optimized titles...")
            youtube_titles = generate_youtube_titles(transcript, chapters_for_optimization, api_key)
            
            # Save chapters and tags
            pathlib.Path('chapters').mkdir(exist_ok=True)
            chapters_file = f"chapters/{sanitized_title}.txt"
            
            with open(chapters_file, 'w') as f:
                f.write("SUGGESTED TITLES:\n")
                for i, title in enumerate(youtube_titles, 1):
                    f.write(f"{i}. {title}\n")
                
                f.write("\n\nCHAPTERS:\n")
                for t, title in aligned_chapters[:args.chapters]:
                    f.write(f"{format_time(t)} {title}\n")
                
                f.write(f"\n\nYOUTUBE TAGS:\n{youtube_tags}\n")
            
            print(f"\n✅ Generated {len(aligned_chapters[:args.chapters])} chapters!")
            print(f"💾 Saved to: {chapters_file}")
            
            print("\n📝 Suggested Titles:")
            for i, title in enumerate(youtube_titles, 1):
                print(f"   {i}. {title}")
            
            print("\n📋 Chapter Preview:")
            for t, title in aligned_chapters[:args.chapters]:
                print(f"   {format_time(t)} {title}")
            print(f"\n🏷️ YouTube Tags:\n{youtube_tags}")
        else:
            print("Failed to generate chapters.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup audio file
        if 'audio_file' in locals() and os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"Cleaned up: {audio_file}")

if __name__ == "__main__":
    main()
