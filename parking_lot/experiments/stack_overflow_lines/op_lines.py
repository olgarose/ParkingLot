import cv2 as cv

window_name = ("Sobel Demo - Simple Edge Detector")
scale = 1
delta = 0
ddepth = cv.CV_16S
## [variables]

src = cv.imread("p2.jpg")
## [reduce_noise]
# Remove noise by blurring with a Gaussian filter ( kernel size = 3 )
src = cv.GaussianBlur(src, (3, 3), 0)
## [reduce_noise]

## [convert_to_gray]
# Convert the image to grayscale
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
## [convert_to_gray]

## [sobel]
# Gradient-X
# grad_x = cv.Scharr(gray,ddepth,1,0)
grad_x = cv.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

# Gradient-Y
# grad_y = cv.Scharr(gray,ddepth,0,1)
grad_y = cv.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
## [sobel]

## [convert]
# converting back to uint8
abs_grad_x = cv.convertScaleAbs(grad_x)
abs_grad_y = cv.convertScaleAbs(grad_y)
## [convert]

## [blend]
## Total Gradient (approximate)
grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
## [blend]


_, contours, hierarchy = cv.findContours(grad, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

for x in contours:
    area = cv.contourArea(x)
    print("Area ", area)
    if area > 10:
        cv.drawContours(src, x, -1, (0, 255, 0), 1)
        M = cv.moments(x)
        centroid_x = int(M["m10"] / M["m00"])
        centroid_y = int(M["m01"] / M["m00"])
        cv.circle(src, (centroid_x, centroid_y), 5, 255, -1)
        print(centroid_x)
        print(centroid_y)
        print()

cv.imshow("normalThreshold", src)
cv.waitKey(0)
cv.destroyAllWindows()
