import click
import cv2 as cv
import numpy as np
import pyautogui
import time
import mss
import math

#   global variables
monitornumber = 1
middleofthescreen = [960, 540]

#   doscreenshot()
# creates a screenshot based on the monitor number
# monitor 1 = secondary screen on the right
# monitor 2 = secondary screen on the left
def doscreenshot(monitornb):
    with mss.mss() as sct:
        mon = sct.monitors[monitornb]
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitornumber,
        }
        img = np.array(sct.grab(monitor))
        return img.astype(np.uint8)


#   findtile()
# finds tile based on the image provided and clicks on it
def findtile(imageprovided):
    imgrgb = imageprovided
    imggray = cv.cvtColor(imgrgb, cv.COLOR_RGB2GRAY)
    template = cv.imread("images/template.png", 0)
    res = cv.matchTemplate(imggray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    istheretiles = len(loc[0])
    coords = []

    if istheretiles > 1:
        print("ressource detected")
        for pt in zip(*loc[::-1]):
            coords += [(pt[0], pt[1])]
        print("i found the following coordinates: ", coords)
        coords.sort(key=lambda x: math.sqrt((x[0] - 960) ** 2 + (x[1] - 540) ** 2))
        print("clicking on the closest one: ", coords[0])
        return coords[0]
    else:
        print("no ressource detected, let's move on.")
        return None


#   clicktile()
# clicks on the tile given by a coordinates tuple as a parameter
def clicktile(coordinates):
    pyautogui.click(button="right", x=coordinates[0], y=coordinates[1])


#   main
time.sleep(3)
try:
    clicktile(findtile(doscreenshot(monitornumber)))
except TypeError:
    print(
        "then, we should try to move back to the starting point and continue our journey"
    )
