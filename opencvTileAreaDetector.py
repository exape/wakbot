import cv2 as cv
import numpy as np
import pyautogui
import time
import mss
import math

# global variables
kernel = cv.imread("image.png")
monitor_number = 1
middleofthescreen = [960, 540]

#   doscreenshot()
# creates a screenshot based on the monitor number
# monitor 1 = adrien
# monitor 2 = flavien, lucas
def doscreenshot(monitornumber):
    with mss.mss() as sct:
        mon = sct.monitors[monitornumber]
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitornumber,
        }
        # Grab the image screen
        img = np.array(sct.grab(monitor))
        return img.astype(np.uint8)


#   findtile()
# finds tile based on the image provided and clicks on it
def findtile(imageprovided):
    img_rgb = imageprovided
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
    template = cv.imread("image.png", 0)
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    isThereTiles = len(loc[0])
    coords = []

    if isThereTiles > 1:
        print("Ressource detected")
        for pt in zip(*loc[::-1]):
            coords += [(pt[0], pt[1])]
        print("i found the following coordinates: ", coords)
        coords.sort(key=lambda x: math.sqrt((x[0] - 960) ** 2 + (x[1] - 540) ** 2))
        print("Clicking on the closest one: ", coords[0])
        return coords[0]
    else:
        print("No ressource detected, let's move on.")


#   clicktile()
# clicks on the tile given by a tuple as a parameter
def clicktile(coordinates):
    a = coordinates[0]
    b = coordinates[1]
    pyautogui.click(button="right", x=a, y=b)


# main
time.sleep(3)
clicktile(findtile(doscreenshot(monitor_number)))
