# Controlling-game-with-hand-gestures
This project lets you control a game using your hand gestures via your webcam — no keyboard or mouse needed!

By tracking the index finger using MediaPipe, OpenCV, and pyautogui, you can play the game Boxy Run with just hand movements:

👉 Move your index finger left or right to steer the player.

🖐️ Uses gesture detection logic to ensure smooth, intentional control.

🔧 Tech Stack
Python

MediaPipe – for real-time hand tracking

OpenCV – for video capture and processing

pyautogui – for simulating keyboard inputs

NumPy – for gesture calculations

🕹 How It Works
Captures video from your webcam.

Detects your hand and tracks the index fingertip.

Converts finger position into game controls (arrow key presses).

Smoothly plays the game hands-free.
