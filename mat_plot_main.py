import numpy as np
import cv2
from statistics import mean
import matplotlib.image as img

def in_range_img(im):
    width, height = im.shape[:2]
    new_img = np.zeros([width, height, 4])

    for i in range(width):
        for j in range(height):
            rgb = [float(im[i][j][0]), float(im[i][j][1]), float(im[i][j][2])]
            avg = float(mean(rgb)/250)
            if avg > 0.9:
                avg = 0
            else:
                avg = 1
            new_img[i][j][0] = avg
            new_img[i][j][1] = avg
            new_img[i][j][2] = avg
            new_img[i][j][3] = 1
    return new_img

def find_contour():
    return True

def find_defect_points(img, contours):
    return True

def count_fingers(defects, contours):
    if defects is not None:
        cnt = 0
        biggie = False
    for i in range(defects.shape[0]):  # calculate the angle

        s, e, f, d = defects[i][0]
        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])

        a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
        if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
            cnt += 1
            cv2.circle(img, far, 4, [0, 255, 0], -1)
        elif angle >= np.pi / 2 and angle <= np.pi / 1.5 and cnt == 0:
            cnt = 1
            biggie = True
            cv2.circle(img, far, 4, [255, 0, 0], -1)
    if cnt > 0 and biggie == False:
        cnt = cnt + 1

# Read the image
im = img.imread("finger4.jpg")

result = in_range_img(im)

cv2.imshow("Result", result)
cv2.waitKey(0)