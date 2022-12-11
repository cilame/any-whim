# python3 
# pip install ddddocr

from io import BytesIO
import ddddocr
from PIL import Image, ImageDraw, ImageFont

clz_ocr = ddddocr.DdddOcr(show_ad=False)
loc_ocr = ddddocr.DdddOcr(det=True, show_ad=False)

def cut_img_from_bytes(img_bytes, cut_size=None):
    img = Image.open(BytesIO(img_bytes))
    if cut_size:
        img = img.crop(cut_size)
        byt = BytesIO()
        img.save(byt, 'png')
        img_bytes = byt.getvalue()
    return img_bytes

def get_loc_words(img_bytes, cut_size=None):
    img_bytes = cut_img_from_bytes(img_bytes, cut_size)
    loc_list = loc_ocr.detection(img_bytes)
    ret = {}
    dimg = Image.open(BytesIO(img_bytes))
    for loc in loc_list:
        cut = dimg.crop(loc)
        byt = BytesIO()
        cut.save(byt, 'png')
        word = clz_ocr.classification(byt.getvalue())
        ret[word] = int((loc[0] + loc[2]) / 2), int((loc[1] + loc[3]) / 2)
    return ret

with open(r'./b3a7ad61cd14adb010ea7ca728bf5871.jpg', 'rb') as f:
    img_bytes = f.read()


def get_local_list(tip, item):
    tiplist = sorted(list(tip.items()), key=lambda e:e[1][0])
    retlist = []
    for i in tiplist:
        name = i[0]
        if name not in item:
            print('error not all match key...')
            return
        else:
            retlist.append(item[name])
    return retlist
tip = get_loc_words(img_bytes, (0, 344, 344, 384))
item = get_loc_words(img_bytes, (0, 0, 344, 344))
print('小图识别', tip)
print('大图识别', item)
locallist = get_local_list(tip, item)
if locallist:
    print('识别成功')
    print(locallist)







# 展示用测试

def test(img_bytes, cut_size=None):
    img_bytes = cut_img_from_bytes(img_bytes, cut_size)
    loc_list = loc_ocr.detection(img_bytes)
    font_type = "./simsun.ttc"
    font_size = 20
    font = ImageFont.truetype(font_type, font_size)
    dimg = Image.open(BytesIO(img_bytes))
    draw = ImageDraw.Draw(dimg)
    for loc in loc_list:
        x1, y1, x2, y2 = loc
        cut = dimg.crop(loc)
        byt = BytesIO()
        cut.save(byt, 'png')
        word = clz_ocr.classification(byt.getvalue())
        draw.line(([(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)]), width=1, fill="red")
        hloc = y1 - 30 if y2 > 300 else y2
        draw.text((int((x1 + x2)/2), hloc), word, font=font, fill="red")
    dimg.show()

test(img_bytes, (0, 0, 344, 344))