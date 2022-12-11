##   ___   ___   ___ _ __ _   __ ___
##  / o | / _/ ,' _//// // \,' // _/
## /  ,' / _/ _\ `./ U // \,' // _/ 
##/_/`_\/___//___,'\_,'/_/ /_//___/        <zhoulin>
##/---------------\---------------------/-----------\
##|%%%%%/----------------------------\//|   -----   |
##|%%%%%|  Sat Dec 10 16:16:31 2016  |//|  / _ _ \  |
##|%%%%%\----------------------------///| (| @ @ |) |
##|%%%%%%%%%%%%/-------------\//////////|  |  .  |  |
##|%%%/--------| zhoulin     |----------|  \  _  /  |
##|%%%| name:  | 24          |b51k{VX/(j|   \ _ /   |
##|%%%| age:   | male        |9M;`().#sZ|  /\ _ /\  |
##\---| gender:| guiyang     |5m*%U1T9Xm\-----------/
##|///| from:  | 186-------- |Nccfz\)-)o11np}:|////|
##|///| phone: \-------------/IBiWBoT/----------------\
##|///\-----------////|FO7ey+![vH\2=)| <prosperous>   |
##/--------------\////|+/----------\)| <democratic>   |
##| College,Pro: |////|I|  -+--+-  |z| <civilized>    |
##\--------------/------|   /___   |w| <harmonious>   |
##|////|  Shaoxing      |  / _  |  |e| <freedom>      |
##|////|  University    |   [_] |  |-| <equality>     |
##|////|  (zhejiang)    |    __/   |/| <justice>      |
##|////|  Machinery     \----------/-| <legal system> |-----\
##|/---------------\      |Oh/"yX;<=J| <patriotism>   |`)_$I|
##|| Hobby,WeChat: |-------\+,oiIW"wH| <dedication>   |.*%G5|
##|\---------------/       |T/-------| <integrity>    |--\Zf|
##|/////|  Literature      |4|%%%%%%%| <kindness>     |%%|2,|
##|/////|  Poetry          |^|%%%%%%%\----------------/%%|Z;|
##|/////|  Computer(now)   |V|%%%/-----------------------------\
##|/////|  vilame          |J|%%%| talk smile wind sound       |
##|//---------------\-------\|%%%\-----------------------------/
##|/| Computer Edu: |       ||%%%/-----------------------------\
##|/\---------------/ Self- ||%%%| people born through check   |
##|//////|  study computer  ||%%%\-----------------------------/
##|//////|  for almost      ||%%%/-----------------------------\
##|//////|  a year          ||%%%| 2473495041@qq.com           |
##/------\--------/----------\%%%\--------------/------\-------/
##|  /\  |//////--| Ex work: |-----------\%%%%%%|  /\  |%|+o|
##| /--\ |/////|  \----------/           |------| /--\ |-/;<|
##|/|/\|\|/////|  [0],Copy editor        |xx\99a|/|/\|\|Sk;_|
##|\|\/|/|/////|  [1],Video review       |f.op}L|\|\/|/|1R>$|
##| \--/ |/////|  [2],The Writer         |------| \--/ |----/
##|  \/  |/////|  [3],Seller             |//////|  \/  |
##\------/-----\-------------------------/------\------/


#一个简单的字符表格框架，实现覆盖功能，效果如上，F5运行
#--------------------------------
import re,time,random,string
#--------------------------------
class frame:
    __fram = []
    __in_fram = []
    __real_fram = []
    over_mod = False
    ignore_lenth = False
    def __init__(self,lenth,width):
        self.lenth = lenth
        self.width = width
        self.__fram = [self.lenth,self.width]
        self.make_fram_original(self.__fram)
    def insert_fram(self,x,y,lenth,width,strs=''):
        if self.ignore_lenth:pass
        else:
            if lenth+x > self.lenth:
                print('some fram lenth must be overflow')
                return False
        if width+y > self.width:
            print('some fram width must be overflow')
            return False
        if type(strs)==str:strs_in = self.box_inner_deal(strs,[x,y,lenth,width])
        if isinstance(strs, (list, map)):strs_in = [i[:lenth] for i in strs]
        self.__in_fram.append([[x,y,lenth,width],strs_in])
    def make_fram_original(self,fram):
        self.__real_fram.append('/'+'-'*(fram[0]-2)+'\\')
        for i in range(fram[1]-2):
            self.__real_fram.append('|'+' '*(fram[0]-2)+'|')
        self.__real_fram.append('\\'+'-'*(fram[0]-2)+'/')
    def make_fram_insert(self,fram,strs=[]):
        self.__real_fram[fram[1]]=self.change_box(self.__real_fram[fram[1]],fram[0],fram[2],0)
        if strs==[]:
            for i in range(fram[1]+1,fram[1]+fram[3]+1):
                self.__real_fram[i]=self.change_box(self.__real_fram[i],fram[0],fram[2],1,self.over_mod)
        else:
            for i in range(fram[1]+1,fram[1]+fram[3]+1):
                if len(strs)>=i-fram[1]:strs_in=strs[i-fram[1]-1]
                else:strs_in=''
                self.__real_fram[i]=self.change_box(self.__real_fram[i],fram[0],fram[2],1,self.over_mod,strs=strs_in)
        self.__real_fram[fram[1]+fram[3]+1]=self.change_box(self.__real_fram[fram[1]+fram[3]+1],fram[0],fram[2],2)
    def make_frams(self):
        for i,j in self.__in_fram:
            self.make_fram_insert(i,j)
    def change_box(self,a,x,lenth,top=0,over_mod=False,strs=''):
        inner='-'*(lenth)
        if top==0:
            tenon=['/','\\']
        if top==1:
            tenon=['|','|']
            inner=a[x+1:lenth+x+1]
            if over_mod:inner=' '*lenth
            if strs!='':inner=strs.ljust(lenth)
        if top==2:
            tenon=['\\','/']
        if x!=0:return a[:x]+tenon[0]+inner+tenon[1]+a[x+lenth+2:]
        else:return tenon[0]+inner+tenon[1]+a[lenth+2:]
    def box_inner_deal(self,strs,size):
        str_list = re.findall('.{'+str(size[2])+'}|.+',strs)
        if len(str_list)>size[3]:
            print('some string must be too long')
            return []
        return str_list
    def show_fram(self):
        for i in self.__real_fram:
            print(i)
