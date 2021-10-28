import cv2
import imutils
import numpy as np
import time

im_lower = np.array([20, 75, 75], dtype="uint8")
im_upper = np.array([35, 255, 255], dtype="uint8")
im_lower_g = np.array([40, 254,40], dtype="uint8")
im_upper_g = np.array([100, 255, 255], dtype="uint8")
kernel = np.ones((3, 3), np.uint8)

def landmark_recog(img):
	img_copy = img.copy()
	im_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
	im_mask = cv2.inRange(im_hsv, im_lower, im_upper)
	im_mask = cv2.morphologyEx(im_mask, cv2.MORPH_OPEN, kernel)
	cur_cnt, _ = cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return cur_cnt, im_mask

vs = cv2.VideoCapture("/home/thuan/LAB/IMAGE_CALIBRATION_V2/landmark_tracker/project.avi")

#time.sleep(2.0)

(H, W) = (None, None)

#Pos_def = np.array([681, 446], [324, 442], [655, 257], [334, 266])

while True:
    frame = vs.read()[1]
    frame = imutils.resize(frame, width=1000)
    
    if W is None or H is None:
	    (H, W) = frame.shape[:2]

    cnts = landmark_recog(frame)

    area_sort = [x for x in cnts[0] if (100 < cv2.contourArea(x) < 500)]
    
    count = 1
    for c in area_sort:
	# compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # draw the contour and center of the shape on the image
        cv2.circle(frame, (cX, cY), 4, (1, 255, 1), -1)
        cv2.putText(frame, str(count) , (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        count += 1
    
    # rects = []
    # for i in range(len(area_sort)):
	#     cnt = area_sort[i]
	#     x,y,w,h = cv2.boundingRect(cnt)
	#     box = np.array([x, y, x + w, y + h])
	#     rects.append(box.astype("int"))
    # print(rects)

    # count = 0
    # print(len(area_sort))
    cv2.imshow("a", frame)
    cv2.imshow("b", cnts[1])

    key = cv2.waitKey() & 0xFF
    if key == ord("q"):
	    break
	

    

	# angle_0_2_1_ref = angle_dect(vectors[0, 2], vectors[1, 2])
	# angle_0_2_3_ref = angle_dect(vectors[0, 2], vectors[3, 2])

    # 	if (count):
	# 	#rects = [np.array([621, 392, 635, 401]), np.array([212, 373, 225, 382]), np.array([587, 273, 601, 281]), np.array([293, 264, 306, 272])]
	# 	rects = [np.array([675, 425, 699, 446]), np.array([322, 425, 345, 442]), np.array([650, 243, 669, 258]), np.array([330, 254, 349, 267])]
	# 	base_cnts = [0, 1, 2, 3]
	# 	#Pos = np.array([[628, 396],[218, 377],[594, 277],[299, 268]])
	# 	Pos = np.array([[686, 434], [332, 432], [658, 250], [339, 255]])
	# 	count = False
    
    #	area_sort = [x for x in cnts if (200 < cv2.contourArea(x) < 500)]
