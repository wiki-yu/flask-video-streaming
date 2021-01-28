import cv2

img = cv2.imread("1.jpg")
height = 500
width = 500
dim = (height, width)
img1 = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("img", img1)
cv2.waitKey(0)