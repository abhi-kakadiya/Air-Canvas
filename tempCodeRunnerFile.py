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
		

			if len(X_Y_Points) >= 0:
				if len(X_Y_Points) == 0:
						X_Y_Points.append([x1,y1])

				if len(X_Y_Points) > 0:
					x1 = (X_Y_Points[-1][0] + x1) // 2
					y1 = (X_Y_Points[-1][1] + y1) // 2
					x1 = (X_Y_Points[-1][0] + x1) // 2
					y1 = (X_Y_Points[-1][1] + y1) // 2
	
					# print(X_Y_Points)
					X_Y_Points.append([x1,y1])
			
			cv2.circle(img,radius=20,center=(x1,y1),color=drawColor,thickness=-1)		
			
			# BY DEFAULT IT WILL NOT START DRAWING AT THE STARTING INDEX OF X AND Y --> (0,0)
			if xStart == 0 and yStart == 0: