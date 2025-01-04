"""Threaded video capture module"""
import cv2
from threading import Thread
from queue import Queue
import time

class ThreadedVideoCapture:
    def __init__(self, source, queue_size=3):
        self.source = source
        self.queue = Queue(maxsize=queue_size)
        self.stopped = False
        self.cap = None
        self.initialize_capture()
        
    def initialize_capture(self):
        """Initialize video capture with fallback options"""
        if isinstance(self.source, int):  # Webcam
            # Try different backends
            backends = [cv2.CAP_ANY, cv2.CAP_DSHOW, cv2.CAP_V4L2, cv2.CAP_MSMF]
            for backend in backends:
                self.cap = cv2.VideoCapture(self.source, backend)
                if self.cap.isOpened():
                    break
                self.cap.release()
        else:  # Video file
            self.cap = cv2.VideoCapture(self.source)
            
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError(f"Failed to open video source: {self.source}")
            
        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps <= 0:  # Invalid FPS (common with webcams)
            self.fps = 30.0
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Set buffer size
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        
        # Start capture thread
        self.thread = Thread(target=self._capture, daemon=True)
        self.thread.start()
    
    def _capture(self):
        while not self.stopped:
            if not self.queue.full():
                ret, frame = self.cap.read()
                if not ret:
                    self.stopped = True
                    break
                    
                if not self.queue.full():
                    self.queue.put(frame)
            else:
                time.sleep(0.001)
    
    def read(self):
        if self.stopped and self.queue.empty():
            return False, None
        return True, self.queue.get()
    
    def is_opened(self):
        return self.cap is not None and self.cap.isOpened()
    
    def release(self):
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join()
        if self.cap:
            self.cap.release()