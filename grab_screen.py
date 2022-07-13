"""
Script for image processing. Original image is transformed into
black&white (b&w) and edges are detected. Finally the most dominant
edges are considered the lanes and are drawn on the original image.
Adapted from Sentdex: https://pythonprogramming.net/finding-lanes-self-driving-car-python-plays-gta-v/?completed=/hough-lines-python-plays-gta-v/
"""

from draw_lanes import draw_lanes
import cv2
import numpy as np

def roi(img, vertices):
    """
    Defining a region of interest (roi) of a given image
    """
    #blank mask:
    mask = np.zeros_like(img)
    
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, 255)
    
    #returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(image):
    """
    Converts given image into b&w and detects edges
    of the image in the defined roi.
    Returns b&w image with highlighted edges and original image
    with the two most dominant lanes.
    """
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1 = 150, threshold2=190)
    processed_img = cv2.GaussianBlur(processed_img,(3,3),0)
    vertices = np.array([[10,500],[10,300],[300,250],[500,250],[800,300],[800,500],
                         ], np.int32)
    processed_img = roi(processed_img, [vertices])

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                                     rho   theta   thresh  min length, max gap:        
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]),      20,       15)
    lane_1 = 0
    lane_2 = 0
    try:
        l1, l2, lane_1,lane_2 = draw_lanes(original_image,lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
                
                
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img,original_image, lane_1, lane_2
