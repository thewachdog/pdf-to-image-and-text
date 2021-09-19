import PyPDF2
import pytesseract
import fitz
import io
from PIL import Image
import os
import datetime

todaydate = datetime.datetime.now()
file = "test1.pdf"
pdf_file = fitz.open(file)
imagetextfile = open(f'{file}.csv', 'w')

for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    image_list = page.getImageList()
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    for image_index, img in enumerate(page.getImageList(), start=1):
        xref = img[0]
        base_image = pdf_file.extractImage(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image = Image.open(io.BytesIO(image_bytes))
        imagepath = "images/"
        try:
            os.mkdir(imagepath)
        except:
            FileExistsError
        image.save(open(f"{imagepath}{file}_{todaydate.strftime('%d%m%Y')}_page{page_index+1}_image{image_index}.{image_ext}", "wb"))
        imagetextfile.write(f"{file},{todaydate.strftime('%d%m%Y')},{pytesseract.image_to_string(image)}")
imagetextfile.close()
