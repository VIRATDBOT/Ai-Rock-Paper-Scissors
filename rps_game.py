"""
AI Rock-Paper-Scissors — Hand Gesture Game
--------------------------------------------
Simple explanation: this program turns on your webcam, watches your hand,
counts how many fingers are up, and figures out if you showed Rock, Paper,
or Scissors. Then the computer picks randomly, and we see who wins.

How finger-counting maps to a move:
  0 fingers up  -> Rock
  2 fingers up  -> Scissors
  5 fingers up  -> Paper
"""

import cv2
import random
import time
from cvzone.HandTrackingModule import HandDetector

# ---------- SETTINGS ----------
CAMERA_INDEX = 0          # change to 1 if your webcam doesn't show
COUNTDOWN_SECONDS = 3      # "3, 2, 1, Show!" before each round
MOVES = ["Rock", "Paper", "Scissors"]

# ---------- SETUP ----------
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(3, 900)   # width
cap.set(4, 720)   # height

detector = HandDetector(maxHands=1, detectionCon=0.8)

player_score = 0
computer_score = 0

state = "waiting"       # waiting -> countdown -> result
countdown_start = 0
result_text = ""
player_move = None
computer_move = None


def fingers_to_move(finger_list):
    """
    finger_list looks like [0,1,1,0,0] — one entry per finger (thumb to pinky),
    1 means "up", 0 means "down". We just count how many are up.
    """
    total_up = sum(finger_list)
    if total_up == 0:
        return "Rock"
    elif total_up == 2:
        return "Scissors"
    elif total_up == 5:
        return "Paper"
    else:
        return None  # not a recognized gesture yet


def decide_winner(player, computer):
    if player == computer:
        return "Draw!"
    wins_against = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
    if wins_against[player] == computer:
        return "You Win!"
    else:
        return "Computer Wins!"


print("Press SPACE to start a round. Press Q to quit.")

while True:
    success, img = cap.read()
    if not success:
        print("Couldn't read from webcam. Check CAMERA_INDEX in the settings.")
        break

    img = cv2.flip(img, 1)  # mirror image, feels more natural
    hands, img = detector.findHands(img, flipType=False)

    # ---------- DRAW SCORE ----------
    cv2.rectangle(img, (0, 0), (900, 90), (20, 20, 20), -1)
    cv2.putText(img, f"You: {player_score}", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (245, 208, 51), 3)
    cv2.putText(img, f"Computer: {computer_score}", (650, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 62, 128), 3)

    # ---------- STATE MACHINE ----------
    if state == "countdown":
        elapsed = time.time() - countdown_start
        remaining = COUNTDOWN_SECONDS - int(elapsed)

        if remaining > 0:
            cv2.putText(img, str(remaining), (420, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (232, 163, 61), 8)
        else:
            # time's up — read the player's hand right now
            if hands:
                fingers = detector.fingersUp(hands[0])
                move = fingers_to_move(fingers)
            else:
                move = None

            if move is None:
                result_text = "Couldn't see a clear gesture — try again!"
                player_move = None
                computer_move = None
            else:
                player_move = move
                computer_move = random.choice(MOVES)
                result_text = decide_winner(player_move, computer_move)
                if result_text == "You Win!":
                    player_score += 1
                elif result_text == "Computer Wins!":
                    computer_score += 1

            state = "result"

    elif state == "result":
        cv2.putText(img, f"You: {player_move or '?'}", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (245, 208, 51), 3)
        cv2.putText(img, f"Computer: {computer_move or '?'}", (30, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 62, 128), 3)
        cv2.putText(img, result_text, (30, 260),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        cv2.putText(img, "Press SPACE for next round", (30, 700),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 2)

    else:  # waiting
        cv2.putText(img, "Press SPACE to play a round", (200, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 3)

    cv2.imshow("AI Rock Paper Scissors - by Virat Chopra", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord(' ') and state in ("waiting", "result"):
        state = "countdown"
        countdown_start = time.time()
        result_text = ""

cap.release()
cv2.destroyAllWindows()
