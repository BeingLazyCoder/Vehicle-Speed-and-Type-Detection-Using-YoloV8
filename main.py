"""Main entry point for the vehicle speed detection system"""
import sys
import os
import logging
from video_processor import VideoProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Get video source
        if len(sys.argv) > 1:
            video_source = sys.argv[1]
            if not os.path.exists(video_source):
                logger.error(f"Video file not found: {video_source}")
                return
        else:
            video_source = 0  # Default to webcam
        
        print("Vehicle Speed Detection System")
        print("------------------------------")
        print(f"Source: {'Webcam' if video_source == 0 else video_source}")
        print("Press 'q' to quit")
        
        processor = VideoProcessor(video_source)
        processor.process_video()
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()