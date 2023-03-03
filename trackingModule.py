import cv2
import mediapipe as mp
import time


class handDetector:
	def __init__(self):

		self.mpHands = mp.solutions.hands
		self.mpDraw = mp.solutions.drawing_utils

		self.hand = self.mpHands.Hands(False,max_num_hands=2,min_tracking_confidence=0.5,min_detection_confidence=0.85)



	def HandDetection(self, img, draw=True):

		""" TO DETECT HAND IN WINDOW AND DRAW LANDMARKS ON IT """
		imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		self.result = self.hand.process(imgRGB)

		if self.result.multi_hand_landmarks:
			for handlandmarks in self.result.multi_hand_landmarks:
				if draw == True:
					self.mpDraw.draw_landmarks(img,handlandmarks,self.mpHands.HAND_CONNECTIONS)
		return img


	def findPosition(self, img, handNumber=0,draw = True):

		""" TO STORE POSITION OF SELECTED HAND'S LANDMARK AND RETURN IT"""
		self.landMarkList = [] 		
		if self.result.multi_hand_landmarks:
			self.selectedHand = self.result.multi_hand_landmarks[handNumber]
			for id,landmark in enumerate(self.selectedHand.landmark):
				if draw:
					# print(id,landmark)
					height,width,channels = img.shape
					cX,cY = int(landmark.x * width),int(landmark.y * height)

					# print(id,cX,cY)
					self.landMarkList.append([id,cX,cY])
		
		return self.landMarkList

	def fingers_Fisted_Splayed(self):
		
		self.tip_IDX = [4,8,12,16,20]
		self.fingers = []

		if len(self.landMarkList) != 0:

			if self.landMarkList[self.tip_IDX[0]][1] > self.landMarkList[self.tip_IDX[0]-1][1] :
				self.fingers.append(0)
			else:
				self.fingers.append(1)


			for i in range(1,5):
					                       
				if (self.landMarkList[self.tip_IDX[i]][2] > self.landMarkList[self.tip_IDX[i]-1][2]):
					self.fingers.append(0)
				else:
					self.fingers.append(1)
				
		self.fingersCount = self.fingers.count(1)
		
		return list(self.fingers)
					


def main():

	currentTime = 0
	previousTime = 0

	cap = cv2.VideoCapture(0)
	detector = handDetector()

	cap.set(cv2.CAP_PROP_FPS, 60)

	while True:
		_,img = cap.read()
		img = detector.HandDetection(img)
		img = cv2.flip(img,1)
		detector.findPosition(img)
		

		currentTime = time.time()
		fps = 1/(currentTime-previousTime)
		previousTime = currentTime

		font = cv2.FONT_HERSHEY_COMPLEX
		cv2.putText(img,text=str(int(fps)),org=(10,70),fontFace=font,fontScale=2,color=(255,0,0),thickness=3)
		cv2.imshow("Tracking",img)

		if cv2.waitKey(1) & 0xFF == 27:
			break

	cv2.destroyAllWindows()



if __name__ == '__main__':
	main()