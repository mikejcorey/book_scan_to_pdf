import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from imutils.perspective import four_point_transform


def enhance_img(img):
    '''Turn up sharpness and contrast before cropping'''
    sharpened = ImageEnhance.Sharpness(img).enhance(3.0)
    contrasted = ImageEnhance.Contrast(sharpened).enhance(2.0)
    return img


def crop_to_white_boundary_imutils(img_path, cropped_path):
    ''' There is a big black border around the actual pages when the raw scans come in from the book scanner. Let's get rid of it, which 1) helps to normalize the position of the actual records, no matter where the person scanning placed the book vertically 2) might save a little space. This version also attempts to rotate the page somewhat to get the page level. Source: https://stackoverflow.com/questions/66219912/how-to-rotate-an-image-to-align-the-text-for-extraction'''
    # Load image, grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Find contours and sort for largest contour
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None

    for c in cnts:
        # Perform contour approximation
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            displayCnt = approx
            break

    try:
        # Obtain birds' eye view of image
        warped = four_point_transform(image, displayCnt.reshape(4, 2))
    except AttributeError:
        print("Couldn't find four_point_transform solution, will try again with alternate method")
        return False
    
    # Check to see how big the warped image is
    if warped.shape[0] >= 50 and warped.shape[1] >= 50:
        cv2.imwrite(cropped_path, warped, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return cropped_path

    print("Resulting image was too small, trying alternate method...")
    return False


def crop_to_white_boundary_cv2(img_path, cropped_path):
    ''' There is a big black border around the actual pages when the raw scans come in from the book scanner. Let's get rid of it, which 1) helps to normalize the position of the actual records, no matter where the person scanning placed the book vertically 2) might save a little space. This is the original version from scanner_wars.'''
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

    blurred = cv2.blur(gray, (25, 25))  # Introduce a little blur to get rid of individual shiny reflections in the edge zone

    # threshold to find the white-ish areas of the document
    retval, thresh_gray = cv2.threshold(blurred, thresh=127, maxval=255, type=cv2.THRESH_BINARY)
    # over 127 is white, 0 is black 255 is white

    # find where the white area is is and make a cropped region
    points = np.argwhere(thresh_gray == 255)  # find where the white pixels are
    points = np.fliplr(points)  # store them in x,y coordinates instead of row,col indices

    x, y, w, h = cv2.boundingRect(points)  # create a rectangle around those points
    # print(x, y, w, h)
    crop = img[y:y + h, x:x + w]  # create a cropped region of the original image
    #** EXPLAIN Y:Y + H, ETC

    cv2.imwrite(cropped_path, crop, [cv2.IMWRITE_JPEG_QUALITY, 80])

    return cropped_path


def rotate_img(img_path, img):
    # Get last digit of page number to determine rotation
    page_num_final_digit = os.path.basename(img_path).split('.')[0][-1]
    
    odd = str([1, 3, 5, 7, 9])
    even = str([2, 4, 6, 8, 0])

    rotation_value = 0

    if page_num_final_digit[-1] in odd:
        rotation_value = 270
    elif page_num_final_digit[-1] in even:
        rotation_value = 90
    else:
        rotation_value = 0
        print('file' + os.path.basename(raw_page) + ' does not have a valid page number')

    return img.rotate(rotation_value, expand=True)


def rotate_and_crop_image(page_object):
    '''Runs each page through a series of steps to prepare for merging into a PDF.
    Because it will be used with multithreading, input is only a single argument that needs to be parsed:
    
    Expected input: {'book_root': 'root/folder/of/book', 'page_path': 'path/to/a/page.jpg'}
    '''
    book_root = page_object['book_root']
    img_path = page_object['page_path']

    print(f"Starting {img_path}...")

    filename_parts = os.path.basename(img_path).split('.')
    file_base = filename_parts[0]
    file_ext = filename_parts[1]

    temp_path = os.path.join(book_root, 'temp_images', f"{file_base}_rotated.{file_ext}")
    cropped_path = os.path.join(book_root, 'cropped_pages', f"{file_base}_cropped.{file_ext}")

    # The first two operations, rotate to correct general orientation and enhance, are done with Pillow/PIL
    img = Image.open(img_path)
    img_rotated = rotate_img(img_path, img)
    img_enhanced = enhance_img(img_rotated)
    img_enhanced.save(temp_path, dpi=(300, 300))

    # Cropping is done with imutils/cv2 and if that doesn't work, using cv2 only
    img_cropped_path = crop_to_white_boundary_imutils(temp_path, cropped_path)
    if img_cropped_path:
        return img_cropped_path
    else:
        img_cropped_path = crop_to_white_boundary_cv2(temp_path, cropped_path)
    return img_cropped_path
