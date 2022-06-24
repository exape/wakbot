import cv2 as cv
import numpy as np
import pyautogui
import time
import mss
import math

#   global variables
monitor_number = 1
middle_of_the_screen = [960, 540]
template_button = cv.imread("images/template_button.png", 0)
template_ressource = cv.imread("images/template_ressource.png", 0)
template_mining = cv.imread("images/template_mining_in_progress.png", 0)
template_mining_while_click = cv.imread("images/template_click_while_mining.png", 0)
something_in_the_area = 1
harvesting = 0

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
            "mon": monitornb,
        }
        img = np.array(sct.grab(monitor))
        # needs to remove the hud on the bottom of screenshot with black pixels
        return img.astype(np.uint8)


#   find()
# finds occurence based on the image provided
def find(imageprovided, template, tres):
    imgrgb = imageprovided
    imggray = cv.cvtColor(imgrgb, cv.COLOR_RGB2GRAY)
    res = cv.matchTemplate(imggray, template, cv.TM_CCOEFF_NORMED)
    threshold = tres
    loc = np.where(res >= threshold)
    istheretiles = len(loc[0])
    coords = []
    if istheretiles > 1:
        print("something to collect detected")
        for pt in zip(*loc[::-1]):
            coords += [(pt[0], pt[1])]
        coords.sort(key=lambda x: math.sqrt((x[0] - 960) ** 2 + (x[1] - 540) ** 2))
        print("clicking on the closest one: ", coords[0])
        return coords[0]
    else:
        return None


#   clicktile()
# clicks on the tile given by a coordinates tuple as a parameter
def clicktile(coordinates):
    pyautogui.click(button="right", x=coordinates[0], y=coordinates[1])


#   clickharvest()
# clicks on the button to harvest the ressource by a coordinates tuple as a parameter
def clickharvest(coordinates):
    pyautogui.click(button="left", x=coordinates[0], y=coordinates[1])


#   isharvesting()
# finds if the bot is harvesting based on the image provided
def isharvesting(imageprovided, template, tres):
    imgrgb = imageprovided
    imggray = cv.cvtColor(imgrgb, cv.COLOR_RGB2GRAY)
    res = cv.matchTemplate(imggray, template, cv.TM_CCOEFF_NORMED)
    threshold = tres
    loc = np.where(res >= threshold)
    istheretiles = len(loc[0])
    if istheretiles > 1:
        return True
    else:
        return False


def explorezone():
    print("exploring zone")
    global something_in_the_area
    while something_in_the_area:
        global harvesting
        harvesting = isharvesting(
            doscreenshot(monitor_number), template_mining, 0.7
        ) | isharvesting(doscreenshot(monitor_number), template_mining_while_click, 0.7)

        print("harvesting:", harvesting)
        while harvesting is not True:
            try:
                clicktile(find(doscreenshot(monitor_number), template_ressource, 0.7))
                clickharvest(find(doscreenshot(monitor_number), template_button, 0.6))
                time.sleep(12)
                harvesting = isharvesting(
                    doscreenshot(monitor_number), template_mining, 0.7
                ) | isharvesting(
                    doscreenshot(monitor_number), template_mining_while_click, 0.7
                )
            except TypeError:
                print("no more ressource here, leaving")
                something_in_the_area = 0


# main
time.sleep(3)
something_in_the_area = find(doscreenshot(monitor_number), template_ressource, 0.7)
explorezone()
