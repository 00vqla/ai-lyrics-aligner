#!/usr/bin/env python3
"""
Setup script for AI Lyrics Aligner
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-lyrics-aligner",
    version="1.0.0",
    author="AI Lyrics Aligner",
    author_email="",
    description="AI-powered tool to align and timestamp lyrics in MP3 files",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/00vqla/ai-lyrics-aligner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "lyrics-aligner=lyrics_aligner:main",
        ],
    },
    keywords="lyrics, audio, mp3, alignment, timestamp, ai, whisper, music",
    project_urls={
        "Bug Reports": "https://github.com/00vqla/ai-lyrics-aligner/issues",
        "Source": "https://github.com/00vqla/ai-lyrics-aligner",
        "Documentation": "https://github.com/00vqla/ai-lyrics-aligner#readme",
    },
) 