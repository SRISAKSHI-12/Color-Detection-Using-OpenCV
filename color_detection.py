import cv2
import pandas as pd
import numpy as np
import os

# -----------------------------
# Get current project directory
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(BASE_DIR, "img.jpg")
csv_path = os.path.join(BASE_DIR, "colors.csv")

# -----------------------------
# Read image (supports Unicode paths)
# -----------------------------
try:
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
except Exception as e:
    print("Error loading image:", e)
    exit()

if img is None:
    print("Image not found!")
    print("Expected:", image_path)
    exit()

# -----------------------------
# Read color dataset
# -----------------------------
index = ["color", "color_name", "hex", "R", "G", "B"]

try:
    csv = pd.read_csv(csv_path, names=index, header=None)
except Exception as e:
    print("Error loading colors.csv:", e)
    exit()

# -----------------------------
# Global variables
# -----------------------------
r = g = b = 0
xpos = ypos = 0
mouse_moved = False


# -----------------------------
# Find nearest color
# -----------------------------
def getColorName(R, G, B):

    minimum = 1000
    color_name = ""

    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + \
            abs(G - int(csv.loc[i, "G"])) + \
            abs(B - int(csv.loc[i, "B"]))

        if d < minimum:
            minimum = d
            color_name = csv.loc[i, "color_name"]

    return color_name


# -----------------------------
# Mouse Move Event
# -----------------------------
def mouse_event(event, x, y, flags, param):

    global r, g, b, xpos, ypos, mouse_moved

    if event == cv2.EVENT_MOUSEMOVE:

        xpos = x
        ypos = y

        b, g, r = img[y, x]

        b = int(b)
        g = int(g)
        r = int(r)

        mouse_moved = True


# -----------------------------
# Window
# -----------------------------
cv2.namedWindow("Color Detection")
cv2.setMouseCallback("Color Detection", mouse_event)

# -----------------------------
# Main Loop
# -----------------------------
while True:

    display = img.copy()

    if mouse_moved:

        cv2.rectangle(display, (20, 20), (780, 70), (b, g, r), -1)

        text = f"{getColorName(r,g,b)}    R={r} G={g} B={b}"

        text_color = (255, 255, 255)

        if r + g + b >= 600:
            text_color = (0, 0, 0)

        cv2.putText(display,
                    text,
                    (30, 55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    text_color,
                    2,
                    cv2.LINE_AA)

    cv2.imshow("Color Detection", display)

    key = cv2.waitKey(1)

    if key == 27:     # ESC key
        break

cv2.destroyAllWindows()