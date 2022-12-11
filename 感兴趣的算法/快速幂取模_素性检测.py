# 快速幂
def qk_pow(a,b):
    ans = 1
    while b>0:
        if b & 1:
            ans *= a
        a *= a
        b >>= 1
    return ans

# 快速幂取模，注意，python自带的pow函数加上第三个参数等同于下面的函数
def qk_pow_mod(a,b,m):
    ans = 1
    while b>0:
        if b & 1:
            ans = a * ans % m
        a = a * a % m
        b >>= 1
    return ans

# 一般素性检测
def isprime(a):
    for i in range(2, int(a**.5)+1):
        if a%i == 0:
            return True

# miller-rabin 算法素性检测
def mr(a,b=[2, 3, 5, 7, 11, 13, 17]):
    # 根据网上描述：当 b = [2, 3, 5, 7, 11, 13, 17] 时
    # 在小于 3.41*10**15 范围内都是正确的
    if a == 2:return True
    if a % 2 == 0:return False
    for x in b:
        t = a - 1
        while t%2 == 0:
            v = pow(x,t,a)
            # print('{}**{} % {} = {}'.format(x,t,a,v))
            if v not in [0,1,a-1]:
                return False
            else:
                if v in [0,a-1]: break
                t //= 2
    return True

print('(quick pow) {}**{} = {}'.format(2,8,qk_pow(2,8)))
print('(quick pow mod) {}**{} % {} = {}'.format(2,10**128,100,qk_pow_mod(2,10**128,100)))

for i in range(500):
    num = 10**125 + 1 + i*2
    print('(miller-rabin) {} {} a prime.'.format(num, 'very likely' if mr(num) else 'is not'))
