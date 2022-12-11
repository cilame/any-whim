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
c = pow(m*p+n, e, n)

print('n =', n)
print('c =', c)
print('e =', e)

# c = ((m+q)*p)^e + k*q*p
# c%p = 0

p = gcd(c, n)
q = n // p
d = invert(e, (p-1)*(q-1))
m = pow(c, d, n)
m = (m) // p
print(m)
data = bytes.fromhex(hex(m)[2:])
print(data)


