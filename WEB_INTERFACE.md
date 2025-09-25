# YouTube Chapter Generator - Web Interface

A beautiful, user-friendly web interface for generating YouTube chapters with AI.

## Features

- **Modern UI**: Clean, responsive design with beautiful gradients
- **Real-time Processing**: Upload YouTube URLs and get chapters instantly
- **Progress Tracking**: Visual feedback during processing
- **Multiple Formats**: Support for general videos and Q&A structure
- **Easy Export**: Download chapters or copy to clipboard
- **Mobile Friendly**: Works on desktop, tablet, and mobile devices

## Quick Start

1. **Install Dependencies**
   ```bash
   source venv/bin/activate
   pip install flask
   ```

2. **Configure API Key**
   Ensure your OpenAI API key is set in `config/config.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the Web Server**
   ```bash
   python app.py
   ```

4. **Open Browser**
   Navigate to: http://localhost:5000

## How to Use

1. **Enter YouTube URL**: Paste any YouTube video URL
2. **Set Chapter Count**: Choose how many chapters (1-200)
3. **Select Format**: 
   - General: For educational videos, lectures
   - Q&A Format: For intro + questions + song structure
4. **Generate**: Click the generate button and wait
5. **Export**: Download the file or copy text for YouTube

## Supported Video Types

### Educational Videos (General Mode)
- Medical education (USMLE Step 1 prep)
- University lectures
- Tutorial series
- Long-form educational content

Example: 100 chapters for a 6-hour medical review

### Q&A Videos (Questions Mode)
- Introduction + Questions + Song format
- Educational Q&A sessions
- Structured interview content

Example: 12 chapters (intro + 10 questions + song)

## Interface Features

### Visual Progress
- Animated loading spinner
- Progress bar during processing
- Clear status messages

### Results Display
- Chapter list with timestamps
- Raw text ready for YouTube
- One-click copy to clipboard
- Download as .txt file

### Error Handling
- URL validation
- Clear error messages
- Graceful failure handling

## Technical Details

### Backend
- **Flask**: Web framework
- **Python**: Calls existing chapter generation script
- **OpenAI**: Whisper transcription + GPT analysis
- **yt-dlp**: YouTube audio extraction

### Frontend
- **Bootstrap 5**: Responsive design
- **Font Awesome**: Icons
- **Vanilla JS**: No heavy frameworks
- **CSS3**: Modern styling with gradients

### Security
- Input validation
- URL sanitization
- Timeout protection (30 minutes max)
- No file storage on server

## API Endpoints

### POST /api/generate
Generate chapters from YouTube URL
```json
{
  "url": "https://youtube.com/watch?v=...",
  "chapters": 100,
  "questions": false
}
```

### GET /api/download/<video_id>
Download generated chapters file

## Development

### Local Development
```bash
export FLASK_ENV=development
python app.py
```

### Production Deployment
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

1. **"OpenAI API key not configured"**
   - Check `config/config.env` has valid API key

2. **"Invalid YouTube URL format"**
   - Use full YouTube URLs: https://youtube.com/watch?v=...
   - Or short URLs: https://youtu.be/...

3. **Processing timeout**
   - Very long videos (6+ hours) may timeout
   - Try reducing chapter count

4. **Module not found errors**
   - Ensure virtual environment is activated
   - Run `pip install -r config/requirements.txt`

### Performance Tips

- Shorter videos process faster
- Q&A mode is faster than general mode
- Lower chapter counts process quicker

## Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## Screenshots

The interface includes:
- Clean header with gradient background
- Feature explanation cards
- Input form with validation
- Progress indication
- Results with copy/download options
- Responsive design for all screen sizes
