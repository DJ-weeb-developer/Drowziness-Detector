# Driver Drowsiness Detection System

A real-time computer vision system that monitors driver fatigue using facial landmarks (MediaPipe) and Eye Aspect Ratio (EAR). The system provides visual and audio alerts when drowsiness is detected.

## Features
- **Real-time Eye Tracking**: Uses MediaPipe Face Mesh to precisely locate eye landmarks.
- **Drowsiness Detection**: Calculates EAR to detect prolonged eye closure.
- **Blink Counting**: Tracks normal blink rates.
- **Audio/Visual Alerts**: Plays a sound and shows on-screen warnings when fatigued.
- **Web Interface**: Modern Flask-based web UI to view the stream and control settings.
- **Adjustable Sensitivity**: Change detection thresholds live from the UI.

## Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Generate Alert Sound**:
    Run the helper script to create a beep sound (or place your own `alert.wav` in the folder).
    ```bash
    python generate_sound.py
    ```

## Usage

1.  **Start the Server**:
    ```bash
    python app.py
    ```
2.  **Open Browser**:
    Go to `http://127.0.0.1:5000`

3.  **Controls**:
    - Click **Start Monitor** to begin the feed.
    - Adjust **EAR Threshold** if the system triggers too easily (lower it) or doesn't trigger when eyes are closed (raise it).
    - **Frames for Drowsiness**: How long (in frames) eyes must be closed to trigger the alarm.

## Technical Details
- **EAR Formula**: The Eye Aspect Ratio is calculated using the euclidean distance between vertical eye landmarks divided by twice the horizontal distance.
- **Thresholds**: Default EAR threshold is 0.25. If EAR falls below this for ~20 frames (approx 1 sec at 20fps), alarm triggers.

## Project Structure
- `app.py`: Flask server and main entry point.
- `drowsiness_detector.py`: Core logic for Face Mesh and EAR.
- `audio_alert.py`: Threaded audio player.
- `templates/index.html`: Frontend UI.
