import numpy as np
from collections import OrderedDict
from itertools import groupby
from tkinter import *
from functools import partial

# 五子棋类
# 包装了下棋函数，判断是否胜利函数以及估值函数，深度搜索估值函数。
# 下棋函数如果返回值为真则在该点下棋，否则下棋失败（被其他棋子占用）
# 每下一步棋就会更新 self.win 。如果该值不为 False 则为胜利者
# player in[1, 2]
class WZQ:
    def __init__(self, h, w):
        self.s_map = np.zeros((h,w)).astype(np.int32)


        self.h = h
        self.w = w
        self._lu = np.zeros((h,w)).astype(np.bool8)
        self._ru = np.zeros((h,w)).astype(np.bool8)
        self._area_eval = np.zeros((h,w),dtype=np.int32)
        self._scal_eval = self._create_scal(5)
        self._scal_ecal_large = self._create_scal(9)
        self.win = False

        #分值列表，如果有新加入的估值，按照分值顺序插入即可。
        self._values = OrderedDict([
            [(1,1,1,1,1),1000],#活五1000分
            [(1,0,1,1,1,0,1),400],#活四
            [(0,1,1,1,1,0),400],#活四
            [(1,1,1,1,0),100],#冲四
            [(1,1,1,0,1),100],#冲四
            [(1,1,0,1,1),100],#冲四
            [(1,0,1,1,1),100],#冲四
            [(0,1,1,1,1),100],#冲四
            [(0,1,1,1,0,0),100],#活三
            [(0,0,1,1,1,0),100],#活三
            
            #优冲三：因为这里如果被对手中间截断也能很快再生成冲三，所以分值较高
            [(0,0,0,1,1,0,1),50],#优冲三
            [(1,0,1,1,0,0,0),50],#优冲三
            [(0,0,1,0,1,0,1),30],#优眠三
            [(1,0,1,0,1,0,0),30],#优眠三
            
            #劣冲三：因为这里如果被对手截断那么在这一维就直接失去价值所以分值低
            [(0,1,1,1,0),20],#劣活三
            [(1,1,1,0,0),20],#劣冲三
            [(0,0,1,1,1),20],#劣冲三
            [(1,1,0,1,0),20],#劣冲三
            [(0,1,0,1,1),20],#劣冲三
            [(0,1,1,0,0),6],#活二
            [(0,0,1,1,0),6],#活二
            [(0,1,0,1,0),6],#活二
            [(1,0,1,0,0),2],#冲二
            [(0,0,1,0,1),2],#冲二
            [(1,1,0,0,0),2],#冲二
            [(0,0,0,1,1),2],#冲二
            
            #这里是因为考虑到边界问题, 如果对手过于靠近边界, 那么程序至少会选择能有五格空间的方向落子
            [(0,0,0,0,1),1],#一
            [(0,0,0,1,0),1],#一
            [(0,0,1,0,0),1],#一
            [(0,1,0,0,0),1],#一
            [(1,0,0,0,0),1],#一
            ])

    #米字形的矩阵生成，用于优化计算范围
    def _create_scal(self, n):
        c = int(n/2)
        v = np.zeros((n,n),dtype=np.int32)
        v[c,:],v[:,c] = 1,1
        v = np.eye(n,dtype=np.int32)|np.eye(n,dtype=np.int32)[:,::-1]|v
        return v
    
    #找到一个点所在位置的横竖斜上的所有点以及该点在其array里的坐标
    def _find_crossNslash(self, point):
        oh,ow = self.s_map.shape
        h,w = point
        self._lu = np.eye(oh,ow,w-h).astype(np.bool8)
        self._ru = np.eye(oh,ow,ow-w-1-h).astype(np.bool8)[:,::-1]
        ph,harray = w,self.s_map[h,:]
        pw,warray = h,self.s_map[:,w]    
        plu,luarray = min((h,w))        ,self.s_map[self._lu]
        pru,ruarray = min((h,ow-w-1))   ,self.s_map[self._ru]
        return [(ph,harray),(pw,warray),(plu,luarray),(pru,ruarray)]
    
    #判断胜利
    def _jug_win(self, point):
        for idx,arr in self._find_crossNslash(point):
            for i,j in groupby(arr):
                if i!=0 and len(list(j)) >= 5:
                    return i
        return False
    
    #确保当前point没有其他落子
    #确保每下一步都会更新 self.win 。
    def play_1_round(self, point, player):
        assert player in [1,2]
        if self.s_map[point] != 0:
            return False
        self.s_map[point] = player
        self._area_eval_add(point)
        self.win = self._jug_win(point)
        return True

    #根据自身修正 array 排除对手棋子的干扰
    def _revise_array(self, idx, arr, player):
        k = 3 - player
        v = np.where(arr[:idx]==k)[0]
        minx = v.max() + 1 if len(v) else 0
        ridx = idx - minx if len(v) else idx
        v = np.where(arr[idx:]==k)[0]
        maxx = v.min() + idx if len(v) else len(arr)
        return ridx,arr[minx:maxx]

    #估值算法
    def evaluate(self, point, player, _max=False):
        assert self.s_map[point] == 0 #函数只估值未下过棋的点
        self.s_map[point] = player
        core = 0
        for idx,arr in self._find_crossNslash(point):
            idx,arr = self._revise_array(idx, arr, player)
            _core_list = []
            for val in self._values:
                iidx = idx - len(val)+1 if idx - len(val)+1 > 0 else 0
                jidx = idx + 1
                _val = np.array(val) * player
                for i in range(iidx,jidx):
                    _arr = arr[i:i+len(_val)]
                    if len(_arr) == len(_val) and np.any(_arr^_val)==False:
                        _core_list.append(self._values[val])
                        break
                if len(_core_list)!= 0:
                    break
            if _max:
                core = max(core, max(_core_list) if len(_core_list) else 0)
            else:
                core += max(_core_list) if len(_core_list) else 0
        #估值结束再把 s_map 原本样子还回去
        self.s_map[point] = 0
        return core

    #需要计算估值的范围
    def _area_eval_add(self, point):
        ph,pw = point
        (u,l) = np.maximum(np.array(point)-2, 0)
        (d,r) = np.minimum(np.array(point)+3, self.s_map.shape)
        gu,gl,gd,gr = 2-(ph-u), 2-(pw-l), 2+(d-ph), 2+(r-pw)
        self._area_eval[u:d,l:r] |= self._scal_eval[gu:gd,gl:gr]

    #将估值函数包装一下，使得使用起来会更加方便
    def _calc_eval_map(self, player, _think_enemy=True, _max=False):
        self._temp1_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
        for i,j in np.vstack(np.where((self._area_eval==1)&(self.s_map==0))).transpose():
            self._temp1_eval_map[i,j] = self.evaluate((i,j),player,_max=_max)
        if _think_enemy:
            self._temp2_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
            for i,j in np.vstack(np.where((self._area_eval==1)&(self.s_map==0))).transpose():
                self._temp2_eval_map[i,j] = self.evaluate((i,j),3-player,_max=_max)
            #这里的0.8是为了防止在预测中对手权重过高过度防御导致连自己的连五都被无视
            return (self._temp1_eval_map+self._temp2_eval_map*.8)
        else:
            return self._temp1_eval_map

    #test 一层的逻辑
    #经过测试，该简单算法不能应对较为复杂的多层考虑，仅仅应用于简单难度，对新手来说该算法胜率还不错
    def robot_level1(self, player):
        v = self._calc_eval_map(player)
        v = np.vstack(np.where(v==v.max())).transpose()
        v = v[np.random.choice(range(len(v)))]
        return v

