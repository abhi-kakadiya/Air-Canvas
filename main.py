import cv2
import time
import numpy as np
import os
import pygame
import streamlit as st
import trackingModule as tm
from random_word import RandomWords
from PIL import Image

st.title("Air Canvas")
FRAME_WINDOW = st.image([])

folderPath = 'Images'
list_Images = os.listdir(folderPath)

img_weight = 0.1
canvas_weight = 0.9

X_Y_Points = []
imagesArray = []

pygame.mixer.init()
drawingSound = pygame.mixer.Sound("Audio/drawingmp3.mp3")
eraserSound = pygame.mixer.Sound("Audio/erasermp3.mp3")
selectingSound = pygame.mixer.Sound("Audio/selectClickmp3.mp3")

for imgPath in list_Images:
	img = cv2.imread(f'{folderPath}/{imgPath}')
	imagesArray.append(img)
	
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FPS, 60)

# DEFAULT COLOR IS BLACK
drawColor = (0, 0, 0)

# STARTING POSITION
list1 = []
xStart,yStart = 0,0

canvas = np.ones((480,640,3),np.uint8)
canvas[:,:] = canvas[:,:] * 255

displayImage = imagesArray[0]
displayImage = cv2.resize(displayImage, (640, 60))

handTracker = tm.handDetector()

soundStarted_drawing = False
soundStartTime_drawing = 0
soundDuration_drawing = 0

soundStarted_eraser = False
soundStartTime_eraser = 0
soundDuration_eraser = 0

soundStarted_selection = False
soundStartTime_selection = 0
soundDuration_selection = 0

dict = {}
for i in range(1,len(imagesArray)+1):
	dict[i] = 1

total_Fingers = 0
x1,y1,x2,y2 = 0,0,0,0

def initializeSoundAttributes():
	global soundStarted_drawing,soundStarted_eraser,soundStarted_selection,soundDuration_drawing,soundDuration_eraser,soundDuration_selection,drawingSound,eraserSound,selectingSound

	if not soundStarted_drawing:
		soundDuration_drawing = drawingSound.get_length()
		soundStarted_drawing = True

	if not soundStarted_eraser:
		soundDuration_eraser = eraserSound.get_length()
		soundStarted_eraser = True
	
	if not soundStarted_selection:
		soundDuration_selection = selectingSound.get_length()
		soundStarted_selection = True

def time_elapsed(i):
	global soundStartTime_selection
	timeElapsed = time.time() - soundStartTime_selection
	soundStartTime_selection = time.time()
	if int(timeElapsed) != 0 and dict[i]:
		selectingSound.play()
	else:
		for j in dict.keys():
			if i==j:
				dict[j] = 0
			else:
				dict[j] = 1
		soundStartTime_selection = 0

def findLandmarks(img):
	global total_Fingers,x1,y1,x2,y2
	img = handTracker.HandDetection(img)
	landMarkList = handTracker.findPosition(img,False)
	if len(landMarkList) != 0 :

		# INDEX FINGER
		x1,y1 = landMarkList[8][1:]
		# MIDDLE FINGER
		x2,y2 = landMarkList[12][1:]

	total_Fingers = handTracker.fingers_Fisted_Splayed()
	return total_Fingers,x1,y1,x2,y2

