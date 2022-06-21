import cv2
from cv2 import pencilSketch
import numpy as np

list = []


def tilefinder(imagetoscan):
    # image read
    img = cv2.imread(imagetoscan, 1)

    # fill black on sides to fix hud problem
    for i in range(15):
        img[:, i] = 0
        img[i, :] = 0
        img[:, len(img[0]) - i - 1] = 0
        img[len(img) - i - 1, :] = 0

    # convert hsv from image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # setting bounds for color detection
    lower_bound = np.array([120, 50, 50])
    upper_bound = np.array([190, 255, 255])

    # finding the colors using the boundaries created right before
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # remove unnecessary noise from mask
    kernel = np.ones((10, 10), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # segment only the detected region
    segmented_img = cv2.bitwise_and(img, img, mask=mask)

    # draw contours from the mask
    contours, _ = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    output = cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)

    # find centers coordinates
    for i in contours:
        M = cv2.moments(i)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(output, (cx, cy), 7, (0, 0, 255), -1)
            print("found tile! coords are: ", cx, cy)
            coords = [cx, cy]
            list.append(coords)
        else:
            print("no tiles found")

    cv2.imshow("lol", output)
    cv2.waitKey(0)


# program itself
tilefinder("images/ore1.png")
