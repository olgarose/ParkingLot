import cv2
import numpy as np

img = cv2.imread("../tree_lot.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
cv2.imshow("blur", blur_gray)
edges = cv2.Canny(blur_gray, 50, 150, apertureSize=3)
cv2.imshow("canny", edges)
lines = cv2.HoughLines(edges, 5, np.pi / 180, 10)

for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow("hough", img)
cv2.waitKey(0)
