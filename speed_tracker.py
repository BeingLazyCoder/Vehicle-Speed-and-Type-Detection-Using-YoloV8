"""Track vehicle positions and calculate speeds"""
import cv2
import numpy as np
from collections import deque
from typing import Dict, Tuple, Deque
import config
from detector import Detection
from calibration import get_scaling_factor
from speed_calculator import calculate_speed

class SpeedTracker:
    def __init__(self):
        self.positions: Dict[int, Deque[Tuple[float, float, float]]] = {}
        self.speeds: Dict[int, Deque[float]] = {}
        self.frame_height: float = None
        self.last_speeds: Dict[int, float] = {}  # Cache for last calculated speeds
        
    def get_last_speed(self, track_id: int) -> float:
        """Get the last calculated speed for a track"""
        return self.last_speeds.get(track_id, 0.0)
        
    def update(self, detection: Detection, frame_height: float) -> float:
        """Update tracker with new detection and return speed"""
        try:
            if self.frame_height is None:
                self.frame_height = frame_height
                
            track_id = detection.track_id
            center_x = (detection.bbox[0] + detection.bbox[2]) / 2
            center_y = (detection.bbox[1] + detection.bbox[3]) / 2
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            
            # Initialize tracking for new vehicle
            if track_id not in self.positions:
                self.positions[track_id] = deque(maxlen=config.FRAME_BUFFER)
                self.speeds[track_id] = deque(maxlen=config.FRAME_BUFFER)
            
            # Add current position
            self.positions[track_id].append((center_x, center_y, current_time))
            
            # Calculate speed if we have enough frames
            if len(self.positions[track_id]) >= config.MIN_DETECTION_FRAMES:
                # Get scaling factor
                scale = get_scaling_factor(detection.bbox, frame_height, config.__dict__)
                
                # Calculate speed
                speed = calculate_speed(list(self.positions[track_id]), scale)
                
                # Apply smoothing
                if self.speeds[track_id]:
                    prev_speed = self.speeds[track_id][-1]
                    speed = (prev_speed * (1 - config.SPEED_SMOOTHING_FACTOR) + 
                            speed * config.SPEED_SMOOTHING_FACTOR)
                
                self.speeds[track_id].append(speed)
                self.last_speeds[track_id] = speed  # Cache the speed
                return speed
                    
            return 0.0
            
        except Exception as e:
            print(f"Error calculating speed: {e}")
            return 0.0
            
    def cleanup(self):
        """Remove old tracks"""
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        for track_id in list(self.positions.keys()):
            if self.positions[track_id]:
                last_update = self.positions[track_id][-1][2]
                if current_time - last_update > 1.0:  # Remove after 1 second of no updates
                    del self.positions[track_id]
                    del self.speeds[track_id]
                    del self.last_speeds[track_id]