"""Color wheel state and logic management"""

import numpy as np
import cv2
from gesture_detector import GestureDetector
import config


class ColorWheelState:
    """Manages the state of the color wheel"""
    
    def __init__(self, num_colors=config.DEFAULT_NUM_COLORS):
        self.num_colors = num_colors
        self.rotation_angle = 0
        self.prev_hand_angle = None
        self.wheel_center = None
        self.wheel_radius = None
        self.is_rotating = False
        self.hand_near_wheel = False
        
        # Auto-spin state
        self.is_auto_spinning = False
        self.spin_velocity = 0
        
        # Button state
        self.spin_button_rect = None
        self.spin_button_hovered = False
        self.spin_button_pressed = False
        
        # Generate colors
        self.colors = self.generate_colors(num_colors)
    
    def generate_colors(self, num_colors):
        """Generate evenly spaced colors around the HSV color wheel"""
        colors = []
        for i in range(num_colors):
            hue = int(180 * i / num_colors)
            color_hsv = np.uint8([[[hue, 255, 255]]])
            color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)
            colors.append(color_bgr[0][0].tolist())
        return colors
    
    def set_num_colors(self, num_colors):
        """Update the number of colors"""
        self.num_colors = max(config.MIN_COLORS, min(num_colors, config.MAX_COLORS))
        self.colors = self.generate_colors(self.num_colors)
    
    def increase_colors(self):
        """Increase number of colors"""
        if self.num_colors < config.MAX_COLORS:
            self.set_num_colors(self.num_colors + 1)
    
    def decrease_colors(self):
        """Decrease number of colors"""
        if self.num_colors > config.MIN_COLORS:
            self.set_num_colors(self.num_colors - 1)
    
    def start_auto_spin(self):
        """Start automatic spinning with random velocity"""
        if not self.is_auto_spinning:
            self.spin_velocity = np.random.uniform(
                config.MIN_SPIN_SPEED, config.MAX_SPIN_SPEED
            )
            if np.random.random() < 0.5:
                self.spin_velocity = -self.spin_velocity
            self.is_auto_spinning = True
            print("🎡 Wheel is spinning!")
    
    def update_auto_spin(self):
        """Update the wheel rotation during auto-spin"""
        if self.is_auto_spinning:
            self.rotation_angle += self.spin_velocity
            self.rotation_angle %= 360
            
            self.spin_velocity *= config.SPIN_DECELERATION
            
            if abs(self.spin_velocity) < config.MIN_SPIN_VELOCITY:
                self.is_auto_spinning = False
                self.spin_velocity = 0
                self.spin_button_pressed = False
                print("🎯 Wheel stopped!")
    
    def update_wheel_position(self, frame_width, frame_height):
        """Calculate wheel position based on frame dimensions"""
        self.wheel_center = (
            frame_width - config.WHEEL_OFFSET_FROM_RIGHT, 
            frame_height // 2
        )
        self.wheel_radius = min(
            config.WHEEL_OFFSET_FROM_RIGHT - 50, 
            frame_height // 3
        )
    
    def check_hand_near_wheel(self, hand_x, hand_y):
        """Check if hand is near the wheel"""
        distance = GestureDetector.calculate_distance_to_point(
            hand_x, hand_y, self.wheel_center[0], self.wheel_center[1]
        )
        self.hand_near_wheel = distance < (self.wheel_radius * config.HAND_NEAR_WHEEL_MULTIPLIER)
        return self.hand_near_wheel
    
    def check_button_interaction(self, hand_landmarks, hand_x, hand_y):
        """Check if hand is interacting with the spin button"""
        if self.spin_button_rect is None:
            return False
        
        button_x, button_y, button_width, button_height = self.spin_button_rect
        
        # Check if finger is over button
        if (button_x <= hand_x <= button_x + button_width and 
            button_y <= hand_y <= button_y + button_height):
            self.spin_button_hovered = True
            
            # Check for pinch gesture
            is_pinching = GestureDetector.is_pinching(hand_landmarks, config.PINCH_THRESHOLD)
            
            if is_pinching and not self.is_auto_spinning and not self.spin_button_pressed:
                self.spin_button_pressed = True
                return True
        else:
            self.spin_button_hovered = False
            if not self.is_auto_spinning:
                self.spin_button_pressed = False
        
        return False
    
    def update_manual_rotation(self, current_angle):
        """Update rotation angle based on hand movement"""
        if self.prev_hand_angle is not None:
            angle_diff = current_angle - self.prev_hand_angle
            
            # Handle angle wrapping
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360
            
            self.rotation_angle += angle_diff
            self.rotation_angle %= 360
            self.is_rotating = True
        
        self.prev_hand_angle = current_angle
    
    def reset_manual_rotation(self):
        """Reset manual rotation state"""
        if not self.is_auto_spinning:
            self.prev_hand_angle = None
            self.is_rotating = False
    
    def reset_hand_state(self):
        """Reset all hand-related state"""
        self.prev_hand_angle = None
        self.hand_near_wheel = False
        self.spin_button_hovered = False
        if not self.is_auto_spinning:
            self.spin_button_pressed = False
            self.is_rotating = False
    
    def get_button_state(self):
        """Get current button state as a dictionary"""
        return {
            'is_spinning': self.is_auto_spinning,
            'is_hovered': self.spin_button_hovered,
            'is_pressed': self.spin_button_pressed
        }
