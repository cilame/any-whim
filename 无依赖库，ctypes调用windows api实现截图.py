# mod by: https://github.com/BoboTiG/python-mss/tree/master/mss

import zlib
import ctypes
from struct import pack, calcsize, unpack
GetWindowDC             = ctypes.windll.user32.GetWindowDC
GetSystemMetrics        = ctypes.windll.user32.GetSystemMetrics
SelectObject            = ctypes.windll.gdi32.SelectObject
DeleteObject            = ctypes.windll.gdi32.DeleteObject
BitBlt                  = ctypes.windll.gdi32.BitBlt
GetDIBits               = ctypes.windll.gdi32.GetDIBits
CreateCompatibleDC      = ctypes.windll.gdi32.CreateCompatibleDC
CreateCompatibleBitmap  = ctypes.windll.gdi32.CreateCompatibleBitmap


def screenshot(shape:'left,top,width,height'=None):
    ''' 
    无依赖库的截屏处理，生成png类型的图片数据流
    默认参数 None ，全屏截图 
    '''
    def png_bit(data, size, level=6):
        width, height = size
        line = width * 3
        png_filter = pack(">B", 0)
        scanlines = b"".join(
            [png_filter + data[y * line : y * line + line] for y in range(height)][::-1]
        )
        magic = pack(">8B", 137, 80, 78, 71, 13, 10, 26, 10)
        ihdr = [b"", b"IHDR", b"", b""]
        ihdr[2] = pack(">2I5B", width, height, 8, 2, 0, 0, 0)
        ihdr[3] = pack(">I", zlib.crc32(b"".join(ihdr[1:3])) & 0xFFFFFFFF)
        ihdr[0] = pack(">I", len(ihdr[2]))
        idat = [b"", b"IDAT", zlib.compress(scanlines, level), b""]
        idat[3] = pack(">I", zlib.crc32(b"".join(idat[1:3])) & 0xFFFFFFFF)
        idat[0] = pack(">I", len(idat[2]))
        iend = [b"", b"IEND", b"", b""]
        iend[3] = pack(">I", zlib.crc32(iend[1]) & 0xFFFFFFFF)
        iend[0] = pack(">I", len(iend[2]))
        return magic + b"".join(ihdr + idat + iend)

    left, top, width, height = shape if shape else (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
    bmi      = pack('LHHHH', calcsize('LHHHH'), width, height, 1, 32)
    srcdc    = GetWindowDC(0)
    memdc    = CreateCompatibleDC(srcdc)
    svbmp    = CreateCompatibleBitmap(srcdc, width, height)
    SelectObject(memdc, svbmp); BitBlt(memdc, 0, 0, width, height, srcdc, left, top, 13369376)
    _data    = ctypes.create_string_buffer(height * width * 4)
    got_bits = GetDIBits(memdc, svbmp, 0, height, _data, bmi, 0)
    DeleteObject(memdc)
    data = bytes(_data)
    rgb = bytearray(width * height * 3)
    rgb[0::3],rgb[1::3],rgb[2::3] = data[2::4],data[1::4],data[0::4]
    size = (width, height)
    return png_bit(rgb, size) # 全屏截图 png bit 数据


def create_png_pixel(png_bit):
    ''' 
    从 png 图片流数据中解析出像素信息生成列表 pixel
        其中r,g,b均为0-255的正整数
        该功能用于无依赖库处理小图片的相似度对比
    pixel = [[[r,g,b], [r,g,b], [r,g,b]...],
             [[r,g,b], [r,g,b], [r,g,b]...],
             [[r,g,b], [r,g,b], [r,g,b]...],
             [[r,g,b], [r,g,b], [r,g,b]...],]
    '''
    b = png_bit.find(b'IHDR')
    q = calcsize(">2I")
    w, h = unpack(">2I", png_bit[b+4:b+4+q])
    b = png_bit.find(b'IDAT')
    q = calcsize(">I")
    v = unpack(">I", png_bit[b-q:b])[0]
    v = png_bit[b+4:b+4+v]
    z = zlib.decompress(v[2:-4], -15)
    l, pixel = w * 3 + 1, []
    for i in range(h):
        li = z[i*l:(i+1)*l][1:]
        ni = [list(li[j*3:(j+1)*3]) for j in range(w)]
        pixel.append(ni)
    return {'pixel': pixel, 'width': w, 'height': h}


from ctypes.wintypes import LONG
byref        = ctypes.byref
GetCursorPos = ctypes.windll.user32.GetCursorPos
class POINT(ctypes.Structure): _fields_ = [("x", LONG), ("y", LONG)]
def get_cursor_rect(size=(50, 50)):
    '''
    根据鼠标当前位置获取一鼠标为中心，以size为大小的 shape
    其中，图片的大小在窗口边缘有约束限制，注意
    主要是用于单点判断，在鼠标处进行图片判断逻辑的生成，方便后续写工具使用
    '''
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
    point = POINT()
    GetCursorPos(byref(point))
    w, h = size
    x, y =  point.x, point.y
    lx, ly = max([x - w//2, 0]),     max([y - h//2, 0])
    rx, ry = min([x + w//2, width]), min([y + h//2, height])
    left, top, width, height = lx, ly, rx-lx, ry-ly
    return left, top, width, height


if __name__ == '__main__':
    filename = './screenshot.png'
    screenshot_bit = screenshot(shape=get_cursor_rect(size=(100, 100)))
    with open(filename,'wb') as f:
        f.write(screenshot_bit)
    png_pixel = create_png_pixel(screenshot_bit)
    print(png_pixel['pixel'][:10])
    