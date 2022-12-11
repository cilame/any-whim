def y(e, t):
    def i(e, t):
        r = []
        for idx,i in enumerate(t):
            v = ord(i) ^ ord(e[idx%len(e)])
            r.append(v)
        return r
    r = i(e, t)
    def m(e, t, n):
        a = ["i", "/", "x", "1", "X", "g", "U", "0", "z", "7", "k", "8", "N", "+", "l", "C", "p", "O", "n", "P", "r", "v", "6", "\\", "q", "u", "2", "G", "j", "9", "H", "R", "c", "w", "T", "Y", "Z", "4", "b", "f", "S", "J", "B", "h", "a", "W", "s", "t", "A", "e", "o", "M", "I", "E", "Q", "5", "m", "D", "d", "V", "F", "L", "K", "y"]
        l = "3"
        s = []
        if (1 == n):
            i = e[t]
            r = 0
            o = 0
            s.append(a[i >> 2 & 63])
            s.append(a[(i << 4 & 48) + (r >> 4 & 15)])
            s.append(l)
            s.append(l)
        elif (2 == n):
            i = e[t]
            r = e[t + 1]
            o = 0
            s.append(a[i >> 2 & 63])
            s.append(a[(i << 4 & 48) + (r >> 4 & 15)])
            s.append(a[(r << 2 & 60) + (o >> 6 & 3)])
            s.append(l)
        else:
            if (3 != n):
                print('error!!!!!!!!!!')
            i = e[t]
            r = e[t + 1]
            o = e[t + 2]
            s.append(a[i >> 2 & 63])
            s.append(a[(i << 4 & 48) + (r >> 4 & 15)])
            s.append(a[(r << 2 & 60) + (o >> 6 & 3)])
            s.append(a[63 & o])
        return "".join(s)

    n = []
    e = r
    t = 3
    i = 0
    while i < len(e):
        if not (i+t <= len(e)):
            n.append(m(e, i, len(e)-i))
            break
        n.append(m(e, i, t))
        i += t
    return ''.join(n)

def E(s):
    def j(e):
        t = [None]*4
        t[0] = e >> 24 & 255
        t[1] = e >> 16 & 255
        t[2] = e >> 8 & 255
        t[3] = 255 & e
        return t
    def u(e):
        def s(e):
            l = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
            t = []
            t.append(l[e >> 4 & 15])
            t.append(l[15 & e])
            return "".join(t)
        n = []
        for i in range(len(e)):
            n.append(s(e[i]))
        return ''.join(n)
    def d(e, p=None):
        return u(j(e))
    def S(e):
        w = [0, 1996959894, 3993919788, 2567524794, 124634137, 1886057615, 3915621685, 2657392035, 249268274, 2044508324, 3772115230, 2547177864, 162941995, 2125561021, 3887607047, 2428444049, 498536548, 1789927666, 4089016648, 2227061214, 450548861, 1843258603, 4107580753, 2211677639, 325883990, 1684777152, 4251122042, 2321926636, 335633487, 1661365465, 4195302755, 2366115317, 997073096, 1281953886, 3579855332, 2724688242, 1006888145, 1258607687, 3524101629, 2768942443, 901097722, 1119000684, 3686517206, 2898065728, 853044451, 1172266101, 3705015759, 2882616665, 651767980, 1373503546, 3369554304, 3218104598, 565507253, 1454621731, 3485111705, 3099436303, 671266974, 1594198024, 3322730930, 2970347812, 795835527, 1483230225, 3244367275, 3060149565, 1994146192, 31158534, 2563907772, 4023717930, 1907459465, 112637215, 2680153253, 3904427059, 2013776290, 251722036, 2517215374, 3775830040, 2137656763, 141376813, 2439277719, 3865271297, 1802195444, 476864866, 2238001368, 4066508878, 1812370925, 453092731, 2181625025, 4111451223, 1706088902, 314042704, 2344532202, 4240017532, 1658658271, 366619977, 2362670323, 4224994405, 1303535960, 984961486, 2747007092, 3569037538, 1256170817, 1037604311, 2765210733, 3554079995, 1131014506, 879679996, 2909243462, 3663771856, 1141124467, 855842277, 2852801631, 3708648649, 1342533948, 654459306, 3188396048, 3373015174, 1466479909, 544179635, 3110523913, 3462522015, 1591671054, 702138776, 2966460450, 3352799412, 1504918807, 783551873, 3082640443, 3233442989, 3988292384, 2596254646, 62317068, 1957810842, 3939845945, 2647816111, 81470997, 1943803523, 3814918930, 2489596804, 225274430, 2053790376, 3826175755, 2466906013, 167816743, 2097651377, 4027552580, 2265490386, 503444072, 1762050814, 4150417245, 2154129355, 426522225, 1852507879, 4275313526, 2312317920, 282753626, 1742555852, 4189708143, 2394877945, 397917763, 1622183637, 3604390888, 2714866558, 953729732, 1340076626, 3518719985, 2797360999, 1068828381, 1219638859, 3624741850, 2936675148, 906185462, 1090812512, 3747672003, 2825379669, 829329135, 1181335161, 3412177804, 3160834842, 628085408, 1382605366, 3423369109, 3138078467, 570562233, 1426400815, 3317316542, 2998733608, 733239954, 1555261956, 3268935591, 3050360625, 752459403, 1541320221, 2607071920, 3965973030, 1969922972, 40735498, 2617837225, 3943577151, 1913087877, 83908371, 2512341634, 3803740692, 2075208622, 213261112, 2463272603, 3855990285, 2094854071, 198958881, 2262029012, 4057260610, 1759359992, 534414190, 2176718541, 4139329115, 1873836001, 414664567, 2282248934, 4279200368, 1711684554, 285281116, 2405801727, 4167216745, 1634467795, 376229701, 2685067896, 3608007406, 1308918612, 956543938, 2808555105, 3495958263, 1231636301, 1047427035, 2932959818, 3654703836, 1088359270, 936918e3, 2847714899, 3736837829, 1202900863, 817233897, 3183342108, 3401237130, 1404277552, 615818150, 3134207493, 3453421203, 1423857449, 601450431, 3009837614, 3294710456, 1567103746, 711928724, 3020668471, 3272380065, 1510334235, 755167117]
        t = 4294967295
        n = 0
        while (n < len(e)):
            i = e[n]
            t = (t >> 8) ^ int(w[255 & (t ^ ord(i))])
            n; n += 1
        return d(4294967295 ^ t, 8)
    return S(s)

