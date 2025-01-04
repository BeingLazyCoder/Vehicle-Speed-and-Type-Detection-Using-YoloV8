"""Main video processing module"""
import cv2
import time
import logging
import numpy as np
from detector import VehicleDetector
from speed_tracker import SpeedTracker
from visualizer import Visualizer
from video_capture import ThreadedVideoCapture
from data_logger import SpeedLogger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self, source):
        try:
            self.video = ThreadedVideoCapture(source)
            logger.info(f"Successfully opened video source: {source}")
            logger.info(f"Resolution: {self.video.frame_width}x{self.video.frame_height}")
            logger.info(f"FPS: {self.video.fps}")
            
            # Initialize components
            self.detector = VehicleDetector()
            self.speed_tracker = SpeedTracker()
            self.visualizer = Visualizer()
            self.logger = SpeedLogger()
            
            # Performance optimization
            self.process_every_n_frames = 2
            self.frame_counter = 0
            self.last_detections = []
            
        except Exception as e:
            logger.error(f"Failed to initialize video processor: {str(e)}")
            raise
        
    def process_video(self):
        try:
            frame_count = 0
            start_time = time.time()
            fps_update_interval = 30
            
            while True:
                ret, frame = self.video.read()
                if not ret or frame is None:
                    break
                    
                if frame.size == 0:
                    continue
                
                self.frame_counter += 1
                
                # Process only every nth frame for detection
                if self.frame_counter % self.process_every_n_frames == 0:
                    self.last_detections = self.detector.detect(frame)
                    
                    # Process each detection
                    for det in self.last_detections:
                        speed = self.speed_tracker.update(det, self.video.frame_height)
                        self.visualizer.draw(frame, det, speed)
                        # Log speed violation
                        self.logger.log_violation(det.class_name, speed)
                else:
                    # Use last detections for intermediate frames
                    for det in self.last_detections:
                        speed = self.speed_tracker.get_last_speed(det.track_id)
                        self.visualizer.draw(frame, det, speed)
                
                # Update FPS counter
                frame_count += 1
                if frame_count % fps_update_interval == 0:
                    current_time = time.time()
                    fps = fps_update_interval / (current_time - start_time)
                    start_time = current_time
                    self.visualizer.draw_fps(frame, fps)
                
                # Display frame
                cv2.imshow('Vehicle Speed Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise
            
        finally:
            # Save violations before closing
            self.logger.save()
            self.video.release()
            cv2.destroyAllWindows()
