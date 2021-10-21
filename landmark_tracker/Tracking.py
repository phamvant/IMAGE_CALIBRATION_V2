import CentroidTracker as ct
import numpy as np
import imutils
import time
import cv2
from datetime import date, timedelta
import math
import os
import glob
im_lower = np.array([20, 75, 75], dtype="uint8")
im_upper = np.array([35, 255, 255], dtype="uint8")
im_lower_g = np.array([40, 254,40], dtype="uint8")
im_upper_g = np.array([100, 255, 255], dtype="uint8")
kernel = np.ones((3, 3), np.uint8)
f= open("coord.txt","w+")
vectors = {}


#return new possition of landmark after rotate
def xoay(p1, p2, angle):
      v = [p2[0] - p1[0], p2[1] - p1[1]]

      newX = v[0] * math.cos(angle) + v[1] * math.sin(angle)
      newY = -v[0] * math.sin(angle) + v[1] * math.cos(angle)

      p3 = [int(p1[0] + newX), int(p1[1] + newY)]
      return p3

#detect angle between 2 vectors
def angle_dect(v1, v2):
    unit_vector_1 = v1 / np.linalg.norm(v1)
    unit_vector_2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle= np.arccos(dot_product)
    return angle
    
#define default possition bottom -> top / right -> left
Pos_def = np.array([[628, 396],[218, 377],[594, 277],[299, 268]])
A = Pos_def[0]
B = Pos_def[1]
C = Pos_def[2]
D = Pos_def[3]

#vectors from default landmarks
vectors[1,0] = A - B
vectors[1,3] = D - B
vectors[3,2] = C - D
vectors[0,2] = C - A
vectors[1,2] = C - B
vectors[3,0] = A - D

#predict lost landmarks (2 landmark)
def noisuy(cur_1, cur_2, coord_1, coord_2): #name of nokotteru landmark and their positions
	try:	#figure out what vector are they (depend on defined landmark above)
		vector_def = vectors[cur_1, cur_2]
	except:
		vector_def = vectors[cur_2, cur_1]
		cur_1, cur_2 = cur_2, cur_1
		coord_1, coord_2 = coord_2, coord_1

	vector_new = coord_2 - coord_1		#nokotteru vector
	move = coord_1 - Pos_def[cur_1]		#figure out how nokotteru vector moved
	angle = angle_dect(vector_new, vector_def)	
	noisuy_coord = {}
	#move all default vectors same way
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

def landmark_recog2(img):
	img_copy = img.copy()
	im_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
	im_mask = cv2.inRange(im_hsv, im_lower_g, im_upper_g)
	im_mask = cv2.morphologyEx(im_mask, cv2.MORPH_OPEN, kernel)
	cur_cnt, _ = cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return cur_cnt, im_mask

(H, W) = (None, None)

#get final result
def Position(objects):
	Pos = []
	if len(base_cnts) == 4:
		for i in range(4):
			Pos.append(np.array([0,0]))
		for(x, centroid) in objects.items():
			if x in base_cnts:
				Pos.insert(base_cnts.index(x), centroid)
				Pos.pop(base_cnts.index(x) + 1)
	else:
		for(x, centroid) in objects.items():
			if x in base_cnts:
				Pos.insert(base_cnts.index(x), centroid)
	return Pos

#check if showed up contour is landmark
def find_4(cur_cnts, objects, dis_index):
	#angle relationship of defined landmarks
	# angle_1_3_2_ref = 124
	# angle_1_3_0_ref = 105
	angle_0_2_1_ref = 91
	angle_0_2_3_ref = 72
	Pos = []
	#"objects" store all tracked contour (also in the past) by ID (0 -> 1 -> 2 -> ... -> 99999)
	#store position of 4 contours in Pos[lm0, lm1, lm2, lm3]
	#check angle relationship
	for i in range(4):
		Pos.append(np.array([0,0]))
	for (x, centroid) in objects.items():
		if x in cur_cnts:
			Pos.insert(cur_cnts.index(x), centroid)
			Pos.pop(cur_cnts.index(x) + 1)
	A1 = Pos[0]
	B1 = Pos[1]
	C1 = Pos[2]
	D1 = Pos[3]

	if dis_index == 0 or dis_index == 1 or dis_index == 2:
		vector_1 = A1 - C1
		vector_2 = B1 - C1
		angle = angle_dect(vector_1, vector_2) * 180 / math.pi
		#print(angle)
		if angle_0_2_1_ref - 10 < angle < angle_0_2_1_ref + 10:
			global base_cnts
			base_cnts = cur_cnts.copy()
			return True
		else:
			return False
	else:
		vector_1 = A1 - D1
		vector_2 = C1 - D1
		angle = angle_dect(vector_1, vector_2)
		if angle_0_2_3_ref - 10 < angle < angle_0_2_3_ref + 10:
			base_cnts = cur_cnts.copy()
			return True
		else:
			return False

if os.name == 'nt':
	vs = cv2.VideoCapture(".\\landmark_tracker\\vid.mp4")
else:
	vs = cv2.VideoCapture("/home/thuan/Code/IMAGE_CALIBRATION_V2/landmark_tracker/vid.mp4")


