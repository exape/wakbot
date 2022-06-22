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
    # _, max_val, _, max_loc = cv.minMaxLoc(res)
    # print(max_loc, max_val)
    # # if found, right click on it
    # if max_val >= threshold:
    #     print("Found needle.")
    # pyautogui.click(button="right", x=max_loc[0], y=max_loc[1])

    img_rgb = imageprovided
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
    template = cv.imread("image.png", 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8

    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv.imshow("", img_rgb)
    cv.waitKey(0)


# main
time.sleep(3)
findtile(doscreenshot(monitor_number))
