# Hill Climb Gesture Control 🎮

Control Hill Climb Racing (or any app that uses Left/Right arrow input) with hand gestures through your webcam.

This project combines:
- MediaPipe Hand Landmarker for hand detection
- OpenCV for webcam capture and live preview
- Windows `SendInput` (via `ctypes`) to press and release keyboard scan codes

## Features ✨
- Real-time hand landmark detection from webcam
- Gesture-to-key mapping:
	- Open hand (4 fingers up): hold `Right Arrow` (THROTTLE)
	- Closed fist (0 fingers up): hold `Left Arrow` (BRAKE)
	- Any other pose: release keys (IDLE)
- Automatic model download if `hand_landmarker.task` is missing
- FPS and current mode shown on screen

## Requirements
- Windows (required for `directkeys.py` / `ctypes.windll.user32.SendInput`)
- Python 3.9+
- Webcam

## Project Structure
- `gesture_control.py`: Main loop (camera, detection, gesture logic, key handling)
- `directkeys.py`: Low-level Windows key press/release helpers
- `test.py`: Quick key simulation test script
- `hand_landmarker.task`: MediaPipe model file (auto-downloaded when missing)

## Setup ⚙️
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install opencv-python mediapipe
```

## Run ▶️
Start gesture control:

```powershell
python gesture_control.py
```

Press `q` in the preview window to quit.

## How Gesture Detection Works
The script checks whether each finger is raised by comparing tip and PIP y-coordinates:
- Index: `8` vs `6`
- Middle: `12` vs `10`
- Ring: `16` vs `14`
- Pinky: `20` vs `18`

Then it maps the result:
- 4 raised -> THROTTLE (`Right Arrow` held)
- 0 raised -> BRAKE (`Left Arrow` held)
- Else -> IDLE (no key held)

## Quick Input Test 🧪
To verify key injection works on your machine:

```powershell
python test.py
```

It waits 2 seconds, holds the right key for 2 seconds, then releases.

## Troubleshooting 🛠️
- Camera not opening: close other apps using the webcam and run again.
- No hand detected: improve lighting and keep your hand fully visible in frame.
- Wrong gesture behavior: adjust hand distance/angle; thresholds can be tuned in `gesture_control.py`.
- Game not responding: keep the game window focused; some games may block simulated input.
- MediaPipe model errors: delete `hand_landmarker.task` and rerun to force a fresh download.

## Notes
- This project is intended for personal experimentation.
- Use responsibly and only where synthetic keyboard input is allowed.
