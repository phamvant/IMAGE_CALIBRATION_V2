import CentroidTracker
from imutils.video import VideoStream
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

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker.CentroidTracker()
(H, W) = (None, None)

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

def next(rects):
	#CentroidTracker.py
	objects = ct.update(rects)

	# loop over the tracked objects
	for (objectID, centroid) in objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
	b = datetime.datetime.now()
	print((b - a).total_seconds() * 1000)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


# loop over the frames from the video stream
while True:
	# read the next frame from the video stream and resize it
	a = datetime.datetime.now()
	frame = vs.read()
	frame = imutils.resize(frame, width=500)

	# if the frame dimensions are None, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	cnts = landmark_recog(frame)[0]
	area_cnt = [cv2.contourArea(cnt) for cnt in cnts]
	#keep landmarks that contourArea > 150
	b = [x for x in area_cnt if x > 150]
	area_sort = np.argsort(b)

	#bounding box info
	rects = []
	for i in range(len(area_sort)):
		print(len(area_sort))
		cnt = cnts[area_sort[i]]
		x,y,w,h = cv2.boundingRect(cnt)
		box = np.array([x, y, x + w, y + h])
		rects.append(box.astype("int"))

	#rects = 4 corner of bounding box (all bounding box)
	next(rects)
