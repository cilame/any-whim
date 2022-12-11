#静态pe文件分析python脚本
#------------------------
from struct import unpack
import time
#------------------------
class pe_checker:
    def __init__(self,strcwd=''):
        self.__strcwd = strcwd
    def __readbt(self,f,offset,lenth):
        f.seek(offset)
        return f.read(lenth)
    def __readbt2int(self,f,offset,lenth):
        f.seek(offset)
        if lenth==8:return f.read(lenth)
        if lenth==4:return unpack('i',f.read(lenth))[0]
        if lenth==2:return unpack('h',f.read(lenth))[0]
    #------------------------------
    def __check_yn(self,strs=''):
        __chkpe = 0
        if strs=='':strs = self.__strcwd
        if strs=='':return False
        with open(strs,'rb') as f:
            if self.__readbt(f,0,2)=='\x4d\x5a':__chkpe = 1
            f.seek(self.__readbt2int(f,0x3c,4))
            if f.read(4)=='\x50\x45\x00\x00':__chkpe = 2
        if __chkpe==1 or __chkpe==0:return False
        if __chkpe==2:return True
    def __vaddr2raddr(self,vaddr,strs):
        for i in self.check_info(strs,show=False):
            if vaddr>=i[2] and vaddr<=i[1]+i[2]:
                return vaddr-i[2]+i[4]
    def __readbt2str(self,f,vaddr):
        name=''
        raddr=self.__vaddr2raddr(vaddr,f.name)
        for i in range(200):
            namebt=self.__readbt(f,raddr+i,1)
            if namebt=='\x00':return name
            name+=namebt
    def __showtable(self,table):
        print ''.ljust(50)
        print 'v_func'.ljust(10),'r_func'.ljust(10),'numb'.ljust(8),'n+base'.ljust(8),'func_name'
        for a,b,c,d,e in table:
            print '0x'+hex(a).replace('0x','').rjust(8,'0'),'0x'+hex(b).replace('0x','').rjust(8,'0'),str(c).ljust(8),str(d).ljust(8),e
        print ''.ljust(50)
    def __no_exp_table(self):
        print 'no exp table'
        return False
    def __no_imp_table(self):
        print 'no imp table'
        return False
    def __no_file(self):
        print 'no file'
        return False
    #------------------------------
    def check_yn(self,strs=''):
        if self.__check_yn(strs):print 'this is pe file'
        else:print 'not pe file'
    def check_info(self,strs='',show=True):
        if strs=='':strs = self.__strcwd
        if strs=='':return self.__no_file()
        if self.__check_yn(strs)==False:return self.check_yn(strs)
        with open(strs,'rb') as f:
            m = []
            nt_rva=self.__readbt2int(f,0x3c,4)
            if show:
                print hex(self.__readbt2int(f,nt_rva+0x06,2)).ljust(10),'numb of sections'
                print hex(self.__readbt2int(f,nt_rva+0x14,2)).ljust(10),'size of option'
                print hex(self.__readbt2int(f,nt_rva+0x28,4)).ljust(10),'entry point'
                print hex(self.__readbt2int(f,nt_rva+0x38,4)).ljust(10),'section alignment'
                print hex(self.__readbt2int(f,nt_rva+0x3c,4)).ljust(10),'file alignment'
            size_opt = self.__readbt2int(f,nt_rva+0x14,2)
            numb_sec = self.__readbt2int(f,nt_rva+0x06,2)
            if show:print 'name'.ljust(8)+'v_size'.rjust(12)+'v_addr'.rjust(12)+\
               'size_raw'.rjust(12)+'point_raw'.rjust(12)
            for i in range(0,numb_sec):
                rva = nt_rva+size_opt+0x18+0x28*i
                strs = ''
                for i in range(0,5):
                    if i==0:strs+=self.__readbt2int(f,rva,8).ljust(8).replace('\x00',' ')
                    else:strs+=hex(self.__readbt2int(f,rva+(i+1)*4,4)).rjust(12)
                if show:print strs
                m.append([strs[0:8],int(strs[8:20],16),int(strs[20:32],16),int(strs[32:44],16),int(strs[44:56],16)])
            if show!=True:return m
    def check_exptable(self,strs='',show=True,showtable=True):
        if strs=='':strs = self.__strcwd
        if strs=='':return self.__no_file()
        if self.__check_yn(strs)==False:return self.check_yn(strs)
        with open(strs,'rb') as f:
            nt_rva=self.__readbt2int(f,0x3c,4)
            exp_rva=self.__readbt2int(f,nt_rva+0x78,4)
            if exp_rva==0:return self.__no_exp_table()
            exp_rva=self.__vaddr2raddr(exp_rva,strs)
            if show:
                print 'export table addr:',hex(exp_rva)
                print 'export table time:',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.__readbt2int(f,exp_rva+4,4)))
                print 'export table name:',self.__readbt2str(f,self.__readbt2int(f,exp_rva+0xc,4))
                print 'export table bass:',self.__readbt2int(f,exp_rva+0x10,4)
                print 'export table all_out:',self.__readbt2int(f,exp_rva+0x14,4)
                print 'export table name_out:',self.__readbt2int(f,exp_rva+0x18,4)
                print 'export table <v_addr_of_func>:',hex(self.__readbt2int(f,exp_rva+0x1c,4)),'  <r_addr_of_func>:',hex(self.__vaddr2raddr(self.__readbt2int(f,exp_rva+0x1c,4),strs))
                print 'export table <v_addr_of_name>:',hex(self.__readbt2int(f,exp_rva+0x20,4)),'  <r_addr_of_name>:',hex(self.__vaddr2raddr(self.__readbt2int(f,exp_rva+0x20,4),strs))
                print 'export table <v_addr_of_numb>:',hex(self.__readbt2int(f,exp_rva+0x24,4)),'  <r_addr_of_numb>:',hex(self.__vaddr2raddr(self.__readbt2int(f,exp_rva+0x24,4),strs))
            name_out = self.__readbt2int(f,exp_rva+0x18,4)
            bass = self.__readbt2int(f,exp_rva+0x10,4)
            r_addr_of_func=self.__vaddr2raddr(self.__readbt2int(f,exp_rva+0x1c,4),strs)
            r_addr_of_name=self.__vaddr2raddr(self.__readbt2int(f,exp_rva+0x20,4),strs)
            r_addr_of_numb=self.__vaddr2raddr(self.__readbt2int(f,exp_rva+0x24,4),strs)
            table = []
            for i in range(name_out):
                current = self.__readbt2int(f,r_addr_of_name+i*4,4)
                v_func = self.__readbt2int(f,r_addr_of_func+i*4,4)
                r_func = self.__vaddr2raddr(v_func,strs)
                numb = self.__readbt2int(f,r_addr_of_numb+i*2,2)
                name = self.__readbt2str(f,current)
                table.append([v_func,r_func,numb,numb+bass,name])
            if showtable:self.__showtable(table)
            return table
    def check_imptable(self,strs='',show=True,showtable=True):
        if strs=='':strs = self.__strcwd
        if strs=='':return self.__no_file()
        if self.__check_yn(strs)==False:return self.check_yn(strs)
        with open(strs,'rb') as f:
            nt_rva=self.__readbt2int(f,0x3c,4)
            imp_rva=self.__readbt2int(f,nt_rva+0x80,4)
            if imp_rva==0:return self.__no_exp_table()
            imp_rva=self.__vaddr2raddr(imp_rva,strs)
            if show:print 'export table rva:',hex(imp_rva)
            iid = []
            for i in range(10000):
                table = self.__readbt(f,imp_rva+i*20,20)
                if table == '\x00'*20:break
                iid.append(table)
            if showtable:
                show=False
                for i in iid:
                    print self.__readbt2str(f,unpack('i',i[12:16])[0])
                    org_fst_chunk = self.__vaddr2raddr(unpack('i',i[0:4])[0],strs)
                    for j in range(10000):
                        chunk = self.__readbt2int(f,org_fst_chunk+j*4,4)
                        if chunk<0:
                            print 'this func seek by func_numb',~chunk^0x7fffffff
                            continue
                        if chunk == 0:break
                        print hex(self.__readbt2int(f,chunk,2)).replace('0x','').rjust(4,'0').rjust(5),self.__readbt2str(f,chunk+2)
                    print
            if show:
                for i in iid:
                    print self.__readbt2str(f,unpack('i',i[12:16])[0])
            return iid

if __name__ == '__main__':
    x = pe_checker('KernelBase.dll')
    x.check_info()
    #x.check_exptable()
    #x.check_imptable()
    


        
    
