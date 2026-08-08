import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Tasks API
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Path to the hand tracking model
MODEL_PATH = "hand_landmarker.task"

# Configure hand detector
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7,
)

# Start webcam
cap = cv2.VideoCapture(0)

canvas = None
prev_x, prev_y = None, None

with HandLandmarker.create_from_options(options) as detector:

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Mirror the webcam
        frame = cv2.flip(frame, 1)

        # Create canvas
        if canvas is None:
            canvas = np.zeros_like(frame)

        h, w, _ = frame.shape

        # OpenCV BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hand
        result = detector.detect(mp_image)

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            # Landmark 8 = index finger tip
            index_finger = hand[8]

            x = int(index_finger.x * w)
            y = int(index_finger.y * h)

            # Show finger position
            cv2.circle(
                frame,
                (x, y),
                10,
                (0, 255, 0),
                -1
            )

            # Draw line
            if prev_x is not None and prev_y is not None:

                cv2.line(
                    canvas,
                    (prev_x, prev_y),
                    (x, y),
                    (255, 0, 0),
                    5
                )

            prev_x, prev_y = x, y

        else:
            prev_x, prev_y = None, None

        # Combine camera and drawing
        output = cv2.addWeighted(
            frame,
            0.7,
            canvas,
            0.3,
            0
        )

        cv2.imshow("Gesture Controlled Drawing", output)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()