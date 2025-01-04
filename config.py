"""Configuration settings for the vehicle detection system"""

# Model settings
YOLO_MODEL = 'yolov8n.pt'  # Using smaller model for better webcam performance
CONFIDENCE_THRESHOLD = 0.5

# Speed calculation
FRAME_BUFFER = 10  # Increased for smoother speed calculations
MIN_DETECTION_FRAMES = 3
SPEED_SMOOTHING_FACTOR = 0.3
SPEED_UNIT = 'km/h'  # or 'mph'

# Camera calibration
CAMERA_HEIGHT = 5.0  # meters
CAMERA_ANGLE = 30.0  # degrees from horizontal
FOCAL_LENGTH = 1000.0  # pixels
REAL_WORLD_WIDTH = 3.5  # meters (typical lane width)

# Speed limits per vehicle type (km/h)
VEHICLE_SPEED_LIMITS = {
    'Car': 120,
    'Motorcycle': 120,
    'Bus': 80,
    'Truck': 100,
    'Van': 120
}

# Vehicle classes mapping (COCO dataset indices)
VEHICLE_CLASSES = {
    2: 'Car',
    5: 'Bus',
    7: 'Truck',
    3: 'Motorcycle',
    0: 'person',
    1: 'bicycle',
    4: 'airplane',
    6: 'train',
    8: 'boat',
}