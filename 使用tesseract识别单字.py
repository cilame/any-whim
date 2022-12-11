# 使用 tesseract 进行单字识别，注意 tesseract 参数 “--psm 10”

# 安装包下载地址 https://github.com/UB-Mannheim/tesseract/wiki
# 语言包下载地址 https://github.com/tesseract-ocr/tessdata
#   找到 chi_sim.traineddata， chi_tra.traineddata 下载（chi_sim简体，chi_tra繁体）
#   下载时候使用迅雷之类的工具下载会快很多。

import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'D:/Tesseract-OCR/tesseract.exe'
os.environ['TESSDATA_PREFIX'] = "D:/Tesseract-OCR/tessdata"
cmd_config = '--psm 10'

image = Image.open("word.png")
code = pytesseract.image_to_string(image, lang='chi_sim', config=cmd_config)
print(code)
print(repr(code))