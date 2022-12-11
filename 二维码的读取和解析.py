# 关于二维码的生成和解密
# 预装 qrcode （生成）

# 预装 Pillow （读图）
# 预装 pyzbar （解密）

# 二维码生成
import qrcode 
img = qrcode.make('hello, qrcode')
img.save('test.png')

# 二维码解密
import pyzbar.pyzbar as pyzbar
from PIL import Image,ImageEnhance
image = "test.png"
img = Image.open(image)
#img = ImageEnhance.Brightness(img).enhance(2.0)#增加亮度
#img = ImageEnhance.Sharpness(img).enhance(17.0)#锐利化
#img = ImageEnhance.Contrast(img).enhance(4.0)#增加对比度
#img = img.convert('L')#灰度化
#img.show()
barcodes = pyzbar.decode(img)
for barcode in barcodes:
    barcodeData = barcode.data.decode("utf-8")
    print(barcodeData)
