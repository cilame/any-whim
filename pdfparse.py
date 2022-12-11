# 需要预装 pdfminer3k 库

from pdfminer.pdfinterp import PDFResourceManager,process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO, BytesIO

import requests
r = requests.get("http://www.commonlii.org/sg/journals/SGYrBkIntLaw/2006/19.pdf")

def readPDF(bitfile):
    rsrcmgr     = PDFResourceManager()
    retstr      = StringIO()
    laparams    = LAParams()
    device      = TextConverter(rsrcmgr,retstr,laparams=laparams)
    process_pdf(rsrcmgr,device,BytesIO(bitfile))
    content     = retstr.getvalue()
    return content

bitfile = r.content
outputString=readPDF(bitfile)
print(outputString)
