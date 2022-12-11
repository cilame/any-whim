import math
def pell (D):
    a0 = int (D**0.5)
    if a0*a0 == D: return None
    gp = [0, a0]
    gq = [1, D-a0**2]
    a = [a0, int((a0+gp[1])/gq[1])]
    p = [a[0], a[0]*a[1]+1]
    q = [1, a[1]]
    maxdepth = None
    n = 1
    while maxdepth is None or n < maxdepth:
        if maxdepth is None and a[-1] == 2*a[0]:
            r = n-1
            if r % 2 == 1: return p[r], q[r]
            maxdepth = 2*r+1
        n += 1
        gp.append (a[n-1]*gq[n-1]-gp[n-1])
        gq.append ((D-gp[n]**2)//gq[n-1])
        a.append (int ((a[0]+gp[n])//gq[n]))
        p.append (a[n]*p[n-1]+p[n-2])
        q.append (a[n]*q[n-1]+q[n-2])
    return p[2*r+1], q[2*r+1]
def gen_pell(D, maxtimes=10):
    idx = 1
    x1, y1 = pell(D)
    x, y = x1, y1
    yield x, y
    idx += 1
    while True:
        x, y = x1*x+D*y1*y, x1*y+y1*x
        assert x*x-D*y*y == 1
        yield x, y
        idx += 1
        if idx > maxtimes:
            return

if __name__ == '__main__':
    for x, y in gen_pell(0x1337):
        print('x =', x)
        print('y =', y)
        print()