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
            if avg > 0.58:
                avg = 0
            else:
                avg = 1
            new_img[i][j][0] = avg
            new_img[i][j][1] = avg
            new_img[i][j][2] = avg
            new_img[i][j][3] = 1
    return new_img

def find_contour(im):
    height, width = im.shape[:2]
    new_img = np.zeros([height, width, 4])
    conts = []
    for i in range(height-1):
        for j in range(width-1):
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
    height, width = im.shape[:2]
    points = []
    firstPoint = (conts[indexes[0]][1], conts[indexes[0]][0])
    for i in range(len(indexes)-1):
        start_point= (conts[indexes[i]][1], conts[indexes[i]][0])
        if(start_point[1]< height-10) :
            points.append(start_point)
        end_point=(conts[indexes[i+1]][1], conts[indexes[i+1]][0])
        im = cv2.line(im, start_point, end_point, color=color, thickness=2)
    im = cv2.line(im, firstPoint, end_point, color=color, thickness=2)
    return im, points

def getKey(item):
    return item[0]

def sort_points(points, im):
    points_result =[]
    points.sort(key=getKey)

    for i in range(len(points)-1):
        x1 = points[i][0]
        y1= points[i][1]
        x2= points[i+1][0]
        y2 = points[i+1][1]
        dist = distance(x1,y1,x2,y2)
        im = cv2.circle(im, (x1, y1), radius=3, color=(255, 255, 255), thickness=-1)
        if dist > 70 or i == len(points)-2:
            im = cv2.circle(im, (x1,y1), radius=3, color=(255,0,255), thickness=-1)
            points_result.append((x1, y1))
    points_result = sort_by_X_axis(points_result)
    return im, points_result

def sort_by_X_axis(points):
    result = []
    for i in range(len(points)-1):
        if(abs(points[i][0] - points[i+1][0])>20):
            result.append(points[i])
            if (i == len(points)-2):
                result.append(points[i+1])
    return result


def distance(x1, y1, x2, y2):
    return np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))

def count_fingers(points, centerX, centerY):
    count = 0
    dist = []
    sum = 0
    for i in range(len(points)):
        d = distance(points[i][0], points[i][1], centerX, centerY)
        dist.append(d)
        sum +=d
        print("Distance "+str(d))

    for j in range(len(dist)):
        if (dist[j]>250):
            count+=1

    return count

# Images mine: test1.jpg -5, test10.jpg -2, test11.jpg - 3, test9.jpg -1

# Main
# Read image
im = cv2.imread("test1.jpg")
print('read image. now copy')
original = im.copy()
print('copied. now black and white.')

# Convert to black and white
black_and_white = in_range_img(im)
print('black and white done. now show')
cv2.imshow("Black and white", black_and_white)
cv2.waitKey(0)

# Find contour
result, conts = find_contour(black_and_white)
im = draw_contour(im, conts, (0, 0, 255))
cv2.imshow("Contour", im)
cv2.waitKey(0)

# Find convex hull
hull = find_convex_hull(conts)
im, points = draw_hull(im, conts, hull, (0,255,0))
cv2.imshow("Convex hull", im)
cv2.waitKey(0)

# Sorting points and connecting them with center
im, points_result = sort_points(points,im)
height, width = im.shape[:2]
centerX = int(width / 2)
centerY = height - 100
im = cv2.circle(im, (centerX, centerY), radius=3, color=(255, 0, 0), thickness=-1)
for i in range(len(points_result)):
    im = cv2.line(im, (centerX,centerY), points_result[i], color=(255,0,0), thickness=2)
cv2.imshow("Points added", im)
cv2.waitKey(0)

# Counting fingers
cnt = count_fingers(points_result, centerX, centerY)
cv2.putText(original, str(cnt), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
cv2.imshow("Fingers counted", original)
cv2.waitKey(0)

