import streamlit as st
import cv2
import numpy as np
import pygame
import time
from cvzone.HandTrackingModule import HandDetector

# Initialize pygame
pygame.mixer.init()

# Load sound for each white key
sound_q = pygame.mixer.Sound("./AudioFiles/sound_q.wav")  # Replace "sound_q.wav" with your sound file for key 'q'
sound_w = pygame.mixer.Sound("./AudioFiles/sound_w.wav")  # Replace "sound_w.wav" with your sound file for key 'w'
sound_e = pygame.mixer.Sound("./AudioFiles/sound_e.wav")  # Replace "sound_e.wav" with your sound file for key 'e'
sound_r = pygame.mixer.Sound("./AudioFiles/sound_r.wav")  # Replace "sound_r.wav" with your sound file for key 'r'
sound_t = pygame.mixer.Sound("./AudioFiles/sound_t.wav")  # Replace "sound_t.wav" with your sound file for key 't'
sound_y = pygame.mixer.Sound("./AudioFiles/sound_q.wav")  # Replace "sound_y.wav" with your sound file for key 'y'
sound_u = pygame.mixer.Sound("./AudioFiles/sound_w.wav")  # Replace "sound_u.wav" with your sound file for key 'u'

# Function to play sound based on the position of the rectangle
def play_sound(key):
    if key == 'q':
        sound_q.play()
    elif key == 'w':
        sound_w.play()
    elif key == 'e':
        sound_e.play()
    elif key == 'r':
        sound_r.play()
    elif key == 't':
        sound_t.play()
    elif key == 'y':
        sound_y.play()
    elif key == 'u':
        sound_u.play()


# Center the layout in Streamlit
st.set_page_config(layout="centered")
# Center the "Virtual Piano" title using custom HTML
st.markdown("""
    <h1 style="text-align: center; font-size: 3em;">Virtual Piano</h1>
""", unsafe_allow_html=True)

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set a wider width
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set a larger height if needed

camera.set(cv2.CAP_PROP_FPS, 120)

ret, frame = camera.read()
H, W = frame.shape[:2]

detector = HandDetector(detectionCon=0.8)

stframe = st.image([])

time.sleep(1)

# Track the keys that have been pressed
pressed_keys = set()

while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    hands, img = detector.findHands(frame, draw=True, flipType=True)

    # Draw white keys
    white_keys = {'q': (50, -10), 'w': (200, -10), 'e': (350, -10), 'r': (500, -10), 't': (650, -10), 'y': (800, -10), 'u': (950, -10)}
    for key, (rect_x, rect_y) in white_keys.items():
        rect_width, rect_height = 100, 200
        rect_color = (255, 255, 255)
        cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), rect_color, cv2.FILLED)

        # Add text
        cv2.putText(img, key, (rect_x + 20, rect_y + 50), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

    # Draw black keys
    black_keys = {'1': (125, -10), '2': (275, -10), '3': (425, -10), '4': (575, -10), '5': (725, -10), '6': (875, -10), '7': (1025, -10)}
    for key, (rect_x, rect_y) in black_keys.items():
        rect_width, rect_height = 60, 120
        rect_color = (0, 0, 0)
        cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), rect_color, cv2.FILLED)

    # Display image
    stframe.image(frame, channels="BGR", use_column_width=True)

    # Call play_sound function when a hand is detected over a white key
    if hands:
        for hand in hands:
            hand_x, hand_y = hand["lmList"][8][0], hand["lmList"][8][1]  # Position of the tip of the index finger
            for key, (key_x, key_y) in white_keys.items():
                if key_x <= hand_x <= key_x + 100 and key_y <= hand_y <= key_y + 200:
                    if key not in pressed_keys:
                        play_sound(key)  # Play sound only if the key is not already pressed
                        pressed_keys.add(key)  # Add the key to the set of pressed keys
                else:
                    if key in pressed_keys:
                        pressed_keys.remove(key)  # Remove the key if the hand is no longer over it