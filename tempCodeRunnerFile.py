if pArray.shape[0] >= 4:
			# 	# print(pArray.shape)
			# 	tck, u = splprep(pArray, u=None, s=0.0, per=1)
			# 	x_interp, y_interp = splev(np.linspace(0, 1, num=100), tck, der=0)
			# 	interpPoints = np.column_stack((x_interp, y_interp))
			# 	cv2.polylines(canvas, [np.int32(interpPoints)], False, drawColor, thickness=3)