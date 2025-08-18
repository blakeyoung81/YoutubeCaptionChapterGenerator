import argparse
import yt_dlp
import math
import os
import re
import openai
import json
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

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def analyze_transcript_with_ai(transcript, suggested_chapters, api_key):
    """Use AI to analyze transcript and create intelligent chapters"""
    client = openai.OpenAI(api_key=api_key)
    
    # Create a text version of the transcript with timestamps
    # Sample the transcript more intelligently to cover the whole video
    total_entries = len(transcript)
    sample_size = min(500, total_entries)  # Increase sample size for better coverage
    step = max(1, total_entries // sample_size)
    
    transcript_text = ""
    sampled_entries = transcript[::step]  # Sample evenly across the entire video
    
    for entry in sampled_entries:
        timestamp = format_time(entry['start'])
        transcript_text += f"[{timestamp}] {entry['text']}\n"
    
    prompt = f"""Analyze this NBME 26 Step 1 exam review video transcript and create EXACTLY 100 chapter divisions. 

This is a 6+ hour medical education video covering Step 1 topics. You MUST create exactly 100 chapters, no more, no less.

Transcript:
{transcript_text}

You MUST create exactly 100 chapters that:
1. Cover the ENTIRE video duration (6+ hours) with 100 evenly distributed timestamps
2. Have meaningful, professional titles that describe specific medical topics
3. Are evenly spaced across the video timeline (approximately every 3.7 minutes)
4. Focus on specific medical topics, not broad system overviews
5. Use proper medical terminology and clear descriptions

IMPORTANT: You must return EXACTLY 100 chapters. Do not create broad system chapters - create specific topic chapters.

Examples of good titles:
- "Immunodeficiency Disorders"
- "Tumor Lysis Syndrome" 
- "Autoimmune Hemolytic Anemia"
- "Cardiovascular Physiology Basics"
- "Renal Tubular Acidosis"
- "Genetic Inheritance Patterns"

Return your response as a JSON object with EXACTLY 100 chapters:
{{
    "chapters": [
        {{"timestamp": "00:00:00", "title": "Introduction to NBME 26"}},
        {{"timestamp": "00:03:43", "title": "BTK Gene Mutations and Immunodeficiency"}},
        {{"timestamp": "00:07:24", "title": "Tumor Lysis Syndrome and Uric Acid"}},
        ... (continue with exactly 100 chapters)
        {{"timestamp": "06:06:03", "title": "Final Review and Conclusion"}}
    ]
}}

You MUST return exactly 100 chapters covering the entire video duration."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert medical educator who creates clear, professional chapter divisions for medical education videos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,  # Increased for 100 chapters
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
    parser = argparse.ArgumentParser(description="Generate intelligent YouTube chapters from a transcript using AI.")
    parser.add_argument("url", help="The YouTube video URL.")
    parser.add_argument("chapters", type=int, help="Suggested number of chapters (AI will determine optimal number).")
    parser.add_argument("--api-key", help="OpenAI API key for AI analysis (optional if set in config.env).")
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

    try:
        info = get_video_info(video_id)
        duration = info.get('duration', 0)
        video_title = info.get('title', video_id)
        
        # Clean the title for filename use
        clean_title = re.sub(r'[<>:"/\\|?*]', '', video_title)  # Remove invalid filename characters
        clean_title = clean_title.replace(' ', '_')  # Replace spaces with underscores
        clean_title = clean_title[:50]  # Limit length to 50 characters
        
        if not os.path.exists(subtitle_file):
            print("Could not retrieve transcript.")
            return

        transcript = parse_vtt(subtitle_file)
        
        if not transcript:
            print("Could not parse transcript.")
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
            
            # YouTube only allows 100 chapters maximum
            # Divide the ENTIRE video into exactly 100 chapters
            target_chapters = 100
            chapter_length = duration / target_chapters
            
            chapters = []
            chapters.append("00:00:00 Introduction")

            for i in range(1, target_chapters):
                chapter_time = i * chapter_length
                closest_entry = min(transcript, key=lambda x: abs(x['start'] - chapter_time))
                timestamp = format_time(closest_entry['start'])
                text = closest_entry['text'].strip()[:100]  # Get more text for better context
                chapters.append(f"{timestamp} {text}")
            
            print(f"Generated {len(chapters)} time-based chapters to cover entire video (YouTube limit: 100)")

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
        if os.path.exists(subtitle_file):
            os.remove(subtitle_file)


if __name__ == "__main__":
    main()
