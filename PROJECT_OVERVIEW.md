# YouTube Chapter Generator Project

## Overview
A streamlined tool for automatically generating YouTube chapters from video transcripts using Whisper transcription and AI analysis. Optimized for educational content, particularly medical education videos like USMLE Step 1 preparation materials.

## Current Architecture

### Core Component
- **generate_youtube_chapters.py** - Single, comprehensive script handling the entire workflow

### Key Features
- **Whisper Transcription** - High-quality audio-to-text conversion
- **AI Chapter Generation** - Content-aware chapter creation using GPT-4
- **Timestamp Alignment** - Precise chapter timing based on transcript segments
- **Multiple Formats** - Support for general videos and Q&A structured content

## Workflow

1. **Audio Extraction** - Downloads audio from YouTube using yt-dlp
2. **Transcription** - Uses OpenAI Whisper for accurate speech-to-text
3. **AI Analysis** - Analyzes transcript to identify topic introduction points
4. **Chapter Generation** - Creates chapters with 4-word maximum titles
5. **Timestamp Alignment** - Snaps chapter marks to exact transcript boundaries
6. **Output** - Saves ready-to-use YouTube chapters

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
- Timestamp alignment to transcript segments
- Support for both general and Q&A structured videos
- Automatic cleanup of temporary files
- Error handling and robust processing

### File Structure
```
├── generate_youtube_chapters.py  # Main processing script
├── chapters/                     # Generated chapter files
│   ├── VIDEO_ID_Nchapters.txt   # Final chapter outputs
├── config/                       # Configuration
│   ├── config.env               # API keys
│   └── requirements.txt         # Dependencies
└── docs/                        # Documentation
    └── README.md                # User guide
```

## Usage Examples

### Medical Education (100 chapters)
```bash
python generate_youtube_chapters.py https://youtu.be/iKEcax0auH0 100
```
Generates: `chapters/iKEcax0auH0_100chapters.txt`

### Q&A Video (12 chapters: intro + 10 questions + song)
```bash
python generate_youtube_chapters.py https://youtu.be/vXpvPSYmI4I 12 --questions
```
Generates: `chapters/vXpvPSYmI4I_12chapters.txt`

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

This project has been simplified from multiple specialized scripts to a single, robust solution that handles all use cases while maintaining high quality output and ease of use.