# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import re
import cv2,glob
from preprocess import load_preprocess,Run_tesseract
from result import  result,remove_before_income_tax
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #for maximum file upload size

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "file upload success"


def Read_image_folder():
    imdir = 'path/to/files/'
    ext = ['png', 'jpg', 'gif']  # Add image formats here

    files = []
    [files.extend(glob.glob(imdir + '*.' + e)) for e in ext]

    images = [cv2.imread(file) for file in files]
    print(images)

#@app.route('/')
def Main():
   # ap = argparse.ArgumentParser()
   # ap.add_argument("-i", "--image", required=True,
    #            help="path to input image to be OCR'd")
   # ap.add_argument("-p", "--preprocess", type=str, default="thresh",
    #            help="type of preprocessing to be done, choose from blur, linear, cubic or bilateral")
   # args = vars(ap.parse_args())

    #***************************************************88

    image = cv2.imread(UPLOAD_FOLDER/*.)
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


if __name__ == "__main__":
    #app.run(debug = True, host = "127.0.0.1",port=5000)
    Main()