def Y(e, t):
    # import random
    def j(e):
        t = [None]*4
        t[0] = e >> 24 & 255
        t[1] = e >> 16 & 255
        t[2] = e >> 8 & 255
        t[3] = 255 & e
        return t
    def I(e):
        v = [ord(i) if isinstance(i, str) else i for i in e]
        t = len(e)
        O = C = 4
        l = (C - t % C - O) if (t % C <= C - O) else (2 * C - t % C - O)
        for i in range(l):
            v.append(0)
        v.extend(j(len(e)))
        return v
    def a(t, n):
        r = [None]*len(t)
        for i in range(len(t)):
            r[i] = (ord(t[i]) if isinstance(t[i], str) else t[i])^n[i]
        return r
    def x(e):
        l = int(len(e)/4) if len(e)%4 == 0 else int(len(e)/4)+1
        r = []
        for i in range(l):
            r.append(e[i*4:(i+1)*4])
        return r
    def _byte(e):
        if (e < -128):
            return _byte(128 - (-128 - e))
        if (e >= -128 and e <= 127):
            return e
        if (e > 127):
            return _byte(-129 + e - 127)
    def _o(a, b):
        return _byte(_byte(a) ^ _byte(b))
    def _p(a, b):
        return _byte(_byte(a) + _byte(b))
    def M(e, t):
        for i in range(len(e)):
            e[i] = _o(e[i], t)
        return e
    def D(e, t):
        for i in range(len(e)):
            e[i] = _p(e[i], t)
        return e
    def L(e):
        t = M(e, 56)
        n = D(t, -40)
        i = M(n, 103)
        return i
    def r(e, t):
        n = []
        for i in range(len(e)):
            n.append(_p(e[i], t[i%len(t)]))
        return n
    def A(e):
        R = [120, 85, -95, -84, 122, 38, -16, -53, -11, 16, 55, 3, 125, -29, 32, -128, -94, 77, 15, 106, -88, -100, -34, 88, 78, 105, -104, -90, -70, 90, -119, -28, -19, -47, -111, 117, -105, -62, -35, 2, -14, -32, 114, 23, -21, 25, -7, -92, 96, -103, 126, 112, -113, -65, -109, -44, 47, 48, 86, 75, 62, -26, 72, -56, -27, 66, -42, 63, 14, 92, 59, -101, 19, -33, 12, -18, -126, -50, -67, 42, 7, -60, -81, -93, -86, 40, -69, -37, 98, -63, -59, 108, 46, -45, 93, 102, 65, -79, 73, -23, -46, 37, -114, -15, 44, -54, 99, -10, 60, -96, 76, 26, 61, -107, 18, -116, -55, -40, 57, -76, -82, 45, 0, -112, -77, 29, 43, -30, 109, -91, -83, 107, 101, 81, -52, -71, 84, 36, -41, 68, 39, -75, -122, -6, 11, -80, -17, -74, -73, 35, 49, -49, -127, 80, 103, 79, -25, 52, -43, 56, 41, -61, -24, 17, -118, 115, -38, 8, -78, 33, -85, -106, 58, -98, -108, 94, 116, -125, -51, -9, 71, 82, 87, -115, 9, 69, -123, 123, -117, 113, -22, -124, -87, 64, 13, 21, -89, -2, -99, -97, 1, -4, 34, 20, 83, 119, 30, -12, -110, -66, 118, -48, 6, -36, 104, -58, -102, 97, 5, -20, 31, -72, 70, -39, 67, -68, -57, 110, 89, 51, 10, -120, 28, 111, 127, 22, -3, 54, 53, -1, 100, 74, 50, 91, 27, -31, -5, -64, 124, -121, 24, -13, 95, 121, -8, 4]
        t = e >> 4 & 15
        n = 15 & e
        i = 16 * t + n
        return R[i]
    def N(e):
        t = []
        for i in e:
            t.append(A(i))
        return t

    n = [-55, -51, 0, 73] # 随机数 -127~128
    t = t[:4]
    t = a(t, n)
    i = t
    o = I(e)
    l = x(o)
    s = []
    s.extend(n)
    f = 0
    u = len(l)
    while f < u:
        c = L(l[f])
        j = a(c, t)
        d = r(j, i)
        j = a(d, i)
        h = N(j)
        h = N(h)
        i = h
        s.extend(h)
        f += 1
    return s
