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
g = n + 1

assert m < n
c = (pow(g,p,n*n) * pow(m,n,n*n)) % (n*n)
hint = pow(m,n,n*n)

print('c =', c)
print('n =', n)
print('hint =', hint)

# h = m^n%n*n
# c = ((n+1)^p%n*n * m^n%n*n) % n*n
# c = ((n+1)^p%n*n * h) % n*n
# c = (n+1)^p*h % n*n

# h1 = invert(h, n*n)
# c*h1 = (n+1)^p % n*n // 二项式分解
# c*h1 = (knp+1) % n*n
# c*h1-1 = knp % np*q
# (c*h1-1)//n = kp

h1 = invert(hint, n*n)
p = gcd((c * h1 - 1)//n, n)
q = n // p
d = invert(n, (p-1)*(q-1)**2)
print(d)

m = pow(hint, d, n)
print()
print(m)
print(libnum.n2s(int(m)))