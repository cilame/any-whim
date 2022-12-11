class Mat:
    def __init__(self, mx):
        self.mx = mx
        self.dct = self._init9x9pos()
        self.pos = self._get9x9pos()
        self.cnt = 0
    def get9x9(self, num=None, pidx=0):
        self.cnt += 1
        if self.cnt % 10000 == 0:
            print('cost step:', self.cnt)
        if pidx >= (num if num else len(self.pos)):
            print('cost step:', self.cnt)
            return self.mx
        x, y = self.pos[pidx]
        for key in self._get_rest_list(x, y, self.dct):
            self.mx[y][x] = key
            ret = self.get9x9(num=num, pidx=pidx+1)
            if ret:
                return ret
            else:
                self.mx[y][x] = 0
    def _init9x9pos(self):
        d = {}
        for y in range(len(self.mx)):
            for x in range(len(self.mx[0])):
                if self.mx[y][x] == 0:
                    d[(x, y)] = self._get_rest_list(x, y)
        return d
    def _get9x9pos(self):
        d = self.dct.items()
        d = sorted(d, key=lambda i:len(i[1]))
        pos = [pos[0] for pos in d]
        return pos
    def _get_rest_list(self, x, y, dct=None):
        anum = []
        for i in self.mx[y]:
            if i:    anum.append(i)
        for i in self.mx:
            if i[x]: anum.append(i[x])
        if   x >= 0 and x < 3: rngx = [0,1,2]
        elif x >= 3 and x < 6: rngx = [3,4,5]
        elif x >= 6 and x < 9: rngx = [6,7,8]
        if   y >= 0 and y < 3: rngy = [0,1,2]
        elif y >= 3 and y < 6: rngy = [3,4,5]
        elif y >= 6 and y < 9: rngy = [6,7,8]
        for _x in rngx:
            for _y in rngy:
                if self.mx[_y][_x]:
                    anum.append(self.mx[_y][_x])
        rest = []
        for i in dct[(x, y)] if dct else range(1, 10):
            if i not in anum:
                rest.append(i)
        return rest

s = [
    [0,0,0,  8,0,0,  0,0,0],
    [0,0,0,  5,6,0,  0,9,0],
    [0,0,7,  0,0,0,  2,0,0],
    [8,0,0,  0,0,0,  0,0,0],
    [5,0,0,  1,0,0,  0,0,0],
    [0,0,0,  0,2,0,  4,0,7],
    [0,0,0,  0,0,0,  0,1,0],
    [0,0,4,  0,0,0,  0,0,0],
    [3,0,0,  0,0,0,  0,5,8],
]
# s = [
#     [8,0,0,  0,0,0,  0,0,0],
#     [0,0,3,  6,0,0,  0,0,0],
#     [0,7,0,  0,9,0,  2,0,0],
#     [0,5,0,  0,0,7,  0,0,0],
#     [0,0,0,  8,4,5,  7,0,0],
#     [0,0,0,  1,0,0,  0,3,0],
#     [0,0,1,  0,0,0,  0,6,8],
#     [0,0,8,  5,0,0,  0,1,0],
#     [0,9,0,  0,0,0,  4,0,0]
# ]

s = Mat(s)
v = s.get9x9() # 对于难度比较高的数独，最慢五六秒也能出结果。
for i in v:
    print(i)