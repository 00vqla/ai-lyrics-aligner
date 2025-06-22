# AI Lyrics Aligner

An AI-powered tool that extracts embedded lyrics from MP3 files, aligns them with the audio using OpenAI's Whisper model, and re-embeds timestamped lyrics back into the audio file.

## Features

- 🔍 **Extract embedded lyrics** from MP3 ID3 tags
- 🤖 **AI-powered alignment** using OpenAI Whisper for accurate timing
- ⏱️ **Smart timing estimation** combining AI transcription with duration-based fallback
- 📝 **Re-embed timestamped lyrics** back into the audio file
- 🎯 **Multiple output formats** (USLT and TXXX tags for compatibility)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download FFmpeg (if not already installed)
curl -L https://evermeet.cx/ffmpeg/getrelease/zip -o ffmpeg.zip
unzip ffmpeg.zip
chmod +x ffmpeg
export PATH=$PATH:$(pwd)

# Run the aligner
python3 run_aligner.py
```

This will process all MP3 files in the current directory and create timestamped versions.

## Requirements

- Python 3.7+
- FFmpeg (for audio processing)
- OpenAI Whisper model

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg:**
   ```bash
   # Download FFmpeg binary (no compilation needed)
   curl -L https://evermeet.cx/ffmpeg/getrelease/zip -o ffmpeg.zip
   unzip ffmpeg.zip
   chmod +x ffmpeg
   export PATH=$PATH:$(pwd)
   ```

## Usage

### Method 1: Process All Files (Recommended)

Place your MP3 files with embedded lyrics in the same directory and run:

```bash
python3 run_aligner.py
```

This will automatically process all MP3 files in the current directory.

### Method 2: Process Single File

```bash
# Process a single file
python3 lyrics_aligner.py "your_song.mp3"

# Specify output file
python3 lyrics_aligner.py "your_song.mp3" -o "aligned_song.mp3"

# Use different Whisper model (tiny, base, small, medium, large)
python3 lyrics_aligner.py "your_song.mp3" -m small
```

### Method 3: Python API

```python
from lyrics_aligner import ImprovedLyricsAligner

# Initialize aligner
aligner = ImprovedLyricsAligner(model_name="base")

# Process a file
success = aligner.process_audio_file("your_song.mp3")

if success:
    print("Lyrics aligned successfully!")
```

## How It Works

1. **Extract Lyrics:** Reads embedded lyrics from MP3 ID3 tags (USLT, TXXX)
2. **Clean Lyrics:** Removes formatting and splits into individual lines
3. **AI Transcription:** Uses Whisper to transcribe audio with word-level timestamps
4. **Smart Alignment:** Combines AI transcription with duration-based estimation for optimal accuracy
5. **Generate Timestamps:** Creates precise start/end times for each line
6. **Embed Results:** Saves timestamped lyrics back to the audio file

## Output Format

The timestamped lyrics are embedded in the format:
```
[00:00.000] First line of lyrics
[00:03.500] Second line of lyrics
[00:07.200] Third line of lyrics
...
```

## Supported Whisper Models

- **tiny:** Fastest, least accurate (39MB)
- **base:** Good balance of speed/accuracy (74MB) - **Default**
- **small:** Better accuracy, slower (244MB)
- **medium:** High accuracy, slower (769MB)
- **large:** Best accuracy, slowest (1550MB)

## File Requirements

Your MP3 files must have lyrics embedded in one of these ID3 tags:
- `USLT::eng` (Unsynchronized Lyrics)
- `TXXX::LYRICS`
- `TXXX::UNSYNCEDLYRICS`
- `TXXX::SYNCEDLYRICS`

## Example Output

```
Found 1 MP3 file(s):
1. 79 wtf.mp3

==================================================
Processing: sample_song.mp3
==================================================

1. Extracting embedded lyrics...
Found lyrics in tag: USLT::eng
Extracted lyrics: (Indigo) (Okay, Embasin)...

2. Cleaning and splitting lyrics...
Split into 72 lines

3. Smart aligning lyrics with audio...
Loading Whisper model: base
Transcribing audio with Whisper...
Found 613 words with timestamps
Using AI-powered alignment...
AI Aligned: 'Uh break down all this ****' (123.30s - 125.44s)
AI Aligned: 'Yeah then roll it up' (70.56s - 72.22s)
...

4. Formatting timestamped lyrics...
5. Embedding timestamped lyrics...
Improved timestamped lyrics embedded successfully: 79 sample_song_improved.mp3

✅ Success! Improved lyrics embedded in: 79 sample_song_improved.mp3
```

## Troubleshooting

### "No embedded lyrics found"
- Ensure your MP3 file has lyrics embedded in ID3 tags
- Try using a media player to view/edit embedded lyrics

### "FFmpeg not found"
- Make sure FFmpeg is downloaded and in your PATH
- Run: `export PATH=$PATH:$(pwd)` to add the local FFmpeg to PATH

### "Whisper model not found"
- The first run will download the Whisper model (~74MB for base model)
- Ensure you have internet connection for the initial download

### Poor alignment accuracy
- Try using a larger Whisper model (`-m small` or `-m medium`)
- Ensure the audio quality is good
- Check that the embedded lyrics match the actual sung lyrics

## Files

- `lyrics_aligner.py` - Main lyrics alignment engine
- `run_aligner.py` - Simple runner script
- `requirements.txt` - Python dependencies
- `ffmpeg` - FFmpeg binary (downloaded automatically)
- `README.md` - This documentation

## License

This project is open source and available under the MIT License. 