def _(e):
    def m(e, t, n):
        a = ["i", "/", "x", "1", "X", "g", "U", "0", "z", "7", "k", "8", "N", "+", "l", "C", "p", "O", "n", "P", "r", "v", "6", "\\", "q", "u", "2", "G", "j", "9", "H", "R", "c", "w", "T", "Y", "Z", "4", "b", "f", "S", "J", "B", "h", "a", "W", "s", "t", "A", "e", "o", "M", "I", "E", "Q", "5", "m", "D", "d", "V", "F", "L", "K", "y"]
        l = "3"
        s = []
        if (1 == n):
            i = e[t]
            r = 0
            o = 0
            s.append(a[i >> 2 & 63])
            s.append(a[(i << 4 & 48) + (r >> 4 & 15)])
            s.append(l)
            s.append(l)
        elif (2 == n):
            i = e[t]
            r = e[t + 1]
            o = 0
            s.append(a[i >> 2 & 63])
            s.append(a[(i << 4 & 48) + (r >> 4 & 15)])
            s.append(a[(r << 2 & 60) + (o >> 6 & 3)])
            s.append(l)
        else:
            if (3 != n):
                print('error!!!!!!!!!!')
            i = e[t]
            r = e[t + 1]
            o = e[t + 2]
            s.append(a[i >> 2 & 63])
            s.append(a[(i << 4 & 48) + (r >> 4 & 15)])
            s.append(a[(r << 2 & 60) + (o >> 6 & 3)])
            s.append(a[63 & o])
        return "".join(s)

    n = []
    t = 3
    i = 0
    while i < len(e):
        if not (i+t <= len(e)):
            n.append(m(e, i, len(e)-i))
            break
        n.append(m(e, i, t))
        i += t
    return ''.join(n)
def sample(e, t=50):
    n = len(e)
    if (n <= t):
        return e
    i = []
    r = 0
    o = 0
    while (o < n):
        if o >= r * (n - 1) / (t - 1):
            i.append(e[o])
            r += 1
        o; o += 1
    return i
def B(e):
    r = "14731382d816714fC59E47De5dA0C871D3F"
    i = e + E(e)
    o = Y(i, r)
    return _(o)
def p(e):
    return B(e)









# 易盾解密，这里只给出滑块拖动处理的参数生成的解密 acToken
# 有可能这些加密算法会用在其他地方，我暂时懒得看。

# 其中有四个参数 d,m,p,ext
# 只要是非空则都需要 token 参数进行加密的处理
# d: 轨迹信息
# m: 空字符串
# p: 真实移动了的距离占总长度的百分比信息
# ext: 鼠标点击次数和鼠标轨迹信息长度的信息



