# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:37:44 2024

@author: AI-Developer
"""

# =============================================================================
# Import Libraries
# =============================================================================
import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt
from skimage.filters import threshold_local

# =============================================================================
# Image Processing Setup
# =============================================================================
img_path = "paper.jpg"
input_img = cv2.imread(img_path)
resize_factor = input_img.shape[0] / 500.0
scaled_img = imutils.resize(input_img, height=500)

# Convert image to grayscale and blur it
grayscale = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)

# Perform edge detection
edge_map = cv2.Canny(grayscale, 75, 200)

# =============================================================================
# Detect Contours
# =============================================================================
contours = cv2.findContours(edge_map.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key = cv2.contourArea, reverse=True)[:5]

# Loop through contours and find quadrilateral contour
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx_points = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    if len(approx_points) == 4:
        document_contour = approx_points
        break

# =============================================================================
# Perspective Transformation Helpers
# =============================================================================
def reorder_points(points):
    ordered_points = np.zeros((4, 2), dtype="float32")
    
    point_sum = points.sum(axis=1)
    ordered_points[0] = points[np.argmin(point_sum)]
    ordered_points[2] = points[np.argmax(point_sum)]
    
    point_diff = np.diff(points, axis=1)
    ordered_points[1] = points[np.argmin(point_diff)]
    ordered_points[3] = points[np.argmax(point_diff)]
    
    return ordered_points

def perspective_transform(image, points):
    rect = reorder_points(points)
    (tl, tr, br, bl) = rect
    
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    
    destination_points = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")
    
    transformation_matrix = cv2.getPerspectiveTransform(rect, destination_points)
    warped_image = cv2.warpPerspective(image, transformation_matrix, (max_width, max_height))
    
    return warped_image

# =============================================================================
# Apply Transformation and Thresholding
# =============================================================================
warped_img = perspective_transform(input_img, document_contour.reshape(4, 2) * resize_factor)
grayscale_warped = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to simulate a scanned effect
threshold_value = threshold_local(grayscale_warped, 11, offset=10, method="gaussian")
final_output = (grayscale_warped > threshold_value).astype("uint8") * 255

# Display results
cv2.imshow("Original Image", imutils.resize(input_img, height=650))
cv2.imshow("Scanned Effect", imutils.resize(final_output, height=650))
cv2.waitKey(0)
