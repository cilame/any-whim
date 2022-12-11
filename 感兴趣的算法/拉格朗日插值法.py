# 题目： 1,4,9,16,_,36,49 请按照数字规律，找出空白处的数

listx = [1,2,3,4,5,6,7]
listy = [1,4,9,16,114514,36,49]

def get_rest(listx, listy, symx):
    expr = 0
    for index, _ in enumerate(listx):
        retu = 1
        para = 1
        ridx = listx[index]
        rest = []
        for idx, i in enumerate(listx):
            if index != idx:
                rest.append(i)
        for i in rest:
            para *= ridx - i
            retu *= symx - i
        retu /= para
        retu *= listy[index]
        expr += retu
    return expr

import sympy
symx = sympy.Symbol('x')
simexpr = str(sympy.simplify(get_rest(listx, listy, symx)))
print('表达式为:', simexpr)

# 验算
print('验算结果')
for x in listx:
    print('x:{}, y:{}'.format(x, eval(simexpr)))

# 表达式为: 38163*x**6/16 - 877749*x**5/16 + 7899741*x**4/16 - 35300775*x**3/16 + 5113843*x**2 - 23012289*x/4 + 2404269
# 验算结果
# x:1, y:1.0
# x:2, y:4.0
# x:3, y:9.0
# x:4, y:16.0
# x:5, y:114514.0
# x:6, y:36.0
# x:7, y:49.0

# 对的，按照上面的公式可以得出，当x等于5时结果是 114514 ，所以空白处的结果就是 114514