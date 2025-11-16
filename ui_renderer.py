"""UI rendering utilities for the color wheel application"""

import cv2
import config


class UIRenderer:
    """Handles all UI rendering operations"""
    
    @staticmethod
    def draw_color_wheel(frame, center, radius, colors, rotation_angle, hand_near_wheel):
        """Draw a segmented color wheel with top indicator"""
        num_colors = len(colors)
        angle_per_segment = 360 / num_colors
        
        # Draw colored segments
        for i in range(num_colors):
            start_angle = int(i * angle_per_segment + rotation_angle)
            end_angle = int((i + 1) * angle_per_segment + rotation_angle)
            
            # Draw segment
            cv2.ellipse(frame, center, (radius, radius), 0, 
                       start_angle, end_angle, colors[i], -1)
            # Draw border
            cv2.ellipse(frame, center, (radius, radius), 0, 
                       start_angle, end_angle, config.COLOR_BLACK, 2)
        
        # Draw center grab area
        center_radius = int(radius * config.CENTER_RADIUS_MULTIPLIER)
        center_color = config.COLOR_GRAB_ACTIVE if hand_near_wheel else config.COLOR_LIGHT_GRAY
        cv2.circle(frame, center, center_radius, center_color, -1)
        cv2.circle(frame, center, center_radius, config.COLOR_BLACK, 2)
        cv2.putText(frame, "GRAB", (center[0] - 30, center[1] + 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, config.COLOR_BLACK, 2)
        
        # Draw top indicator (pointer)
        UIRenderer._draw_pointer(frame, center, radius)
        
        # Calculate and display selected color
        selected_color = UIRenderer._get_selected_color(colors, rotation_angle, angle_per_segment)
        UIRenderer._draw_selected_color_box(frame, center, selected_color)
        
        return selected_color
    
    @staticmethod
    def _draw_pointer(frame, center, radius):
        """Draw the top indicator arrow"""
        indicator_length = radius + config.INDICATOR_LENGTH_OFFSET
        indicator_tip = (center[0], center[1] - indicator_length)
        indicator_base = (center[0], center[1] - radius - 5)
        
        # Draw arrow line
        cv2.line(frame, indicator_base, indicator_tip, config.COLOR_BLACK, 5)
        cv2.line(frame, indicator_base, indicator_tip, config.COLOR_WHITE, 3)
        
        # Draw arrow head
        arrow_size = config.ARROW_SIZE
        cv2.line(frame, indicator_tip, 
                (indicator_tip[0] - arrow_size//2, indicator_tip[1] + arrow_size), 
                config.COLOR_BLACK, 5)
        cv2.line(frame, indicator_tip, 
                (indicator_tip[0] + arrow_size//2, indicator_tip[1] + arrow_size), 
                config.COLOR_BLACK, 5)
        cv2.line(frame, indicator_tip, 
                (indicator_tip[0] - arrow_size//2, indicator_tip[1] + arrow_size), 
                config.COLOR_WHITE, 3)
        cv2.line(frame, indicator_tip, 
                (indicator_tip[0] + arrow_size//2, indicator_tip[1] + arrow_size), 
                config.COLOR_WHITE, 3)
    
    @staticmethod
    def _get_selected_color(colors, rotation_angle, angle_per_segment):
        """Calculate which color is selected at the top position"""
        pointer_position = 270  # Top position in OpenCV coordinate system
        segment_angle = (pointer_position - rotation_angle) % 360
        selected_color_index = int(segment_angle / angle_per_segment) % len(colors)
        return colors[selected_color_index]
    
    @staticmethod
    def _draw_selected_color_box(frame, center, selected_color):
        """Draw the selected color display box"""
        box_width = 150
        box_height = 60
        box_top_left = (center[0] - box_width//2, 10)
        box_bottom_right = (center[0] + box_width//2, 10 + box_height)
        
        # Background
        cv2.rectangle(frame, box_top_left, box_bottom_right, config.COLOR_WHITE, -1)
        cv2.rectangle(frame, box_top_left, box_bottom_right, config.COLOR_BLACK, 3)
        
        # Color box
        margin = 5
        color_box_tl = (box_top_left[0] + margin, box_top_left[1] + margin)
        color_box_br = (box_bottom_right[0] - margin, box_bottom_right[1] - margin)
        cv2.rectangle(frame, color_box_tl, color_box_br, 
                     [int(c) for c in selected_color], -1)
        cv2.rectangle(frame, color_box_tl, color_box_br, config.COLOR_BLACK, 2)
        
        # Label
        cv2.putText(frame, "SELECTED", (center[0] - 55, 85), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2)
        cv2.putText(frame, "SELECTED", (center[0] - 55, 85), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_BLACK, 1)
    
    @staticmethod
    def draw_spin_button(frame, wheel_center, wheel_radius, button_state):
        """Draw the spin button with appropriate state"""
        button_width = config.BUTTON_WIDTH
        button_height = config.BUTTON_HEIGHT
        button_x = wheel_center[0] - button_width // 2
        button_y = wheel_center[1] + wheel_radius + config.BUTTON_OFFSET_BELOW_WHEEL
        
        # Determine button appearance based on state
        if button_state['is_spinning']:
            button_color = config.COLOR_GRAY
            text_color = config.COLOR_LIGHT_GRAY
            button_text = "SPINNING..."
            text_scale = 0.8
        elif button_state['is_pressed']:
            button_color = config.COLOR_DARK_GREEN
            text_color = config.COLOR_WHITE
            button_text = "SPIN!"
            text_scale = 1.2
        elif button_state['is_hovered']:
            button_color = config.COLOR_BRIGHT_GREEN
            text_color = config.COLOR_BLACK
            button_text = "SPIN!"
            text_scale = 1.1
        else:
            button_color = config.COLOR_GREEN
            text_color = config.COLOR_WHITE
            button_text = "SPIN!"
            text_scale = 1.0
        
        # Draw shadow
        shadow_offset = 5
        cv2.rectangle(frame, 
                     (button_x + shadow_offset, button_y + shadow_offset),
                     (button_x + button_width + shadow_offset, button_y + button_height + shadow_offset),
                     config.COLOR_SHADOW, -1)
        
        # Draw button
        cv2.rectangle(frame, (button_x, button_y), 
                     (button_x + button_width, button_y + button_height), 
                     button_color, -1)
        
        # Draw border
        border_thickness = 6 if button_state['is_hovered'] else 4
        cv2.rectangle(frame, (button_x, button_y), 
                     (button_x + button_width, button_y + button_height), 
                     config.COLOR_WHITE, border_thickness)
        
        # Draw text
        text_size = cv2.getTextSize(button_text, cv2.FONT_HERSHEY_DUPLEX, text_scale, 3)[0]
        text_x = button_x + (button_width - text_size[0]) // 2
        text_y = button_y + (button_height + text_size[1]) // 2
        
        cv2.putText(frame, button_text, (text_x + 2, text_y + 2), 
                   cv2.FONT_HERSHEY_DUPLEX, text_scale, config.COLOR_BLACK, 3)
        cv2.putText(frame, button_text, (text_x, text_y), 
                   cv2.FONT_HERSHEY_DUPLEX, text_scale, text_color, 3)
        
        # Instruction text
        if not button_state['is_spinning']:
            instruction = "Touch button with finger to spin!"
            inst_size = cv2.getTextSize(instruction, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            inst_x = button_x + (button_width - inst_size[0]) // 2
            cv2.putText(frame, instruction, (inst_x, button_y + button_height + 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2)
        
        return (button_x, button_y, button_width, button_height)
    
    @staticmethod
    def draw_pinch_indicator(frame, hand_landmarks, frame_width, frame_height):
        """Draw visual indicator for pinch gesture"""
        from gesture_detector import GestureDetector
        
        thumb_x, thumb_y = GestureDetector.get_thumb_position(
            hand_landmarks, frame_width, frame_height
        )
        index_x, index_y = GestureDetector.get_index_finger_position(
            hand_landmarks, frame_width, frame_height
        )
        
        is_pinching = GestureDetector.is_pinching(hand_landmarks, config.PINCH_THRESHOLD)
        
        if is_pinching:
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), config.COLOR_GREEN, 3)
            cv2.circle(frame, (thumb_x, thumb_y), 8, config.COLOR_GREEN, -1)
            cv2.circle(frame, (index_x, index_y), 8, config.COLOR_GREEN, -1)
        else:
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), config.COLOR_YELLOW, 2)
            cv2.circle(frame, (thumb_x, thumb_y), 6, config.COLOR_YELLOW, -1)
            cv2.circle(frame, (index_x, index_y), 6, config.COLOR_YELLOW, -1)
    
    @staticmethod
    def draw_hand_indicator(frame, hand_x, hand_y, is_near_wheel, is_near_button):
        """Draw visual indicator for hand position"""
        if is_near_wheel and not is_near_button:
            cv2.circle(frame, (hand_x, hand_y), 15, config.COLOR_GREEN, -1)
            cv2.circle(frame, (hand_x, hand_y), 15, config.COLOR_WHITE, 2)
        elif not is_near_button:
            cv2.circle(frame, (hand_x, hand_y), 10, config.COLOR_RED, -1)
    
    @staticmethod
    def draw_instructions(frame, num_colors, rotation_angle, is_spinning, 
                         hand_near_wheel, button_hovered):
        """Draw instructions and status on screen"""
        h = frame.shape[0]
        x = 10
        
        # Title
        cv2.putText(frame, "Hand-Controlled Color Wheel", 
                   (x, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   config.FONT_SCALE_TITLE, config.COLOR_WHITE, 2)
        
        # Instructions
        cv2.putText(frame, "Instructions:", 
                   (x, h - 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2)
        cv2.putText(frame, "1. PINCH (thumb + index) over SPIN button", 
                   (x, h - 120), cv2.FONT_HERSHEY_SIMPLEX, 
                   config.FONT_SCALE_INSTRUCTIONS, config.COLOR_WHITE, 1)
        cv2.putText(frame, "2. OR grab wheel manually to rotate", 
                   (x, h - 95), cv2.FONT_HERSHEY_SIMPLEX, 
                   config.FONT_SCALE_INSTRUCTIONS, config.COLOR_WHITE, 1)
        cv2.putText(frame, "3. OR press SPACE key to spin", 
                   (x, h - 70), cv2.FONT_HERSHEY_SIMPLEX, 
                   config.FONT_SCALE_INSTRUCTIONS, config.COLOR_WHITE, 1)
        cv2.putText(frame, "Top indicator shows selected color", 
                   (x, h - 45), cv2.FONT_HERSHEY_SIMPLEX, 
                   config.FONT_SCALE_INSTRUCTIONS, config.COLOR_WHITE, 1)
        cv2.putText(frame, "Press 'q' to quit | '+'/'-' for colors", 
                   (x, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                   config.FONT_SCALE_INSTRUCTIONS, config.COLOR_WHITE, 1)
        
        # Status
        status_text = f"Colors: {num_colors} | Angle: {int(rotation_angle)}°"
        if is_spinning:
            status_text += " | 🎡 AUTO-SPINNING"
            status_color = config.COLOR_CYAN
        elif hand_near_wheel:
            status_text += " | ✋ GRABBING"
            status_color = config.COLOR_GREEN
        elif button_hovered:
            status_text += " | 👆 HOVER - PINCH TO SPIN"
            status_color = config.COLOR_YELLOW
        else:
            status_color = config.COLOR_WHITE
        
        cv2.putText(frame, status_text, (x, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, config.FONT_SCALE_STATUS, 
                   status_color, 2)
