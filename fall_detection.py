import cv2
import tkinter as tk
from tkinter import filedialog

def select_file():
    file_path = filedialog.askopenfilename()
    return file_path

def use_webcam():
    cap = cv2.VideoCapture(0)
    return cap

root = tk.Tk()
root.withdraw()

mode = input("Enter 'webcam' to use webcam or 'file' to select a file: ")

if mode == 'webcam':
    cap = use_webcam()
elif mode == 'file':
    file_path = select_file()
    cap = cv2.VideoCapture(file_path)
else:
    print("Invalid mode. Exiting program.")
    exit()

fgbg = cv2.createBackgroundSubtractorKNN()
j = 0
consecutive_frames = 0
while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

    if contours:
        areas = []
        heights = []
        widths = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            ar = cv2.contourArea(contour)
            areas.append(ar)
            heights.append(h)
            widths.append(w)

        max_area = max(areas or [0])
        max_area_index = areas.index(max_area)

        cnt = contours[max_area_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3)

        if h < w:
            consecutive_frames += 1
        
        aspect_ratio = h / w
        if consecutive_frames > 10 and aspect_ratio < 0.5:
            cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if aspect_ratio >= 0.5:
            consecutive_frames = 0
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('video', frame)

        if cv2.waitKey(2) & 0xff == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
