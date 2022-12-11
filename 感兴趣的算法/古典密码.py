# 凯撒密码
def caesar(t, n, keys='abcdefghijklmnopqrstuvwxyz'):
    s = list(keys)
    r = ''
    for i in t:
        if i in s:
            r += s[(s.index(i) + n)% len(keys)]
        else:
            r += i
    return r



# 莫斯密码
def morse_dec(string, a='.', b='-', p=None):
    morse = {
        '.-'  :'A', '-...':'B', '-.-.':'C', '-..' :'D', '.'   :'E',
        '..-.':'F', '--.' :'G', '....':'H', '..'  :'I', '.---':'J',
        '-.-':'K', '.-..' : 'L', '--' :'M', '-.' :'N', '---':'O',
        '.--.' : 'P', '--.-' : 'Q', '.-.':'R', '...':'S', '-'  :'T',
        '..-':'U', '...-' : 'V', '.--':'W', '-..-' : 'X', '-.--' : 'Y',
        '--..' : 'Z', '.----' : '1', '..---' : '2', '...--' : '3', 
        '....-' : '4', '.....' : '5', '-....' : '6', '--...' : '7', 
        '---..' : '8','----.' : '9','-----' : '0',
        '-...-' : '=', '.-.-':'~', '.-...' :'<AS>', '.-.-.' : '<AR>', '...-.-' : '<SK>',
        '-.--.' : '<KN>', '..-.-' : '<INT>', '....--' : '<HM>', '...-.' : '<VE>',
        '.-..-.' : '\\', '.----.' : '\'', '...-..-' : '$', '-.--.' : '(', '-.--.-' : ')', 
        '--..--' : ',', '-....-' : '-', '.-.-.-' : '.', '-..-.' : '/', '---...' : ':', 
        '-.-.-.' : ';', '..--..' : '?', '..--.-' : '_', '.--.-.' : '@', '-.-.--' : '!'
    }
    _a, _b = '.', '-'
    _names = string.split() if p is None else string.split(p)
    r = []
    for ps in _names:
        ps = ps.replace(a, _a).replace(b, _b)
        ge = morse.get(ps)
        if ge:
            r.append(ge)
        else:
            r.append('[undefined:{}]'.format(ps))
    return ''.join(r)
def morse_enc(string, a='.', b='-', p=None):
    morse = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': 
        '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 
        'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', 
        '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', 
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', 
        '=': '-...-', '~': '.-.-', '<AS>': '.-...', '<AR>': '.-.-.', 
        '<SK>': '...-.-', '(': '-.--.', '<INT>': '..-.-', '<HM>': '....--', 
        '<VE>': '...-.', '\\': '.-..-.', "'": '.----.', '$': '...-..-', 
        ')': '-.--.-', ',': '--..--', '-': '-....-', '.': '.-.-.-', '/': '-..-.', 
        ':': '---...', ';': '-.-.-.', '?': '..--..', '_': '..--.-', '@': '.--.-.', '!': '-.-.--'
    }
    _a, _b = '.', '-'
    r = []
    for i in string:
        if i.upper() in morse:
            v = morse[i.upper()].replace(_a, a).replace(_b, b)
        else:
            v = '[undefined:{}]'.format(i)
        r.append(v)
    return ' '.join(r) if p is None else p.join(r)

# 栅栏密码
def rail_fence_enc(string, n, padding=None):
    b = []
    q = []
    for idx,i in enumerate(string, 1):
        q.append(i)
        if idx % n == 0:
            b.append(q)
            q = []
    r = []
    if q:
        for i in '~!@#$%^&*': # 自动选一个padding进行处理
            if i not in string:
                padding = i
                break
        if padding is None: 
            raise 'cannot find a padding, cos ~!@#$%^&* all in string.'
        q += [padding] * (n - len(q))
        b.append(q)
    for i in zip(*b):
        r.extend(i)
    return ''.join(r), padding

def rail_fence_dec(string, n, padding=None):
    a = len(string)/n
    b = len(string)//n
    n = b if a == b else b+1
    b = []
    for i in range(0,n):
        b.append(string[i::int(n)])
    r = []
    for i in zip(b):
        r.extend(i)
    return ''.join(r).rstrip(padding)







# brainfuck
def evaluate(code:str):
    code = cleanup(list(code))
    bmap = buildbmap(code)
    cells, ptr, cellptr, ret = [0], 0, 0, []
    while ptr < len(code):
        cmd = code[ptr]
        if cmd == ">": 
            cellptr += 1
            if cellptr == len(cells): cells.append(0)
        if cmd == "<": cellptr = 0 if cellptr <= 0 else cellptr - 1
        if cmd == "+": cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        if cmd == "-": cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        if cmd == "[" and cells[cellptr] == 0: ptr = bmap[ptr]
        if cmd == "]" and cells[cellptr] != 0: ptr = bmap[ptr]
        if cmd == ",": cells[cellptr] = b'\xff'
        if cmd == ".": ret.append(chr(cells[cellptr]))
        ptr += 1
    return ''.join(ret)

