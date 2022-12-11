import libnum
import uuid
from gmpy2 import *
from Crypto.Util.number import *

import uuid
flag = 'flag{'+str(uuid.uuid4())+'}'
print(flag)
m = libnum.s2n(flag)
while True:
    p = libnum.generate_prime(512)
    q = libnum.generate_prime(512)
    t = bin(p * q)[2:]
    if len(t) == 1024:
        break
e = 0x10001
n = p * q
c = pow(m, e, n)

h1 = pow(2022*p+2021*q, 1919, n)
h2 = pow(2021*p+2022*q, 9191, n)

print('h1 =', h1)
print('h2 =', h2)
print('n =', n)
print('c =', c)

# 若 a => b(mod p), 则对与正整数 c, 都有 a^c => b^c(mod p)

# h1^9191 = (2022*p+2021*q) ^ (1919*9191) + kn
# h2^1919 = (2021*p+2022*q) ^ (1919*9191) + kn
# h1^9191 = 2022 ^ (1919*9191) * p ^ (1919*9191) + kq
# h2^1919 = 2021 ^ (1919*9191) * p ^ (1919*9191) + kq
# h1^9191 * 2021 ^ (1919*9191) = 2021 ^ (1919*9191) * 2022 ^ (1919*9191) * p ^ (1919*9191) + kq
# h2^1919 * 2022 ^ (1919*9191) = 2022 ^ (1919*9191) * 2021 ^ (1919*9191) * p ^ (1919*9191) + kq
# # 上下相减得
# h1^9191 * 2021 ^ (1919*9191) - h2^1919 * 2022 ^ (1919*9191) = kq
# p = gcd(h1^9191*2021^(1919*9191) - h2^1919*2022^(1919*9191), n)

p = gcd(pow(h1, 9191, n) * pow(2021, 1919*9191, n) - pow(h2, 1919, n) * pow(2022, 1919*9191, n), n)
q = n // p
d = invert(e, (p-1)*(q-1))
m = pow(c, d, n)
print(m)
data = bytes.fromhex(hex(m)[2:])
print(data)