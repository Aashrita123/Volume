import cv2 
import numpy as np 
import math 
import mediapipe as mp 
import pyautogui 
import time 
# Initialize volume control parameters 
volume = 0 
max_volume = 100 
min_volume = 0 
vol_range = max_volume - min_volume 
# Initialize hand tracking 
mp_drawing = mp.solutions.drawing_utils 
mp_hands = mp.solutions.hands 
hands = mp_hands.Hands() 
# Initialize webcam 
cap = cv2.VideoCapture(0) 
# Set screen width and height 
screen_width, screen_height = pyautogui.size() 
# Define hand landmarks for volume control 
thumb_tip_id = 4 
index_finger_tip_id = 8 
# Define gesture thresholds 
gesture_distance_threshold = 50 
volume_change_threshold = 10 
# Initialize gesture variables 
previous_volume = 0 
gesture_start_time = time.time() 
while True: 
 # Read frame from webcam 
 ret, frame = cap.read() 
 if not ret: 
   break 
 # Flip the frame horizontally for a mirrored view 
 frame = cv2.flip(frame, 1) 
 # Convert the BGR image to RGB 
 image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
 # Process the image and detect hands 
 results = hands.process(image_rgb) 
 # Draw hand landmarks on the frame 

 if results.multi_hand_landmarks: 
   for hand_landmarks in results.multi_hand_landmarks: 
    mp_drawing.draw_landmarks(frame, hand_landmarks, 
mp_hands.HAND_CONNECTIONS) 
 # Get thumb and index finger coordinates 
 thumb_tip = hand_landmarks.landmark[thumb_tip_id] 
 index_finger_tip = hand_landmarks.landmark[index_finger_tip_id] 
 # Convert thumb and index finger coordinates to screen coordinates 
 thumb_x, thumb_y = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height) 
 index_x, index_y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * 
screen_height) 
 # Calculate distance between thumb and index finger 
 distance = math.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) 
 # Map the distance to the volume range 
 volume = np.interp(distance, [0, screen_width], [min_volume, max_volume]) 
 volume = int(volume) 
 # Determine volume change based on the difference between the current volume and the 
 # previous volume 
 volume_change = volume - previous_volume 
 # Update the previous volume 
 previous_volume = volume 
 # Perform volume control based on the gesture 
 if abs(volume_change) > volume_change_threshold: 
   if volume_change > 0: 
     pyautogui.press('volumeup', presses=abs(volume_change)) 
 else: 
   pyautogui.press('volumedown', presses=abs(volume_change)) 
 # Display volume on the frame 
 cv2.putText(frame, f"Volume: {volume}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 
(0, 255, 0), 2, cv2.LINE_AA) 
 # Show the frame 
 cv2.imshow('Hand Gesture Volume Control', frame) 
 # Exit if 'q' is pressed 
 if cv2.waitKey(1) & 0xFF == ord('q'): 
   break 
# Release the webcam and destroy windows 
cap.release() 
cv2.destroyAllWindows() 