import cv2
import mediapipe as mp
import numpy as np
import math
import random

# ============================================================
# MEDIAPIPE
# ============================================================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL_PATH = "hand_landmarker.task"

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.6,
)

# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# ============================================================
# VARIABLES
# ============================================================

charge = 0.0

charging = False
was_charging = False

previous_midpoint = None

projectile = None

particles = []

screen_flash = 0

# ============================================================
# COLORS - BGR
# ============================================================

PURPLE = (255, 0, 180)
DARK_PURPLE = (180, 0, 100)

RED = (0, 0, 255)
ORANGE = (0, 100, 255)

PINK = (255, 50, 220)
WHITE = (255, 255, 255)

# ============================================================
# PALM CENTER
# ============================================================

def get_palm_center(hand, width, height):

    points = [
        hand[0],   # wrist
        hand[5],   # index base
        hand[9],   # middle base
        hand[13],  # ring base
        hand[17]   # pinky base
    ]

    x = sum(p.x for p in points) / len(points)
    y = sum(p.y for p in points) / len(points)

    return (
        int(x * width),
        int(y * height)
    )


# ============================================================
# DISTANCE
# ============================================================

def distance(p1, p2):

    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


# ============================================================
# NORMALIZE VECTOR
# ============================================================

def normalize(x, y):

    length = math.sqrt(
        x * x + y * y
    )

    if length == 0:
        return 1, 0

    return (
        x / length,
        y / length
    )


# ============================================================
# CREATE ENERGY PARTICLES
# ============================================================

def create_energy_particles(
    center_x,
    center_y,
    amount,
    radius
):

    for _ in range(amount):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        distance_from_center = random.uniform(
            radius * 0.7,
            radius * 1.4
        )

        x = (
            center_x +
            math.cos(angle) * distance_from_center
        )

        y = (
            center_y +
            math.sin(angle) * distance_from_center
        )

        speed = random.uniform(
            1,
            5
        )

        particles.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.randint(15, 35),
            "size": random.randint(2, 5),
            "type": random.choice([
                "fire",
                "energy"
            ])
        })


# ============================================================
# UPDATE PARTICLES
# ============================================================

def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["life"] -= 1

        particle["vx"] *= 0.98
        particle["vy"] *= 0.98

        if particle["life"] <= 0:

            particles.remove(
                particle
            )


# ============================================================
# DRAW PARTICLES
# ============================================================

def draw_particles(frame):

    for particle in particles:

        x = int(particle["x"])
        y = int(particle["y"])

        size = particle["size"]

        if particle["type"] == "fire":

            color = random.choice([
                RED,
                ORANGE,
                (0, 180, 255)
            ])

        else:

            color = random.choice([
                PURPLE,
                PINK,
                WHITE
            ])

        cv2.circle(
            frame,
            (x, y),
            size,
            color,
            -1
        )


# ============================================================
# DRAW ENERGY ORB
# ============================================================

def draw_energy_ball(
    frame,
    x,
    y,
    radius
):

    # --------------------------------------------------------
    # BIG PURPLE GLOW
    # --------------------------------------------------------

    for r in range(
        int(radius * 2.5),
        int(radius),
        -8
    ):

        overlay = frame.copy()

        cv2.circle(
            overlay,
            (x, y),
            r,
            PURPLE,
            -1
        )

        alpha = 0.025

        frame[:] = cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1 - alpha,
            0
        )

    # --------------------------------------------------------
    # RED INNER GLOW
    # --------------------------------------------------------

    overlay = frame.copy()

    cv2.circle(
        overlay,
        (x, y),
        int(radius * 1.25),
        RED,
        -1
    )

    frame[:] = cv2.addWeighted(
        overlay,
        0.12,
        frame,
        0.88,
        0
    )

    # --------------------------------------------------------
    # PURPLE OUTER BALL
    # --------------------------------------------------------

    cv2.circle(
        frame,
        (x, y),
        int(radius),
        PURPLE,
        -1
    )

    # --------------------------------------------------------
    # RED ENERGY CORE
    # --------------------------------------------------------

    cv2.circle(
        frame,
        (x, y),
        int(radius * 0.72),
        RED,
        -1
    )

    # --------------------------------------------------------
    # WHITE HOT CENTER
    # --------------------------------------------------------

    cv2.circle(
        frame,
        (x, y),
        int(radius * 0.35),
        WHITE,
        -1
    )

    # --------------------------------------------------------
    # ENERGY RINGS
    # --------------------------------------------------------

    cv2.circle(
        frame,
        (x, y),
        int(radius * 1.35),
        PINK,
        2
    )

    cv2.circle(
        frame,
        (x, y),
        int(radius * 1.65),
        RED,
        2
    )


