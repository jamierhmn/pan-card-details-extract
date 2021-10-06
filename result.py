# Initializing data variable
import re
def result(text):
    name = None
    fname = None
    dob = None
    pan = None
    nameline = []
    dobline = []
    panline = []
    text0 = []
    text1 = []
    text2 = []

    # Searching for PAN
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n', '')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    text1 = list(filter(None, text1))
    # print(text1)
    return text1


# to remove any text read from the image file which lies before the line 'Income Tax Department'
def remove_before_income_tax(text1):
    lineno = 0  # to start from the first line of the text file.

    for wordline in text1:
        xx = wordline.split('\n')
        if ([w for w in xx if re.search(
            '(INCOMETAXDEPARWENT @|mcommx|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$',
            w)]):
            text1 = list(text1)
            lineno = text1.index(wordline)
            break

    # text1 = list(text1)
    text0 = text1[lineno + 1:]
    print("text0=",text0)  # Contains all the relevant extracted text in form of a list - uncomment to check
    return text0




