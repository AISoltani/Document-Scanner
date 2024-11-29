# Document Scanner Script

This Python script implements an automatic document scanning and perspective transformation process to simulate a scanned effect for an image containing a document. The script utilizes several image processing techniques, including edge detection, contour detection, and perspective warping to extract and enhance the document from an image.

## Requirements

To run this script, you'll need to install the following Python libraries:

- `numpy`
- `opencv-python`
- `imutils`
- `matplotlib`
- `scikit-image`

You can install these dependencies using `pip`:

```bash
pip install numpy opencv-python imutils matplotlib scikit-image
```
Here's a well-structured README.md documentation for your code, formatted as requested. You can copy and paste the following into your README.md file on GitHub:

markdown
Copy code
# Document Scanner Script

This Python script implements an automatic document scanning and perspective transformation process to simulate a scanned effect for an image containing a document. The script utilizes several image processing techniques, including edge detection, contour detection, and perspective warping to extract and enhance the document from an image.

## Requirements

To run this script, you'll need to install the following Python libraries:

- `numpy`
- `opencv-python`
- `imutils`
- `matplotlib`
- `scikit-image`

You can install these dependencies using `pip`:

```bash
pip install numpy opencv-python imutils matplotlib scikit-image
```
Description
Key Steps
Image Processing:

The input image is read from a file path (paper.jpg) and resized to a manageable height for further processing.
The image is converted to grayscale and blurred to reduce noise and improve edge detection.
The Canny edge detector is applied to highlight edges in the image.
Contour Detection:

The script detects contours in the edge map and sorts them by area, selecting the top 5 largest contours.
It then loops through the contours to find a quadrilateral contour, which likely represents the document in the image.
Perspective Transformation:

Once the document contour is found, the script uses the cv2.getPerspectiveTransform function to apply a perspective transformation, simulating the effect of viewing the document from the top.
Thresholding:

The warped image (perspective-corrected document) is then thresholded to simulate a scanned effect, using adaptive thresholding from scikit-image.
Display Output:

The original image and the transformed image (with the "scanned" effect) are displayed side by side.

## Code Walkthrough

### 1. Image Processing Setup

```bash
img_path = "paper.jpg"
input_img = cv2.imread(img_path)
resize_factor = input_img.shape[0] / 500.0
scaled_img = imutils.resize(input_img, height=500)
```
The image is read from a file and resized to a height of 500 pixels. The resize_factor will be used later for scaling points in the transformation process.

2. Grayscale Conversion, Blurring, and Edge Detection
```bash
grayscale = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
edge_map = cv2.Canny(grayscale, 75, 200)
```

The image is converted to grayscale and blurred to reduce noise.
Canny edge detection is performed to find the edges in the image.
3. Contour Detection
```bash
contours = cv2.findContours(edge_map.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
```
The contours are found in the edge map and sorted by area. The script keeps the top 5 largest contours to filter out noise and focus on potential document contours.
4. Finding the Document Contour
```bash
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx_points = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    if len(approx_points) == 4:
        document_contour = approx_points
        break

```
The script loops through the sorted contours, approximating the perimeter of each contour. It looks for the contour that forms a quadrilateral (i.e., 4 points), which is assumed to be the document.
5. Perspective Transformation
```bash
def reorder_points(points):
    ...
    
def perspective_transform(image, points):
    ...

```
The reorder_points function ensures that the points representing the document are ordered in a way that corresponds to the top-left, top-right, bottom-right, and bottom-left corners.
The perspective_transform function uses these points to warp the image into a top-down view of the document.

6. Thresholding
```bash
threshold_value = threshold_local(grayscale_warped, 11, offset=10, method="gaussian")
final_output = (grayscale_warped > threshold_value).astype("uint8") * 255
```
Adaptive thresholding is applied to the warped image to simulate a scanned effect, where darker areas are turned black, and lighter areas are turned white.
7. Displaying the Result
```bash
cv2.imshow("Original Image", imutils.resize(input_img, height=650))
cv2.imshow("Scanned Effect", imutils.resize(final_output, height=650))
cv2.waitKey(0)
```
The original image and the final scanned effect are displayed in separate windows.


