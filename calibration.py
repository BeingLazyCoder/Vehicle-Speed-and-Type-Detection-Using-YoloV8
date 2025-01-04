"""Camera calibration and real-world measurements"""
import math
import numpy as np
from typing import Tuple

def calculate_real_distance(
    pixel_height: float,
    y_position: float,
    frame_height: float,
    config: dict
) -> float:
    """Calculate real-world distance using camera parameters"""
    # Convert angle to radians
    angle_rad = math.radians(config['CAMERA_ANGLE'])
    
    # Calculate distance using perspective projection
    relative_y = (frame_height - y_position) / frame_height
    distance = config['CAMERA_HEIGHT'] * math.tan(angle_rad + 
               math.atan(relative_y * math.tan(math.pi/3)))
    
    return distance

def get_scaling_factor(
    bbox: Tuple[float, float, float, float],
    frame_height: float,
    config: dict
) -> float:
    """Calculate scaling factor based on position in frame"""
    _, y1, _, y2 = bbox
    center_y = (y1 + y2) / 2
    
    # Calculate distance from camera
    distance = calculate_real_distance(y2 - y1, center_y, frame_height, config)
    
    # Calculate scaling factor
    return config['REAL_WORLD_WIDTH'] / distance