#--------------------------------
def random_len(lens):
    strs = ''
    for i in range(lens):strs+=random.choice(string.printable[:-6])
    return strs
#--------------------------------
label = ['name:','age:','gender:','from:','phone:']
info = ['zhoulin','24','male','guiyang','186--------']
face = ['-----','/ _ _ \\','(| @ @ |)','|  .  |','\\  _  /','\\ _ /','/\\ _ /\\']
sign = ['/\\', '/--\\', '/|/\\|\\', '\\|\\/|/', '\\--/', '\\/']
resume = ['   ___   ___   ___ _ __ _   __ ___','  / o | / _/ ,\' _//// // \,\' // _/',
' /  ,\' / _/ _\ `./ U // \,\' // _/ ','/_/`_\/___//___,\'\\_,\'/_/ /_//___/ ']
livewith = ['prosperous','democratic','civilized','harmonious','freedom','equality','justice','legal system','patriotism','dedication','integrity','kindness']
oldman = ['-+--+-',' /___ ','/ _  |',' [_] |','  __/ ']
cp = ['Shaoxing','University','(zhejiang)','Machinery']
hw = ['','Literature','Poetry','Computer(now)','vilame']
ce = ['','          Self-','study computer','for almost','a year']
ew = ['','[0],Copy editor','[1],Video review','[2],The Writer','[3],Seller']
#--------------------------------
if __name__ == "__main__":
    for i in resume[:-1]:
        print(i)
    print(resume[-1]+' '*(50-len(resume[-1])-len('<zhoulin>'))+'<zhoulin>')
    x = frame(50,40)
    x.ignore_lenth=True
    x.over_mod=True
    x.insert_fram(0,0,48,38,'/'*48*38)
    x.insert_fram(20,5,23,10,random_len(23*10))
    x.insert_fram(0,0,15,7,'%'*15*7)
    x.insert_fram(19,18,38,18,random_len(38*18))
    x.insert_fram(27,21,27,12,'%'*27*12)
    x.insert_fram(4,5,11,5,map(lambda i:' '+i,label))
    x.insert_fram(13,4,13,5,map(lambda i:' '+i,info))
    x.insert_fram(5,14,18,5,['  '+i for i in cp])
    x.insert_fram(6,20,18,5,['  '+i for i in hw])
    x.insert_fram(7,26,18,5,['  '+i for i in ce])
    x.insert_fram(13,33,25,5,['  '+i for i in ew])
    x.insert_fram(0,12,14,1,' College,Pro:')
    x.insert_fram(1,19,15,1,' Hobby,WeChat:')
    x.insert_fram(2,26,15,1,' Computer Edu:')
    x.insert_fram(16,32,10,1,' Ex work:')
    x.insert_fram(35,10,16,12,[' <'+i+'>' for i in livewith])
    x.insert_fram(31,24,29,1,' talk smile wind sound'.ljust(29))
    x.insert_fram(31,27,29,1,' people born through check'.ljust(29))
    x.insert_fram(31,30,29,1,' 2473495041@qq.com'.ljust(29))
    x.insert_fram(6,1,28,1,str(time.asctime()).center(28))
    x.insert_fram(38,0,11,7,[i.center(11) for i in face])
    x.insert_fram(46,32,6,6,[i.center(6) for i in sign])
    x.insert_fram(0,32,6,6,[i.center(6) for i in sign])
    x.insert_fram(22,12,10,5,[i.center(10) for i in oldman])
    x.make_frams()
    x.show_fram()
