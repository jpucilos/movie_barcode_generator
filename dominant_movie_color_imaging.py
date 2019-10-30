import cv2
import sys
import math
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

def get_dominant_color(image):
	image = image.reshape((image.shape[0] * image.shape[1], 3))
	clt = KMeans(n_clusters = 2)
	labels = clt.fit_predict(image)
	label_counts = Counter(labels)
	dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
	return list(dominant_color)

def count_frames(path, override=False):

	video = cv2.VideoCapture(path)
	total = 0
	if override:
		total = count_frames_manual(video)
	else:
		try:
			total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
		except:
			print("Manually Counting Frames, this may take awhile....")
			total = count_frames_manual(video)
 
	video.release()
	return total

def count_frames_manual(video):
	# initialize the total number of frames read
	total = 0
 
	# loop over the frames of the video
	while True:
		# grab the current frame
		(grabbed, frame) = video.read()
		if not grabbed:
			break
		total += 1
 
	# return the total number of frames in the video file
	return total
	
result_image = np.zeros((1080,1920,3), np.uint8)

movie = cv2.VideoCapture(sys.argv[1])
frameCount = 0
frameSkip = math.ceil((count_frames(sys.argv[1])) / 1940)
success = True
imageCount = 0

while(success):
	if frameCount < frameSkip - 1:
		success = movie.grab()
		frameCount+=1
	else:
		print("Processing Column: " + str(imageCount))	
		success,image = movie.read()
		image = cv2.resize(image,None,fx=0.05,fy=0.05)
		if imageCount < 1920:
			result_image[:, imageCount] = get_dominant_color(image)
		else:
			break
		imageCount += 1
		if imageCount % 100 == 0:
			cv2.imwrite((sys.argv[1]).split(".")[0] + "_Barcode.jpg", result_image)
		frameCount = 0
		
cv2.imwrite((sys.argv[1]).split(".")[0] + "_Barcode.jpg", result_image)