import cv2
import numpy as np

# read in image... opencv converts to numpy ndarray
img = cv2.imread('images/IMG_6720.jpg')
img = cv2.resize(img, (600, 800))   

# convert image to gray scale
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# threshold on image
# note the high threshold so we are easily able to destinguish between the white paper and everything else
# this works as long as we are not looking at an all white background
ret,thresh = cv2.threshold(imgray,200,255,cv2.THRESH_BINARY)
# contouring, this helps to find the white paper
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# look for the contour with the largest area this will be the white paper with barcode on it
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt=contours[max_index]

x,y,w,h = cv2.boundingRect(cnt)
#cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)


# method to find corners
def find_rectangle_corners():
	def max_x(pixel):
		return pixel[0][0]

	def max_y(pixel):
		return pixel[0][0]
	# these functions will be used to find the corners of the paper

# once the corners are found we do the corresponding geometry to find how large the barcode appears in the image
# 	+ this value will tell us how far away we are
# find 'skew' between the front of the paper and the back of the paper
# 	+ this value in combination with our distance from the paper will tell us what angle we are looking at the paper from
# 	+ i.e. directly over it or some angle x from it
# lastly we will need to detect the three smaller squares within the barcode
# 	+ this will allow us to find how the barcode is rotated and will give us our third position

# the combination of these three points will allow us to find the (x,y,z) coordinate at which the picture was taken


cv2.drawContours(img, contours, max_index, (0,125,0), 3)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

