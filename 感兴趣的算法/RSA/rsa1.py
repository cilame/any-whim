# pip install libnum sympy gmpy2 pycryptodome

import libnum
import sympy
from gmpy2 import *
from Crypto.Cipher import AES


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
M = 2021 * m * 1001 * p
c = pow(M, e, n)

# 因为
# c = M^e%n
# c = M^e + k*p*q
# c = (2021*m*1001*p)^e + k*p*q
# 明显发现里面都用公因子 p
# 所以 c % p = 0
# 又因为 n = p * q
# gcd(c, n) == p

print('n =', n)
print('c =', c)

p = gcd(c, n)
q = n // p
d = invert(e, (p-1)*(q-1))

data = int(pow(c, d, n))
data = data // 2021 // 1001 // p
print(data)
print(libnum.n2s(int(data)))







