# -*- coding: utf-8 -*-
from tkinter import *
from win32service import *

def hook_dropfiles(hwnd,func=lambda i:print(i)):
    import ctypes
    from ctypes.wintypes import DWORD
    prototype = ctypes.WINFUNCTYPE(DWORD,DWORD,DWORD,DWORD,DWORD)
    WM_DROPFILES = 0x233
    GWL_WNDPROC = -4

    def py_drop_func(hwnd,msg,wp,lp):
        if msg == WM_DROPFILES:
            count = ctypes.windll.shell32.DragQueryFile(wp,-1,None,None)
            szFile = ctypes.c_buffer(260)
            for i in range(count):
                ctypes.windll.shell32.DragQueryFile(wp,i,szFile,ctypes.sizeof(szFile))
                dropname = szFile.value
                func(dropname)
            ctypes.windll.shell32.DragFinish(wp)
        return ctypes.windll.user32.CallWindowProcW(org_wndproc,hwnd,msg,wp,lp)

    global org_wndproc,new_wndproc
    org_wndproc = None
    new_wndproc = prototype(py_drop_func)

    ctypes.windll.shell32.DragAcceptFiles(hwnd,True)
    org_wndproc = ctypes.windll.user32.GetWindowLongW(hwnd,GWL_WNDPROC)
    ctypes.windll.user32.SetWindowLongW(hwnd,GWL_WNDPROC,new_wndproc)


class MyServiceInstaller:
    def __init__(self):
        self.master = Tk()
        self.master.resizable(False,False)
        self.master.title(u'驱动加载(支持拖拽)')
        self.label = Label(self.master,text="welcome")
        self.entry = Entry(self.master)
        self.width = 60    
        self.label.pack(fill=X)
        self.entry.pack(fill=X)
        self.tk_install   = Button(self.master,command=self.install      ,text = u"安装")
        self.tk_starts    = Button(self.master,command=self.starts       ,text = u"启动")
        self.tk_stops     = Button(self.master,command=self.stops        ,text = u"停止")
        self.tk_uninstall = Button(self.master,command=self.uninstall    ,text = u"卸载")
        self.tk_close     = Button(self.master,command=self.master.quit  ,text = u"关闭")
        self.tk_install.pack  (side=LEFT)
        self.tk_starts.pack   (side=LEFT)
        self.tk_stops.pack    (side=LEFT)
        self.tk_uninstall.pack(side=LEFT)
        self.tk_close.pack    (side=LEFT)
        self.label['width']          = self.width
        self.entry['width']          = self.width
        self.tk_install['width']     = int(self.width/5)
        self.tk_starts['width']      = int(self.width/5)
        self.tk_stops['width']       = int(self.width/5)
        self.tk_uninstall['width']   = int(self.width/5)
        self.tk_close['width']       = int(self.width/5)
        self.scm = OpenSCManager(None,None,SC_MANAGER_ALL_ACCESS)
        self.service_handle = None
        hook_dropfiles(self.entry.winfo_id(),self.func)
        mainloop()

    def func(self,bstr):
        try:
            p = bstr.decode('gbk')
        except:
            p = bstr.decode('utf-8')
        self.entry.delete(0,END)
        self.entry.insert(0,p)
        

    def fullpathname(self):
        return self.entry.get()
    def name(self):
        if self.fullpathname().strip()=='':return ''
        else:return self.fullpathname().rsplit('\\',1)[1].rsplit('.')[0]
    

    def install(self):
        name = self.name()
        fullpathname = self.fullpathname()
        try:
            self.service_handle = CreateService( self.scm,
                                  name, #驱动程序的在注册表中的名字    
                                  name, # 注册表驱动程序的 DisplayName 值    
                                  SERVICE_ALL_ACCESS, # 加载驱动程序的访问权限    
                                  SERVICE_KERNEL_DRIVER,# 表示加载的服务是驱动程序    
                                  SERVICE_DEMAND_START, # 注册表驱动程序的 Start 值    
                                  SERVICE_ERROR_IGNORE, # 注册表驱动程序的 ErrorControl 值    
                                  fullpathname, # *****注册表驱动程序的 ImagePath 值*****
                                  None,    
                                  0,    
                                  None,    
                                  None,    
                                  None)
            self.label['text'] = 'install ok'
        except:
            try:
                self.service_handle = OpenService(self.scm,name,SERVICE_ALL_ACCESS)
                self.label['text'] = 'install ok'
            except:
                self.service_handle = None
                self.label['text'] = 'install failed, pls check filepath'

    def starts(self):
        if self.service_handle != None:
            try:
                StartService(self.service_handle,None)
                self.label['text'] = 'starts ok'
            except:
                self.label['text'] = 'start failed, maybe it already start.'
        else:
            self.label['text'] = 'None service handle.'

    def stops(self):
        if self.service_handle != None:
            try:
                ControlService(self.service_handle,SERVICE_CONTROL_STOP)
                self.label['text'] = 'stops ok'
            except:
                self.label['text'] = 'stop failed, maybe it already stop.'
        else:
            self.label['text'] = 'None service handle.'
        
    def uninstall(self):
        if self.service_handle != None:
            try:
                DeleteService(self.service_handle)
                CloseServiceHandle(self.service_handle)
                self.service_handle = None
                self.label['text'] = 'uninstall ok'
            except:
                self.label['text'] = 'uninstall failed, maybe it already uninstall.'
        else:
            self.label['text'] = 'None service handle.'
        

if __name__ == '__main__':
    MyServiceInstaller()
    
    
