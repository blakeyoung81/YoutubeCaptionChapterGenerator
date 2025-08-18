# YouTube Chapter Generator - Project Overview

## 🎯 Purpose
This project automatically generates intelligent chapters for YouTube videos using AI analysis. It's particularly useful for educational content, long-form videos, and content creation.

## 📁 Project Structure

```
Youtube Captions/
├── 📁 src/                       # Source Code
│   ├── main.py                   # Original script (subtitles only)
│   └── main_enhanced.py          # Enhanced script with Whisper
├── 📁 config/                    # Configuration
│   ├── config.env                # Your API keys (PRIVATE)
│   ├── config.env.example        # Configuration template
│   └── requirements.txt          # Python dependencies
├── 📁 chapters/                  # Generated Chapters (Auto-organized)
│   ├── 📁 nbme_26/               # NBME 26 exam content
│   ├── 📁 nbme_27/               # NBME 27 exam content  
│   ├── 📁 nbme_29/               # NBME 29 exam content
│   └── 📁 other/                 # Other video types
├── 📁 docs/                      # Documentation
│   └── README.md                 # Detailed documentation
├── 📁 .venv/                     # Python virtual environment
├── generate_chapters.py          # 🚀 Main launcher script
└── PROJECT_OVERVIEW.md           # This file
```

## 🚀 Quick Start

### 1. Simple Usage (Recommended)
```bash
python generate_chapters.py "https://www.youtube.com/watch?v=VIDEO_ID" 100
```

### 2. Advanced Usage
```bash
# Force Whisper transcription
python generate_chapters.py "https://youtu.be/VIDEO_ID" 50 --use-whisper

# Use custom API key
python generate_chapters.py "https://youtu.be/VIDEO_ID" 75 --api-key YOUR_KEY
```

## 🔧 How It Works

1. **Input**: YouTube URL + suggested chapter count
2. **Subtitle Check**: Tries to download existing subtitles
3. **Whisper Fallback**: Downloads audio and transcribes if no subtitles
4. **AI Analysis**: Uses OpenAI GPT to create intelligent chapters
5. **Output**: Saves organized chapter files ready for YouTube

## 📊 Generated Content Examples

### Medical Education (NBME Content)
```
00:00:00 Introduction
00:07:39 Metabolic Pathways
00:13:27 Medical Treatment Considerations
00:19:23 Gout and Crystal Formation
00:25:13 Anemia of Chronic Disease
```

### Educational Content (ACT Prep)
```
00:00:00 Introduction
00:02:07 ACT English Section Tips
00:05:06 Comma Rules and Independent Clauses
00:10:59 Prepositions and Sentence Structure
```

## 🎯 Use Cases

- **📚 Educational Content**: Medical school, test prep, tutorials
- **🎬 Long-form Videos**: Podcasts, lectures, documentaries
- **✂️ Content Creation**: YouTube uploads, video editing
- **🔍 Research**: Quick navigation to specific topics

## 🔑 Key Features

- **🤖 AI-Powered**: Intelligent topic detection and naming
- **🎵 Audio Processing**: Works even without subtitles
- **📂 Auto-Organization**: Categorizes outputs by content type
- **⚡ Smart Fallbacks**: Multiple backup methods ensure reliability
- **🎨 Clean Output**: YouTube-ready chapter format

## 📈 Performance

- **Speed**: 2-5 minutes for typical 20-30 minute videos
- **Accuracy**: High-quality chapters using GPT analysis
- **Reliability**: Multiple fallback methods prevent failures
- **Efficiency**: Automatic cleanup of temporary files

## 🛠️ Maintenance

### Adding New Content Categories
1. Create new folder in `chapters/` directory
2. Modify auto-organization logic if needed

### Updating Dependencies
```bash
pip install -r config/requirements.txt --upgrade
```

### Backup Important Files
- `config/config.env` (your API keys)
- `chapters/` directory (your generated content)

## 🚨 Important Notes

- **API Costs**: Uses OpenAI tokens (typically $0.01-0.05 per video)
- **Processing Time**: Longer videos take more time to process
- **Audio Quality**: Results depend on original video audio quality
- **Privacy**: Keep your `config/config.env` file secure

## 📞 Support

- Check `docs/README.md` for detailed documentation
- Review error messages for troubleshooting hints
- Ensure FFmpeg is installed for audio processing
- Verify OpenAI API key is correctly configured

---

**Last Updated**: Generated automatically during project organization
**Version**: Enhanced with Whisper fallback support
