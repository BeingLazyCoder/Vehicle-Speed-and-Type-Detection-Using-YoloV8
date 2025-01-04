import numpy as np
from typing import List, Tuple
import logging
from scipy import stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_positions(positions: List[Tuple[float, float, float]]) -> bool:
    """Validates position data for speed calculation"""
    return bool(positions and len(positions) >= 2 and all(len(p) == 3 for p in positions))

def detect_motion(positions: List[Tuple[float, float, float]], min_displacement: float = 1.0) -> bool:
    """Detects if significant motion occurred"""
    if not positions:
        return False
    start = np.array(positions[0][:2])
    end = np.array(positions[-1][:2])
    return np.linalg.norm(end - start) >= min_displacement

def calculate_speed(positions: List[Tuple[float, float, float]], scale: float = 1.0) -> float:
    """
    Calculate vehicle speed from position history
    Args:
        positions: List of (x, y, timestamp) tuples
        scale: Pixels to meters conversion factor
    Returns:
        Speed in km/h
    """
    try:
        if not validate_positions(positions):
            logger.warning("Invalid position data")
            return 0.0

        # Constants
        MIN_SPEED = 1.0  # km/h
        MAX_SPEED = 150.0  # km/h
        MIN_TIME_DELTA = 0.01  # seconds
        
        # Convert to numpy array
        pos_array = np.array(positions, dtype=float)
        
        # Check for motion
        if not detect_motion(positions):
            logger.debug("No significant motion detected")
            return 0.0

        # Calculate distances between consecutive points
        distances = np.sqrt(
            np.sum(
                np.square(
                    pos_array[1:, :2] - pos_array[:-1, :2]
                ),
                axis=1
            )
        ) * scale  # Convert to meters

        # Calculate time differences
        time_diffs = pos_array[1:, 2] - pos_array[:-1, 2]
        
        # Valid measurements filter
        valid_mask = time_diffs >= MIN_TIME_DELTA
        
        if not np.any(valid_mask):
            logger.debug("No valid time measurements")
            return 0.0

        # Calculate instantaneous speeds (km/h)
        speeds = (distances[valid_mask] / time_diffs[valid_mask]) * 3.6

        # Remove outliers using Z-score
        z_scores = np.abs(stats.zscore(speeds))
        speeds = speeds[z_scores < 2.0]
        
        # Apply physical limits
        speeds = speeds[(speeds >= MIN_SPEED) & (speeds <= MAX_SPEED)]

        if len(speeds) == 0:
            logger.debug("No valid speeds after filtering")
            return 0.0

        # Use median for robustness
        final_speed = float(np.median(speeds))
        logger.debug(f"Calculated speed: {final_speed:.1f} km/h")
        
        return final_speed

    except Exception as e:
        logger.error(f"Speed calculation error: {str(e)}")
        return 0.0