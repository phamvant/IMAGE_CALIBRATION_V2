from textwrap import indent
from numpy.core.numeric import base_repr
from scipy.spatial import distance
import CentroidTracker as ct
import numpy as np
import imutils
import time
import cv2
import datetime
import math

im_lower = np.array([20, 75, 75], dtype="uint8")
im_upper = np.array([35, 255, 255], dtype="uint8")
kernel = np.ones((3, 3), np.uint8)

vectors = {}

def xoay(p1, p2, angle):
      v = [p2[0] - p1[0], p2[1] - p1[1]]

      newX = v[0] * math.cos(angle) + v[1] * math.sin(angle)
      newY = -v[0] * math.sin(angle) + v[1] * math.cos(angle)

      p3 = [int(p1[0] + newX), int(p1[1] + newY)]
      return p3

def angle_dect(v1, v2):
    unit_vector_1 = v1 / np.linalg.norm(v1)
    unit_vector_2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle= np.arccos(dot_product)
    return angle
    

Pos_def = np.array([[440, 277],[153, 264],[415, 194],[209, 188]])
A = Pos_def[0]
B = Pos_def[1]
C = Pos_def[2]
D = Pos_def[3]

vectors[1,0] = A - B
vectors[1,3] = D - B
vectors[3,2] = C - D
vectors[0,2] = C - A
vectors[1,2] = C - B
vectors[3,0] = A - D

def noisuy(cur_1, cur_2, coord_1, coord_2):
	try:
		vector_def = vectors[cur_1, cur_2]
	except:
		vector_def = vectors[cur_2, cur_1]
		cur_1, cur_2 = cur_2, cur_1
		coord_1, coord_2 = coord_2, coord_1
	vector_new = coord_2 - coord_1
	move = coord_1 - Pos_def[cur_1]
	angle = angle_dect(vector_new, vector_def)
	noisuy_coord = {}
	for i in range(4):
		if i != cur_1 and i != cur_2:
			temp_move = Pos_def[i] + move
			p3 = xoay(coord_1, temp_move, angle)
			noisuy_coord[i] = np.array(p3)
	return noisuy_coord

def landmark_recog(img):
	img_copy = img.copy()
	im_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
	im_mask = cv2.inRange(im_hsv, im_lower, im_upper)
	im_mask = cv2.morphologyEx(im_mask, cv2.MORPH_OPEN, kernel)
	cur_cnt, _ = cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return cur_cnt, im_mask

(H, W) = (None, None)

#get final result
def Position(objects):
	Pos = []
	for(x, centroid) in objects.items():
		if x in base_cnts:
			Pos.insert(base_cnts.index(x), centroid)
	return Pos

#check if showed up contour is landmark
# def find_4(cur_cnts, objects):
# 	#angle relationship of defined landmarks
# 	angle_1_3_2_ref = 124
# 	angle_1_3_0_ref = 105
# 	angle_0_2_1_ref = 91
# 	angle_0_2_3_ref = 72
# 	Pos = []
# 	#"objects" store all tracked contour (also in the past) by ID (0 -> 1 -> 2 -> ... -> 99999)
# 	#store position of 4 contours in Pos[lm0, lm1, lm2, lm3]
# 	#check angle relationship
# 	for (x, centroid) in objects.items():
# 		if x in cur_cnts:
# 			Pos.insert(cur_cnts.index(x), centroid)
# 	vector_0_2 = [Pos[0][0] - Pos[2][0], Pos[0][1] - Pos[2][1]]
# 	vector_1_2 = [Pos[1][0] - Pos[2][0], Pos[1][1] - Pos[2][1]]
# 	angle = angle_dect(vector_0_2, vector_1_2)
# 	if angle_0_2_1_ref - 10 < angle < angle_0_2_1_ref + 10:
# 		global base_cnts
# 		base_cnts = cur_cnts.copy()
# 		return True
# 	else:
# 		return False

#vs = cv2.VideoCapture("D:\\CodeGit\\IMAGE_CALIBRATION_V2\\landmark_tracker\\vid.mp4")
vs = cv2.VideoCapture("./landmark_tracker/vid.mp4")
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
	area_sort = [x for x in cnts if (20 < cv2.contourArea(x) < 45)]

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
		elif len(objects) == 2:
			cur_cnts = []
			for (x, _ ) in objects.items():
				cur_cnts.append(x)
			kk = list(set(base_cnts) - set(cur_cnts))
			dis = kk[0] #value
			dis_index = base_cnts.index(dis)	#index
			dis_2 = kk[1] #value
			dis_index_2 = base_cnts.index(dis_2)
			base_cnts.remove(dis) #remove value	#index
			base_cnts.remove(dis_2) #remove value
			Pos = Position(objects)
		Pos = Position(objects)
	#if we tracking 3 contours
	elif len(base_cnts) == 3:
		#new contour show up
		# if len(objects) == 4:
		# 	cur_cnts = base_cnts.copy()
		# 	for (x, _ ) in objects.items():
		# 		#cur_cnts: make a copy of base_cnts
		# 		#put new contour in missing landmark's position
		# 		#to check if that's new landmark
		# 		if x in cur_cnts:
		# 			continue
		# 		else:
		# 			cur_cnts.insert(dis_index, x)
		# 			if (find_4(cur_cnts, objects)):
		# 				Pos = Position(objects)
		if len(objects) == 2:
			cur_cnts = []
			for (x, _ ) in objects.items():
				cur_cnts.append(x)
			dis = (list(set(base_cnts) - set(cur_cnts)))[0] #value
			dis_index_2 = base_cnts.index(dis)	#index
			base_cnts.remove(dis) #remove value
			Pos = Position(objects)
		Pos = Position(objects)
	#print(len(base_cnts))
	# print(len(objects))
	# try:
	# 	print(dis_index, dis_index_2)
	# except:
	# 	None
	# print(base_cnts)
	if len(base_cnts) == 2:
		temp = []
		temp_2 = []
		#print(Pos)
		#print(dis_index, dis_index_2)
		Pos = Position(objects)
		for i in range(4):
			if (i != dis_index and i != dis_index_2):
				temp.append(i)
		# print(temp)
		# print(base_cnts)
		for x in base_cnts:
			for (k, centroid) in objects.items():
				if k == x:
					temp_2.append(centroid)
		noisuy_coord = noisuy(temp[0], temp[1], temp_2[0], temp_2[1])
		if len(objects) > 2:
			cur_cnts = base_cnts.copy()
			for(x, centroid) in objects.items():
				if x in cur_cnts:
					continue
				else:
					for i in range(4):
						try:
							if (noisuy_coord[i][0] - 20 < centroid[0] < noisuy_coord[i][0] + 20)\
								 and (noisuy_coord[i][1] - 20 < centroid[1] < noisuy_coord[i][1] + 20):
								base_cnts.insert(i, x)
								print(i)
								if i == dis_index:
									print("OK")
									dis_index_2, dis_index = dis_index, dis_index_2
						except:
							None
			Pos = Position(objects)
			if len(Pos) == 3:
				Pos.insert(dis_index, [0,0])
		else:
			for i in range(4):
				try:
					Pos.insert(i, noisuy_coord[i])
				except:
					None
	#print(Pos)
	if len(Pos) == 3:
		Pos.insert(dis_index,[0,0])
	text = 0
	for centroid in Pos:
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
		cv2.putText(frame, str(text), (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		#print(centroid[0], centroid[1], text)
		text += 1
	# b = datetime.datetime.now()
	# print((b - a) * 1000)
	#print(Pos)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey() & 0xFF
	if key == ord("q"):
		break

	rects = []

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()