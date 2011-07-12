import os
from tkFileDialog import askopenfilename, asksaveasfilename
from shutil import copyfile
import zipfile
import time
import datetime

from libs.pyPdf import PdfFileWriter, PdfFileReader

from libs.defs import *

# output folder
output_folder = os.path.abspath("output")

# get a filename
pdf_filename = askopenfilename(
    title="Choose PDF File",
    filetypes=[
        ("PDF file", ".pdf"),
        ],
    initialdir="%UserProfile%",
    )
print "Chosen file: %s" % pdf_filename

# empty the output directory
empty_directory(output_folder)

# copy pdf to destination and update filename
copyfile(pdf_filename, os.path.join(output_folder, "file.pdf"))
pdf_filename = os.path.join(output_folder, "file.pdf")

# convert to image set
print "generating screenshots..."
os.system(
    # "%PROGRAMFILES%\\ImageMagick-6.7.0-Q16\\convert.exe \"%s\" -resize 500x500 \"%s\\scr.png\"" % (
    "convert \"%s\" -resize 500x500 \"%s\\scr.png\"" % (
        pdf_filename,
        output_folder
        )
    )
print "screenshots generated"

# open pdf file
pdf_file = open(pdf_filename, "rb")
pdf = PdfFileReader(pdf_file)

# iterate through all pages
for i in range(0, pdf.getNumPages()):
    # split pages and save files
    outputFileName = pdf_filename.replace('.pdf', '-%d.pdf' % i)
    output = PdfFileWriter()
    output.addPage(pdf.getPage(i))
    outputStream = open(outputFileName, "wb")
    output.write(outputStream)
    outputStream.close()
    
    # convert to text and save into a file
    convert_pdf(outputFileName)
    translate_txt(outputFileName.replace('.pdf', '.txt'))

    # remove pdf page file
    # os.remove(outputFileName)
    
    print "page %d is processed" % (i + 1)

# close pdf file
pdf_file.close()

# choose output zip filename
zip_filename = asksaveasfilename(
    title="Save as",
    initialfile=datetime.datetime.now().strftime("%Y-%m-%d.zip"),
    initialdir="%UserProfile%\\Desktop",
    )

# zip output folder
print "zipping output files"
output_files = os.listdir(output_folder)
# zip_filename = os.path.join(output_folder, "output.zip")
zip_file = zipfile.ZipFile(zip_filename, "w")

for entity in output_files:
    filename = os.path.join(output_folder, entity)

    if os.path.isfile(filename):
        zip_file.write(filename, entity)

    os.remove(filename)

zip_file.close()
print "done!"

# wait 5 seconds and close the window
time.sleep(4)