class GUI_WZQ:
    def __init__(self,h,w):
        self.master = Tk()
        self.master.title('mini_wzq')
        self.master.resizable(width=False, height=False)
        self.wzq = WZQ(h,w)
        self.h = h
        self.w = w
        self._cur_point = None

        self.v = IntVar(value=1)
        if self.v.get():
            self.player = 2
        else:
            self.player = 1
        self.enemy = 3 - self.player
        self.player_text = {1:'●',2:'〇'}
        self.player_head = {1:'黑',2:'白'}

        self.headarea = self.create_headarea()
        self.gamearea = self.create_gamearea(h,w)
        self.headarea.pack()
        self.gamearea.pack()
        self.init()
        self.master.mainloop()

    def init(self):
        if self.v.get():
            self.player = 2
        else:
            self.player = 1
        self.enemy = 3 - self.player
        self.headlabel['text'] = 'next:'+self.player_head[self.player]
        if self.player == 2:
            self.wzq.play_1_round((int(self.h/2),int(self.w/2)),self.enemy)
            exec("self.e%d_%d['text']='●'"%(int(self.h/2),int(self.w/2)))
            exec("self.e%d_%d['relief']='%s'"%(int(self.h/2),int(self.w/2),'raised'))
            self._cur_point = (int(self.h/2),int(self.w/2))

    def reset(self):
        self.wzq = WZQ(self.h,self.w)
        for i in range(self.h):
            for j in range(self.w):
                exec("self.e%d_%d['text']='  '"%(i,j))
                exec("self.e%d_%d['relief']='%s'"%(i,j,'groove'))
        self.init()

    def flash(self,i,j):
        if self.wzq.win:
            return
        if self.wzq.play_1_round((i,j),self.player):
            if self._cur_point:
                exec("self.e%d_%d['relief']='%s'"%(self._cur_point+('groove',)))
            exec("self.e%d_%d['relief']='%s'"%(i,j,'raised'))
            self._cur_point = (i,j)
            exec("self.e%d_%d['text']='%s'"%(i,j,self.player_text[self.player]))
            if self.player==1:
                self.player = 2
            elif self.player==2:
                self.player = 1
            if self.wzq.win:
                self.headlabel['text'] = 'win:'+self.player_head[self.wzq.win]
            else:
                self.headlabel['text'] = 'next:'+self.player_head[self.player]
                if self.player == self.enemy:
                    #这里的 robot_level1 是 robot 使用的简单难度算法只考虑一层
                    point = self.wzq.robot_level1(self.player).tolist()
                    self.flash(*point)
            

    def create_headarea(self):
        head = Frame(self.master)
        self.headlabel = headarea = Label(head,text='next:'+self.player_head[self.player])
        resetbot = Button(head,text='reset',font=('黑体',9),relief='groove',command=self.reset)
        robot = Checkbutton(head,text = 'robot first?',variable = self.v)
        headarea.pack(side=LEFT)
        robot.pack(side=RIGHT)
        resetbot.pack(side=RIGHT)
        return head

    def create_gamearea(self,h,w):
        gamearea = Frame(self.master)
        for i in range(h):
            for j in range(w):
                exec("self.e%d_%d = Button(gamearea,text='  ',font=('黑体',7),width=1,relief='groove',command=partial(self.flash,%d,%d))"%(i,j,i,j))
                exec("self.e%d_%d.grid(row=i,column=j,sticky=W+E+N+S)"%(i,j))
        return gamearea


if __name__ == "__main__":
    v = GUI_WZQ(15,15)
