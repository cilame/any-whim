import re, os
import urllib.parse

appdatapath = os.environ['APPDATA'] or os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
pippath = os.path.join(appdatapath, 'pip')
pipfile = os.path.join(pippath, 'pip.ini')
if not os.path.isdir(pippath):
    os.mkdir(pippath)

diclist = [
    ['http://pypi.douban.com/simple/', '豆瓣'],
    ['http://mirrors.aliyun.com/pypi/simple/', '阿里云'],
    ['http://pypi.tuna.tsinghua.edu.cn/simple/', '清华大学'],
    ['http://pypi.mirrors.ustc.edu.cn/simple/', '中国科学技术大学'],
]
dic_url2name = {}
dic_name2url = {}
for k,v in diclist:
    dic_url2name[k] = v
    dic_name2url[v] = k

def read_setting():
    if not os.path.isfile(pipfile):
        return None
    else:
        with open(pipfile) as f:
            setstr = f.read()
        mirrors = re.findall('\nmirrors = ([^\n]+)', setstr)[0]
        return dic_url2name.get(mirrors)

def write_setting(name=None):
    setting = '''[global]\nindex-url = {}\n[install]\nuse-mirrors = true\nmirrors = {}\ntrusted-host = {}'''.strip()
    if name is None:
        if os.path.isfile(pipfile):
            os.remove(pipfile)
        return
    if name not in dic_name2url:
        raise Exception("{} must in {}".format(name, list(dic_name2url)))
    mirrors = dic_name2url.get(name)
    index_url = mirrors.strip(' /')
    trusted_host = urllib.parse.urlsplit(index_url).netloc
    with open(pipfile, 'w') as f:
        f.write(setting.format(index_url, mirrors, trusted_host))

if __name__ == '__main__':
    write_setting('豆瓣')
    v = read_setting()
    print(v)