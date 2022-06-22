import cv2 as cv
import numpy as np
import pyautogui
import time
import mss

# global variables
kernel = cv.imread("image.png")
monitor_number = 1

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
# finds tile based on the image provided
def findtile(imageprovided):
    img = imageprovided[:, :, 0:3]
    # fill black on sides to fix hud problem
    for i in range(15):
        img[:, i] = 0
        img[i, :] = 0
        img[:, len(img[0]) - i - 1] = 0
        img[len(img) - i - 1, :] = 0
    # find the pattern based on the image provided
    res = cv.matchTemplate(img, kernel, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(res)
    threshold = 0.8
    print(max_loc, max_val)
    # if found, right click on it
    if max_val >= threshold:
        print("Found needle.")
    pyautogui.click(button="right", x=max_loc[0], y=max_loc[1])


# main
time.sleep(3)
findtile(doscreenshot(monitor_number))
