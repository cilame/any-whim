# 后续考虑将库的二进制文件压缩放在脚本内
# 目前仅仅实现简单的不依赖 PIL 实现的纯py将全屏截图的数据传递给 pyzbar
# 目前还是需要依赖 pyzbar

import pyzbar.pyzbar as pyzbar

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

def create_png_pixel_tobytes(png_bit):
    b = png_bit.find(b'IHDR')
    q = calcsize(">2I")
    w, h = unpack(">2I", png_bit[b+4:b+4+q])
    b = png_bit.find(b'IDAT')
    q = calcsize(">I")
    v = unpack(">I", png_bit[b-q:b])[0]
    v = png_bit[b+4:b+4+v]
    z = zlib.decompress(v[2:-4], -15)
    l, p = w * 3 + 1, []
    n = 0 # 通道，0，1，2
    for i in range(h):
        li = z[i*l:(i+1)*l][1:]
        for j in range(w):
            p.append(li[(j+n)*1 : (j+1+n)*1]) # 只能使用一个通道
    return b''.join(p), w, h

if __name__ == '__main__':
    filename = './screenshot.png'
    screenshot_bit = screenshot()
    pixbytes, w, h = create_png_pixel_tobytes(screenshot_bit)
    for i in pyzbar.decode((pixbytes, w, h)):
        print(i)