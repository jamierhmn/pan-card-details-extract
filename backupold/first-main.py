# We import the necessary packages
# import the needed packages
import cv2
import os, argparse
import pytesseract
from PIL import Image
import re

# We then Construct an Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",
                required=True,
                help="Path to the image folder")
ap.add_argument("-p", "--pre_processor",
                default="thresh",
                help="the preprocessor usage")
args = vars(ap.parse_args())

# We then read the image with text
images = cv2.imread(args["image"])

# convert to grayscale image
gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)

# checking whether thresh or blur
if args["pre_processor"] == "thresh":
    cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
if args["pre_processor"] == "blur":
    cv2.medianBlur(gray, 3)

# memory usage with image i.e. adding image to memory
filename = "{}.jpg".format(os.getpid())
cv2.imwrite(filename, gray)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
#print(text)

key_words = ["GOVT. OF INDIA"]
line =  text
found = re.findall('('+'|'.join(key_words)+')'+r'\s+([ A-Z]+[A-Z])',line)
name=found[0][1]
# show the output images
#cv2.imshow("Image Input", images)
#cv2.imshow("Output In Grayscale", gray)
res = line.partition(name)[2]

print(res)
#cv2.waitKey(0)