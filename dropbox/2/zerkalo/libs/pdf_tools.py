from libs.pyPdf import PdfFileWriter, PdfFileReader
from libs.pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from libs.pdfminer.converter import TextConverter
from libs.pdfminer.layout import LAParams
from libs.pdfminer.pdfparser import PDFDocument, PDFParser
from libs.pdfminer.pdfdevice import PDFDevice
from libs.pdfminer.cmapdb import CMapDB

import os
from xml.dom.minidom import parse

# split pdf to pages and return pdf filenames
def pdf_split(filename, output_directory):
    # open pdf file
    pdf_file = open(filename, "rb")
    pdf = PdfFileReader(pdf_file)
    
    # list of pdf page filenames
    filenames = []

    # iterate through all pages
    for i in range(0, pdf.getNumPages()):
        # split pages and save files
        outputFileName = os.path.join(output_directory, os.path.basename(filename)[:-4] + '-%d.pdf' % (i + 1))
        output = PdfFileWriter()
        output.addPage(pdf.getPage(i))
        outputStream = open(outputFileName, "wb")
        output.write(outputStream)
        outputStream.close()
        
        filenames.append(outputFileName)
    
    return filenames

def extract_text(filename, chars_xml_filename):
    # converts pdf file to txt with the same name
    convert_pdf(filename)
    
    # and return translated text
    return translate_txt(filename[:-3] + 'txt', chars_xml_filename)

# converts pdf file to txt with the same name
def convert_pdf(path, outtype='txt', opts={}):
    outfile = path[:-3] + outtype
    outdir = '/'.join(path.split('/')[:-1])

    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    codec = 'utf-8'
    pageno = 1
    scale = 1
    showpageno = True
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
        elif k == '-m': maxpages = int(v)
        elif k == '-P': password = v
        elif k == '-o': outfile = v
        elif k == '-n': laparams = None
        elif k == '-A': laparams.all_texts = True
        elif k == '-D': laparams.writing_mode = v
        elif k == '-M': laparams.char_margin = float(v)
        elif k == '-L': laparams.line_margin = float(v)
        elif k == '-W': laparams.word_margin = float(v)
        elif k == '-O': outdir = v
        elif k == '-t': outtype = v
        elif k == '-c': codec = v
        elif k == '-s': scale = float(v)
    #
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFDocument.debug = debug
    PDFParser.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager()
    if not outtype:
        outtype = 'txt'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout
    if outtype == 'txt':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    else:
        return usage()

    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password)
    fp.close()
    device.close()

    outfp.close()

# translate text, remove file and return unicode string
def translate_txt(path, chars_xml_filename):
    # load xml dictionary
    xml = parse(chars_xml_filename)
    
    # create a dictionary
    dict = {}
    for key in xml.getElementsByTagName('key'):
        dict[get_xml_element_text(key.childNodes)] = key.getAttribute('value')
    
    # translate the text
    txt_input = open(path, 'r')
    output_string = ''
    for char in txt_input.read().decode('utf-8').lower():
        if dict.has_key(char):
            output_string += dict[char]
        else:
            output_string += ' '

    # close and remove input text file
    txt_input.close()
    os.remove(path)
    
    # remove whitespaces
    
    # return string in UTF
    return output_string.encode('UTF-8')

def get_xml_element_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return unicode(''.join(rc))

# generate pdf screenshot and get its filename
def pdf_screenshot(page_filename, scr_filename):
    os.system(
    "convert \"%s\" -resize 500x500 \"%s\"" % (
        page_filename,
        scr_filename,
        )
    )
    return scr_filename