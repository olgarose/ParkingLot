import cv2
import numpy as np

img = cv2.imread("../tree_lot.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel_size = 5
# blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)


blur_gray = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)
cv2.imshow("blur", blur_gray)
edges = cv2.Canny(blur_gray, 50, 150, apertureSize=3)
cv2.imshow("canny", edges)
lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi/180, threshold=80, minLineLength=15, maxLineGap=5)
print(lines)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)


cv2.imshow("hough", img)
cv2.waitKey(0)
