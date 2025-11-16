"""Gesture detection utilities for hand tracking"""

import math


class GestureDetector:
    """Detect hand gestures like pinch"""
    
    @staticmethod
    def calculate_pinch_distance(hand_landmarks):
        """Calculate distance between thumb and index finger tips"""
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        
        distance = math.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2
        )
        return distance
    
    @staticmethod
    def is_pinching(hand_landmarks, threshold=0.05):
        """Check if hand is performing a pinch gesture"""
        distance = GestureDetector.calculate_pinch_distance(hand_landmarks)
        return distance < threshold
    
    @staticmethod
    def get_index_finger_position(hand_landmarks, frame_width, frame_height):
        """Get the position of the index finger tip"""
        index_finger = hand_landmarks.landmark[8]
        x = int(index_finger.x * frame_width)
        y = int(index_finger.y * frame_height)
        return x, y
    
    @staticmethod
    def get_thumb_position(hand_landmarks, frame_width, frame_height):
        """Get the position of the thumb tip"""
        thumb = hand_landmarks.landmark[4]
        x = int(thumb.x * frame_width)
        y = int(thumb.y * frame_height)
        return x, y
    
    @staticmethod
    def calculate_hand_angle(hand_landmarks, center_x, center_y, frame_width, frame_height):
        """Calculate angle from center point to index finger tip"""
        hand_x, hand_y = GestureDetector.get_index_finger_position(
            hand_landmarks, frame_width, frame_height
        )
        
        angle = math.atan2(hand_y - center_y, hand_x - center_x)
        return math.degrees(angle), hand_x, hand_y
    
    @staticmethod
    def calculate_distance_to_point(x1, y1, x2, y2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
