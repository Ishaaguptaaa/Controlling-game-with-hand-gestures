import cv2
import mediapipe as mp
import util
import pyautogui
import time

# Screen size
screen_width, screen_height = pyautogui.size()

# MediaPipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)
draw = mp.solutions.drawing_utils

# Track previous direction
prev_direction = None
frame_count = 0

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def move_player(index_finger_tip, center_x=0.5, threshold=0.05):
    global prev_direction

    if index_finger_tip:
        x = index_finger_tip.x
        y = index_finger_tip.y

        direction = None

        if x < center_x - threshold:
            direction = 'left'
        elif x > center_x + threshold:
            direction = 'right'

        # Press only when direction changes
        if direction != prev_direction:
            if direction:
                pyautogui.press(direction)
                print(f"Pressed {direction}")
            prev_direction = direction

        # Jump if hand goes above 30% height
        if y < 0.3:
            pyautogui.press('up')
            print("Jump")

    else:
        prev_direction = None

def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)

        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
        index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])

        if thumb_index_dist < 50 and index_angle > 90:
            move_player(index_finger_tip)
        else:
            move_player(None)

def main():
    global frame_count
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []

            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            # Only process every 2nd frame to reduce lag
            if frame_count % 2 == 0:
                detect_gesture(frame, landmark_list, processed)

            frame_count += 1

            cv2.imshow('Hand Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.01)

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
