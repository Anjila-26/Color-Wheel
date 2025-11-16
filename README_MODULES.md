# Hand-Controlled Color Wheel - Modular Structure

## Files Overview

### Main Application
- **`color_wheel_app.py`** - Main application entry point

### Core Modules
- **`config.py`** - Configuration constants and settings
- **`color_wheel_state.py`** - State management for the color wheel
- **`gesture_detector.py`** - Hand gesture detection utilities
- **`ui_renderer.py`** - UI rendering functions

## Running the Application

### Using the modular version:
```bash
python color_wheel_app.py
```

### Using the original version:
```bash
python color.py
```

## Architecture

```
HandColorWheel (color_wheel_app.py)
    ├── ColorWheelState (color_wheel_state.py)
    │   ├── Manages rotation angle
    │   ├── Handles auto-spin logic
    │   └── Tracks button and hand state
    │
    ├── GestureDetector (gesture_detector.py)
    │   ├── Detects pinch gestures
    │   ├── Calculates hand positions
    │   └── Computes angles and distances
    │
    └── UIRenderer (ui_renderer.py)
        ├── Draws color wheel
        ├── Renders spin button
        └── Displays instructions and status
```

## Benefits of Modular Structure

1. **Easier to Maintain** - Each module has a single responsibility
2. **Easier to Test** - Can test individual components
3. **Easier to Extend** - Add new features without modifying everything
4. **Better Code Organization** - Related functionality grouped together
5. **Reusable Components** - Can use parts in other projects

## Configuration

Edit `config.py` to customize:
- Number of colors
- Spin speed and deceleration
- Button appearance
- Detection thresholds
- Visual settings
