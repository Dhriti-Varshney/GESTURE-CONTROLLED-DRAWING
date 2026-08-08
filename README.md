# 🔥 Two-Hand Gesture-Controlled Anime Power

A computer vision project that turns **hand gestures into an anime-style energy attack**.

Using a webcam and real-time hand tracking, both hands are used to charge an energy ball made from **purple and red energy with fire-like particles**. Once enough energy is charged, separating the hands launches the energy projectile.

This project is an experiment in combining **computer vision, gesture recognition, particle effects, and interactive graphics**.

---

## ⚡ Features

* 👐 Two-hand gesture detection
* 🔴🟣 Red and purple energy ball
* 🔥 Fire-like particles and energy effects
* ⚡ Energy arcs around the ball
* 📈 Charge system that increases the power of the attack
* 💥 Energy projectile with a glowing trail
* ✨ Particle effects during charging and firing
* 🎯 Projectile direction based on hand movement
* 📷 Real-time webcam interaction

---

## 🎮 Controls

| Gesture / Action             | Effect             |
| ---------------------------- | ------------------ |
| 👐 Both hands close together | Create energy ball |
| 🤲 Hold hands together       | Charge energy      |
| ↔️ Separate hands            | Fire energy ball   |
| `Q`                          | Quit               |

The longer the energy ball is charged, the larger and more powerful the projectile becomes.

---

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – webcam capture, image processing and rendering
* **MediaPipe** – real-time hand landmark detection
* **NumPy** – image and graphics operations
* **Random / Math** – particle movement and energy effects

---

## 📁 Project Structure

```text
GESTURE-CONTROLLED-DRAWING/
│
├── anime.py
├── hand_landmarker.task
├── README.md
├── .gitignore
└── venv/
```

> The `venv` folder should not be uploaded to GitHub. Add it to `.gitignore`.

---

## ⚙️ Installation

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

### 4. Install the required libraries

```bash
pip install opencv-python mediapipe numpy
```

---

## 📦 MediaPipe Model

This project uses the **MediaPipe Hand Landmarker** model to detect hand landmarks.

The required model file is:

```text
hand_landmarker.task
```

Make sure this file is located in the same directory as `anime.py`.

---

## ▶️ Running the Project

Activate the virtual environment:

```bash
source venv/Scripts/activate
```

Then run:

```bash
python anime.py
```

A webcam window should open.

Place both hands in front of the camera and bring them closer together.

---

## 🧠 How It Works

The project follows this pipeline:

```text
             WEBCAM
                ↓
          OpenCV Capture
                ↓
        MediaPipe Hand Tracking
                ↓
        Detect Two Hands
                ↓
       Calculate Hand Positions
                ↓
       Calculate Hand Distance
                ↓
          Energy Charging
                ↓
       ┌────────┴────────┐
       ↓                 ↓
   Energy Ball       Fire Particles
       ↓                 ↓
       └────────┬────────┘
                ↓
         Projectile System
                ↓
          Visual Effects
                ↓
              SCREEN
```

### 1. Hand Detection

MediaPipe detects the landmarks of both hands in real time.

The program uses these landmarks to determine the approximate position of each palm.

### 2. Energy Formation

The distance between the two palms is calculated.

When the hands are close enough, the program enters the **charging state**.

### 3. Charging

While the hands remain together:

* Energy power increases
* The energy ball grows
* Red and purple effects appear
* Fire particles are generated
* Energy arcs appear around the ball

### 4. Firing

When the hands separate after charging, the program creates an energy projectile.

The projectile contains:

* 🔴 Red energy
* 🟣 Purple energy
* 🔥 Fire particles
* ⚡ Energy arcs
* ✨ Glowing core
* 💨 Energy trail

### 5. Particle System

Particles are continuously created around the energy ball and projectile.

Each particle has properties such as:

```text
Position
Velocity
Size
Lifetime
Type
```

This creates the appearance of moving fire and energy.

---

## 🚀 Current Version

### Version 1 — Two-Hand Energy Ball

The current version focuses on:

```text
👐
 ↓
🔴🟣 Charge
 ↓
🔥 Energy Ball
 ↓
💥 Fire
 ↓
🔴🟣 Projectile
```

---

## 🔮 Future Improvements

This project is still being developed. Possible improvements include:

* 🎯 More accurate projectile aiming
* 🤜 Physical forward hand thrust to fire
* 💥 Larger impact explosions
* 🌪️ Shockwaves
* 📳 Camera shake
* ✨ Motion blur
* 🔥 Better fire simulation
* 🛡️ Different defensive gestures
* ⚔️ Multiple attack types
* 🎨 Custom anime-style visual effects
* 🧍 Full-body gesture interaction
* 🎮 Turn the project into a complete gesture-controlled game

---

## 📌 Project Goal

The goal of this project is to explore how **computer vision and gesture recognition can be combined with visual effects to create interactive experiences**.

Instead of controlling an application with a keyboard or mouse, the user becomes the controller.

---

## 👨‍💻 Built With

**Python + OpenCV + MediaPipe**

Created as a hands-on project to learn and experiment with:

* Computer Vision
* Hand Tracking
* Gesture Recognition
* Real-Time Image Processing
* Particle Systems
* Interactive Graphics

---

## ⭐ Future Vision

The long-term goal is to turn this into a complete **gesture-controlled anime combat system**, where different hand gestures trigger different abilities.

```text
👐  → Energy
✊  → Charge
🖐️  → Fire
✌️  → Shield
🤏  → Compress
👊  → Melee Attack
```

More abilities and effects will be added as the project develops.
