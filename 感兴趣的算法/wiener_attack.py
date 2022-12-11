# 函数用于在知道rsa其中的 e,n 时直接计算出 d 参数的算法
# 该函数使用有一个前提，就是 e 必须在很大（与n参数相当）时该函数才有效

import decimal

# 使用自带函数库实现高精度计算，十进制1000位已经够用
decimal.getcontext().prec = 1000
Decimal = decimal.Decimal

def trans(x, y):
    res = []
    while y:
        res.append(x //y)
        x, y = y, x%y
    return res
    
def next_fract(sub_res):
    num, denom = 1, 0
    for i in sub_res[::-1]:
        denom, num = num, i*num+denom
    return denom, num

def ex_gcd(a,b):
    if b == 0:
        return (1,0,a)
    (x, y, r) = ex_gcd(b,a%b)
    t = x
    x = y
    y = t - a//b*y
    return (x,y,r)

def sub_fract(e, n):
    res = trans(e, n)
    res = list(map(next_fract,(res[0:i] for i in range(1,len(res)))))
    return res

def get_pq(a,b,c):
    par = (Decimal(str(b)) * Decimal(str(b)) \
            - Decimal('4') * Decimal(str(a)) * Decimal(str(c))) \
                **  Decimal(str('0.5'))
    par = int(par) # 将 Decimal 对象转换回 int 对象，以免在后续出现异常
    return (-b+par)//(2*a),  (-b-par)//(2*a)

def wiener_attack(e, n):
    for d, k in sub_fract(e, n):  #用一个for循环来注意试探e/n的连续函数的渐进分数，直到找到一个满足条件的渐进分数
        if k==0:            continue
        if (e*d-1) % k!=0:  continue
        try:
            px, qy = get_pq(1, n-((e*d-1)//k)+1, n)
        except:
            return 'Error, Wiener_attack algorithm does not work!'
        if px*qy == n:
            p, q    = abs(px), abs(qy)     #可能会得到两个负数，负负得正未尝不会出现
            a, b, r = ex_gcd((p-1)*(q-1), e)
            return b
    
e = 14058695417015334071588010346586749790539913287499707802938898719199384604316115908373997739604466972535533733290829894940306314501336291780396644520926473
n = 33608051123287760315508423639768587307044110783252538766412788814888567164438282747809126528707329215122915093543085008547092423658991866313471837522758159
d = wiener_attack(e, n)
print("d =",d)

e = 354611102441307572056572181827925899198345350228753730931089393275463916544456626894245415096107834465778409532373187125318554614722599301791528916212839368121066035541008808261534500586023652767712271625785204280964688004680328300124849680477105302519377370092578107827116821391826210972320377614967547827619
n = 460657813884289609896372056585544172485318117026246263899744329237492701820627219556007788200590119136173895989001382151536006853823326382892363143604314518686388786002989248800814861248595075326277099645338694977097459168530898776007293695728101976069423971696524237755227187061418202849911479124793990722597
d = wiener_attack(e, n)
print("d =",d)