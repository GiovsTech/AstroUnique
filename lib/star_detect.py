import cv2
import numpy as np


def is_star(frame, template_in="templates/template.jpg"):
    img = frame
    template  = cv2.imread(template_in,0)
    w,h = template.shape[::-1]
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    threh = 5.0
    for i in result:
        if i.any() >= threh:
            return True
    return False


def star_database_selection():
    pass
    # TODO: A WEB PAGE TO EXPLORE PHOTOS AND DATABASE CONTENTS