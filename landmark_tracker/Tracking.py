from numpy.core.numeric import base_repr
import CentroidTracker as ct
import numpy as np
import imutils
import time
import cv2
import datetime

im_lower = np.array([20, 75, 75], dtype="uint8")
im_upper = np.array([35, 255, 255], dtype="uint8")
kernel = np.ones((3, 3), np.uint8)

def landmark_recog(img):
	img_copy = img.copy()
	im_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
	im_mask = cv2.inRange(im_hsv, im_lower, im_upper)
	im_mask = cv2.morphologyEx(im_mask, cv2.MORPH_OPEN, kernel)
	cur_cnt, _ = cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return cur_cnt, im_mask

def angle_dect(v1, v2):
    unit_vector_1 = v1 / np.linalg.norm(v1)
    unit_vector_2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle= np.arccos(dot_product) * 180 / 3.14
    return angle

(H, W) = (None, None)

#get final result
def Position(objects):
	Pos = []
	for(x, centroid) in objects.items():
		if x in base_cnts:
			Pos.insert(base_cnts.index(x), centroid)
	return Pos

#check if showed up contour is landmark
def find_4(cur_cnts, objects):
	#angle relationship of defined landmarks
	angle_1_3_2_ref = 124
	angle_1_3_0_ref = 105
	angle_0_2_1_ref = 91
	angle_0_2_3_ref = 72
	Pos = []
	#"objects" store all tracked contour (also in the past) by ID (0 -> 1 -> 2 -> ... -> 99999)
	#store position of 4 contours in Pos[lm0, lm1, lm2, lm3]
	#check angle relationship
	for (x, centroid) in objects.items():
		if x in cur_cnts:
			Pos.insert(cur_cnts.index(x), centroid)
	vector_0_2 = [Pos[0][0] - Pos[2][0], Pos[0][1] - Pos[2][1]]
	vector_1_2 = [Pos[1][0] - Pos[2][0], Pos[1][1] - Pos[2][1]]
	angle = angle_dect(vector_0_2, vector_1_2)
	if angle_0_2_1_ref - 10 < angle < angle_0_2_1_ref + 10:
		global base_cnts
		base_cnts = cur_cnts.copy()
		return True
	else:
		return False

vs = cv2.VideoCapture("D:\\CodeGit\\IMAGE_CALIBRATION_V2\\landmark_tracker\\vid.mp4")
time.sleep(2.0)

count = True
# loop over the frames from the video stream
while True:
	# read the next frame from the video stream and resize it
	a = datetime.datetime.now()
	frame = vs.read()[1]
	frame = imutils.resize(frame, width=700)

	# if the frame dimensions are None, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	cnts = landmark_recog(frame)[0]
	#keep landmarks that have fixed area
	area_sort = [x for x in cnts if (10 < cv2.contourArea(x) < 45)]

	rects = []

	#get boundingbox of contour
	for i in range(len(area_sort)):
		cnt = area_sort[i]
		x,y,w,h = cv2.boundingRect(cnt)
		box = np.array([x, y, x + w, y + h])
		rects.append(box.astype("int"))

	if (count):
		rects = [np.array([435, 274, 445, 281]), np.array([149, 261, 157, 267]),\
			np.array([411, 192, 419, 196]), np.array([205, 186, 214, 190])]
		base_cnts = [0, 1, 2, 3]
		Pos = [np.array([440, 277]), np.array([153, 264]), np.array([415, 194]), np.array([209, 188])]
		count = False

	#tracking contour
	#view Readme.txt to see how this func work
	#"objects = [[ID, Position], [ID, Position],...]"
	objects = ct.update(rects)
	
	#all contour has their own ID
	#if they disappeared and come back, they will have new ID
	#base_cnts : ID of being tracked contour that we know are landmarks
	#For example: At first we track 4 contours
	#so base_cnts = [0, 1, 2, 3]
	#if contour 0 disappear and comeback
	#base_cnts = [4, 1, 2, 3]
	if len(base_cnts) == 4:
		#if 1 landmark disappear
		if len(objects) == 3:
			cur_cnts = []
			for (x, _ ) in objects.items():
				cur_cnts.append(x)
			dis = (list(set(base_cnts) - set(cur_cnts)))[0]
			#remember position of missing landmark
			dis_index = base_cnts.index(dis)
			#remove it from tracking contour list
			base_cnts.remove(dis)
		#Pos: return position of landmarks that we use to calibrate images (final result)
		Pos = Position(objects)
	#if we tracking 3 contours
	elif len(base_cnts) == 3:
		#new contour show up
		if len(objects) == 4:
			cur_cnts = base_cnts.copy()
			for (x, _ ) in objects.items():
				#cur_cnts: make a copy of base_cnts
				#put new contour in missing landmark's position
				#to check if that's new landmark
				if x in cur_cnts:
					continue
				else:
					cur_cnts.insert(dis_index, x)
					if (find_4(cur_cnts, objects)):
						Pos = Position(objects)
		Pos = Position(objects)

	text = 0
	if len(Pos) == 3:
		Pos.insert(dis_index, [0,0])
	for centroid in Pos:
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
		cv2.putText(frame, str(text), (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		text += 1

	# b = datetime.datetime.now()
	# print((b - a) * 1000)
	#print(Pos)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

	rects = []

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()