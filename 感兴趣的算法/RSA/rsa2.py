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
p1 = invert(p, q)
q1 = invert(q, p)
c = pow(m, e, n)
print('p1 =', p1)
print('q1 =', q1)
print('n =', n)
print('e =', e)
print('c =', c)

# p1*p = 1%q
# q1*q = 1%p

# p1*p-1 = kq
# q1*q-1 = kp
# (p1*p-1) * q1*q-1 = kq * kp = kn
# (p1*p-1) * q1*q-1 = kq * kp = kn
# p1*q1*n - (p1*p+q1*q) + 1 = kn
# (p1*p+q1*q) - 1 = kn

# ∵ 在 (p1*p+q1*q)-1= kn 中 k 值为 1 （这里的逻辑推导过程不详）
#   （我感觉大概是 p1,p,q1,q 这几个数均为正整数，所以结果的位数有限制，导致k值只能为1
# ∴ (p1*p+q1*q)-1-n = 0
# 又 (p-1)*(q-1)-phi = 0
# 联立方程解出 p,q

p,q = sympy.symbols('p,q')
f1 = p*q-n
f2 = (p1*p+q1*q)-1-n
so = sympy.solve([f1,f2], [p,q])

if '/' in str(so[0]):
    p,q = so[1]
else:
    p,q = so[0]

p = int(p)
q = int(q)
d = invert(e, (p-1)*(q-1))

data = int(pow(c, d, n))
print(data)
print(libnum.n2s(data))






