s = [
    [3,2,0],
    [3,2,2],
    [0,3,1]
]
def has_equal_line(s):
    def all_equal(a):
        if not a: raise
        for i in a:
            if not a[0] == i:
                return False
        return True
    for i in s:
        if all_equal(i):
            return True
    for i in range(len(s)):
        ls = []
        for j in range(len(s[0])):
            ls.append(s[j][i])
        if all_equal(ls):
            return True
    return False
def mk_swap_list_point(s):
    def make_next_point(p1, maxc, maxn):
        ls = []
        if p1[0] - 1 >= 0:      ls.append((p1[0] - 1, p1[1]))
        if p1[0] + 1 < maxc:    ls.append((p1[0] + 1, p1[1]))
        if p1[1] - 1 >= 0:      ls.append((p1[0], p1[1] - 1))
        if p1[1] + 1 < maxn:    ls.append((p1[0], p1[1] + 1))
        return ls
    maxc = len(s)
    maxn = len(s[0])
    ret = []
    for i in range(maxc):
        for j in range(maxn):
            p1 = (i, j)
            for p2 in make_next_point(p1, maxc, maxn):
                ret.append([p1, p2])
    return ret
plist = mk_swap_list_point(s)
def swap(s, p1, p2):
    temp = s[p1[0]][p1[1]]
    s[p1[0]][p1[1]] = s[p2[0]][p2[1]]
    s[p2[0]][p2[1]] = temp

for p1, p2 in plist:
    swap(s, p1, p2)
    if has_equal_line(s):
        print(p1, p2)
    swap(s, p1, p2)