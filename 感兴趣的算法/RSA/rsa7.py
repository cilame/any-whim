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
d = invert(e, (p-1)*(q-1))
c = pow(m, e, n)
c_mod_p = c % p
c_mod_q = c % q

print('n =', n)
print('e =', e)
print('c_mod_p =', c_mod_p)
print('c_mod_q =', c_mod_q)


# c1 = c%p
# c2 = c%q
# c = c1 + kp
# c2 = (c1 + kp)%q
# # 若 a => b(mode p), 则对于任意的 c, 都有 (a+c) => (b+c)(mode p)
# c2-c1 = kp%q
# (c2-c1)*p1%q = k # (p1为p,q的逆元)
# k = (c2-c1)*p1%q
# c = c1 + ((c2-c1)*p1%q)*p

p1 = invert(p, q)
c = c_mod_p + (c_mod_q-c_mod_p)*p1%q*p
print('c =', c)
m = pow(c, d, n)
print()
print(m)
data = bytes.fromhex(hex(m)[2:])
print(data)