# ============================================================
# FIRE / ENERGY ARCS
# ============================================================

def draw_energy_arcs(
    frame,
    x,
    y,
    radius
):

    points = 20

    for color in [
        PURPLE,
        RED,
        ORANGE
    ]:

        pts = []

        start_angle = random.uniform(
            0,
            math.pi * 2
        )

        for i in range(points):

            angle = (
                start_angle +
                i * (math.pi * 2 / points)
            )

            variation = random.uniform(
                0.85,
                1.2
            )

            r = radius * variation

            px = int(
                x +
                math.cos(angle) * r
            )

            py = int(
                y +
                math.sin(angle) * r
            )

            pts.append(
                (px, py)
            )

        for i in range(
            0,
            len(pts) - 1,
            2
        ):

            cv2.line(
                frame,
                pts[i],
                pts[i + 1],
                color,
                random.randint(1, 3)
            )


# ============================================================
# FIRE TRAIL
# ============================================================

def draw_projectile(
    frame,
    projectile
):

    if projectile is None:
        return

    x = int(
        projectile["x"]
    )

    y = int(
        projectile["y"]
    )

    radius = projectile["radius"]

    vx = projectile["vx"]
    vy = projectile["vy"]

    # --------------------------------------------------------
    # TRAIL
    # --------------------------------------------------------

    for i in range(
        12,
        0,
        -1
    ):

        trail_x = int(
            x - vx * i * 2
        )

        trail_y = int(
            y - vy * i * 2
        )

        trail_radius = max(
            2,
            int(radius * (1 - i / 15))
        )

        color = (
            RED
            if i % 2 == 0
            else PURPLE
        )

        cv2.circle(
            frame,
            (trail_x, trail_y),
            trail_radius,
            color,
            -1
        )

    # --------------------------------------------------------
    # MAIN BALL
    # --------------------------------------------------------

    draw_energy_ball(
        frame,
        x,
        y,
        radius
    )

    draw_energy_arcs(
        frame,
        x,
        y,
        radius
    )


# ============================================================
# EXPLOSION
# ============================================================

def explosion(
    x,
    y
):

    global screen_flash

    screen_flash = 10

    for _ in range(100):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            3,
            15
        )

        particles.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.randint(
                20,
                50
            ),
            "size": random.randint(
                3,
                8
            ),
            "type": random.choice([
                "fire",
                "energy"
            ])
        })


# ============================================================
# MAIN
# ============================================================

