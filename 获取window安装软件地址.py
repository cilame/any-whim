import os
import winreg
sub_key = [
    'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall', 
    'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
]
def get_install_list(key, root):
    try:
        _key = winreg.OpenKey(root, key, 0, winreg.KEY_ALL_ACCESS)
        for j in range(0, winreg.QueryInfoKey(_key)[0]-1):
            try:
                each_key = winreg.OpenKey(root, key + '\\' + winreg.EnumKey(_key, j), 0, winreg.KEY_ALL_ACCESS)
                displayname, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                install_loc, REG_SZ = winreg.QueryValueEx(each_key, 'InstallLocation')
                display_var, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayVersion')
                yield displayname, install_loc, display_var
            except WindowsError:
                pass
    except:
        pass
for key in sub_key:
    for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
        for name, local, var in get_install_list(key, root):
            print(name, local, var)