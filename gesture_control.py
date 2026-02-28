import cv2
import mediapipe as mp
import time
from directkeys import PressKey, ReleaseKey
from directkeys import right_pressed, left_pressed

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

current_key = None
prev_time = 0

with mp_hand.Hands(
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6) as hands:

    while True:
        ret, image = video.read()
        if not ret:
            break

        image = cv2.flip(image, 1)

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = hands.process(rgb)
        rgb.flags.writeable = True

        lmList = []
        mode = "IDLE"
        desired_key = None

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

                for id, lm in enumerate(hand_landmark.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

        if len(lmList) != 0:
            fingers = []

            # Index, Middle, Ring, Pinky
            finger_tips = [8, 12, 16, 20]
            finger_pips = [6, 10, 14, 18]

            for tip, pip in zip(finger_tips, finger_pips):
                if lmList[tip][2] < lmList[pip][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total = fingers.count(1)

            if total == 4:
                mode = "THROTTLE"
                desired_key = right_pressed

            elif total == 0:
                mode = "BRAKE"
                desired_key = left_pressed
            
        # Key Handling (Stable)
        if desired_key != current_key:

            if current_key is not None:
                ReleaseKey(current_key)

            if desired_key is not None:
                PressKey(desired_key)

            current_key = desired_key

        # FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
        prev_time = current_time

        cv2.putText(image, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(image, f"Mode: {mode}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Gesture Hill Climb Control", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
if current_key is not None:
    ReleaseKey(current_key)

video.release()
cv2.destroyAllWindows()