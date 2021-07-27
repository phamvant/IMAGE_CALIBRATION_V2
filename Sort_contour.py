from sys import path
import numpy as np
import cv2

from numpy.lib.function_base import append
from numpy.lib.type_check import imag

# Initiate threshold values, for later image processing (contour recognition based on color)
im_lower = np.array([20, 75, 75], dtype="uint8")
im_upper = np.array([35, 255, 255], dtype="uint8")
kernel = np.ones((3, 3), np.uint8)

def Print(a):
    print(a)
    exit(0)

#smaller image
def resize_img(img):
    size = 1000
    dim = (size, int(1080 * size / 1920))
    resized = cv2.resize(img, dim)
    cv2.imshow('a', resized)
    cv2.waitKey()
    # exit(0)
    return resized

def angle(v1, v2):
    unit_vector_1 = v1 / np.linalg.norm(v1)
    unit_vector_2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle= np.arccos(dot_product) * 180 / 3.14
    return angle

# def sort_contours(cnts):
# 	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
# 	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
# 		key=lambda b:b[1][1], reverse=False))
# 	# return the list of sorted contours and bounding boxes
# 	return (cnts, boundingBoxes)

def landmark_recog(img):

    img_copy = img.copy()
    im_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    im_mask = cv2.inRange(im_hsv, im_lower, im_upper)
    im_mask = cv2.morphologyEx(im_mask, cv2.MORPH_OPEN, kernel)
    # resize_img(im_mask)

    # Finding contours available on image
    cur_cnt, _ = cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cur_cnt, im_mask

path_4 = "D:\\CodeGit\\IMAGE_CALIBRATION_V2\\data_process\\C9\\ref_image\\imageplaceholder.jpg"
path_3 = "D:\\CodeGit\\IMAGE_CALIBRATION_V2\\data_process\\C9\\ref_image\\imageplaceholder_3.jpg"

# cur_1, cur_2, cur_3, cur_4 = landmark_recog(path_4)
def lm_3(image):
    Pos = []
    left = []
    right = []
    i = 0
    mid_X = mid_Y = 0

    #angle_3_1_2 : angle between vector(1, 3) and vector (1, 2) (defined by user)
    angle_3_1_2_ref = 124
    angle_3_1_4_ref = 105
    angle_4_2_3_ref = 91
    angle_4_2_1_ref = 72

    (h, w, d) = image.shape 
    center = (w // 2, h // 2) 
    M = cv2.getRotationMatrix2D(center, 0, 1.0) 
    image = cv2.warpAffine(image, M, (w, h))

    cnts, im_mask = landmark_recog(image)

    # 3 largest landmarks
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:3]

    #Pos = [[,][,][,][,]] #coordinates of 4 landmarks
    for c in cnts:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        Pos.append([cX, cY])
        mid_X = mid_X + Pos[i][0]
        mid_Y = mid_Y + Pos[i][1]
        i = i + 1

    
    #left[]: coordinates of landmarks on the left
    #right[]: coordinates of landmarks on the right
    mid = [int(mid_X / 3), int(mid_Y / 3)]
    for i in range(3):
        if Pos[i][0] < mid[0]:
            left.append(Pos[i])
        else:
            right.append(Pos[i])

    #sort left = [[lm1], [lm3]] 
    #right = [[lm2], [lm4]]
    if len(left) == 2:
        if left[0][1] > left[1][1]:
            left[0], left[1] = left[1], left[0]
    if len(right) == 2:
        if right[0][1] > right[1][1]:
            right[0], right[1] = right[1],right[0]

    #put text
    if len(left) == 2:
        #if there are 2 landmarks on the left => landmark_1 and landmark_3 => puttext
        cv2.putText(image, "#1", (int(left[0][0]), int(left[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)
        cv2.putText(image, "#3", (int(left[1][0]), int(left[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)
        #vector_ll : vector go through 2 landmarks on the left
        #vector_lr: vector go through landmark 1 and landmark on the right
        vector_ll = [left[1][0] - left[0][0], left[1][1] - left[0][1]]
        vector_lr = [right[0][0] - left[0][0], right[0][1] - left[0][1]]
        #vector between ll and lr ~ angle_3_1_4 or angle_3_1_2
        if angle_3_1_4_ref - 10 < angle(vector_ll, vector_lr) < angle_3_1_4_ref + 10:
            cv2.putText(image, "#4", (int(right[0][0]), int(right[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)
        else:   #~angle_3_1_2
            cv2.putText(image, "#2", (int(right[0][0]), int(right[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)
    else:   #if len(right) == 2
        cv2.putText(image, "#2", (int(right[0][0]), int(right[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)
        cv2.putText(image, "#4", (int(right[1][0]), int(right[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)
        #same
        vector_rr = [right[1][0] - right[0][0], right[1][1] - right[0][1]]
        vector_rl = [left[0][0] - right[0][0], left[0][1] - right[0][1]]
        if angle_4_2_1_ref - 10 < angle(vector_rr, vector_rl) < angle_4_2_1_ref + 10:
            cv2.putText(image, "#1", (int(left[0][0]), left(right[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)
        else:
            print(angle(vector_rr, vector_rl))
            cv2.putText(image, "#3", (int(left[0][0]), int(left[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 2)

    return image

for i in range(150):
    filename = "C:\\Users\\phamt\\Downloads\\DATA.2020_12_30\\lmTst_{}.jpg".format(i)
    image = cv2.imread(filename)
    image = lm_3(image)
    resize_img(image)

exit()
