# Simple human fall detection using OpenCV

This Python script uses OpenCV and tkinter libraries to perform fall detection in a video stream. The program prompts the user to either use a webcam or select a file to use as input. Afterward, the program applies a background subtraction algorithm to the frames to detect moving objects, then extracts the contours of the moving objects and analyzes them to detect if a fall has occurred.

Here's a explanation for the code:

1.	Import the necessary libraries:
import cv2
import tkinter as tk
from tkinter import filedialog

2.	Define two functions:
•	select_file() uses a tkinter file dialog to prompt the user to select a file and returns the file path.
•	use_webcam() initializes the OpenCV VideoCapture object and returns it for use in the main program.

3.	Create a root tkinter window and hide it using the withdraw() method:
root = tk.Tk()
root.withdraw()

4.	Prompt the user to select a mode of operation, either "webcam" or "file":
mode = input("Enter 'webcam' to use webcam or 'file' to select a file: ")

5.	Based on the mode selected by the user, initialize the OpenCV VideoCapture object:
•	If the mode is "webcam", call the use_webcam() function to obtain the camera input.
•	If the mode is "file", call the select_file() function to obtain the file path, then pass it to the cv2.VideoCapture() function to obtain the video file input.

6.	If the mode is invalid, print an error message and exit the program:
if mode == 'webcam':
    cap = use_webcam()
elif mode == 'file':
    file_path = select_file()
    cap = cv2.VideoCapture(file_path)
else:
    print("Invalid mode. Exiting program.")
    exit()

7.	Create a BackgroundSubtractorKNN object to perform background subtraction:
fgbg = cv2.createBackgroundSubtractorKNN()

8.	Set up a loop that reads frames from the input source until there are no more frames to read:
while True:
    ret, frame = cap.read()
    if not ret:
        break

9.	Convert each frame to grayscale and apply background subtraction to detect moving objects:
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
fgmask = fgbg.apply(gray)

10.	Extract the contours of the moving objects using the cv2.findContours() function:
contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

11.	If there are contours present, analyze them to detect if a fall has occurred:
•	Compute the area, height, and width of each contour.
•	Find the contour with the largest area and extract its index.
•	Draw the largest contour on the foreground mask using cv2.drawContours().
•	Compute the aspect ratio of the largest contour and compare it to a threshold.
•	If the aspect ratio is below the threshold and the contour has been present for a certain number of consecutive frames, annotate the image with the word "FALL" using cv2.putText().
•	Draw a bounding box around the largest contour on the original image using cv2.rectangle().
if contours:
    areas = []
    heights = []
    widths = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        ar = cv2.contourArea(contour)
        areas.append(ar)
        heights

12. Press 'q' to exit the program.

