# PAVORA AI CONTROL — Phase 1

Local Windows 11 webcam hand tracking prototype (Python, OpenCV, MediaPipe, PyAutoGUI).

**Status:** Code prepared; actual webcam/hardware testing pending. This is NOT yet a voice AI agent or unrestricted iPhone controller.

## Setup
1. Install Python 3.11 with Python Launcher from https://python.org/downloads/
2. Connect a USB webcam.
3. Download this folder and double-click `run_windows.bat`.
4. In Windows Settings > Privacy & security > Camera, enable desktop-app camera access.
5. Press **E** in preview to enable; **E** again pauses; **Q** or **Esc** exits.

## Controls
- Index finger raised: cursor movement
- Thumb-index pinch, other fingers lowered: left click (cooldown)
- Index and middle fingers: scroll up/down with hand
- Four fingers/open palm: pause
- PyAutoGUI top-left-corner fail-safe is on

No footage is uploaded or recorded; webcam processing stays local. Mouse actions start PAUSED, and no automatic startup service is installed.

## Tests
```powershell
py -3.11 -m unittest discover -s tests -v
```

## Limitations
A webcam is required to test live input. Hand recognition may be imperfect in low light or odd angles. iOS does not permit third-party apps unrestricted system-wide touch automation. Later phases: voice AI executor with confirmations and iPhone Shortcuts companion.

Project is stored under `pavora-ai-control/` in an existing GitHub repository, separately from the PAVORA social app.
