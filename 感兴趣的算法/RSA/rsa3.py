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

hint = pow(2020*p+2021, q, n)

print('n =', n)
print('c =', c)
print('hint =', hint)


# h = (2020*p+2021)^q%n
# h = (2020*p+2021)^q + k*p*q
# # 多项式 (2020*p+2021)^q 展开后，除了最后一项没有p相关，其余项均存在 p
# # 所以可以转变成下面这样
# h = k1*p + 2021^q + k*q*p
# h%p = 2021^q%p
# 2021^q-h = kp

# # 要求的就是下面这个，但是里面 h-2021^q 仍然有一个未知的 q
# p = gcd(2021^q-h, n)

# # 得求证一下
# # 2021^q%p = 2021^n%p

# 2021^n%p
# 2021^(q*p)%p
# (2021^q)^p%p 
# # 根据费马小定理 a^p 与 a%p 同余
# # 所以可以转换成如下结果
# (2021^q)%p
# # 最后 2021^n%p = (2021^q)%p
# (2021^q)%p = 2021^n%p = 2021^n+kp

# # 综上 
# p = gcd(2021^n%n-h, n)

p = gcd(pow(2021, n, n) - hint, n)
q = n // p
print(p)

d = invert(e, (p-1)*(q-1))
m = pow(c, d, n)
print(m)
info = bytes.fromhex(hex(m)[2:])
print(info)



