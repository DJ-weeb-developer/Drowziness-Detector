# 👁️ Real-Time Drowsiness Detector

A robust, computer-vision-based drowsiness detection system that uses **MediaPipe Face Mesh** to monitor driver fatigue in real-time. By analyzing the **Eye Aspect Ratio (EAR)** and counting blinks, the system triggers alerts when it identifies signs of sleepiness or prolonged eye closure.

## ✨ Key Features

* **High-Fidelity Tracking**: Leverages 468+ facial landmarks via MediaPipe for precise eye contour detection.
* **Adaptive Lighting (CLAHE)**: Normalizes frame lighting using Contrast Limited Adaptive Histogram Equalization, making the detector reliable in low-light or high-glare environments.
* **Smart Fatigue Metrics**:
* **EAR Analysis**: Tracks the vertical vs. horizontal eye ratio to detect micro-sleeps.
* **Blink Counter**: Automatically logs total blinks during a session.
* **Fatigue Duration**: Records exactly how long a user has been in a "drowsy" state.


* **Audio-Visual Alerts**: Integrated with an `AudioAlert` system to trigger sirens and on-screen warnings when the EAR stays below **0.25** for more than **20 consecutive frames**.

---

## 🛠️ Tech Stack

* **Core Logic**: Python
* **Computer Vision**: [OpenCV](https://opencv.org/) (Image processing & CLAHE)
* **AI Framework**: [MediaPipe](https://www.google.com/search?q=https://google.github.io/mediapipe/) (Face Mesh & Landmarks)
* **Math**: [NumPy](https://numpy.org/) (Euclidean distance & Matrix operations)

---

## 🧠 How It Works: The Science

The core of this detector is the **Eye Aspect Ratio (EAR)**. For each eye, the script identifies 6 specific landmarks:

* **Left Eye Indices**: `[362, 385, 387, 263, 373, 380]`
* **Right Eye Indices**: `[33, 160, 158, 133, 153, 144]`

The ratio is calculated as:

When the eyes are open, the EAR is relatively constant. When a blink or micro-sleep occurs, the EAR drops significantly toward zero.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* Webcam

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/drowsiness-detector.git
cd drowsiness-detector

```


2. **Install dependencies**:
```bash
pip install opencv-python mediapipe numpy

```



### Usage

Run the main script (assuming your entry point is `main.py`):

```python
from drowsiness_detector import DrowsinessDetector
import cv2

detector = DrowsinessDetector()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break
    
    # The detector handles resizing, lighting, and EAR logic
    processed_frame = detector.process_frame(frame)
    
    cv2.imshow('Drowsiness Detector', processed_frame)
    if cv2.waitKey(5) & 0xFF == 27: break

detector.close()
cap.release()

```

---

## ⚙️ Configuration

You can fine-tune the sensitivity in the `DrowsinessDetector` class constructor:

* `EAR_THRESHOLD (0.25)`: The value below which an eye is considered closed.
* `CONSEC_FRAMES_DROWSY (20)`: How many frames the eyes must be closed to trigger the alarm.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ for Road Safety.**
