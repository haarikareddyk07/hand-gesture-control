import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

while True:   # 👈 LOOP START

    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            x = int(hand.landmark[8].x * screen_width)
            y = int(hand.landmark[8].y * screen_height)

            pyautogui.moveTo(x, y)

            thumb_x = int(hand.landmark[4].x * screen_width)
            thumb_y = int(hand.landmark[4].y * screen_height)

            distance = abs(x - thumb_x) + abs(y - thumb_y)

            if distance < 80:
                pyautogui.click()
                pyautogui.sleep(0.5)

            finger_X = hand.landmark[8].x

            if finger_X > 0.8:
               pyautogui.press("right")
               pyautogui.sleep(2)
            elif finger_X < 0.2:
               pyautogui.press("left")
               pyautogui.sleep(2)


               



    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) == 27:   # 👈 MUST BE INSIDE LOOP
        break

# 👇 OUTSIDE LOOP
cap.release()
cv2.destroyAllWindows()