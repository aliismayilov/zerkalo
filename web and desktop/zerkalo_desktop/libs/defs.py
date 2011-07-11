import os
from xml.dom.minidom import parse

from libs.PIL import Image

from libs.pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from libs.pdfminer.converter import TextConverter
from libs.pdfminer.layout import LAParams
from libs.pdfminer.pdfparser import PDFDocument, PDFParser
from libs.pdfminer.pdfdevice import PDFDevice
from libs.pdfminer.cmapdb import CMapDB

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
    return True

def translate_txt(path):
    # load xml dictionary
    xml = parse("libs/chars.xml")
    
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
    
    # save to file
    output_string_utf8 = output_string.encode('UTF-8')
    txt_output = open(path, 'w')
    txt_output.write(output_string_utf8)
    txt_output.close()

def get_xml_element_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return unicode(''.join(rc))

def empty_directory(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception, e:
            print e
