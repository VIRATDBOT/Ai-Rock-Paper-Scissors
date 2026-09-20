# ✊✋✌️ AI Rock-Paper-Scissors (Hand Gesture Game)

A real-time Rock-Paper-Scissors game that uses your **webcam** to see your
hand and figure out what move you made — no keyboard, no mouse, just your
hand in front of the camera.

## How it works (in plain words)

1. Your webcam turns on.
2. When you press **SPACE**, a 3-2-1 countdown starts.
3. When the countdown hits zero, the camera looks at your hand and counts
   how many fingers are up:
   - **0 fingers up** → Rock
   - **2 fingers up** → Scissors
   - **5 fingers up** → Paper
4. The computer randomly picks a move at the same moment.
5. Whoever wins gets a point. Press SPACE again for another round.

This uses a computer vision technique called **hand landmark detection** —
the same underlying idea used in real gesture-control and sign-language
recognition systems, just applied to a fun game.

## Run it on your own computer

1. **Install Python** (python.org) if you don't have it already
2. Open a terminal in this folder and run:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the game:
   ```bash
   python rps_game.py
   ```
4. A window will open showing your webcam. Press **SPACE** to play a round,
   **Q** to quit.

## Tips

- Play in good lighting — the hand detector works much better when it can
  clearly see your fingers.
- Keep your whole hand inside the camera frame.
- If your webcam doesn't show up, open `rps_game.py` and change
  `CAMERA_INDEX = 0` to `1`.

## Built with

- Python
- OpenCV — reads the webcam and draws the game UI
- cvzone + MediaPipe — detects the hand and counts fingers

## Created by

**CREATED BY :- VIRAT CHOPRA**

## License

MIT
