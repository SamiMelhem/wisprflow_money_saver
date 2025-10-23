# WisprFlow Money Saver MVP

## Overview

Build a Python-based command-line tool that captures the WisprFlow application window, extracts the "372 words" and "126 WPM" metrics from the top-right area using OCR, then calculates time and cost savings compared to typing.

## Architecture

### Core Components

1. **Window Capture Module** (`window_capture.py`)

   - Find WisprFlow application window by title (likely contains "Flow" or "WisprFlow")
   - Capture screenshot of the window or specific region (top-right area)
   - Use `pywin32` or `mss` for Windows screen capture

2. **OCR Module** (`ocr_extractor.py`)

   - Use `pytesseract` with Tesseract OCR to extract text from the top-right region
   - Parse extracted text to identify:
     - Words count (pattern: "XXX words")
     - Speaking WPM (pattern: "XXX WPM")
   - Return structured data (words, wpm)

3. **Savings Calculator** (`calculator.py`)

   - Input: speaking words, speaking WPM, typing WPM, subscription type
   - Calculate time saved:
     - Time spent speaking = words / speaking_wpm
     - Time would have spent typing = words / typing_wpm
     - Time saved = typing_time - speaking_time
   - Calculate cost per minute based on subscription:
     - Student: $7/month = ~$0.0048/minute (30 days)
     - Pro Monthly: $15/month = ~$0.0104/minute
     - Pro Annually: $12/month = ~$0.0083/minute
   - Calculate value of time saved = time_saved_minutes * cost_per_minute

4. **CLI Interface** (`main.py`)

   - Prompt user for:
     - Typing speed (WPM)
     - Subscription type (Student/Pro Monthly/Pro Annually)
   - Trigger window capture and OCR
   - Display results:
     - Words spoken
     - Speaking WPM
     - Time saved
     - Cost savings

## Technology Stack

- **Python 3.8+**
- **pytesseract** + Tesseract OCR for text extraction
- **Pillow (PIL)** for image processing
- **pywin32** or **mss** for window/screen capture
- **pygetwindow** for window management

## Dependencies (`requirements.txt`)

```
pytesseract>=0.3.10
Pillow>=10.0.0
mss>=9.0.1
pygetwindow>=0.0.9
pywin32>=306
```

## Implementation Steps

1. Set up project structure with modules
2. Implement window finder to locate WisprFlow window
3. Implement screenshot capture of top-right region
4. Integrate Tesseract OCR to extract text
5. Parse OCR output to extract words and WPM values
6. Implement savings calculation logic
7. Build CLI interface with user prompts
8. Add error handling (window not found, OCR failures)
9. Test with the provided WisprFlow screenshot

## Future Enhancements (Post-MVP)

- Background service to periodically capture data
- Store historical data in CSV/JSON file
- Track cumulative savings over time
- Web dashboard for visualization