def selectAndDraw(img,total_Fingers,x1,y1,x2,y2):
	global displayImage,drawColor,canvas,canvas_weight,img_weight,drawingSound,eraserSound,selectingSound,X_Y_Points,xStart,yStart,soundStartTime_drawing,soundStartTime_eraser,soundDuration_drawing,soundDuration_eraser,soundDuration_selection
	if len(total_Fingers) != 0:			

		# SELECTION MODE
		if (total_Fingers[1] ==True) and (total_Fingers[2] == True):

			drawingSound.stop()
			eraserSound.stop()

			X_Y_Points = []
			xStart = x1
			yStart = y1
			# SELECT DIFFERENT CRAYONS
			if y2 < 60:
				
				if 0< ((x1+x2)//2) <80:
					i = 1
					displayImage = imagesArray[1]
					drawColor = (-1, -1, -1)
					time_elapsed(i)

				elif 80< ((x1+x2)//2) <160:
					i = 2
					displayImage = imagesArray[2]
					drawColor = (0, 0, 255)
					time_elapsed(i)

				elif 160< ((x1+x2)//2) <240:
					i = 3
					displayImage = imagesArray[3]
					drawColor = (0, 127, 255)
					time_elapsed(i)

				elif 240< ((x1+x2)//2) <320:
					i = 4
					displayImage = imagesArray[4]
					drawColor = (0, 255, 255)
					time_elapsed(i)

				elif 320< ((x1+x2)//2) <400:
					i = 5
					displayImage = imagesArray[5]
					drawColor = (0, 255, 0)
					time_elapsed(i)

				elif 400< ((x1+x2)//2) <480:
					i = 6
					displayImage = imagesArray[6]
					drawColor = (255, 0, 0)
					time_elapsed(i)

				elif 480< ((x1+x2)//2) <560:
					i = 7
					displayImage = imagesArray[7]
					drawColor = (0,0,0)
					time_elapsed(i)

				elif 560< ((x1+x2)//2) <640:
					i = 8
					displayImage = imagesArray[8]
					drawColor = (255,255,255)
					time_elapsed(i)

			else:
				displayImage = imagesArray[0]

				

			cv2.circle(img,radius=20,center=((x1+x2)//2,(y1+y2)//2),color=drawColor,thickness=-1)

			print('SELECTION MODE')

		# DRAWING MODE
		elif ((total_Fingers[1] == True) and (total_Fingers[2] == False) and (total_Fingers[3] == False) and (total_Fingers[4] == False)) or (total_Fingers[3] == False):			
		
			selectingSound.stop()

			if len(X_Y_Points) >= 0:
				if len(X_Y_Points) == 0:
						X_Y_Points.append([x1,y1])

				if len(X_Y_Points) > 0:
					x1 = (X_Y_Points[-1][0] + x1) // 2
					y1 = (X_Y_Points[-1][1] + y1) // 2
	
					# print(X_Y_Points)
					X_Y_Points.append([x1,y1])
			
			cv2.circle(img,radius=10,center=(x1,y1),color=(0,0,0),thickness=-1)		
			
			# BY DEFAULT IT WILL NOT START DRAWING AT THE STARTING INDEX OF X AND Y --> (0,0)
			if xStart == 0 and yStart == 0:
				xStart = x1 
				yStart = y1 
			
			if drawColor != (-1,-1,-1):
				if drawColor == (255,255,255):
					thickness = 30
					cv2.line(canvas,(xStart,yStart),(x1,y1),color=drawColor,thickness=thickness)

					if not pygame.mixer.get_busy():
						soundStartTime_eraser = time.time()
						eraserSound.play()
					else:
						timeElapsed = time.time() - soundStartTime_eraser
						if timeElapsed > soundDuration_eraser:
							eraserSound.stop()
							eraserSound.play()
							soundStartTime_eraser = time.time()

				
				elif drawColor != (255, 255, 255):
					points = np.array(X_Y_Points)			
					cv2.polylines(canvas, [points], False, drawColor, thickness = 5)	
				
					if not pygame.mixer.get_busy():
						soundStartTime_drawing = time.time()
						drawingSound.play()
					else:
						timeElapsed = time.time() - soundStartTime_drawing
						if timeElapsed > soundDuration_drawing:
							drawingSound.stop()
							drawingSound.play()
							soundStartTime_drawing = time.time()
			
				print('DRAWING MODE')

			else:
				canvas[:] = (255,255,255)

			# NOW OUR NEW POINTS WILL PREVIOUS POINTS
			xStart = x1
			yStart = y1
		
		displayImage = cv2.resize(displayImage, (640, 60))
	else:
		eraserSound.stop()
		drawingSound.stop()
		selectingSound.stop()
		

	return displayImage

initializeSoundAttributes()
button_bool = st.button("PAUSE WEB-CAM")
# Main loop
while True:
	if (button_bool) == False:
		# IMAGE IMPORTED AND RESIZED
		_,img = cap.read()
		img = cv2.resize(img, (640, 480)) 
		img = cv2.flip(img,1)
		
		# FIND HAND LANDMARKS
		total_Fingers,x1,y1,x2,y2 = findLandmarks(img)
		displayImage = selectAndDraw(img,total_Fingers,x1,y1,x2,y2)

		# FIRST IMAGE TO BE DISPLAYED IS APPLIED
		img[:60,0:640] = displayImage
		blended = cv2.addWeighted(img[60:,0:640],img_weight, canvas[60:,0:640], canvas_weight, 10)
		img[60:,0:640] = blended
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		FRAME_WINDOW.image(img)

		# if cv2.waitKey(1) & 0xFF == 32:
		# 	break

	else:
		with st.spinner('Wait for it...'):
			st.success('Done!')
		folderPath = 'Web Static'
		landscape_img = 'Background.jpg'
		st.image(f"{folderPath}/{landscape_img}")
		st.header("_Web_ _Cam_ :red[stopped] :sunflower:")
		button_bool = False
		break


pygame.mixer.music.stop()
cv2.destroyAllWindows()
pygame.quit()