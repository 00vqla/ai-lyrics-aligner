# Contributing to AI Lyrics Aligner

Thank you for your interest in contributing to AI Lyrics Aligner! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/yourusername/ai-lyrics-aligner/issues) section
2. If not, create a new issue with:
   - A clear and descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your operating system and Python version
   - Any error messages or logs

### Suggesting Enhancements

1. Check if the enhancement has already been suggested
2. Create a new issue with:
   - A clear description of the enhancement
   - Use cases and benefits
   - Any implementation ideas you have

### Code Contributions

1. Fork the repository
2. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Add tests if applicable
5. Ensure your code follows the project's style guidelines
6. Commit your changes with clear commit messages
7. Push to your fork and create a Pull Request

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/ai-lyrics-aligner.git
   cd ai-lyrics-aligner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install FFmpeg (see README.md for instructions)

4. Test your changes:
   ```bash
   python3 run_aligner.py
   ```

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and reasonably sized
- Add comments for complex logic

## Testing

Before submitting a pull request, please:

1. Test with different MP3 files
2. Test with various lyric formats
3. Test error handling scenarios
4. Ensure the code works on different platforms

## Pull Request Guidelines

1. Provide a clear description of the changes
2. Include any relevant issue numbers
3. Add screenshots or examples if applicable
4. Ensure all tests pass
5. Update documentation if needed

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, feel free to open an issue or contact the maintainers.

Thank you for contributing to AI Lyrics Aligner! 🎵 