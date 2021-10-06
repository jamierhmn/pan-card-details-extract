# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import re
import cv2
from preprocess import load_preprocess,Run_tesseract
from result import  result,remove_before_income_tax
# from nostril import nonsense


################################################################################################################
############################# Section 1: Initiate the command line interface ###################################
################################################################################################################
if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done, choose from blur, linear, cubic or bilateral")
    args = vars(ap.parse_args())

    #***************************************************88
    image = cv2.imread(args["image"])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we should apply thresholding to preprocess the
    # image
    if args["preprocess"] == "thresh":
          grfilenameay = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    elif args["preprocess"] == "adaptive":
         gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    if args["preprocess"] == "linear":
         gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    elif args["preprocess"] == "cubic":
         gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


    if args["preprocess"] == "blur":
         gray = cv2.medianBlur(gray, 3)

    elif args["preprocess"] == "bilateral":
         gray = cv2.bilateralFilter(gray, 9, 75, 75)

    elif args["preprocess"] == "gauss":
         gray = cv2.GaussianBlur(gray, (5, 5), 0)
#******************************************************************
    dictofitems = {}
    image = cv2.imread(args["image"])
    filename = load_preprocess(image,gray)
    text = Run_tesseract(filename)
    text1= result(text)
    listofitems=remove_before_income_tax(text1)

    dictofitems["name"] = listofitems[0]
    dictofitems["Father Name"] = listofitems[1]
    dictofitems["dateofbirth"] = listofitems[2]

    print(dictofitems)