with HandLandmarker.create_from_options(
    options
) as detector:

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Mirror webcam
        frame = cv2.flip(
            frame,
            1
        )

        height, width, _ = frame.shape

        # ====================================================
        # HAND DETECTION
        # ====================================================

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = detector.detect(
            mp_image
        )

        # ====================================================
        # TWO HANDS
        # ====================================================

        if len(result.hand_landmarks) >= 2:

            hand1 = result.hand_landmarks[0]
            hand2 = result.hand_landmarks[1]

            palm1 = get_palm_center(
                hand1,
                width,
                height
            )

            palm2 = get_palm_center(
                hand2,
                width,
                height
            )

            # ------------------------------------------------
            # DISTANCE BETWEEN HANDS
            # ------------------------------------------------

            hand_distance = distance(
                palm1,
                palm2
            )

            # ------------------------------------------------
            # MIDPOINT
            # ------------------------------------------------

            center_x = int(
                (palm1[0] + palm2[0]) / 2
            )

            center_y = int(
                (palm1[1] + palm2[1]) / 2
            )

            # ------------------------------------------------
            # DRAW HAND LANDMARKS
            # ------------------------------------------------

            for hand in [
                hand1,
                hand2
            ]:

                for landmark in hand:

                    lx = int(
                        landmark.x * width
                    )

                    ly = int(
                        landmark.y * height
                    )

                    cv2.circle(
                        frame,
                        (lx, ly),
                        3,
                        PINK,
                        -1
                    )

            # ------------------------------------------------
            # CONNECTION BETWEEN HANDS
            # ------------------------------------------------

            cv2.line(
                frame,
                palm1,
                palm2,
                PURPLE,
                2
            )

            # =================================================
            # CHARGING
            # =================================================

            if hand_distance < width * 0.48:

                charging = True

                # More charge while hands stay together
                charge += 1.2

                charge = min(
                    charge,
                    100
                )

                # ------------------------------------------------
                # BALL SIZE
                # ------------------------------------------------

                radius = int(
                    20 +
                    charge * 0.75
                )

                # ------------------------------------------------
                # ENERGY
                # ------------------------------------------------

                draw_energy_ball(
                    frame,
                    center_x,
                    center_y,
                    radius
                )

                draw_energy_arcs(
                    frame,
                    center_x,
                    center_y,
                    radius
                )

                create_energy_particles(
                    center_x,
                    center_y,
                    8,
                    radius
                )

                # ------------------------------------------------
                # HAND AURA
                # ------------------------------------------------

                cv2.circle(
                    frame,
                    palm1,
                    20,
                    RED,
                    2
                )

                cv2.circle(
                    frame,
                    palm2,
                    20,
                    PURPLE,
                    2
                )

            else:

                charging = False

            # =================================================
            # FIRE
            # =================================================

            # If we were charging and hands suddenly separate
            if (
                was_charging
                and not charging
                and charge > 15
            ):

                # ------------------------------------------------
                # FIND DIRECTION
                # ------------------------------------------------

                if previous_midpoint is not None:

                    dx = (
                        center_x -
                        previous_midpoint[0]
                    )

                    dy = (
                        center_y -
                        previous_midpoint[1]
                    )

                    # If movement is too small,
                    # shoot toward the right
                    if abs(dx) + abs(dy) < 10:

                        dx = 1
                        dy = 0

                else:

                    dx = 1
                    dy = 0

                dx, dy = normalize(
                    dx,
                    dy
                )

                # ------------------------------------------------
                # PROJECTILE
                # ------------------------------------------------

                projectile = {

                    "x": center_x,

                    "y": center_y,

                    "vx": dx * 18,

                    "vy": dy * 18,

                    "radius": int(
                        20 +
                        charge * 0.45
                    )
                }

                create_energy_particles(
                    center_x,
                    center_y,
                    40,
                    80
                )

                charge = 0

            previous_midpoint = (
                center_x,
                center_y
            )

        else:

            charging = False

        # =====================================================
        # PROJECTILE MOVEMENT
        # =====================================================

        if projectile is not None:

            projectile["x"] += (
                projectile["vx"]
            )

            projectile["y"] += (
                projectile["vy"]
            )

            # Fire particles behind projectile
            create_energy_particles(
                projectile["x"],
                projectile["y"],
                5,
                projectile["radius"]
            )

            draw_projectile(
                frame,
                projectile
            )

            # ------------------------------------------------
            # OFF SCREEN
            # ------------------------------------------------

            if (
                projectile["x"] < -150
                or projectile["x"] > width + 150
                or projectile["y"] < -150
                or projectile["y"] > height + 150
            ):

                explosion(
                    projectile["x"],
                    projectile["y"]
                )

                projectile = None

        # =====================================================
        # PARTICLES
        # =====================================================

        update_particles()

        draw_particles(
            frame
        )

        # =====================================================
        # UI
        # =====================================================

        if charging:

            status = "CHARGING"

        elif projectile is not None:

            status = "FIRE!!!"

        else:

            status = "READY"

        cv2.putText(
            frame,
            f"STATUS: {status}",
            (30, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            WHITE,
            2
        )

        cv2.putText(
            frame,
            f"POWER: {int(charge)}%",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            RED,
            2
        )

        cv2.putText(
            frame,
            "TWO HANDS = ENERGY",
            (30, height - 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            PURPLE,
            2
        )

        cv2.putText(
            frame,
            "SEPARATE HANDS = FIRE",
            (30, height - 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            RED,
            2
        )

        # =====================================================
        # SCREEN FLASH
        # =====================================================

        if screen_flash > 0:

            overlay = frame.copy()

            overlay[:] = (
                100,
                0,
                255
            )

            alpha = (
                screen_flash / 30
            )

            frame = cv2.addWeighted(
                overlay,
                alpha,
                frame,
                1 - alpha,
                0
            )

            screen_flash -= 1

        # =====================================================
        # DISPLAY
        # =====================================================

        cv2.imshow(
            "ANIME POWER SYSTEM - TWO HANDS",
            frame
        )

        # Q = quit
        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


cap.release()

cv2.destroyAllWindows()