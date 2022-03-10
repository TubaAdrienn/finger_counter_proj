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

def blur_image(image):
    width, height = im.shape[:2]
    blurred = np.zeros([width,height,3])

    for i in range(width-1):
        for j in range(height-1):
            sum_points = image[i-1][j+1] + image[i][j + 1] + image[i + 1][j + 1] + image[i - 1][j] + image[i][j] + image[i +1][j] + image[i - 1][j - 1] + image[i][j - 1] + image[i + 1][j - 1]
            blurred[i][j] = (sum_points/9)

    return blurred

def find_contour(im):
    width, height = im.shape[:2]
    new_img = np.zeros([width, height, 4])
    conts = []
    for i in range(width-1):
        for j in range(height-1):
            current = float(im[i][j][0])
            next_x = float(im[i+1][j][0])
            next_y = float(im[i][j+1][0])
            if current == (1-next_x) or current == (1-next_y):
                new_img[i][j][0] = 0
                new_img[i][j][1] = 0
                new_img[i][j][2] = 1
                new_img[i][j][3] = 1
                conts.append([i, j])
    return new_img, conts


def left_index(points):
    minn = 0
    for i in range(1, len(points)):
        if points[i][0] < points[minn][0]:
            minn = i
        elif points[i][0] == points[minn][0]:
            if points[i][1] > points[minn][1]:
                minn = i
    return minn


def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def find_convex_hull(conts):
    n = len(conts)
    l = left_index(conts)
    hull = []
    p = l
    q = 0
    while (True):
        hull.append(p)
        q = (p + 1) % n

        for i in range(n):
            if (orientation(conts[p], conts[i], conts[q]) == 2):
                q = i
        p = q
        if (p == l):
            break

    return hull


def find_defect_points(img, contours):
    return True

def count_fingers(defects, contours):
    if defects is not None:
        cnt = 0
        biggie = False
    for i in range(defects.shape[0]):  # calculate the angle

        s, e, f = defects[i][0]
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

def draw_contour(im, conts, color):
    for i in range(len(conts)):
        im = cv2.circle(im, (conts[i][1], conts[i][0]), radius=1, color=color, thickness=-1)
    return im

def draw_hull(im, conts, indexes, color):
    for i in range(len(indexes)-1):
        start_point= (conts[indexes[i]][1], conts[indexes[i]][0])
        end_point=(conts[indexes[i+1]][1], conts[indexes[i+1]][0])
        im = cv2.line(im, start_point, end_point, color=color, thickness=2)
    return im


# Main

im = cv2.imread("6.jpg")
black_and_white = in_range_img(im)
result, conts = find_contour(black_and_white)
im = draw_contour(im, conts, (0, 0, 255))
hull = find_convex_hull(conts)
im = draw_hull(im, conts, hull, (0,255,0))
cv2.imshow("hull", im)
cv2.waitKey(0)

