# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import re
import cv2,glob
from preprocess import load_preprocess,Run_tesseract
from result import  result,remove_before_income_tax
# from nostril import nonsense
from flask import Flask, request, redirect, url_for
app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_image():
  for img in glob.glob("./uploads/*.*"):
      if(allowed_file(img)):

          cv_img = cv2.imread(img)
          return cv_img

#read image from folder upload and extract images text
@app.route('/', methods=['GET', 'POST'])
def Run():
    image =read_image()
    print("image found=", image)
    #***************************************************88

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dictofitems = {}
    # image = cv2.imread(args["image"])
    filename = load_preprocess(image,gray)
    text = Run_tesseract(filename)
    text1= result(text)
    listofitems=remove_before_income_tax(text1)

    dictofitems["name"] = listofitems[0]
    dictofitems["Father Name"] = listofitems[1]
    dictofitems["dateofbirth"] = listofitems[2]

    print(dictofitems)
    return(dictofitems)

if __name__ == "__main__":
     app.run(debug = True, host = "127.0.0.1",port=5000)
