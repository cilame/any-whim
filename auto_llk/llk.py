import random
import numpy as np

# 根据输入的方向返回该方向上的同链为零的端点坐标
# 以及其端点延伸一格的坐标（坐标受限于 s_map 范围中）
def get_cross(s_map,point,target):
    h0,w0 = point
    h,w = s_map.shape
    ret,packer = [],[]
    for i in target:
        if i.lower() in ('left','l'):
            p = np.where(s_map[h0,:w0]!=0)[0]
            if len(p):
                k = p.max() + 1
                packer.append((h0, k-1))
            else:
                k = 0
        if i.lower() in ('right','r'):
            p = np.where(s_map[h0,w0:]!=0)[0]
            if len(p):
                k = p.min() + w0 - 1
                packer.append((h0, k+1))
            else:
                k = w - 1
        if i.lower() in ('up','u'):
            p = np.where(s_map[:h0,w0]!=0)[0]
            if len(p):
                k = p.max() + 1
                packer.append((k-1, w0))
            else:
                k = 0
        if i.lower() in ('down','d'):
            p = np.where(s_map[h0:,w0]!=0)[0]
            if len(p):
                k = p.min() + h0 - 1
                packer.append((k+1, w0))
            else:
                k = h - 1
        ret.append(k)
    return ret,packer

# 鱼骨抽关键点的这种算法，不指定 target 就默认是随机左右 or 上下方向
def get_fish(s_map,point,target='rd'):
    pack = []
    assert target in ['rd','lr','ud'] # random, left-right, up-down
    if target=='rd':
        target = np.random.choice(('lr','ud'))
    if target=='lr':
        (l,r),packer = get_cross(s_map,point,('l','r'))
        pack += packer
        for i in range(l,r+1):
            pt = (point[0],i)
            _,packer = get_cross(s_map,pt,('u','d'))
            pack += packer
        return pack
    if target=='ud':
        (u,d),packer = get_cross(s_map,point,('u','d'))
        pack += packer
        for i in range(u,d+1):
            pt = (i,point[1])
            _,packer = get_cross(s_map,pt,('l','r'))
            pack += packer
        return pack

# 根据坐标点获取其坐标的类别以字典形式返回
def get_class_point(s_map,fishpoint):
    dc = dict()
    for i in fishpoint:
        key = s_map[i]
        if not dc.get(key):
            dc[s_map[i]] = [i]
        else:
            dc[s_map[i]] += [i]
    return dc

# 通过类别坐标字典，获取该字典可以被返回的所有双点
# 双点即为连连看每次需要选择的两个坐标点
def pick_dc_all(dc):
    pts = []
    for i in dc:
        for _ in range(int(len(dc[i])/2)):
            pts.append((dc[i].pop(),dc[i].pop()))
    return pts

# 单个点获取该点下鱼骨端点后能获取到的所有可消除的双点
def get_1point_results(s_map,point):
    fish = get_fish(s_map,point)
    dc   = get_class_point(s_map,fish)
    pts  = pick_dc_all(dc)
    return pts

# 两点框的遍历，解决相邻问题
def get_close(s_map):
    chain = []
    h,w = s_map.shape
    for i in range(h):
        for j in range(w-1):
            a,b = s_map[(i,j)],s_map[(i,j+1)]
            if a!=0 and b!=0 and a==b:
                s_map[(i,j)],s_map[(i,j+1)] = 0,0
                chain.append(((i,j),(i,j+1)))
    for i in range(w):
        for j in range(h-1):
            a,b = s_map[(j,i)],s_map[(j+1,i)]
            if a!=0 and b!=0 and a==b:
                s_map[(j,i)],s_map[(j+1,i)] = 0,0
                chain.append(((j,i),(j+1,i)))
    return chain

# 直接获取该 s_map 的全解链。
def get_chain(s_map):
    s_map = s_map.copy()
    chain = get_close(s_map)
    cur_flash = (s_map.ravel()!=0).tolist().count(True)
    over_break = 0
    while np.any(s_map!=0):
        zpoints = list(zip(*map(lambda i:i.tolist(),np.where(s_map==0))))
        point = random.choice(zpoints)
        result = get_1point_results(s_map,point)
        for idx1,idx2 in result:
            chain.append((idx1,idx2))
            s_map[idx1],s_map[idx2] = 0,0
        next_flash = (s_map.ravel()!=0).tolist().count(True)
        # 连连看存在无解情况，所以以下就是返回在 s_map 完全无解之前
        # 算法能找到的所有有解链 chain
        if cur_flash != next_flash:
            cur_flash = next_flash
            over_break = 0
            continue
        else:
            if over_break > 100:
                break
            over_break += 1
    return chain