# 轨迹信息
# 每个坐标均为如下结构，逗号分隔成三份，1x坐标，2y坐标，3按下时间距离最开始按下时间的时间长度，毫秒级
# "351,-46,3679"
# 每个轨迹都会加密成一个字符串形成列表，加密函数为 y（例如 y(token, "351,-46,3679") ），并且需要 token 参数，加密后的每个点信息都存在一个列表里
# 然后将这个列表，经过 sample 函数让列表长度处理成最长为 50 的长度，然后用冒号拼接，生成字符串
# 将这个字符串经过 p 函数就获取到了轨迹的加密
s = ['rOO6Uii7', '\\OOrUii/', 'vpLkiwpi1A33', 'vcek1/pzxvz3', 'vAEk/pavxgjX', 'ri/k/pFvxgp0', 'rc4k/cSvxgpl', 'rAWk/cavxgri', '\\iLk/cFvxgzx', 'vpwPUia7gvj1ri33', 'vp4RUiazgvj16A33', 'vpWnUiakgvji6c33', 'vpepUiaCgvj/vi33', 'vpEPUiaCgvjlvc33', 'vpDvUialgvjCrA33', 'vpDRUia/gvpUrc33', 'vpLvUiaigvpU6c33', 'vpLOUiaigvp0vi33', 'vp/rUiaigvpXvc33', 'vp/vUiaigvpgri33', 'vp/PUiaigvpxrc33', 'vp/pUiaigvpx6c33', 'vp/OUiaigvp/ri33', 'vp/HUiaigvpl6c33', 'vp/6Uiaigvzx6c33', 'vpL6Uia+gvz1vi33', 'vpD6Uiazgvzivc33', 'vpeOUiSlgvz/ri33', 'vpWpUiSkgvzlrc33', 'vpJnUiS7gvzl6c33', 'vp4pUiZCgvzCvi33', 'vpwpUiZ+gvNUvc33', '\\p/k/pSv1gjX', '\\iLk/pcv1gp0', 'rAJkiepN1vp3', 'rcLkiwpN1vz3', 'rcWkiwpN1gp3', 'rcwkiwpN1Eq3', 'rpgkiwpN1Em3', 'rp/kiwpN14i3', 'rpLkiwpNivz3', 'rpgkiwpCivm3', 'rcDkiwpCigN3', 'rADkiwplxvz3', '\\p4kieplxgp3', 'vpwpUiZ7gvXXrc33', 'vpJnUiZ8gvXX6c33', 'vperUiZNgvXgvp33', 'vpERUiZCgvXxvc33', 'vpLnUiZCgvX1ri33', 'vp/OUiZCgvXirc33', 'vpgHUiZ/gvXi6c33', 'vc46UiZ/gvX/vA33', 'vc4HUiZ/gvXlvc33', 'vcJvUiZ/gvXCri33', 'vcJnUiZ/gvmUrc33', 'vcJpUiZ/gvmU6c33', 'vcJPUiZ/gvmCvi33', 'vcJ6UiZ/gvFUvc33', 'vc4nUiZ/gvF0ri33', 'vcwnUiZ/gvFXrA33', 'vpgrUiZ/gvFX6c33', 'vpLvUiZlgvFgvp33', 'vpeOUiZ8gvFxvc33', 'vp4RUiZzgvF1ri33', '\\ieki/pi1Eq3', 'rpek/wpi1Em3', 'vA4k/Opi14i3', 'vpwkUpAvigmx', 'v/O8iOpiigp3', 'v/O8iOpzxvqU', 'v/O8iOpzxvql', 'v/O8iwpzxvj1', 'v/O8iwpzxvpx', 'v/O8iwpzxvFi', 'v/O8i/pzxgqx', 'v/O8i/pzxgjX', 'rwO8/epzxgpU', 'vpLkUpSvxgjX6c33', 'vAwk/Opzxgri', 'riwk/Opzxgzx', 'rpJk/wpzxgNX', 'rcek/wpzxgNC', 'rAek/wpzxgil', '\\iek/wpzxgXi', '\\pJk/wpzxgmx', '\\pgk/epzxgFX', 'vpwPUiavxgpUrc33', 'vp4rUiAvxgpUvp33', 'vp4pUiAvxgp0vi33', 'vpJrUiIvxgpXrp33', 'vpJOUimvxgpgri33', 'vpWrUiFvxgpxrc33', 'vpWOUiivxgpx6c33', 'vperUiXvxgp1vi33', 'vpeOUiXvxgpivc33', 'vpEvUiZzgvjXvvj3', 'vpEpUiZzgvjX64r3', 'vpERUiZzgvjX64I3', 'vpDnUiZ8gvjX6EN3', 'vpDOUiZ8gvjgr4i3', 'vpL\\UiZkgvjgrEj3', 'vpLHUiZNgvjgrgp3', 'vp/\\UiZNgvjgrgz3', 'vp/PUiZCgvjgrvz3', 'vp/HUiZCgvjgv4X3', 'vpg6UiZCgvjgvEj3', 'vpgvUiZlgvjgvgr3', 'vpgOUiZlgvjgvgI3', 'vcwvUiZ/gvjgvvN3', 'vcwpUiS7gvjg64X3', 'vcwRUiS7gvjg6Ej3', 'vc46UiSzgvjxr4r3', 'vc4vUiSzgvjxr4I3', 'vc4HUiSkgvjxrEN3', 'vcJ\\UiSNgvjxrgX3', 'vcJvUiSCgvjxrvj3', 'vcJPUiSlgvjxv4r3', 'vcJpUiSlgvjxv4I3', 'vcJOUiS/gvjxvEN3', 'vcJHUiS/gvjxvgX3', 'vcJOUiSlgvj16Ej3', 'vcJ\\UiSlgvj16EA3', 'vc4nUiSkgvjir4z3', 'vcwvUiS8gvjirEN3', 'vpgrUiS7gvjirgX3', 'vp/rUiZ/gvjirvj3', 'vpDHUiZCgvjiv4r3', 'vpEPUiZNgvjiv4A3', 'vpevUiZ7gvjivEN3', 'vpJpUiXvxgiivc33', 'vp4nUimvxgi/ri33', 'vpwvUiAvxgilrc33', '\\pWk/Opz1Eml', '\\iDkUpZvxgiCvi33', '\\iWkUpZvxgXUvA33', 'rAgkUpavxgX0ri33', 'rA/kUpAvxgXXri33', 'rALkUpAvxgXX6A33', 'rADkUpIvxgXi6c33', '\\iwkUpmvxgm0vi33', '\\igkUpmvxgmXrp33', '\\p/kUpmvxgmgri33', 'vp46U/rCgvjlv4r3', 'vpJrU/rCgvjlv4I3', 'vpWPU/rCgvjlvEN3', 'vpeRU/rCgvjlvgX3', 'vpD\\U/rCgvjlvvj3', 'vpLnU/rCgvjl64r3', 'vp/pU/rNgvjl64I3', 'vpgOU/r8gvjl6EN3', 'vcwpU/rzgvjCr4i3', 'vc4vUicvxgF0ri33', 'vc4pUiZvxgFXrA33', 'vc4HUiZvxgFX6A33', 'vcJ6UiZvxgFxvc33', 'vc4HUiSvxgFlvc33', 'vc4pUiSvxgFCri33', 'vc46UiSvxEqUrc33', 'vpgRUiSvxEqU6c33', 'vp/HUiSvxEq0vi33', 'vpL\\UiZvxEqXvc33', 'vpeOU/rkgvpUrvj3', 'vpJrU/rNgvpUv4r3', '\\pgkUpivxEqx6c33', '\\iWkUpZ7gvpUvEN3', 'rc/kUpZkgvpUvgX3', 'rcwkUpZ+gvpUvvj3', 'rpDkUpZ+gvpU64r3', 'rpekUpZ+gvpU64I3', 'rpekUpZNgvp0rgI3', 'rpEkUpZNgvp0rvN3', 'rcwkUpZNgvp0v4X3', 'rcLkUpZNgvp0vEj3', 'rADkUpZNgvp0vEA3', '\\igkUpZNgvp0vgI3', 'vpwPU/rz1XSXrEzx', 'vpJrU/rz1XSXrEIi', 'vpenU/rz1XSXrEAU', 'vpD6U/rz1XSXrgrX', 'vpLOU/rz1XSXrgrN', 'vp/RU/rz1XSXrgpx', 'vpgHU/rz1XSXrgji', 'vcwrU/rz1XSXrgqU', 'vcwnU/rz1XSXrgXX', 'vcwPU/rz1XSXrgXN', 'vpgHU/rz1XSXrvri', 'vp/OU/rz1ISXrvpU', 'vpLnU/rzirSXrvjg', 'vpEvU/r8xrSXrvjN', 'vpJOU/r8xZSXrvqx', 'vpwnU/r81ISXrvXi', '\\i4kUpSigvpgvEj3', 'rcWkUpa8gvpgvgr3', 'rpekUpakgvpgvgI3', 'riLkUpa+gvpgvvi3', 'riekUpaNgvpg64X3', 'ri4kUpaNgvpg6Ej3', 'riLkUpaNgvpxvgX3', 'rpDkUpaNgvpxvvj3', 'rAwkUpaNgvpx64r3', '\\iJkUpaNgvpx64I3', '\\pekUpaNgvpx6EN3', 'vpwpU/rk1XSXvEr/', 'vp4HU/rk1XSXvEpU', 'vpW6U/rk1rSXvEjg', 'vpWOU/rkxZSXvEj1', 'vpeOU/rkxISXvEqx', 'vpEPU/rkxrSXvEXi', 'vpD\\U/r8iXSXvEiN', 'vpDPU/r8irSXvENX', 'vpDRU/r81ZSXvEN+', 'vpLvU/r81ISXvEzx', 'vpLPU/r81ISXvEIi', 'vpLOU/r81ISXvEAU', 'vpLHU/r81XSXvgrg', 'vpLRU/r81XSXvgrN', 'vp/6U/r81XSXvgzU', 'vp/\\U/r81rSXvvri', 'vp/rU/r81rSX64XX', 'vp/vU/r81rSX64ix', 'vp/nU/r81rSX64zU', 'vp/pU/r81rSX64IX', 'vp/OU/r81rSX64IN', 'vp/HU/r81rSX64Ax', 'vp/RU/r81rSX6Er/', 'vpg6U/r81rSX6EpU', 'vpgrU/r81rSX6Ejg', 'vpgvU/r81rSX6EjN', 'vpgPU/r81rSX6EX0', 'vpgpU/r81rSX6ENX', 'vpgOU/r81rSX6Ez/', 'vpgHU/r81rSX6EIi', 'vpgRU/r81rSX6EAU', 'vcw6U/r81rSgr4rN', 'vcw6U/r81XSgrEjX', 'vcw6U/r81ISgrEjN', 'vpgHU/r81ZSgrEqx', 'vpgrU/rkxrSgrEXi', 'vp/OU/rkxXSgrEiU', 'vp/vU/rkxISgrEi+', 'vpLpU/rk1rSgrENN', 'vpLrU/rk1rSgrEzx', 'vpDpU/rk1XSgrEIi', 'vpDvU/rk1XSgrEAg', 'vpERU/rk1XSgrgrX', 'vpEOU/rk1ISgrgrN', 'vpEnU/rk1ISgrgpx', 'vpErU/rkirSgrgji', 'vpE6U/rkirSgrgqU', 'vpeHU/rkirSgrgq+', 'vpeOU/rkirSgrgXN', 'vpepU/rkirSgrgi/', 'vpePU/rkirSgrgNi', 'vpenU/rkirSgrgzU', 'vpevU/rkirSgrgIX', 'vperU/rkirSgrgIN', 'vpe\\U/rkirSgrvrx', 'vpe6U/rkirSgrvpU', 'vpWRU/rkirSgrvjX', 'vpWHU/rkirSgrvjN', 'vpWOU/rkirSgrvXi', 'vpWpU/rkirSgrviU', 'vpWPU/rkirSgvEIi', 'vpWPU/rk1ZSgvgpx', 'vpWpU/rk1ZSgvgNi', 'vpWOU/rk1ZSgvgAx', 'vpWHU/rk1ZSgvvqx', 'vpWRU/rk1ZSgvvAU', 'vpe6U/rk1ZSg64r1', 'vpe\\U/rk1ZSg64XN', 'vperU/rk1ZSg64ix']
s = sample(s)
v = p(':'.join(s))
print("轨迹信息参数")
print(v)
print()

# 移动距离信息
# 真实移动了的距离占图片总长度的百分比信息，估计就是用这个验证是否移动到正确位置上
token = '072b86090d6f4a8c9c9cfaf5284624de'
t = "72.5"
e = y(token, t)
v = p(e)
print("移动距离信息")
print(v)
print()

# 点击次数和轨迹信息列表长度
# 列表长度取真实长度，（不取规约成最大50的长度，如果长度是200就写200），用逗号分隔
token = '072b86090d6f4a8c9c9cfaf5284624de'
t = "1,200"
e = y(token, t)
v = p(e)
print("点击次数和轨迹信息列表长度")
print(v)
print()