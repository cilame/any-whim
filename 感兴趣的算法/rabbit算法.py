# 目前暂时没有查到哪里有这这个算法其他模式处理
# 貌似主要时用于流加密处理的？
# 并且没有一些可以在线验证的代码，所这里就暂时不考虑其他加密模式(cbc,ctr...)的开发。
# 在给与的测试数据能够正常验证，基本的算法是能够正常加密解密的所以目前就到此为止。

def ROTL32(v,n):
    return (((v<<n)&0xffffffff) | ((v>>(32-n))&0xffffffff))

class Rabbit_state(object):
    def __init__(self):
        self.x = [0] * 8
        self.c = [0] * 8
        self.carry = 0

class Rabbit_ctx(object):
    def __init__(self):
        self.m = Rabbit_state()
        self.w = Rabbit_state()

class Rabbit(object):
    def __init__(self, key, iv):
        self.ctx = Rabbit_ctx();
        self.set_key(key);
        if iv or len(iv):
            self.set_iv(iv);

    def rotl(self, v, n):
        return ROTL32(v, n)
        
    def g_func(self, x):
        x       =     x & 0xffffffff
        x       =   x*x & 0xffffffffffffffff
        result  = x>>32 ^ x&0xffffffff
        return result

    def set_key(self,key):
        #generate four subkeys
        key0 = int.from_bytes(key[0:4],'little')
        key1 = int.from_bytes(key[4:8],'little')
        key2 = int.from_bytes(key[8:12],'little')
        key3 = int.from_bytes(key[12:16],'little')
        s = self.ctx.m
        #generate initial state variables
        s.x[0], s.x[1] = key0, ((key3<<16)&0xffffffff) | ((key2>>16)&0xffff)
        s.x[2], s.x[3] = key1, ((key0<<16)&0xffffffff) | ((key3>>16)&0xffff)
        s.x[4], s.x[5] = key2, ((key1<<16)&0xffffffff) | ((key0>>16)&0xffff)
        s.x[6], s.x[7] = key3, ((key2<<16)&0xffffffff) | ((key1>>16)&0xffff)
        #generate initial counter values
        s.c[0], s.c[1] = self.rotl(key2,16), (key0&0xffff0000) | (key1&0xffff)
        s.c[2], s.c[3] = self.rotl(key3,16), (key1&0xffff0000) | (key2&0xffff)
        s.c[4], s.c[5] = self.rotl(key0,16), (key2&0xffff0000) | (key3&0xffff)
        s.c[6], s.c[7] = self.rotl(key1,16), (key3&0xffff0000) | (key0&0xffff)
        s.carry = 0
        for i in range(4):
            self.next_state(self.ctx.m);
           
        for i in range(8):
            self.ctx.m.c[i]^=self.ctx.m.x[(i+4)&7]
        self.ctx.w=self.copy_state(self.ctx.m)

    def copy_state(self,state):
        n       = Rabbit_state()
        n.carry = state.carry
        for i,j in enumerate(state.x): n.x[i] = j
        for i,j in enumerate(state.c): n.c[i] = j
        return n

    def set_iv(self,iv):
        v = [0] * 4
        v[0] = int.from_bytes(iv[0:4],'little')
        v[2] = int.from_bytes(iv[4:8],'little')
        v[1] =  (v[0]>>16) | (v[2]&0xffff0000)
        v[3] = ((v[2]<<16) | (v[0]&0x0000ffff)) & 0xffffffff
        for i in  range(8): 
            self.ctx.w.c[i] = self.ctx.m.c[i] ^ v[i&3]
        self.ctx.w.x = [cc for cc in self.ctx.m.x]
        for i in range(4): 
            self.next_state(self.ctx.w)

    def next_state(self,state):
        g = [0] * 8
        x = [0x4D34D34D, 0xD34D34D3, 0x34D34D34]
        for i in range(8):
            _tmp = state.c[i]
            state.c[i]  = (state.c[i] + x[i%3] + state.carry) & 0xffffffff
            state.carry = (state.c[i] < _tmp)
        for i in range(8):
            g[i] = self.g_func(state.x[i] + state.c[i])
        i, j = 0, 7
        while i < 8:
            state.x[i] = (g[i] + self.rotl(g[j], 16) + self.rotl(g[j-1], 16)) & 0xffffffff
            i, j = i+1, j+1
            state.x[i] = (g[i] + self.rotl(g[j & 7], 8) + g[j-1]) & 0xffffffff
            i, j = i+1, j+1
            j &= 7
        
    def crypt(self, msg):
        plain   = []
        x       = [0] * 4
        start   = 0
        while True:
            self.next_state(self.ctx.w)
            for i in range(4):
                x[i] = self.ctx.w.x[i<<1]

            print((self.ctx.w.x[5] >> 16) ^ (self.ctx.w.x[3] << 16))
            x[0] ^= (self.ctx.w.x[5] >> 16) ^ (self.ctx.w.x[3] << 16)
            x[1] ^= (self.ctx.w.x[7] >> 16) ^ (self.ctx.w.x[5] << 16)
            x[2] ^= (self.ctx.w.x[1] >> 16) ^ (self.ctx.w.x[7] << 16)
            x[3] ^= (self.ctx.w.x[3] >> 16) ^ (self.ctx.w.x[1] << 16)
            b = [0] * 16
            for i,j in enumerate(x):
                for z in range(4):
                    b[z+4*i] = 0xff & (j >> (8*z))
            for i in range(16):
                plain.append(msg[start] ^ b[i])
                start += 1
                if start == len(msg):
                    return bytes(plain)

if __name__ == '__main__':
    # key 为 16byte 长度的倍数
    # iv 为 8byte 长度
    # plaintext 为 16byte*n、
    # 同时，加密解密使用同一个函数

    plaintext   = b"12345678123"
    key = b'1234567812345678'
    iv  = b'12345678'

    import base64
    cipher  = Rabbit(key, iv)
    data    = cipher.crypt(plaintext)
    v       = base64.b64encode(data)
    print(v)

    cipher  = Rabbit(key, iv) # 解密时也需要重新初始化该对象
    data    = cipher.crypt(data)
    print(data)