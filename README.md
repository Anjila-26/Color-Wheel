# Color Wheel App

## Overview

The Color Wheel App is an interactive Python application that lets users explore and select colors using a dynamic color wheel interface. It features gesture-based controls for a hands-free experience, making color selection intuitive and engaging.

## Features

- **Gesture Control:** Use hand gestures to interact with the color wheel (requires a webcam).
- **Real-Time Feedback:** Instantly see color changes and selections as you interact.
- **Modular Design:** Clean separation of logic for state management, gesture detection, UI rendering, and configuration.
- **Customizable:** Easily adjust settings and extend functionality via the modular codebase.

## Project Structure

- `color_wheel_app.py` — Main application entry point.
- `color_wheel_state.py` — Manages color wheel logic and state.
- `gesture_detector.py` — Handles gesture recognition and tracking.
- `ui_renderer.py` — Renders the color wheel and UI elements.
- `config.py` — Stores configuration settings and constants.
- `README_MODULES.md` — Documentation for individual modules.

## Getting Started

1. **Clone the repository:**
	```bash
	git clone this_repo
	```

2. **Install dependencies:**
	- Make sure you have Python 3.x installed.
	- Install required packages (e.g., OpenCV, MediaPipe):
	  ```bash
	  pip install opencv-python mediapipe
	  ```

3. **Run the application:**
	```bash
	python color_wheel_app.py
	```

4. **Interact:**
	- Use your webcam and hand gestures to control the color wheel.
	- Select colors and see real-time feedback.

## Customization

- Modify `config.py` to change settings (e.g., gesture sensitivity, UI options).
- Extend or replace modules for new features (e.g., add new gesture types or color models).

## Credits

Created by Anjila-26 as part of the "30 Days 30 Projects" challenge.

## License

This project is open source and available under the MIT License.
