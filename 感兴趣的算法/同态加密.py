def isprime_mr(a,b=None):
    if b is None: b = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    if a == 2:return True
    if a%2==0 or a==1:return False
    for x in b:
        t = a - 1
        while t%2 == 0:
            v = pow(x,t,a)# python自带函数pow就带有快速幂取模功能
            if v not in [0,1,a-1]:
                return False
            else:
                if v in [0,a-1]: break
                t //= 2
    return True
def make_primes(length=1024, e=65537):
    if e == 2: raise KeyError('The parameter E must not be equal to 2.')
    import random
    def get_prime(bitlen=1024):
        num = (1<<(bitlen-1)) + random.randint(0,1<<(bitlen-1)) | 1
        while True:
            num += 2
            if isprime_mr(num):
                return num
    while True:
        p = get_prime(length//2)
        q = get_prime(length//2)
        n = p * q
        if n.bit_length() == length and p != q:
            break
    return n,p,q


bits = 64
n,p,q = make_primes(bits)
n2 = n ** 2
print('n,p,q,n2:', n,p,q,n2)

def ex_gcd(a,b):
    if b == 0:
        return (1,0,a)
    (x, y, r) = ex_gcd(b,a%b)
    t = x
    x = y
    y = t - a//b*y
    return (x,y,r)

def modinv(a, m):
    x, y, g = ex_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def lcm(a, b):
    return a * b // ex_gcd(a, b)[-1]




import random

lamb = lcm(p-1, q-1)
x = modinv((pow(n + 1, lamb, n2) - 1) // n, n)
print(lamb, x)

def encrypt(m):
    return (n * m + 1) % n2

def add(a, b):
    return (a * b) % n2

def mult(a, b):
    return pow(a, b, n2)

def decrypt(c):
    return ((pow(c, lamb, n2) - 1) // n * x) % n

e1 = encrypt(2)
e2 = encrypt(3)
print(e1, e2)

e3 = add(e1, e2)
c3 = decrypt(e3)

e4 = mult(e1, 3)
c4 = decrypt(e4)

print('n2:', n2)
print('e3:', e3)
print('c3:', c3)
print('e4:', e4)
print('c4:', c4)