def cleanup(code):
    return ''.join(filter(lambda x: x in '.,[]<>+-', code))

def buildbmap(code):
    _stack, bmap = [], {}
    for pos, cmd in enumerate(code):
        if cmd == "[": _stack.append(pos)
        if cmd == "]":
            start = _stack.pop()
            bmap[start] = pos
            bmap[pos] = start
    return bmap

import re
# ook! 
def parse_ook_to_brainfuckmap(string, abc=('!', '?', '.')):
    maps = {
        ('!', '?'): '[',
        ('?', '!'): ']',
        ('.', '.'): '+',
        ('!', '!'): '-',
        ('.', '?'): '>',
        ('?', '.'): '<',
        ('!', '.'): '.',
        ('.', '!'): ',',
    }
    a, b, c = [i if i not in r'$()*+.[]?\/^{}' else '\\'+i for i in abc]
    rexgep = '|'.join([a, b, c])
    v = re.findall(rexgep, string)
    r = []
    for i in zip(v[::2],v[1::2]):
        t = [j.replace(a[-1], '!')\
              .replace(b[-1], '?')\
              .replace(c[-1], '.') for j in i]
        t = tuple(t)
        r.append(maps.get(t))
    return ''.join(r)




# ROT5：只对数字进行编码，用当前数字往前数的第5个数字替换当前数字，例如当前为0，编码后变成5，当前为1，编码后变成6，以此类推顺序循环。
# ROT13：只对字母进行编码，用当前字母往前数的第13个字母替换当前字母，例如当前为A，编码后变成N，当前为B，编码后变成O，以此类推顺序循环。
# ROT18：这是一个异类，本来没有，它是将ROT5和ROT13组合在一起，为了好称呼，将其命名为ROT18。
# ROT47：对数字、字母、常用符号进行编码，按照它们的ASCII值进行位置替换，用当前字符ASCII值往前数的第47位对应字符替换当前字符，例如当前为小写字母z，编码后变成大写字母K，当前为数字0，编码后变成符号_。用于ROT47编码的字符其ASCII值范围是33－126

def rot5(string):
    s = '0123456789'
    r = []
    for i in string:
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        else:
            v = i
        r.append(v)
    return ''.join(r)

