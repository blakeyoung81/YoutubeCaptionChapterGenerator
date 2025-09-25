# YouTube Chapter Generator Project

## Overview
A comprehensive tool for automatically generating YouTube chapters, SEO-optimized titles, and hashtags from video transcripts using Whisper transcription and AI analysis. Features both command-line and web interfaces, optimized for educational content, particularly medical education videos like USMLE Step 1 preparation materials.

## Current Architecture

### Core Components
- **generate_youtube_chapters.py** - Main script handling video processing, transcription, and AI analysis
- **app.py** - Flask web interface for user-friendly chapter generation
- **demo.py** - Interactive demo script for easy setup and testing

### Key Features
- **Whisper Transcription** - High-quality audio-to-text conversion
- **AI Chapter Generation** - Content-aware chapter creation using GPT-4
- **SEO Title Optimization** - Generates 5 click-optimized video titles with "Step 1 Prep" format
- **YouTube Tag Generation** - Creates 15-20 relevant hashtags for maximum discoverability
- **Video Title Filenames** - Saves chapters using actual video titles for easy organization
- **Timestamp Alignment** - Precise chapter timing based on transcript segments
- **Web Interface** - Beautiful, responsive web UI with Bootstrap 5
- **Multiple Formats** - Support for general videos and Q&A structured content

## Workflow

1. **Video Info Extraction** - Gets video title and metadata from YouTube
2. **Audio Extraction** - Downloads audio from YouTube using yt-dlp with robust bypass methods
3. **Transcription** - Uses OpenAI Whisper for accurate speech-to-text with timestamps
4. **AI Analysis** - Analyzes transcript to identify topic introduction points
5. **Chapter Generation** - Creates chapters with content-based timing and concise titles
6. **SEO Optimization** - Generates optimized video titles and YouTube hashtags
7. **Timestamp Alignment** - Snaps chapter marks to exact transcript boundaries
8. **Output** - Saves complete SEO package with titles, chapters, and tags using video title filename

## Content Types Supported

### General Educational Videos
- Long-form lectures and tutorials
- Multi-topic educational content
- Medical education and exam prep
- Academic presentations

### Q&A Format Videos
- Structured question-answer sessions
- Introduction + Questions + Song/Outro format
- Educational Q&A series

## Current Implementation

### Completed Features ✅
- Single-script workflow for all video types
- Whisper integration for high-quality transcription
- AI-powered content analysis for intelligent chapter placement
- SEO-optimized title generation (Step 1 Prep format)
- YouTube hashtag generation for maximum discoverability
- Video title-based filename generation
- Timestamp alignment to transcript segments
- Support for both general and Q&A structured videos
- Beautiful responsive web interface with Bootstrap 5
- Real-time progress tracking and copy-to-clipboard features
- Robust YouTube download with bypass techniques for current restrictions
- Automatic cleanup of temporary files
- Comprehensive error handling and retry logic
- Interactive demo script for easy setup

### File Structure
```
├── generate_youtube_chapters.py  # Main processing script
├── app.py                        # Flask web interface
├── demo.py                       # Interactive demo and setup
├── templates/                    # Web interface templates
│   └── index.html               # Main web UI template
├── chapters/                     # Generated chapter files
│   ├── Video_Title.txt          # SEO-optimized outputs with video titles as filenames
├── config/                       # Configuration
│   ├── config.env               # API keys (gitignored)
│   ├── config.env.example       # Configuration template
│   └── requirements.txt         # Python dependencies
├── docs/                        # Documentation
│   └── README.md                # Comprehensive user guide
├── WEB_INTERFACE.md             # Web interface documentation
├── PROJECT_OVERVIEW.md          # This technical overview
└── .gitignore                   # Comprehensive gitignore for temporary files
```

## Usage Examples

### Medical Education (100 chapters)
```bash
python generate_youtube_chapters.py https://youtu.be/iKEcax0auH0 100
```
Generates: `chapters/How_to_ace_the_ACT_-_Lesson_9_Final_Math_Review.txt` with complete SEO package

### Q&A Video (12 chapters: intro + 10 questions + song)
```bash
python generate_youtube_chapters.py https://youtu.be/w5cGwydGRrc 12 --questions
```
Generates: `chapters/USMLE_Step_1__High_Yield_Facts.txt` with:
- 5 optimized "Step 1 Prep - Topic1, Topic2..." titles
- 12 content-aligned chapters
- 15-20 medical education hashtags

## Technical Specifications

### Dependencies
- Python 3.7+
- OpenAI API access (for Whisper and GPT-4)
- yt-dlp for video processing
- FFmpeg for audio handling

### Performance
- Processes videos up to 6+ hours
- Transcript alignment to exact segment boundaries
- Automatic memory management for large files
- Token-efficient AI analysis

### Output Quality
- 4-word maximum chapter titles for YouTube optimization
- Content-based timing (not evenly spaced)
- Professional formatting ready for YouTube descriptions
- Accurate timestamps aligned to speech segments

## Project Evolution

This project has evolved from multiple specialized scripts to a comprehensive YouTube optimization platform featuring:

### v1.0: Basic Chapter Generation
- Single script for chapter creation
- Manual file management

### v2.0: AI-Enhanced Analysis  
- Whisper integration for high-quality transcription
- GPT-4 powered content analysis
- Timestamp alignment improvements

### v3.0: Complete SEO Platform (Current)
- SEO-optimized title generation with "Step 1 Prep" format
- YouTube hashtag generation for maximum discoverability
- Video title-based filename organization
- Beautiful responsive web interface
- Real-time progress tracking
- Robust YouTube download with bypass techniques
- Comprehensive error handling and automatic cleanup

The project now serves as a complete YouTube content optimization platform specifically designed for educational content creators, with particular optimization for medical education materials.