 🚗💨 Vehicle Speed Detection System

 🎥 Real-time Traffic Monitoring and Speed Enforcement

🌟 What It Does

This system uses artificial intelligence to detect vehicles in video streams, 
track their movement, and calculate their speeds in real-time. It can:

🚙 Identify different types of vehicles (cars, trucks, buses, motorcycles)
🏎️ Measure vehicle speeds accurately
🚦 Detect and log speed limit violations
📊 Display real-time results on screen


🧩 System Components

Our Vehicle Speed Detection System is composed of several interconnected components,
each playing a crucial role in the overall functionality. 
Here's a detailed breakdown of each component:

 1. 🎬 Main Application (`main.py`)
🚀 Serves as the entry point for the entire system
🎭 Handles command-line arguments for video source selection
🏁 Initializes and kicks off the video processing pipeline

 2. 🎞️ Video Processor (`video_processor.py`)
🧠 Acts as the central brain of the system
🔄 Coordinates interactions between all other components
🖥️ Manages the main processing loop for each video frame
🎚️ Implements performance optimizations like selective frame processing

 3. 🚗 Vehicle Detector (`detector.py`)
👁️ Utilizes YOLOv8 AI model for real-time object detection
🔍 Identifies and locates vehicles in each processed frame
🏷️ Classifies detected objects into vehicle categories (e.g., car, truck, bus, motorcycle)
🎯 Applies confidence thresholding to minimize false positives

4. 🖼️ Visualizer (`visualizer.py`)
🎨 Draws bounding boxes around detected vehicles on the video frame
📝 Overlays vehicle information (type, speed) on the video
🚦 Color-codes speed displays based on speed limit compliance
🖥️ Manages the on-screen display of processing statistics (e.g., FPS counter)

 5. 📊 Data Logger (`data_logger.py`)
📝 Records speed limit violations in real-time
📅 Timestamps each violation entry
📂 Saves violation data to an Excel file for later analysis
🔒 Ensures data integrity with proper file handling and error management

 6. 📹 Video Capture (`video_capture.py`)
🎥 Handles video input from various sources (webcam, video files)
🧵 Implements multi-threading for efficient frame capture
🛠️ Provides fallback options and error handling for different video backends

 7. ⏱️ Speed Tracker (`speed_tracker.py`)
📍 Maintains position history for each detected vehicle
🧮 Calculates vehicle speeds based on position changes over time
🔢 Implements algorithms to smooth speed calculations and reduce fluctuations

 8. 🧮 Speed Calculator (`speed_calculator.py`)
📐 Converts pixel movements to real-world speed measurements
🧪 Applies statistical methods to filter out anomalies in speed data
🎚️ Adapts calculations based on camera perspective and positioning

 9. 📏 Calibration (`calibration.py`)
📐 Handles camera calibration parameters
🗺️ Translates pixel coordinates to real-world distances
🔧 Provides functions to adjust for camera angle and positioning

 10. ⚙️ Configuration (`config.py`)
🎛️ Centralizes all system-wide settings and parameters
🚥 Defines speed limits for different vehicle types
🎚️ Allows easy tuning of detection and tracking parameters
🗃️ Stores mappings for vehicle classes and their corresponding indices

 🛠️ How It Works

1. Video Input: Uses your webcam or a video file
2. Vehicle Detection: Spots vehicles using YOLOv8 AI
3. Tracking: Follows each vehicle across video frames
4. Speed Calculation: Estimates speed based on vehicle movement
5. Visualization: Shows results on screen with bounding boxes and speed info
6. Logging: Records speed violations in an Excel file

 📋 Requirements

Python 3.8 or newer
OpenCV
NumPy
Ultralytics YOLOv8
openpyxl
SciPy

🏃‍➡️🏃‍➡️🏃‍➡️Before Run the Program 🏃‍➡️🏃‍➡️🏃‍➡️:
  Install the required packages:
   ( pip install opencv-python numpy ultralytics openpyxl scipy ) 📏📏OR📏📏 ( pip install -r requirements.txt )

3. Run the Program:
For webcam: `python main.py`
For video file: `python main.py path/to/your/video.mp4`

4. Controls:
Press 'q' to quit
Press 's' to save a screenshot

 ⚙️ Customization

Edit `config.py` to change:
🎯 Detection sensitivity
🏁 Speed calculation settings
🚄 Speed limits for different vehicles

 📊 What You'll See

Live video with:
Boxes around detected vehicles
Vehicle types (car, truck, etc.)
Calculated speeds
Frames per second (FPS) count
`speed_violations.xlsx` file with logged violations

# ScreeShot......
![Screenshot 2025-01-01 130247](https://github.com/user-attachments/assets/d5ef54c7-5682-4c71-8a85-068ba63f51cc)
![Screenshot 2025-01-04 140027](https://github.com/user-attachments/assets/08ab6622-7f20-40d6-8e52-8272823400b4)


 💡 Tips for Best Results

📏 Calibrate the camera settings in `config.py` for your setup
🎥 Use high-quality video input for better accuracy
💻 A computer with a good GPU will run the system faster

 🔮 Future Plans

Night-time detection improvements
License plate recognition
Web interface for remote monitoring
Integration with traffic management systems

 🤝 Want to Contribute?

We welcome your ideas and code contributions! Here's how:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

 📄 License

This project is a Open Source Project.

 👥 Team

[ABHISHEK SINGH](https://github.com/BeingLazyCoder) Project Lead and Creater.

 📞 Need Help?
🐛 Issues: [GitHub Issues Page](https://github.com/BeingLazyCoder/Vehicle-Speed-and-Type-Detection-Using-YoloV8/issues)

---

🌟 Created with passion by [ABHISHEK SINGH] 🌟