def rot13(string):
    s = 'abcdefghijklmnopqrstuvwxyz'
    u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    r = []
    for i in string:
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        elif i in u:
            v = u[(u.index(i)+len(u)//2)% len(u)]
        else:
            v = i
        r.append(v)
    return ''.join(r)

def rot18(string):
    s = '0123456789abcdefghijklmnopqrstuvwxyz'
    u = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    r = []
    for i in string:
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        elif i in u:
            v = u[(u.index(i)+len(u)//2)% len(u)]
        else:
            v = i
        r.append(v)
    return ''.join(r)

def rot47(string):
    s = list(range(33,127))
    r = []
    for i in string.encode():
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        else:
            v = i
        r.append(v)
    return bytes(r).decode()




def bacon_enc(string,ver='v1'):
    if ver == 'v1':
        maps = {
            'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa', 'F': 'aabab', 
            'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab', 'K': 'ababa', 'L': 'ababb', 
            'M': 'abbaa', 'N': 'abbab', 'O': 'abbba', 'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 
            'S': 'baaba', 'T': 'baabb', 'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 
            'Y': 'bbaaa', 'Z': 'bbaab'
        }
    elif ver == 'v2':
        maps = {
            "A":"aaaaa", "G":"aabba", "N":"abbaa", "T":"baaba", "B":"aaaab", "H":"aabbb",
            "O":"abbab", "C":"aaaba", "P":"abbba", "W":"babaa",
            "D":"aaabb", "K":"abaab", "Q":"abbbb", "X":"babab", "E":"aabaa", "L":"ababa",
            "R":"baaaa", "Y":"babba", "F":"aabab", "M":"ababb", "S":"baaab", "Z":"babbb",
            "U":"baabb", "V":"baabb", # "U-V":"baabb"
            "I":"abaaa", "J":"abaaa", # "I-J":"abaaa"
        }
    r = []
    for i in string.upper():
        if i in maps:
            r.append(maps.get(i))
        else:
            r.append('[unfind:{}]'.format(i))
    return ' '.join(r)

def bacon_dec(string,a='a',b='b',ver='v1'):
    if ver == 'v1':
        maps = {
            'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E', 'aabab': 'F', 
            'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I', 'abaab': 'J', 'ababa': 'K', 'ababb': 'L', 
            'abbaa': 'M', 'abbab': 'N', 'abbba': 'O', 'abbbb': 'P', 'baaaa': 'Q', 'baaab': 'R', 
            'baaba': 'S', 'baabb': 'T', 'babaa': 'U', 'babab': 'V', 'babba': 'W', 'babbb': 'X', 
            'bbaaa': 'Y', 'bbaab': 'Z'
        }
    elif ver == 'v2':
        maps = {
            "aaaaa":"A", "aabba":"G", "abbaa":"N", "baaba":"T", "aaaab":"B", 
            "aabbb":"H", "abbab":"O", "baabb":"U-V", "aaaba":"C", "abaaa":"I-J", 
            "abbba":"P", "babaa":"W", "aaabb":"D", "abaab":"K", "abbbb":"Q", 
            "babab":"X", "aabaa":"E", "ababa":"L", "baaaa":"R", "babba":"Y", 
            "aabab":"F", "ababb":"M", "baaab":"S", "babbb":"Z", 
        }
    r = []
    _string = string.replace(a, 'a').replace(b, 'b')
    for i in _string.split():
        if i in maps:
            r.append(maps.get(i)[-1]) # v2 模式统统使用最后一个字符解密
        else:
            r.append('[unfind:{}]'.format(i))
    return ''.join(r)

def bacon_v1_enc(string): return bacon_enc(string, ver='v1')
def bacon_v2_enc(string): return bacon_enc(string, ver='v2')
def bacon_v1_dec(string,a='a',b='b'): return bacon_dec(string,a=a,b=b,ver='v1')
def bacon_v2_dec(string,a='a',b='b'): return bacon_dec(string,a=a,b=b,ver='v2')








if __name__ == '__main__':

    s = caesar('aaabbbcccdddeeefff', 3)
    print(s)
    s = caesar(s, -3)
    print(s)
    print()


    s = morse_dec('-... -.- -.-. - ..-. -- .. ... -.-.')
    print(s)
    s = morse_enc('asdfasdfnj()@/!$asdnLKE???')
    print(s)
    print(morse_dec(s))
    print()


    # 栅栏加密，默认使用带填充模式
    # 也可以通过 padding 来判断加密是否存在自动填充情况
    s, padding = rail_fence_enc('asdfasdfasdff', 3)
    print(s)
    s = rail_fence_dec(s, 3, padding=padding)
    print(s)
    print()


    # 普通的 brainfuck
    s = '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.'
    print(evaluate(s))
    print()


    # ook 加密实际上使用三个种类的字符以长度为2的组合来对应 brainfuck 里面的八个字符，
    # 实际上里面的算法还是使用的 brainfuck 的算法
    s = 'Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook. Ook! Ook.'
    s = parse_ook_to_brainfuckmap(s)
    print(s)
    print(evaluate(s))
    s = '..... ..... ..... ..... !?!!. ?.... ..... ..... ..... .?.?! .?... .!... ..... ..... !.?.. ..... !?!!. ?!!!! !!?.? !.?!! !!!.. ..... ..... .!.?. ..... ...!? !!.?. ..... ..?.? !.?.. ..... .!.?. ..... ..... !?!!. ?!!!! !!!!! !?.?! .?!.? ..... ....! ?!!.? ..... ...?. ?!.?. ..... !.?.. ..... !?!!. ?!!!! !!?.? !.?!! !!!!! !!!!. ..... ...!. ?.... ...!? !!.?. ..... ?.?!. ?..!. ?.... ..... !?!!. ?!!!! !!!!? .?!.? !!!!! !!!!! !!!.? .....'
    s = parse_ook_to_brainfuckmap(s)
    print(s)
    print(evaluate(s))
    print()


    s = 'nihaoaxiongdi1234567890'
    s = rot5(s); print('enc>',s)
    s = rot5(s); print('dec=',s)
    s = rot13(s); print('enc>',s)
    s = rot13(s); print('dec=',s)
    s = rot18(s); print('enc>',s)
    s = rot18(s); print('dec=',s)
    s = rot47(s); print('enc>',s)
    s = rot47(s); print('dec=',s)
    print()



    s = 'lkasjdklfjalsdf'
    s = bacon_v1_enc(s)
    print(s)
    s = bacon_v1_dec(s)
    print(s)
    s = 'lkasjdklfjalsdf'
    s = bacon_v2_enc(s)
    print(s)
    s = bacon_v2_dec(s)
    print(s)



# railfence                 # 栅栏密码
# rot13                     # 循环位移密码
# caesar                    # 凯撒密码

# simplesubstitution        # 简单换位密码      # 就是简单的一一对应置换的密码，大量数据可以通过频谱分析进行处理，不过单条解密仍需密码解密
# vigenere                  # 维吉尼亚密码
# atbash                    # 埃特巴什码密码：a->z,b->y,...,z->a
# affine                    # 仿射密码
# beaufort                  # 博福德密码
# bifid                     # 双密码 
# columnartransposition     # 列位移密码
# delastelle                # 三分密码
# enigma                    # 恩格尼密码 
# foursquare                # 四方密码
# polybius                  # 棋盘密码
# porta                     # 多表代换密码
# fracmorse
# gronsfeld
# m209
# playfair
# adfgvx
# adfgx
# autokey

