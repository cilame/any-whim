# 创建windows快捷方式，无需依赖。

def creat_windows_shortcut():
    # 创建 windows 的桌面快捷方式。
    import os
    import sys
    import shutil
    import tempfile
    vbsscript = '''
set WshShell = WScript.CreateObject("WScript.Shell" )
set oShellLink = WshShell.CreateShortcut(Wscript.Arguments.Named("shortcut") & ".lnk")
oShellLink.TargetPath = Wscript.Arguments.Named("target")
oShellLink.IconLocation = Wscript.Arguments.Named("icon")
oShellLink.WindowStyle = 1
oShellLink.Save
    '''.strip()

    s = tempfile.mkdtemp()
    try:
        vbs = os.path.join(s, 'temp.vbs')
        with open(vbs, 'w', encoding='utf-8') as f:
            f.write(vbsscript)

        # 目前我使用的exe位置
        exe  = os.path.join(os.path.split(sys.executable)[0], r'Scripts', 'vv.exe')
        # 需要绑定的图标位置
        icon = os.path.join(os.path.split(sys.executable)[0], r'Lib\site-packages\vrequest', 'ico.ico')
        # 生成的链接位置（通常是左面，这里只需要修改名字即可）
        link = os.path.join(os.path.expanduser("~"),'Desktop','vrequest')

        if os.path.isfile(link + '.lnk'):
            import tkinter
            import tkinter.messagebox
            top = tkinter.Tk()
            top.withdraw()
            tkinter.messagebox.showinfo('Error','快捷方式已存在，如需重新生成，请删除现有的桌面快捷方式。')
            return

        cmd = r'''
        {} /target:{} /shortcut:"{}" /icon:{}
        '''.format(vbs, exe, link, icon).strip()
        print(cmd)
        v = os.popen(cmd)
        v.read()
        v.close()
    finally:
        import traceback;
        if traceback.format_exc().strip() != 'NoneType: None':
            print('create shortcut failed.')
            traceback.print_exc()
        shutil.rmtree(s)

creat_windows_shortcut()