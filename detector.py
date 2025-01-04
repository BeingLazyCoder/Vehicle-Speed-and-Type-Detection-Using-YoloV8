"""Vehicle detection using YOLOv8"""
from ultralytics import YOLO
from dataclasses import dataclass
import numpy as np
import config

@dataclass
class Detection:
    track_id: int
    class_name: str
    bbox: tuple
    confidence: float

class VehicleDetector:
    def __init__(self):
        self.model = YOLO(config.YOLO_MODEL)
        
    def detect(self, frame):
        try:
            # Run inference with tracking
            results = self.model.track(
                frame,
                persist=True,
                classes=list(config.VEHICLE_CLASSES.keys()),
                conf=config.CONFIDENCE_THRESHOLD,
                verbose=False
            )[0]
            
            detections = []
            
            if hasattr(results, 'boxes') and results.boxes is not None:
                boxes = results.boxes.cpu().numpy()
                
                for box in boxes:
                    # Check if we have tracking ID
                    if box.id is None:
                        continue
                        
                    # Get class name
                    class_id = int(box.cls[0])
                    if class_id not in config.VEHICLE_CLASSES:
                        continue
                    
                    detection = Detection(
                        track_id=int(box.id[0]),
                        class_name=config.VEHICLE_CLASSES[class_id],
                        bbox=tuple(box.xyxy[0]),
                        confidence=float(box.conf[0])
                    )
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Error during detection: {str(e)}")
            return []