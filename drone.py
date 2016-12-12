'''
Author: Jordan Ott
DroneDeploy Coding Test

Method
# Using OpenCV
# we can use pixel scaling to tell us our distance from the barcode
#	+ we know the barcode is printed on an 8.5 by 11 inch piece of paper
#	+ at 1 foot away the paper is 450 by 580 px
# 	+ at 2 feet away the paper is 219 by 285 px
# 	+ measuring the dimensions of the paper we can use these scaling factors to tell how far away the photo was taken
# find 'skew' between the front of the paper and the back of the paper
# 	+ this value in combination with our distance from the paper will tell us what angle we are looking at the paper from
# 	+ i.e. directly over it or some angle x from it
# lastly we will need to detect the three smaller squares within the barcode
# 	+ this will allow us to find how the barcode is rotated and will give us our third position
'''
import cv2
import numpy as np
import math

# read in image... opencv converts to numpy ndarray
img = cv2.imread('images/IMG_6723.jpg')
img = cv2.resize(img, (600, 800))   

def mid_point(point_A, point_B):
	return [(point_A[0]+point_B[0])/2, (point_A[1]+point_B[1])/2]

def distance(point_A, point_B):
	return math.sqrt( (point_A[0] - point_B[0])**2 + (point_A[1] - point_B[1])**2 )
# convert image to gray scale
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# note the high threshold so we are easily able to destinguish between the white paper and everything else
# this works as long as we are not looking at an all white background
ret,thresh = cv2.threshold(imgray,190,255,cv2.THRESH_BINARY)

# contouring, this helps to find the white paper
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# look for the contour with the largest area this will be the white paper with barcode on it
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt=contours[max_index]

x,y,w,h = cv2.boundingRect(cnt)

# this portion will find how the barcode is rotated
d = {}
for c in contours:
	# finding centers of all contours, this will help to find the 3 squares which designate the orientation of the symbol
	M = cv2.moments(c)
	if M["m00"] == 0:
		continue
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	if d.get((cX, cY),0):
		d[(cX, cY)] += 1
	else:
		d[(cX, cY)] = 1
three_hits = []
two_hits = []
for key in d:
	if d[key] == 3:
		three_hits.append(key)
	if d[key] == 2:
		two_hits.append(key)
# this will be used if the rotation of the barcode is necassary, for now I will use the rotation of the rectangle 
if len(three_hits) == 3:
	pass
elif len(three_hits) == 2:
	pass
else:
	pass

rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)

box = np.int0(box)
cv2.drawContours(img,[box],0,(0,0,255),2)
angle = rect[2]

min_dist = 1000
# here we find the distance, in pixels, from the contour corner to the bounded rectangle
for point in box:
	temp_dist = distance(cnt[0][0],point)
	min_dist = min(min_dist,temp_dist)
# the min_distance will be used to show the amount of skew in the image due to the angle the phone is at relative to the barcode


# here we use the bounded rectangle box to determine how far away from the barcode the camera is in feet
A = box[0]
B = box[1]
C = box[2]
D = box[3]

A_B = mid_point(A,B)
C_D = mid_point(C,D)

A_D = mid_point(A,D)
B_C = mid_point(B,C)

AD_BC_dist = distance(A_D,B_C)
AB_CD_dist = distance(A_B,C_D)

if AD_BC_dist > AB_CD_dist:
	width = AD_BC_dist
	height = AD_BC_dist
else:
	width = AD_BC_dist
	height = AD_BC_dist

# at 1 foot away the paper appears 450 by 580 pixels
# this is needed for a depth ratio
width_ratio_1foot = 450
height_ratio_1foot = 580
# at 2 feet away the paper appears 219 by 285 pixels 
width_ratio_2foot = 219
height_ratio_2foot = 285

# use scaling factors from 1 foot and 2 feet 
one_foot_height = 1/(height/height_ratio_1foot)
one_foot_width = 1/(width/width_ratio_1foot)

two_foot_height = 2/(height/height_ratio_2foot)
two_foot_width = 2/(width/width_ratio_2foot)

# we take the average of all four
distance_away = (one_foot_width + one_foot_height + two_foot_width + two_foot_height)/4

print("Image was taken {0:.2f} feet away, {1:.2f} degrees from birds eye view and the barcode is rotated {2:.2f} degrees".format(distance_away,min_dist,angle))

cv2.drawContours(img, contours, max_index, (0,125,0), 3)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

