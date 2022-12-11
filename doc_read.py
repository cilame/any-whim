import os
from win32com.client import Dispatch

word = Dispatch('Word.Application')
word.Visible = 0
word.DisplayAlerts = 0
def get_info_by_doc(path):
    path = os.path.join(os.getcwd(), path)
    doc = word.Documents.Open(FileName=path, Encoding='gbk')
    rstrs = []
    for para in doc.paragraphs:
        rstrs.append(para.Range.Text.replace('\x0b', '\n').replace('\x07', '\n'))
    return ''.join(rstrs)

v = get_info_by_doc(r'./3975988.docx')
print(v)