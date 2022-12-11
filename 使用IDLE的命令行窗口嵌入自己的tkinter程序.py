import sys
import tkinter


root = tkinter.Tk()
fr = tkinter.Frame(root)
fr.pack()




import tkinter
import idlelib.pyshell
import idlelib.window
idlelib.window.ListedToplevel = lambda *a,**k: tkinter._default_root # 这里 root 就是全局的根窗口
def codeline_shell():
    idlelib.pyshell.use_subprocess = True
    flist = idlelib.pyshell.PyShellFileList(root)
    PyShell = idlelib.pyshell.PyShell
    _bak_write, FLAG_LOCAL = PyShell.write, True
    def _write(self, s, tags=()):
        nonlocal FLAG_LOCAL
        if s == "Python %s on %s\n%s\n%s" % (sys.version, sys.platform, PyShell.COPYRIGHT, '') and FLAG_LOCAL:
            s = '用钩子钩住最开始初始输出的内容一次，用来显示自己的内容'
            FLAG_LOCAL = False
        # 所有的执行结果都会经过这个函数，如果想要让执行结果在别的地方输出，可以很简单在这里挂钩
        # 这里的 s 就是执行结果的字符串
        return _bak_write(self, s, tags=tags)
    PyShell.write = _write
    shell = flist.open_shell()
    shell.text_frame.pack_forget() # 取消默认的 pack设置
    shell.status_bar.pack_forget() # 取消显示行列信息
    return shell
shell = codeline_shell()
fr = shell.text_frame
# 这里的 fr 就是idle自带的命令行窗口，可以将这个窗口随便集成在任何其他地方
# fr 的 master 默认是 root，所以如果需要将这个 frame 放在别的 frame 内部则需要修改 master
# fr.master = another_frame
fr.pack()




mycode = '''
s = 123123
'''
mycode2 = 'print(s)'
def run(*a):
    # 提交执行函数给命令行执行，每次执行之后一定要将执行的状态的参数设置回 False
    shell.interp.runsource(mycode)
    shell.interp.tkconsole.executing = False
    shell.interp.runsource(mycode2)
    shell.interp.tkconsole.executing = False
btn = tkinter.Button(fr, text='测试一下', command=run)
btn.pack()
root.mainloop()