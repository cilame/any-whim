# miller-rabin 算法素性检测
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

# Pollcard Rho 质因数分解，比普通质因分解更好的一种算法，能处理更大的数字
def prime_list_rho(n,root=None):
    # 之所以不用 def prime_list_rho(n,root=[]): 的方式是因为这里有坑
    # 作为函数对象的内部参数的临时地址多次使用会一直引用一个地址，
    # 所以考虑到该参数最后会作为结果返回出去，所以需要考虑初始化处理
    if root is None: root = []
    if not root and n<2:
        raise ValueError(n)
    if isprime_mr(n):
        root.append(n)
        return root
    from random import randint
    from math import gcd
    while True:
        x = randint(0,n-1) + 1
        c = randint(0,n-1) + 1
        y = x
        i = j = 2
        while True:
            x = ((x**2)+c)%n
            z = abs(x - y)
            d = gcd(z,n)
            if d>1 and d<n:
                prime_list_rho(d,root)
                prime_list_rho(n//d,root)
                return root
            if x == y: break
            if i == j:
                y = x
                j <<= 1
            i += 1

def test_rho(num):
    print('=========== Pollcard Rho ============')
    import time
    c = time.time()
    try:
        print(v)
    except:
        pass
    v = prime_list_rho(num)
    q = 1
    for i in v:
        q *= i
    print('prime_list',v)
    print('test num:      ',num)
    print('multiplicative:',q)
    print('==================== cost time:',time.time()-c)
    print();print();print()

test_rho(12345678987654321)
test_rho(2222222222222222222222222222)
