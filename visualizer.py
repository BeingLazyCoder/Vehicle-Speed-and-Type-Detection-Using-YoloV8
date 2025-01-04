"""Visualization utilities for vehicle detection"""
import cv2
import numpy as np
import config

class Visualizer:
    def __init__(self):
        self.colors = {
            'Car': (0, 255, 0),      # Green
            'Bus': (255, 165, 0),    # Orange
            'Truck': (0, 165, 255),  # Brown
            'Motorcycle': (0, 255, 255)  # Yellow
        }
        self.default_limits = {
            'car': 120,
            'motorcycle': 120,
            'bus': 80,
            'truck': 100
        }
        
    def get_speed_color(self, speed: float, vehicle_type: str):
        vehicle_type = vehicle_type.lower()
        default = self.default_limits.get(vehicle_type, 100)
        speed_limit = config.VEHICLE_SPEED_LIMITS.get(vehicle_type, default)
        
        if speed < speed_limit * 0.8:  # Under 80% of limit
            return (0, 255, 0)  # Green
        elif speed < speed_limit:  # Under limit
            return (0, 255, 255)  # Yellow
        return (0, 0, 255)  # Red - Over limit
        
    def draw(self, frame, detection, speed):
        """Draw detection box and speed"""
        try:
            x1, y1, x2, y2 = [int(c) for c in detection.bbox]
            
            # Get colors
            vehicle_color = self.colors.get(detection.class_name.lower(), (0, 255, 0))
            speed_color = self.get_speed_color(speed, detection.class_name)
            
            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), vehicle_color, 2)
            
            # Prepare text
            vehicle_type = detection.class_name.lower()
            default = self.default_limits.get(vehicle_type, 100)
            speed_limit = config.VEHICLE_SPEED_LIMITS.get(vehicle_type, default)
            
            # Prepare text
            speed_limit = config.VEHICLE_SPEED_LIMITS.get(detection.class_name.lower(), 150)
            speed_text = f"{speed:.1f} km/h"
            class_text = f"{detection.class_name}"
            
            # Draw background for text
            text_scale = 0.7
            thickness = 2
            padding = 5
            
            for i, text in enumerate([class_text, speed_text]):
                (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, text_scale, thickness)
                text_y = y1 - 10 - (i * (text_h + padding))
                
                # Background rectangle
                cv2.rectangle(
                    frame,
                    (x1, text_y - text_h - padding),
                    (x1 + text_w + padding * 2, text_y + padding),
                    vehicle_color if i == 0 else speed_color,
                    -1
                )
                
                # Text
                cv2.putText(
                    frame,
                    text,
                    (x1 + padding, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    text_scale,
                    (255, 255, 255),
                    thickness
                )
                
        except Exception as e:
            print(f"Error drawing detection: {e}")
            
    def draw_fps(self, frame, fps):
        """Draw FPS counter"""
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )