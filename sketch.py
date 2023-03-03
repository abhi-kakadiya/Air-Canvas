import cv2
import time
import numpy as np
import os
import pygame
import trackingModule as tm


colorDict = {0: (0,0,255),
		1:(0,255,0),
		2:(255,0,0)} 

while True:
	sketch = cv2.imread("download.png", cv2.IMREAD_GRAYSCALE)
	sketch = cv2.resize(sketch,(1000,600))

	# Threshold the sketch to create a binary image
	_, sketch = cv2.threshold(sketch, 128, 255, cv2.THRESH_BINARY)
	# Find the contours of the regions in the sketch
	contours, hierarchy = cv2.findContours(sketch, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	if contours is not None:
		print("Contours found: ", len(contours))

	# Draw the contours on the sketch
	sketch = cv2.cvtColor(sketch,cv2.COLOR_GRAY2BGR)
	print(contours)

	for i in range(3):
		cv2.drawContours(sketch, contours, i, color=colorDict[i], thickness=-1)
	# Show the result
	cv2.imshow("Segmented sketch", sketch)
	if cv2.waitKey(0) & 0xFF == 27:
		break

cv2.destroyAllWindows()
