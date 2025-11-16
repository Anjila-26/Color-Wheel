"""Main application class for Hand-Controlled Color Wheel"""

import cv2
import mediapipe as mp
from color_wheel_state import ColorWheelState
from gesture_detector import GestureDetector
from ui_renderer import UIRenderer
import config


class HandColorWheel:
    """Main application class that coordinates all components"""
    
    def __init__(self, num_colors=config.DEFAULT_NUM_COLORS):
        # Initialize state
        self.state = ColorWheelState(num_colors)
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.HAND_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def process_frame(self, frame):
        """Process a frame and update the color wheel"""
        h, w = frame.shape[:2]
        
        # Update wheel position
        self.state.update_wheel_position(w, h)
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        # Update auto-spin
        self.state.update_auto_spin()
        
        # Draw the color wheel
        UIRenderer.draw_color_wheel(
            frame, 
            self.state.wheel_center, 
            self.state.wheel_radius,
            self.state.colors,
            self.state.rotation_angle,
            self.state.hand_near_wheel
        )
        
        # Draw the spin button
        self.state.spin_button_rect = UIRenderer.draw_spin_button(
            frame,
            self.state.wheel_center,
            self.state.wheel_radius,
            self.state.get_button_state()
        )
        
        # Process hand landmarks
        if results.multi_hand_landmarks:
            self._process_hand_landmarks(frame, results.multi_hand_landmarks[0], w, h)
        else:
            self.state.reset_hand_state()
        
        # Draw instructions and status
        UIRenderer.draw_instructions(
            frame,
            self.state.num_colors,
            self.state.rotation_angle,
            self.state.is_auto_spinning,
            self.state.hand_near_wheel,
            self.state.spin_button_hovered
        )
        
        return frame
    
    def _process_hand_landmarks(self, frame, hand_landmarks, frame_width, frame_height):
        """Process detected hand landmarks"""
        # Draw hand skeleton
        self.mp_draw.draw_landmarks(
            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
        )
        
        # Get hand position and angle
        current_angle, hand_x, hand_y = GestureDetector.calculate_hand_angle(
            hand_landmarks,
            self.state.wheel_center[0],
            self.state.wheel_center[1],
            frame_width,
            frame_height
        )
        
        # Check button interaction
        button_pressed = self.state.check_button_interaction(hand_landmarks, hand_x, hand_y)
        if button_pressed:
            self.state.start_auto_spin()
        
        # Draw pinch indicator when near button
        if self.state.spin_button_hovered:
            UIRenderer.draw_pinch_indicator(frame, hand_landmarks, frame_width, frame_height)
        
        # Check if hand is near wheel
        self.state.check_hand_near_wheel(hand_x, hand_y)
        
        # Manual rotation (only if not spinning and near wheel, not near button)
        if (not self.state.is_auto_spinning and 
            self.state.hand_near_wheel and 
            not self.state.spin_button_hovered):
            
            self.state.update_manual_rotation(current_angle)
            
            # Draw connection line
            cv2.line(frame, (hand_x, hand_y), self.state.wheel_center, 
                    config.COLOR_GREEN, 2)
        else:
            if not self.state.is_auto_spinning:
                self.state.reset_manual_rotation()
        
        # Draw hand indicator
        UIRenderer.draw_hand_indicator(
            frame, hand_x, hand_y,
            self.state.hand_near_wheel,
            self.state.spin_button_hovered
        )
    
    def handle_key_press(self, key):
        """Handle keyboard input"""
        if key == ord(' '):
            self.state.start_auto_spin()
        elif key in [ord('+'), ord('=')]:
            self.state.increase_colors()
        elif key in [ord('-'), ord('_')]:
            self.state.decrease_colors()
    
    def run(self):
        """Main loop to run the application"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        self._print_instructions()
        
        window_name = 'Hand-Controlled Color Wheel'
        cv2.namedWindow(window_name)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame
            frame = self.process_frame(frame)
            
            # Display
            cv2.imshow(window_name, frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            else:
                self.handle_key_press(key)
        
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
    
    def _print_instructions(self):
        """Print startup instructions to console"""
        print("Starting Hand-Controlled Color Wheel...")
        print("Controls:")
        print("  - PINCH (thumb + index finger) over the SPIN button to auto-spin")
        print("  - OR press SPACEBAR to auto-spin the wheel")
        print("  - OR move your hand near the wheel to grab and rotate manually")
        print("  - The top indicator shows which color is selected")
        print("  - Press '+' to increase colors (max 20)")
        print("  - Press '-' to decrease colors (min 3)")
        print("  - Press 'q' to quit")


if __name__ == "__main__":
    app = HandColorWheel(num_colors=config.DEFAULT_NUM_COLORS)
    app.run()
