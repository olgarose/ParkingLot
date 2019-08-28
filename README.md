# Parking Space Detection in OpenCV
For a fun weekend project, I decided to play around with the OpenCV (Open Source Computer Vision) library in python.

OpenCV is an extensive open source library (available in python, Java, and C++) that's used for image analysis and is pretty neat.

The lofty goal for my OpenCV experiment was to take any static image or video of a parking lot and be able to automatically detect whenever a parking space was available or occupied.

Through research and exploration, I discovered how lofty of a goal that was (at least for the scope of a weekend). What I was able accomplish was to detect how many spots were available in a parking lot, with just a bit of upfront work by the user.

This page is a walkthrough of my process and what I learned along the way.

I'll start with an overview, then talk about my process, and end with some ideas for future work.

## Overview
[![Unedited parking lot](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/parking_shot.png)](https://www.youtube.com/watch?v=SszV59YBn_o)

The above link takes you to a video of the parking space detection program in action.

To run:
```python
python main.py --image images/parking_lot_1.png --data data/coordinates_1.yml --video videos/parking_lot_1.mp4 --start-frame 400
```

Program flow is as follows:
- User inputs file name for a video, a still image from the video, and a path for the output file of parking space coordinates.
- User clicks 4 corners for each spot they want tracked. Presses 'q' when all desired spots are marked.
- Video begins with the user provided boxes overlayed the video. Occupied spots initialized with red boxes, available spots with green.
    - Car leaves a space, the red box turns green.
    - Car drives into a free space, the green box turns red.

The data on the entering and exiting of these cars can be used for a number of purposes: closest spot detection, analytics on parking lot usage, and for those counters outside of parking garages that tell you how many cars are on each level (to name a few).

This project was my first tour through computer vision, so to get it working in a weekend, I went the "express learning" route. That consisted of auditing this [Computer Vision and Image Analytics course](https://www.edx.org/course/computer-vision-and-image-analysis), reading through [OpenCV documentation](https://docs.opencv.org/2.4/modules/refman.html), querying the net, and toggling OpenCV function parameters to see what happened. Overall, a lot of learning and a ton of fun.

## Process
### The beginning
My first thought was how can I tell whether a parking space is empty?

Well, if a space is empty, it would be the color of the pavement. Otherwise, it wouldn't be.

I also knew that I needed a way to mark the boundaries of the space, so that I could return the number of spots available.

Let's grab an image and head to the OpenCV docs!

### Line Detection
To detect the parking spots, I knew I could take advantage of the lines demarking the boundaries.

The Hough Transform is a popular feature extraction technique for detecting lines. OpenCV encapsulates the math of the Hough Transform into HoughLines(). Further abstraction in captured in HoughLinesP(), which is the probabilistic model of creating lines with the points that HoughLines() returns. For more info, check out the [OpenCV Hough Lines tutorial.](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html)

The following is a walkthrough to prepare an image to detect lines with the Hough Transform. Links point to OpenCV documentation for each function. Arguments for each function are given as keyword args for clarity.

[Reading](https://docs.opencv.org/master/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56) in this image:
```python
img = cv2.imread(filename='examples/hough_lines/p_lots.jpg')
```
![Org_hough](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/org.png)



I [converted it to gray scale](https://docs.opencv.org/master/d7/d1b/group__imgproc__misc.html#ga397ae87e1288a81d2363b61574eb8cab) to reduce the info in the photo:
```python
gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
```

![Gray_hough](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/s_gray.png)



Gave it a good [Gaussian blur](https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1) to remove even more unnecessary noise:
```python
blur_gray = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)
```
![Blur_hough](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/s_blur.png)



Detected the edges with [Canny](https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de):
```python
edges = cv2.Canny(image=blur_gray, threshold1=50, threshold1=150, apertureSize=3)
```
![Canny_hough](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/s_canny.png)


And then, a few behind-the-scenes rhos and thetas later, we have our [Hough Line](https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga8618180a5948286384e3b7ca02f6feeb) results.

```python
lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi/180, threshold=80, minLineLength=15, maxLineGap=5)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
```
![Hough_transform](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/s_line.png)




Well that wasn't quite what I expected.

I experimented a bit with the hough line, but toggling the parameters kept getting me the same one line.

A bit of digging and I found a [promising post on StackOverflow](https://stackoverflow.com/questions/45322630/how-to-detect-lines-in-opencv)

After following the directions of the top answer, I got this:

![SO_transform](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/stack_overflow_lines.png)


Which gave me more lines, but I still had to figure out which lines were part of the parking space and which weren't. Then, I would also need to detect when a car moved from a spot.

I was running into a challenge; with this approach, I needed an empty parking lot to overlay with an image of a non-empty lot. Which would also call for a mask to cover unimportant information (trees, light posts, etc.)

Given my scope for the weekend, it was time to find another approach.

### Drawing Rectangles

If my program wasn't able to detect parking spots on it's own, maybe it was reasonable to expect that the user give positions for each of the parking spots.

Now, the goal was to find a way to click on the parking lot image and to store the 4 points that made up a parking space for all of the spaces in the lot.

I discovered that I could do this using a [mouse as a "paintbrush"](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_mouse_handling/py_mouse_handling.html)

After some calculations for the center of the rectangle (to label each space), I got this:

![Drawn Rectangles](https://s3-us-west-2.amazonaws.com/parkinglot-opencv/draw_rectangles.png)

### Finishing touches

After drawing the rectangles, all there was left to do was examine the area of each rectangle to see if there was a car in there or not.

By taking each (filtered and blurred) rectangle, determining the area, and doing an average on the pixels, I was able to tell when there wasn't a car in the spot if the average was high (more dark pixels). I changed the color of the bounding box accordingly and viola, a parking detection program!

The code for drawing the rectangles and motion detection is pretty generic. It's seperated out into classes and should be reusable outside of the context of a parking lot. I have tested this with two different parking lot videos and it worked pretty well. I plan to make other improvements and try to seperate OpenCV references to make code easier to test. I'm open to ideas and feedback.

Check out [the code](https://github.com/olgarose/ParkingLot) for more!

## Future work
- Hook up a webcam to a Raspberry Pi and have live parking monitoring at home!
- [Transform parking lot video to have overview perspective](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html) (for clearer rectangles)
- Experiment with [HOG descriptors](https://gurus.pyimagesearch.com/lesson-sample-histogram-of-oriented-gradients-and-car-logo-recognition/) to detect people or other objects of interest


