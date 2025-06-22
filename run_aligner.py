#!/usr/bin/env python3
"""
Simple script to run the improved lyrics aligner on MP3 files in the current directory
"""

import os
import glob
from lyrics_aligner import ImprovedLyricsAligner

def main():
    # Find all MP3 files in the current directory (excluding already processed ones)
    mp3_files = [f for f in glob.glob("*.mp3") if not f.endswith(('_aligned.mp3', '_improved.mp3'))]
    
    if not mp3_files:
        print("No MP3 files found in the current directory.")
        print("Please place your MP3 files with embedded lyrics in this folder.")
        return
    
    print(f"Found {len(mp3_files)} MP3 file(s):")
    for i, file in enumerate(mp3_files, 1):
        print(f"{i}. {file}")
    
    # Process each MP3 file
    aligner = ImprovedLyricsAligner(model_name="base")
    
    for mp3_file in mp3_files:
        print(f"\n{'='*50}")
        print(f"Processing: {mp3_file}")
        print(f"{'='*50}")
        
        success = aligner.process_audio_file(mp3_file)
        
        if success:
            print(f"✅ Successfully processed: {mp3_file}")
        else:
            print(f"❌ Failed to process: {mp3_file}")
    
    print(f"\n{'='*50}")
    print("Processing complete!")
    print("Check for files with '_improved' suffix for the results.")

if __name__ == "__main__":
    main() 