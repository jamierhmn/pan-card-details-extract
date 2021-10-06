import cv2
import os
import re
import io
import json
import ftfy
import argparse
from PIL import Image
import pytesseract

##############################################################################################################
###################### Section 2: Load the image -- Preprocess it -- Write it to disk ########################
##############################################################################################################
def load_preprocess(image,gray):
    # load the example image and convert it to grayscale

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    return filename


##############################################################################################################
######################################## Section 3: Running PyTesseract ######################################
##############################################################################################################

def Run_tesseract(filename):
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename), lang='eng')
    # add +hin after eng within the same argument to extract hindi specific text - change encoding to utf-8 while writing
    os.remove(filename)
    # print(text)

    # show the output images
    # cv2.imshow("Image", image)
    # cv2.imshow("Output", gray)
    # cv2.waitKey(0)

    # writing extracted data into a text file
    text_output = open('outputbase.txt', 'w', encoding='utf-8')
    text_output.write(text)
    text_output.close()

    file = open('outputbase.txt', 'r', encoding='utf-8')
    text = file.read()
    # print(text)

    # Cleaning all the gibberish text
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    return text


