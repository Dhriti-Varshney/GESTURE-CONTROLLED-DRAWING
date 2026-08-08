# GESTURE-CONTROLLED-DRAWING
# ✋ Gesture-Controlled Drawing

A real-time computer vision project that allows you to draw on the screen using **hand gestures** through a webcam.

The project uses **MediaPipe** to detect hand landmarks and **OpenCV** to process the webcam feed and create the drawing canvas.

## 🎯 Features

* Real-time hand tracking using a webcam
* Index finger tracking for drawing
* ✊ Fist gesture for erasing
* ✋ Open hand to stop drawing
* Real-time visual feedback of hand landmarks
* Drawing directly on the webcam screen

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – webcam access, image processing and display
* **MediaPipe** – hand landmark detection
* **NumPy** – canvas and image operations

## 📁 Project Structure

```text
GESTURE-CONTROLLED-DRAWING/
│
├── main.py
├── hand_landmarker.task
├── README.md
└── venv/
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd GESTURE-CONTROLLED-DRAWING
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Git Bash on Windows:

```bash
source venv/Scripts/activate
```

### 4. Install dependencies

```bash
pip install opencv-python mediapipe numpy
```

## ▶️ Run the Project

Make sure your webcam is connected and run:

```bash
python main.py
```

A webcam window will open.

### Controls

| Gesture         | Action       |
| --------------- | ------------ |
| ☝️ Index finger | Draw         |
| ✋ Open hand     | Stop drawing |
| ✊ Fist          | Erase        |
| `Q`             | Exit         |

## 🧠 How It Works

The webcam captures live video using OpenCV.

MediaPipe detects the hand and provides the coordinates of different hand landmarks. The program tracks the position of the **index finger** and uses its movement to draw on a virtual canvas.

Different finger positions are used to identify basic gestures:

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Detection
   ↓
Hand Landmarks
   ↓
Gesture Recognition
   ↓
Drawing / Erasing
   ↓
Screen
```

## 🚀 Future Improvements

Some features I plan to explore:

* 🎨 Multiple drawing colors
* 📏 Adjustable brush size
* ↩️ Undo and redo
* 💾 Save drawings as images
* ✌️ More gesture controls
* 🖐️ Improved gesture recognition
* 🎮 Turn the project into a gesture-controlled interactive application

## 📌 Note

This project was built as a learning project to explore **computer vision, hand tracking, gesture recognition, and real-time image processing** using Python.

More improvements and experiments will be added as I continue developing it.
