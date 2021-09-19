# importing required modules
import PyPDF2
import pytesseract
import fitz
import io
from PIL import Image
import os
import datetime

# for date
todaydate = datetime.datetime.now()

# file path you want to extract images from
file = "test1.pdf"
# open the file
pdf_file = fitz.open(file)

#create twxt file
imagetextfile = open(f'{file}.csv', 'w')

# iterate over PDF pages
for page_index in range(len(pdf_file)):
    # get the page itself
    page = pdf_file[page_index]
    image_list = page.getImageList()
    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    for image_index, img in enumerate(page.getImageList(), start=1):
        # get the XREF of the image
        xref = img[0]
        # extract the image bytes
        base_image = pdf_file.extractImage(xref)
        image_bytes = base_image["image"]
        # get the image extension
        image_ext = base_image["ext"]
        # load it to PIL
        image = Image.open(io.BytesIO(image_bytes))
        # save it to local disk
        imagepath = "images/"
        try:
            os.mkdir(imagepath)
        except:
            FileExistsError
        # image.save(open(f"{imagepath}{file}_{page_index+1}_{image_index}.{image_ext}", "wb"))
        image.save(open(f"{imagepath}{file}_{todaydate.strftime('%d%m%Y')}_page{page_index+1}_image{image_index}.{image_ext}", "wb"))

        # convert image into text
        print(pytesseract.image_to_string(image))
        imagetextfile.write(f"{file},{todaydate.strftime('%d%m%Y')},{pytesseract.image_to_string(image)}")

imagetextfile.close()
