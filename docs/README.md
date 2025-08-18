# YouTube Chapter Generator with Whisper Fallback

This enhanced tool automatically generates intelligent chapters for YouTube videos using AI analysis. When subtitles aren't available, it falls back to downloading audio and using OpenAI's Whisper for transcription.

## Features

- **Automatic Subtitle Detection**: First tries to use existing YouTube subtitles
- **Whisper Fallback**: Downloads audio and transcribes with Whisper when subtitles aren't available
- **AI-Powered Chapters**: Uses OpenAI GPT to create intelligent, topic-based chapters
- **Smart Fallback**: Falls back to time-based chapters if AI analysis fails
- **Multiple Output Formats**: Generates chapters in standard YouTube format
- **Organized Output**: Automatically categorizes chapter files by content type

## Project Structure

```
Youtube Captions/
├── src/                          # Source code
│   ├── main.py                   # Original script (subtitles only)
│   └── main_enhanced.py          # Enhanced script with Whisper
├── config/                       # Configuration files
│   ├── config.env                # Your API keys (keep private)
│   ├── config.env.example        # Template for configuration
│   └── requirements.txt          # Python dependencies
├── chapters/                     # Generated chapter files
│   ├── nbme_26/                  # NBME 26 related chapters
│   ├── nbme_27/                  # NBME 27 related chapters
│   ├── nbme_29/                  # NBME 29 related chapters
│   └── other/                    # Other video chapters
├── docs/                         # Documentation
│   └── README.md                 # This file
└── .venv/                        # Virtual environment (auto-created)
```

## Requirements

- Python 3.7+
- FFmpeg (for audio processing)
- OpenAI API key
- Internet connection

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r config/requirements.txt
   ```
3. **Set up your OpenAI API key**:
   - Copy `config/config.env.example` to `config/config.env`
   - Add your OpenAI API key to `config/config.env`

## Usage

### Basic Usage

```bash
python src/main_enhanced.py "https://www.youtube.com/watch?v=VIDEO_ID" 100
```

### Force Whisper (Even if subtitles exist)

```bash
python src/main_enhanced.py "https://www.youtube.com/watch?v=VIDEO_ID" 100 --use-whisper
```

### With Custom API Key

```bash
python src/main_enhanced.py "https://www.youtube.com/watch?v=VIDEO_ID" 100 --api-key YOUR_API_KEY
```

## How It Works

1. **Subtitle Check**: First attempts to download and parse existing YouTube subtitles
2. **Audio Download**: If no subtitles, downloads audio using yt-dlp
3. **Whisper Transcription**: Uses OpenAI Whisper to transcribe audio to text
4. **AI Analysis**: Sends transcript to OpenAI GPT for intelligent chapter generation
5. **Chapter Creation**: Generates properly formatted chapters with timestamps
6. **Output**: Saves chapters to a text file named after the video title

## Output Format

Chapters are saved in standard YouTube format:
```
00:00:00 Introduction
00:02:07 ACT English Section Tips
00:05:06 Comma Rules and Independent Clauses
...
```

## Example Output

For the video "Harvard Grad Reveals ACT English Secrets You've Never Heard":

```
00:00:00 Introduction
00:02:07 ACT English Section Tips
00:05:06 Comma Rules and Independent Clauses
00:07:34 Building Independent Clauses
00:10:59 Prepositions and Sentence Structure
00:14:29 Keeping It Simple and Consistent
00:18:26 Grammar Techniques and Tips
```

## File Structure

- `main_enhanced.py` - Enhanced script with Whisper fallback
- `main.py` - Original script (subtitles only)
- `config.env` - Configuration file for API keys
- `requirements.txt` - Python dependencies
- `*_chapters.txt` - Generated chapter files

## Troubleshooting

### Common Issues

1. **"No module named 'whisper'"**
   - Install Whisper: `pip install openai-whisper`

2. **"FFmpeg not found"**
   - Install FFmpeg: `brew install ffmpeg` (macOS) or download from ffmpeg.org

3. **"OpenAI API key not found"**
   - Check your `config.env` file has the correct API key

4. **Token limit exceeded**
   - The script automatically reduces sample size and falls back to time-based chapters

### Performance Tips

- **Whisper Model**: Uses "base" model by default. Change to "tiny" for faster processing or "medium"/"large" for better accuracy
- **Audio Quality**: Downloads at 192kbps MP3 for good balance of quality and speed
- **Cleanup**: Automatically removes downloaded audio files after processing

## Use Cases

- **Educational Videos**: Create study guides with specific topic timestamps
- **Long-form Content**: Break down lengthy videos into digestible sections
- **Content Creation**: Generate chapter markers for YouTube uploads
- **Research**: Quickly navigate to specific topics in video content

## Limitations

- **Processing Time**: Whisper transcription can take several minutes for long videos
- **Audio Quality**: Depends on original video audio quality
- **Language**: Currently optimized for English content
- **API Costs**: Uses OpenAI API tokens for chapter generation

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Batch processing of multiple videos
- [ ] Custom chapter templates
- [ ] Integration with YouTube API for direct upload
- [ ] Support for other transcription services

## License

This project is open source and available under the MIT License.
