import numpy as np
import cv2
from statistics import mean
import math

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


def draw_contour(im, conts, color):
    for i in range(len(conts)):
        im = cv2.circle(im, (conts[i][1], conts[i][0]), radius=1, color=color, thickness=-1)
    return im

def draw_hull(im, conts, indexes, color):
    points = []
    for i in range(len(indexes)-1):
        start_point= (conts[indexes[i]][1], conts[indexes[i]][0])
        points.append(start_point)
        end_point=(conts[indexes[i+1]][1], conts[indexes[i+1]][0])
        im = cv2.line(im, start_point, end_point, color=color, thickness=2)
    return im, points

def distance(points, im):
    width, height = im.shape[:2]
    points_result =[]

    for i in range(len(points) - 1):
        x1 = points[i][0]
        y1= points[i][1]
        x2= points[i+1][0]
        y2 = points[i+1][1]
        distance = np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))
        if distance > 50 and y1<height:
            im = cv2.circle(im, (x1,y1), radius=3, color=(255,0,255), thickness=-1)
            points_result.append((x1,y1))
    return im, points_result

# Main
im = cv2.imread("finger3.png")
black_and_white = in_range_img(im)
result, conts = find_contour(black_and_white)
im = draw_contour(im, conts, (0, 0, 255))
hull = find_convex_hull(conts)
im, points = draw_hull(im, conts, hull, (0,255,0))
im, points_result = distance(points,im)
im = cv2.circle(im, (175,350), radius=3, color=(255, 0, 0), thickness=-1)
for i in range(len(points_result)):
    im = cv2.line(im, (175,350), points_result[i], color=(255,0,0), thickness=2)

cv2.imshow("hull", im)
cv2.waitKey(0)

