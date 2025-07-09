import os
import sys
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re
import argparse

try:
    import mutagen
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, USLT, TXXX
    import librosa
    import numpy as np
    import whisper
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required packages:")
    print("pip install mutagen librosa numpy openai-whisper")
    sys.exit(1)


class ImprovedLyricsAligner:
    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self.whisper_model = None
        
    def load_whisper_model(self):
        if self.whisper_model is None:
            print(f"Loading Whisper model: {self.model_name}")
            self.whisper_model = whisper.load_model(self.model_name)
        return self.whisper_model
    
    def extract_embedded_lyrics(self, audio_path: str) -> Optional[str]:
        try:
            audio = MP3(audio_path, ID3=ID3)
            if audio.tags is None:
                print("No ID3 tags found in the audio file")
                return None
            
            # other possible tags
            lyric_tags = [
                'USLT::eng',  # unsynched
                'TXXX::LYRICS',
                'TXXX::UNSYNCEDLYRICS',
                'TXXX::SYNCEDLYRICS'
            ]
            
            for tag in lyric_tags:
                if tag in audio.tags:
                    lyrics = str(audio.tags[tag])
                    if lyrics.strip():
                        print(f"Found lyrics in tag: {tag}")
                        return lyrics
            
            # find USLT tags
            for tag in audio.tags:
                if tag.startswith('USLT'):
                    lyrics = str(audio.tags[tag])
                    if lyrics.strip():
                        print(f"Found lyrics in tag: {tag}")
                        return lyrics
            
            print("No embedded lyrics found in the audio file")
            return None
            
        except Exception as e:
            print(f"Error extracting lyrics: {e}")
            return None
    
    def clean_lyrics(self, lyrics: str) -> List[str]:
        """
        Clean and split lyrics into lines, preserving more structure
        """
        # regex filtering
        lyrics = re.sub(r'\[.*?\]', '', lyrics)  # brackets
        lyrics = re.sub(r'\(.*?\)', '', lyrics)  # parentheses
        
        # split into lines
        lines = []
        for line in lyrics.split('\n'):
            line = line.strip()
            if line:
                lines.append(line)
        
        return lines
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get audio duration using mutagen
        """
        try:
            audio = MP3(audio_path)
            duration = audio.info.length
            print(f"Audio duration: {duration:.2f} seconds")
            return duration
        except Exception as e:
            print(f"Error getting audio duration: {e}")
            return 180.0 
    
    def transcribe_audio(self, audio_path: str) -> List[Dict]:
        """
        Transcribe audio and get word-level timestamps
        """
        print("Transcribing audio with Whisper...")
        model = self.load_whisper_model()
        
        try:
            result = model.transcribe(audio_path, word_timestamps=True)
            
            # word level timestamps
            word_timestamps = []
            for segment in result["segments"]:
                if isinstance(segment, dict) and "words" in segment:
                    words = segment["words"]
                    for word_info in words:
                        word_timestamps.append({
                            "word": word_info["word"].strip(),
                            "start": word_info["start"],
                            "end": word_info["end"]
                        })
            
            print(f"Found {len(word_timestamps)} words with timestamps")
            return word_timestamps
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return []
    
    def smart_align_lyrics(self, audio_path: str, lyrics: List[str]) -> List[Dict]:
        """
        Smart alignment combining duration-based estimation with AI transcription
        """
        duration = self.get_audio_duration(audio_path)
        
        # Get AI transcription
        word_timestamps = self.transcribe_audio(audio_path)
        
        # Filter out empty lines and get content lines
        content_lines = [line for line in lyrics if line.strip()]
        num_lines = len(content_lines)
        
        if num_lines == 0:
            return []
        
        # use if good transcription
        if len(word_timestamps) > 50:  # min threshold for reliable transcription
            return self.ai_align_lyrics(content_lines, word_timestamps, duration)
        else:
            return self.duration_align_lyrics(content_lines, duration)
    
    def ai_align_lyrics(self, lyrics: List[str], word_timestamps: List[Dict], duration: float) -> List[Dict]:
        """
        AI-powered alignment using word timestamps
        """
        print("Using AI-powered alignment...")
        aligned_lyrics = []
        
        for line in lyrics:
            line_words = line.lower().split()
            if not line_words:
                continue
            
            # best for match for line
            best_match = self.find_best_line_match(line_words, word_timestamps)
            
            if best_match:
                aligned_lyrics.append(best_match)
                print(f"AI Aligned: '{line}' ({best_match['start_time']:.2f}s - {best_match['end_time']:.2f}s)")
            else:
                # fallback to duration-based
                estimated = self.estimate_line_timing(len(aligned_lyrics), line, duration, len(lyrics))
                aligned_lyrics.append(estimated)
                print(f"Estimated: '{line}' ({estimated['start_time']:.2f}s - {estimated['end_time']:.2f}s)")
        
        return aligned_lyrics
    
    def find_best_line_match(self, line_words: List[str], word_timestamps: List[Dict]) -> Optional[Dict]:

        if len(line_words) < 2:
            return None
        
        best_score = 0
        best_start = None
        best_end = None
        
        # consec word matches
        for i in range(len(word_timestamps) - len(line_words) + 1):
            score = 0
            consecutive_matches = 0
            
            for j, line_word in enumerate(line_words):
                if i + j < len(word_timestamps):
                    timestamp_word = word_timestamps[i + j]["word"].lower().strip()
                    
                    # More flexible matching
                    if (line_word in timestamp_word or 
                        timestamp_word in line_word or 
                        self.similar_words(line_word, timestamp_word)):
                        score += 1
                        consecutive_matches += 1
                    else:
                        consecutive_matches = 0
                
                # Bonus for consecutive matches
                if consecutive_matches >= 2:
                    score += 0.5
            
            # Require at least 60% match for a valid alignment
            if score >= len(line_words) * 0.6 and score > best_score:
                best_score = score
                best_start = word_timestamps[i]["start"]
                best_end = word_timestamps[min(i + len(line_words) - 1, len(word_timestamps) - 1)]["end"]
        
        if best_start is not None and best_end is not None:
            return {
                "line": " ".join(line_words),
                "start_time": best_start,
                "end_time": best_end,
                "confidence": best_score / len(line_words)
            }
        
        return None
    
    def similar_words(self, word1: str, word2: str) -> bool:
        """
        Check if two words are similar (for flexible matching)
        """
        # filtering
        word1_clean = re.sub(r'[^\w]', '', word1.lower())
        word2_clean = re.sub(r'[^\w]', '', word2.lower())
        
        # match
        if word1_clean == word2_clean:
            return True
        
        # one + other
        if word1_clean in word2_clean or word2_clean in word1_clean:
            return True
        
        # similar length + common chars
        if len(word1_clean) > 3 and len(word2_clean) > 3:
            common_chars = sum(1 for c in word1_clean if c in word2_clean)
            if common_chars >= min(len(word1_clean), len(word2_clean)) * 0.7:
                return True
        
        return False
    
    def duration_align_lyrics(self, lyrics: List[str], duration: float) -> List[Dict]:
        """
        Duration-based alignment as fallback
        """
        print("Using duration-based alignment...")
        aligned_lyrics = []
        num_lines = len(lyrics)
        
        # base timing calculation
        base_time_per_line = duration / num_lines
        
        for i, line in enumerate(lyrics):
            # var based on line length
            line_length = len(line.split())
            time_variation = min(1.0, line_length * 0.2)
            
            start_time = i * base_time_per_line
            end_time = start_time + base_time_per_line + time_variation
            
            # duration check
            if end_time > duration:
                end_time = duration
            
            aligned_lyrics.append({
                "line": line,
                "start_time": start_time,
                "end_time": end_time,
                "confidence": 0.7
            })
            
            print(f"Duration-based: '{line}' ({start_time:.2f}s - {end_time:.2f}s)")
        
        return aligned_lyrics
    
    def estimate_line_timing(self, current_index: int, line: str, duration: float, total_lines: int) -> Dict:
        """
        Estimate timing for a single line
        """
        base_time_per_line = duration / total_lines
        line_length = len(line.split())
        time_variation = min(1.0, line_length * 0.2)
        
        start_time = current_index * base_time_per_line
        end_time = start_time + base_time_per_line + time_variation
        
        if end_time > duration:
            end_time = duration
        
        return {
            "line": line,
            "start_time": start_time,
            "end_time": end_time,
            "confidence": 0.5
        }
    
    def format_timestamped_lyrics(self, aligned_lyrics: List[Dict]) -> str:
        """
        Format aligned lyrics with timestamps
        """
        formatted_lines = []
        
        for entry in aligned_lyrics:
            start_time = entry["start_time"]
            end_time = entry["end_time"]
            line = entry["line"]
            confidence = entry["confidence"]
            
            # format timestamp
            start_timestamp = f"[{int(start_time//60):02d}:{start_time%60:06.3f}]"
            
            formatted_line = f"{start_timestamp} {line}"
            formatted_lines.append(formatted_line)
        
        return "\n".join(formatted_lines)
    
    def embed_timestamped_lyrics(self, audio_path: str, timestamped_lyrics: str, output_path: str = None):
        """
        Embed timestamped lyrics back into the audio file
        """
        if output_path is None:
            output_path = audio_path.replace('.mp3', '_improved.mp3')
        
        try:
            # clone og file
            import shutil
            shutil.copy2(audio_path, output_path)
            
            # load the clone
            audio = MP3(output_path, ID3=ID3)
            
            # create ID3 tag if not available
            if audio.tags is None:
                audio.tags = ID3()
            
            # add timestamped lyrics as USLT
            uslt = USLT(encoding=3, lang='eng', desc='Improved AI Aligned Lyrics', text=timestamped_lyrics)
            audio.tags.add(uslt)
            
            # TXXX
            txxx = TXXX(encoding=3, desc='IMPROVED_TIMESTAMPED_LYRICS', text=timestamped_lyrics)
            audio.tags.add(txxx)
            
            audio.save()
            
            print(f"Improved timestamped lyrics embedded successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error embedding lyrics: {e}")
            return None
    
    def process_audio_file(self, audio_path: str, output_path: str = None) -> bool:
        print(f"Processing: {audio_path}")
        
        # extract
        print("\n1. Extracting embedded lyrics...")
        lyrics = self.extract_embedded_lyrics(audio_path)
        if not lyrics:
            print("No lyrics found to align. Please ensure the audio file has embedded lyrics.")
            return False
        
        print(f"Extracted lyrics:\n{lyrics[:200]}...")
        
        # clean n split
        print("\n2. Cleaning and splitting lyrics...")
        lyrics_lines = self.clean_lyrics(lyrics)
        print(f"Split into {len(lyrics_lines)} lines")
        
        # aligning
        print("\n3. Aligning lyrics with audio...")
        aligned_lyrics = self.smart_align_lyrics(audio_path, lyrics_lines)
        
        # formatting
        print("\n4. Formatting timestamped lyrics...")
        timestamped_lyrics = self.format_timestamped_lyrics(aligned_lyrics)
        
        # embedding
        print("\n5. Embedding timestamped lyrics...")
        result_path = self.embed_timestamped_lyrics(audio_path, timestamped_lyrics, output_path)
        
        if result_path:
            print(f"\n✅ Success! Lyrics embedded in: {result_path}")
            print("\nTimestamped lyrics preview:")
            print(timestamped_lyrics[:500] + "..." if len(timestamped_lyrics) > 500 else timestamped_lyrics)
            return True
        else:
            print("\n❌ Failed to embed timestamped lyrics")
            return False


def main():
    parser = argparse.ArgumentParser(description="Improved AI Lyrics Aligner - Better accuracy")
    parser.add_argument("audio_file", help="Path to the MP3 file with embedded lyrics")
    parser.add_argument("-o", "--output", help="Output file path (default: original_name_improved.mp3)")
    parser.add_argument("-m", "--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.audio_file):
        print(f"Error: File not found: {args.audio_file}")
        sys.exit(1)
    
    # init
    aligner = ImprovedLyricsAligner(model_name=args.model)

    success = aligner.process_audio_file(args.audio_file, args.output)
    
    if success:
        print("\n🎵 Improved lyrics alignment completed successfully!")
    else:
        print("\n❌ Improved lyrics alignment failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 