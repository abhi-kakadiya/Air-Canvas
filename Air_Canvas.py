import cv2
import time
import numpy as np
import os
import pygame
import trackingModule as tm


folderPath = 'Images'
list_Images = os.listdir(folderPath)
print(list_Images)

img_weight = 0.1
canvas_weight = 0.9

X_Y_Points = []
imagesArray = []
pygame.mixer.init()

for imgPath in list_Images:
	img = cv2.imread(f'{folderPath}/{imgPath}')
	imagesArray.append(img)
	
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

# DEFAULT COLOR IS BLACK
drawColor = (0, 0, 0)

# STARTING POSITION
list1 = []
xStart,yStart = 0,0

x1Prev = 0
y1Prev = 0
x2Prev = 0
y2Prev = 0

canvas = np.ones((480,640,3),np.uint8)
canvas[:,:] = canvas[:,:] * 255

displayImage = imagesArray[0]
displayImage = cv2.resize(displayImage, (640, 60))

handTracker = tm.handDetector()
 
while True:

	# IMAGE IMPORTED AND RESIZED
	_,img = cap.read()
	img = cv2.resize(img, (640, 480))
	img = cv2.flip(img,1)
	
	# FIND HAND LANDMARKS
	img = handTracker.HandDetection(img)
	landMarkList = handTracker.findPosition(img,False)
	if len(landMarkList) != 0 :

		# INDEX FINGER
		x1,y1 = landMarkList[8][1:]
		
		# MIDDLE FINGER
		x2,y2 = landMarkList[12][1:]

	total_Fingers = handTracker.fingers_Fisted_Splayed()
	# print(total_Fingers)
	
	

	if len(total_Fingers) != 0:			

		# SELECTION MODE
		if (total_Fingers[1] ==True) and (total_Fingers[2] == True):
			X_Y_Points = []
			xStart = x1
			yStart = y1
			# SELECT DIFFERENT CRAYONS
			if y2 < 60:
				if 200< ((x1+x2)//2) <288:
					displayImage = imagesArray[1]
					drawColor = (32, 66, 235)
				elif 288< ((x1+x2)//2) <376:
					displayImage = imagesArray[4]
					drawColor = (255, 102, 196)
				elif 376< ((x1+x2)//2) <464:
					displayImage = imagesArray[3]
					drawColor = (126, 217, 87)
				elif 464< ((x1+x2)//2) <552:
					displayImage = imagesArray[5]
					drawColor = (255, 222, 89)
				elif 552< ((x1+x2)//2) <640:
					displayImage = imagesArray[2]
					drawColor = (255,255,255)
			else:
				displayImage = imagesArray[0]

				

			cv2.circle(img,radius=20,center=((x1+x2)//2,(y1+y2)//2),color=drawColor,thickness=-1)

			# print('SELECTION MODE')

		# DRAWING MODE
		elif ((total_Fingers[1] == True) and (total_Fingers[2] == False) and (total_Fingers[3] == False) and (total_Fingers[4] == False)) or (total_Fingers[3] == False):

			sound = pygame.mixer.Sound("mixkit-writing-pencil-3194.wav")

			if len(X_Y_Points) >= 0:
				if len(X_Y_Points) == 0:
						X_Y_Points.append([x1,y1])

				if len(X_Y_Points) > 0:
					x1 = (X_Y_Points[-1][0] + x1) // 2
					y1 = (X_Y_Points[-1][1] + y1) // 2
	
					# print(X_Y_Points)
					X_Y_Points.append([x1,y1])
			
			cv2.circle(img,radius=20,center=(x1,y1),color=drawColor,thickness=-1)		
			
			# BY DEFAULT IT WILL NOT START DRAWING AT THE STARTING INDEX OF X AND Y --> (0,0)
			if xStart == 0 and yStart == 0:
				xStart = x1 
				yStart = y1 
			
			
			if drawColor == (255,255,255):
				thickness = 40
				cv2.line(canvas,(xStart,yStart),(x1,y1),color=drawColor,thickness=thickness)
			
			elif drawColor != (0, 0, 0):
				# cv2.line(canvas,(xStart,yStart),(x1,y1),color=drawColor,thickness=10)
				points = np.array(X_Y_Points)				
				cv2.polylines(canvas, [points], False, drawColor, thickness = 7)
				# sound.play()
		
			print('DRAWING MODE')
			
			# NOW OUR NEW POINTS WILL PREVIOUS POINTS
			xStart = x1
			yStart = y1
		
		displayImage = cv2.resize(displayImage, (640, 60))

	# FIRST IMAGE TO BE DISPLAYED IS APPLIED
	img[:60,0:640] = displayImage
	blended = cv2.addWeighted(img[60:,0:640], img_weight, canvas[60:,0:640], canvas_weight, 0)
	img[60:,0:640] = blended
	cv2.imshow('Canvas', img)

	if cv2.waitKey(1) & 0xFF == 27:
		break

cv2.destroyAllWindows()
pygame.quit()
