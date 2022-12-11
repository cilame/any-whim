#coding=utf8

import os
import re
import json
import base64
import shutil
import tempfile
from collections import Counter

import cv2
import numpy as np
import requests
from lxml import etree

def get_word_by_tesseract(_imapath):
    # 感觉识别率太差。
    # pip install pytesseract
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
    image = Image.open(_imapath)
    word = pytesseract.image_to_string(image, lang='chi_sim', config=cmd_config)
    return word.strip()

def get_word_by_baiduapi(_imapath):
    # pip install baidu-aip
    from aip import AipOcr
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    image = get_file_content(_imapath)
    # 请自行申请百度识别的接口，然后调用api实现
    APP_ID = 'xxx'
    API_KEY = 'xxx'
    SECRET_KEY = 'xxx'
    # 下面是我个人使用的 APP_ID，API_KEY，SECRET_KEY（经过个人算法加密）
    # 密码是 123456 算法只有我知道。总之只是方便我个人使用，其他人使用请额外申请百度识别的api。反正每天都有一定量的免费使用。
    # h;OJJf)?TQOMM=F5&VQ}re##7LLP}?>z#`&ANmD(rs1gcF7a8cw4m^|VqQ=aU1;7>=LdGLo!e6LkhH2kVDVqxU%I4F0z1LI*9`U*r|R=Z&ToS5TK(fiLb87*AKC;^jzc^x!^qK))^SFf
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # info = client.basicGeneral(image) # 通用版本，这个识别率低到无法使用
    info = client.basicAccurate(image) # 高精度版本，大部分能识别，勉强能用
    if info.get('error_msg') == 'IAM Certification failed':
        raise Exception('请申请一个能用的百度文字识别的API，然后配置 APP_ID,API_KEY,SECRET_KEY')
    word = info.get('words_result') # 高精度版本
    word = word[0]['words'] if word else 'None'
    return word


def get_info(page):
    def mk_url_headers():
        url = (
            'http://match.yuanrenxue.com/api/match/8_verify'
        )
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "yuanrenxue.project",
        }
        return url,headers

    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    sessionid = re.findall('sessionid=[^;]+;', s.headers['Set-Cookie'])[0]
    e = etree.HTML(json.loads(s.text)['html'])
    words  = e.xpath('//div[contains(text(), "请依次点击")]/p/text()')
    image  = e.xpath('//img/@src')[0].replace('data:image/jpeg;base64,', '').encode()
    bitimg = base64.b64decode(image)
    temppath = None
    try:
        temppath = tempfile.mkdtemp()
        imgpath  = os.path.join(temppath, 'temp.png')
        with open(imgpath, 'wb') as f:
            f.write(bitimg)
        img = cv2.imread(imgpath)
        # 据观察，背景颜色为单色，为了更好的处理，就把背景颜色全部换成白色
        # 统计出最多的像素，直接根据这个修改即可
        _img = img.reshape((-1, 3))
        dic = {}
        for i in _img:
            pix = tuple(i)
            dic[pix] = (dic.get(pix) or 0) + 1
        maxpix = np.array(max(dic, key=dic.get))
        img[img == maxpix] = 255
        # 进行形态学闭运算，去除黑色噪点
        # 然后转换成灰度图，再进行二值化，将不是纯白色的颜色全部涂成黑色，提高识别率
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        img    = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
        img    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img, 254, 255, cv2.THRESH_BINARY)
        # cv2.imshow('test', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 从左往右从上往下，一般阅读的顺序切割出九张单字图
        idx = 0
        dic = {}
        for i in range(3):
            for j in range(3):
                _img = img[i*100:(i+1)*100, j*100:(j+1)*100]
                _imapath = os.path.join(temppath, '_img{}.png'.format(idx))
                cv2.imwrite(_imapath, _img)
                # 感觉 tesseract 太拉胯了，识别率很低。
                # word = get_word_by_tesseract(_imapath)
                # 百度的 api 勉强能用，注意函数内使用的是高精度版。每天免费500次，有点少。
                word = get_word_by_baiduapi(_imapath)
                dic[word] = idx
                idx += 1
                print(word)
                # cv2.imshow('test', _img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        # cv2.imshow('test', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    finally:
        if temppath and os.path.isdir(temppath):
            shutil.rmtree(temppath)

    postmap = {
        0: 156,
        1: 166,
        2: 146,
        3: 485,
        4: 465,
        5: 477,
        6: 755,
        7: 766,
        8: 806,
    }

    params = '|'.join([str(postmap.get(dic.get(i))) for i in words])+'|'
    print(dic)
    print(params)

    def mk_url_headers(page, params, sessionid):
        url = (
            'http://match.yuanrenxue.com/api/match/8'
            '?page={}'
            '&answer={}'
        ).format(page, params)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": (
                sessionid.strip(' ;')
            ),
            "Host": "match.yuanrenxue.com",
            "Pragma": "no-cache",
            "Referer": "http://match.yuanrenxue.com/match/8",
            "User-Agent": "yuanrenxue.project",
            "X-Requested-With": "XMLHttpRequest",
        }
        return url,headers

    url,headers = mk_url_headers(page, params, sessionid)
    s = requests.get(url,headers=headers)
    jsondata = json.loads(s.text)
    return [i['value'] for i in jsondata['data']]

allvalues = []
for page in range(3, 6):
    values = get_info(page)
    print('page:{} --> values:{}'.format(page, values))
    allvalues.extend(values)

from collections import Counter
s = Counter(allvalues).most_common()[0]
print('number:{} --> count:{}'.format(s[0], s[1]))


# 出错的概率还挺高，所以这里我是一条一条执行出来的。
# 其实可以使用不断重试来实现，这里懒得做重试的代码逻辑了。通过率大概能有 20-30% 吧。
# page:1 --> values:[7453, 1457, 5053, 2127, 4455, 4290, 9875, 7453, 8778, 2571]
# page:2 --> values:[3932, 5963, 3372, 9736, 7831, 1706, 887, 9955, 4029, 3034]
# page:3 --> values:[9606, 3850, 4106, 2381, 8545, 2403, 9984, 7453, 3585, 7545]
# page:4 --> values:[5231, 7453, 6090, 6476, 2965, 5510, 3879, 7453, 5821, 1356]
# page:5 --> values:[4798, 8040, 3086, 7453, 9874, 4251, 2862, 677, 9708, 7902]

# 结果是
# number:7453 --> count:6