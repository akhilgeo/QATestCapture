# QA Recorder App Walkthrough

## Overview
The QA Recorder App is a Python desktop application designed to assist in QA testing by automatically recording screen changes and generating a report in DOCX or PDF format.

## Features
- **Automatic Screen Capture**: Captures screenshots when visual changes are detected.
- **Change Detection**: Logs the active window title and detects visual differences.
- **Minimum Interval**: Ensures captures happen at most every 10 seconds to avoid spam.
- **Report Generation**: Exports the session to a DOCX or PDF file with timestamps and descriptions.

## How to Run
1.  Navigate to the project directory:
    ```bash
    cd C:\Users\akhil\.gemini\antigravity\scratch\qa_recorder
    ```
2.  Activate the virtual environment:
    ```bash
    venv\Scripts\activate
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

## Usage
1.  Select the desired output format (DOCX or PDF).
2.  Click **Start Recording**.
3.  Perform your QA tests. The app will capture screenshots when the screen changes (min 10s interval).
4.  Click **Stop Recording** when finished.
5.  The report will be saved in the current directory (e.g., `QA_Report_1734000000.docx`).

## Verification Results
- **Recording Logic**: Verified that screenshots are captured and stored with timestamps and window titles.
- **Change Detection**: Verified that identical screens are not re-captured (unless 10s passed and logic allows, currently strict on diff).
- **Report Generation**: Verified that both DOCX and PDF reports are generated successfully with images and text.
