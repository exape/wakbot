import cv2 as cv
from cv2 import pencilSketch
import numpy as np
import pyautogui
import math
import time
import mss 


def doscreenshot():
    with mss.mss() as sct:
        # get information of monitor 1(adrien) or monitor 2(flavien, lucas)
        monitor_number = 2
        mon = sct.monitors[monitor_number]
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }

        # Grab the image screen
        img = np.array(sct.grab(monitor))

        return img.astype(np.uint8)



kernel = cv.imread('image.png')
test = cv.imread("test.png")
def findmatch():

    # get screenshot
    img = doscreenshot()
    img = img[:,:,0:3]

    # fill black on sides to fix hud problem
    for i in range(15):
        img[:, i] = 0
        img[i, :] = 0
        img[:, len(img[0]) - i - 1] = 0
        img[len(img) - i - 1, :] = 0
        
    res = cv.matchTemplate(img, kernel, cv.TM_CCOEFF_NORMED)
    # cv.imshow('res',res)
    # cv.waitKey()
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    threshold = 0.8
    print(max_loc,max_val)
    if max_val >= threshold:
        print('Found needle.')
    pyautogui.click(button='right',x=max_loc[0]+1920,y=max_loc[1])



# program itself

findmatch()