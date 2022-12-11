from math import factorial
import matplotlib.pyplot as plt

x1 = 100
y1 = 100
x2 = 200
y2 = 200
def step_len(x1, y1, x2, y2):
    ln = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return int(ln / 10)
slen = step_len(x1, y1, x2, y2)

lp = 0
rp = 0
xx1 = int(x1 + (x2 - x1) / 12 * (4-lp*4))
yy1 = int(y1 + (y2 - y1) / 12 * (8+lp*4))
xx2 = int(x1 + (x2 - x1) / 12 * (8+rp*4))
yy2 = int(y1 + (y2 - y1) / 12 * (4-rp*4))

points = [[x1, y1], [xx1, yy1], [xx2, yy2], [x2, y2]]
N = len(points)
n = N - 1 
px = []
py = []
for T in range(slen + 1):
    t = T*(1/slen)
    x,y = 0,0
    for i in range(N):
        B = factorial(n)*t**i*(1-t)**(n-i)/(factorial(i)*factorial(n-i))
        x += points[i][0]*B
        y += points[i][1]*B
    px.append(x)
    py.append(y)

print(px)
print(py)

plt.plot(px,py)
plt.plot([i[0] for i in points],[i[1] for i in points],'r.')
plt.show()