time.sleep(2.0)
cou = 0
count = True
average_time = 0
# loop over the frames from the video stream
while True:
	start = time.monotonic()
	cou+=1
	# if average_time > 100:
	# 	print(cou)
	# 	exit()
	if cou == 570:
		#print(average_time)
		f.write("\n\naverage_time: {}".format(average_time / 570))
		f.close()
		exit()
	# read the next frame from the video stream and resize it
	frame = vs.read()[1]
	frame = imutils.resize(frame, width=1000)

	# if the frame dimensions are None, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	cnts = landmark_recog(frame)[0]
	#keep landmarks that have fixed area
	area_sort = [x for x in cnts if (50 < cv2.contourArea(x) < 100)]

	rects = []

	#get boundingbox of contour
	for i in range(len(area_sort)):
		cnt = area_sort[i]
		x,y,w,h = cv2.boundingRect(cnt)
		box = np.array([x, y, x + w, y + h])
		rects.append(box.astype("int"))

	if (count):
		rects = [np.array([621, 392, 635, 401]), np.array([212, 373, 225, 382]), np.array([587, 273, 601, 281]), np.array([293, 264, 306, 272])]
		base_cnts = [0, 1, 2, 3]
		Pos = np.array([[628, 396],[218, 377],[594, 277],[299, 268]])
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
			#print(cur_cnts)
			dis = (list(set(base_cnts) - set(cur_cnts)))[0]
			#remember position of missing landmark
			dis_index = base_cnts.index(dis)
			#remove it from tracking contour list
			base_cnts.remove(dis)
		#Pos: return position of landmarks that we use to calibrate images (final result)
			Pos = Position(objects)
		elif len(objects) == 2:
			#same way as 1 (add dis_index_2)
			cur_cnts = []
			for (x, _ ) in objects.items():
				cur_cnts.append(x)
			kk = list(set(base_cnts) - set(cur_cnts))
			dis = kk[0]
			dis_index = base_cnts.index(dis)
			dis_2 = kk[1]
			dis_index_2 = base_cnts.index(dis_2)
			base_cnts.remove(dis)
			base_cnts.remove(dis_2)
			Pos = Position(objects)
		else:
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
					if (find_4(cur_cnts, objects, dis_index)):
						Pos = Position(objects)
		#one more disappear
		elif len(objects) == 2:
			cur_cnts = []
			for (x, _ ) in objects.items():
				cur_cnts.append(x)
			dis = (list(set(base_cnts) - set(cur_cnts)))[0]
			base_cnts.insert(dis_index, 0)
			dis_index_2 = base_cnts.index(dis)
			base_cnts.pop(dis_index)
			base_cnts.remove(dis)
			Pos = Position(objects)
		else:
			Pos = Position(objects)
	#if current tracking 2 landmarks
	elif len(base_cnts) == 2:
		temp = []	#nokotteru landmarks
		temp_2 = []	#possition of nokotteru landmarks

		Pos = Position(objects)
		for i in range(4):
			if (i != dis_index and i != dis_index_2):
				temp.append(i)

		for (k, centroid) in objects.items():
			for x in base_cnts:
				if k == x:
					temp_2.append(centroid)
		#predict missing landmarks
		try:
			noisuy_coord = noisuy(temp[0], temp[1], temp_2[0], temp_2[1])
		except:
			exit()
		#if detect new objects
		if len(objects) > 2:
			cur_cnts = base_cnts.copy()
			for(x, centroid) in objects.items():
				if x in cur_cnts:
					continue
				else:
					#check if new objects are landmark
					for i in range(4):
						try:
							cv2.circle(frame, (noisuy_coord[i][0], noisuy_coord[i][1]), 4, (1, 255, 1), -1)
							if (noisuy_coord[i][0] - 70 < centroid[0] < noisuy_coord[i][0] + 70)\
								 and (noisuy_coord[i][1] - 70 < centroid[1] < noisuy_coord[i][1] + 70):
								#if new object is close to predicted landmarks
								f.write("------------------------\n")
								f.write("predict: {}: {}\n".format(i, noisuy_coord[i]))
								f.write("new_landmark: {}\n".format(centroid))
								f.write("------------------------\n")
								if len(objects) == 3 and i == 2:
									base_cnts.insert(i - 1, x)
								else:
									base_cnts.insert(i, x)
								if i == dis_index:
									dis_index_2, dis_index = dis_index, dis_index_2
						except:
							None
			#update current tracking landmark possition
			Pos = Position(objects)
			if len(Pos) == 3:
				Pos.insert(dis_index, [0,0])
			#insert [0,0] as missing landmarks but we won't use it
		else:
			for i in range(4):
				#if no landmark show up (still have only 2 nokotteru landmakrs)
				try:
					#put predicted landmarks position (use it)
					Pos.insert(i, noisuy_coord[i])
				except:
					None
	#insert [0,0] as missing landmarks
	if len(Pos) == 2:
		Pos.insert(dis_index_2, [0,0])
	if len(Pos) == 3:
		Pos.insert(dis_index,[0,0])
	text = 0
	#draw and make write data
	for centroid in Pos:
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (1, 255, 1), -1)
		cv2.putText(frame, str(text), (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (1, 255, 1), 2)
		text += 1

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(10) & 0xFF
	if key == ord("q"):
		break
	

	for i in range(4):
		f.write("{} : {}\n".format(i, Pos[i]))
	if len(base_cnts) == 2:
		f.write("*************************\n")
		f.write("predict landmark: {} {}\n".format(dis_index, dis_index_2))
	f.write("time: {}\n\n\n".format(time.monotonic() - start))
	average_time += time.monotonic() - start
	# exit()

#add new comments
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()