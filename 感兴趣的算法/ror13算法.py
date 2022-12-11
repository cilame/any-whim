# 用于windows函数的一个hash算法。
# 该算法将库名字约束在一个整数范围内，实用于某些汇编函数获取winapi

def ror(r, n=13, s=32):
    return (( r >> n | r << ( s - n ) ) & 0xFFFFFFFF)
def ror13(s):
    r = 0
    for i in s: r = ror(r) + i
    return r

if __name__ == '__main__':
    a = b'loadLibraryA'
    b = b'GetProcAddress'
    c = b'MessageBoxA'
    print(hex(ror13(a)))
    print(hex(ror13(b)))
    print(hex(ror13(c)))