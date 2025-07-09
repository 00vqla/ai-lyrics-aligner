# py-lyric-sync

A python tool to alligns lyrics to audio using OpenAI's Whisper model

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the aligner
python3 run_aligner.py
```

This will process all MP3 files in the current directory and create timestamped versions.

## Requirements

- Python 3.7+
- OpenAI Whisper model

## Usage

### Method 1: Process All Files (Recommended)

Place your MP3 files with embedded lyrics in the same directory and run:

```bash
python run_aligner.py
```

This will automatically process all MP3 files in the current directory.

### Method 2: Process Single File

```bash
# Process a single file
python lyrics_aligner.py "your_song.mp3"

# Specify output file
python lyrics_aligner.py "your_song.mp3" -o "aligned_song.mp3"

# Use different Whisper model (tiny, base, small, medium, large)
python lyrics_aligner.py "your_song.mp3" -m small
```

## How It Works

1. **Extract Lyrics:** Reads embedded lyrics from MP3 ID3 tags (USLT, TXXX)
2. **AI Transcription:** Uses Whisper to transcribe audio with word-level timestamps
3. **Generate Timestamps:** Creates precise start/end times for each line

## Output Format

The timestamped lyrics are embedded in the format:
```
[00:00.000] First line of lyrics
[00:03.500] Second line of lyrics
[00:07.200] Third line of lyrics
...
```

This is a time-synced lyrics format (.LRC format), which can be viewed in music players and apps that support synchronized lyrics display.

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

**Need to embed lyrics?**
If you have trouble finding lyrics for your MP3 files, try using my other project, [Metadata Fetcher](https://github.com/00vqla/metadata-fetcher).

## Example Output

```
Found 1 MP3 file(s):
1. sample_song.mp3

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

### "Whisper model not found"
- The first run will download the Whisper model (~74MB for base model)
- Ensure you have internet connection for the initial download

### Poor alignment accuracy
- Try using a larger Whisper model (`-m small` or `-m medium`)
- Ensure the audio quality is good

## License

This project is open source and available under the MIT License. 
