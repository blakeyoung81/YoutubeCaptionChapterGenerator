# YouTube Chapter Generator

This tool automatically generates YouTube chapters, optimized titles, and SEO tags from video transcripts using Whisper transcription and AI analysis. It creates precise, content-based chapter divisions and click-worthy titles for educational videos.

## Features

- **Whisper Transcription**: High-quality audio transcription using OpenAI Whisper
- **AI-Powered Chapters**: Intelligent chapter generation using GPT-4 models
- **Optimized Video Titles**: 5 high-performing title suggestions designed for maximum clicks
- **YouTube SEO Tags**: Automatically generates 15-20 optimized hashtags for better video discovery
- **Content-Based Timing**: Timestamps aligned to actual topic introduction points
- **Multiple Formats**: Support for general videos and Q&A structured content
- **4-Word Titles**: Concise, YouTube-optimized chapter titles

## Quick Start

### Option 1: Web Interface (Recommended)

1. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r config/requirements.txt
   ```

2. **Configure API Key**
   Add your OpenAI API key to `config/config.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start Web Interface**
   ```bash
   python app.py
   ```
   Then open http://localhost:5000 in your browser

### Option 2: Command Line

```bash
# General educational video (100 chapters)
python generate_youtube_chapters.py https://youtu.be/VIDEO_ID 100

# Q&A video with questions + song structure
python generate_youtube_chapters.py https://youtu.be/VIDEO_ID 12 --questions
```

## How It Works

1. **Download**: Extracts audio from YouTube video
2. **Transcribe**: Uses Whisper to create accurate transcript with timestamps
3. **Analyze**: AI identifies topic introduction points and creates descriptions
4. **Optimize**: Generates click-worthy video titles and SEO hashtags
5. **Align**: Snaps chapter timestamps to exact transcript segment boundaries
6. **Output**: Saves titles, chapters and tags ready for YouTube

## File Structure

```
├── app.py                        # Web interface (Flask)
├── generate_youtube_chapters.py  # Command line script
├── templates/                    # Web interface templates
├── chapters/                     # Generated chapter files
├── config/                       # Configuration files
│   ├── config.env               # API keys
│   └── requirements.txt         # Dependencies
├── docs/                         # Documentation
└── WEB_INTERFACE.md             # Web interface guide
```

## Web Interface Features

The web interface provides a beautiful, user-friendly way to generate chapters:

- **Modern Design**: Clean, responsive interface with gradients
- **Real-time Processing**: Visual progress indicators
- **Title Suggestions**: 5 click-optimized video titles with one-click copying
- **Tag Management**: Display and copy YouTube SEO hashtags
- **Easy Export**: Download files or copy titles/chapters/tags to clipboard
- **Mobile Friendly**: Works on all devices
- **Error Handling**: Clear validation and error messages

![Web Interface](https://via.placeholder.com/800x400/667eea/ffffff?text=Beautiful+Web+Interface)

## Usage Examples

### Medical Education Video (Long-form)
```bash
python generate_youtube_chapters.py https://youtu.be/iKEcax0auH0 100
```

**Output:** `chapters/How_to_ace_the_ACT_-_Lesson_9_Final_Math_Review.txt`
```
SUGGESTED TITLES:
1. "Master Cardiovascular Physiology: Complete USMLE Step 1 Guide!"
2. "Heart & Blood Pressure Secrets: Essential Medical Knowledge!"
3. "Cardiology Made Simple: Everything for Medical Students!"
4. "USMLE Step 1 Cardiology: 100 Key Topics in 6 Hours!"
5. "Complete Heart Physiology: From Basics to Expert Level!"

CHAPTERS:
00:00:00 Introduction
00:03:45 Cardiovascular Physiology Basics
00:07:22 Heart Rate Regulation
00:11:55 Blood Pressure Mechanisms
...
06:35:08 Closing Remarks

YOUTUBE TAGS:
#MedicalEducation #Cardiology #Physiology #USMLE #Step1Prep #HeartPhysiology #BloodPressure #MedicalStudents #HealthEducation #ExamPrep #ClinicalMedicine #MedicalKnowledge #CardiologyReview #MedicalStudy #HealthScience #MedicalTraining #HeartRate #BloodFlow #MedicalSchool #EducationalContent
```

### Q&A Video with Song
```bash
python generate_youtube_chapters.py https://youtu.be/vXpvPSYmI4I 12 --questions
```

**Output:** `chapters/USMLE_Step_1__High_Yield_Facts.txt`
```
SUGGESTED TITLES:
1. "10 Essential Questions Every Student Must Know!"
2. "Master Key Concepts: Q&A Study Session + Music!"
3. "Ultimate Study Guide: Questions & Answers Explained!"
4. "Test Your Knowledge: 10 Must-Know Q&A + Song!"
5. "Complete Review: Essential Questions for Success!"

CHAPTERS:
00:00:00 Introduction
00:01:30 Question One Topic
00:04:15 Question Two Topic
...
00:28:45 Song

YOUTUBE TAGS:
#QuestionAnswer #QAVideo #EducationalContent #LearningVideo #StudyGuide #ExamPrep #Educational #Tutorial #Knowledge #StudentLife #Study #Learning #AcademicContent #QuizVideo #TestPrep #StudyTips #Educational #KnowledgeBase #StudyMaterial #LearningTips
```

## Requirements

- Python 3.7+
- FFmpeg (for audio processing)
- OpenAI API key
- Internet connection

## Installation

1. **Install FFmpeg**
   - macOS: `brew install ffmpeg`
   - Windows: Download from ffmpeg.org
   - Linux: `sudo apt install ffmpeg`

2. **Install Python Dependencies**
   ```bash
   pip install -r config/requirements.txt
   ```

3. **Setup Configuration**
   ```bash
   cp config/config.env.example config/config.env
   # Edit config/config.env and add your OpenAI API key
   ```

## Use Cases

- **Medical Education**: USMLE Step 1 prep videos with 100+ topics
- **Academic Content**: Lecture recordings with multiple subjects
- **Q&A Videos**: Structured question-answer format with intro/outro
- **Long-form Educational**: Multi-hour comprehensive reviews

## Generated Files

- `VIDEO_ID_audio.mp3`: Downloaded audio (automatically cleaned up)
- `VIDEO_ID_transcript.json`: Whisper transcription with timestamps (automatically cleaned up)
- `chapters/Video_Title.txt`: Complete SEO optimization package with:
  - 5 optimized video titles in "Step 1 Prep - Topic1, Topic2..." format
  - Content-aligned chapter timestamps and titles
  - 15-20 YouTube hashtags for maximum discoverability

## Advanced Options

```bash
# Custom API key
python generate_youtube_chapters.py URL COUNT --api-key YOUR_KEY

# Q&A structure (intro + questions + song)
python generate_youtube_chapters.py URL COUNT --questions
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg for your OS
2. **API key error**: Check `config/config.env` has valid OpenAI API key
3. **Memory issues**: Use shorter videos or reduce chapter count
4. **Private videos**: Ensure video is public or unlisted

### Performance Tips

- Whisper uses "base" model for speed/accuracy balance
- AI analysis samples transcript to stay within token limits
- Audio files are automatically cleaned up after processing

## Limitations

- English content only (Whisper limitation)
- Requires OpenAI API credits
- Processing time scales with video length
- Maximum ~6 hour videos (due to memory constraints)

## License

MIT License - See LICENSE file for details