import tkinter


root = tkinter.Tk()

code = tkinter.Text(root)
code.pack()

mycode = '''
import re
import time
import requests

def some(a,b,c):
    print(a,b,c)

some(123,321,333)

v = re.findall('\d+','asdf909080asdf8908asdf980890asdf')
print(v)
v = requests.get('http://www.baidu.com')
print(v)

# for i in range(10):
#     time.sleep(.5)
#     print(i)
'''
code.insert(0.,mycode)


# ==== 使用 idlelib 自带的语法高亮 ====
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
d = ColorDelegator()
Percolator(code).insertfilter(d)



mlog = tkinter.Text(root)
mlog.pack()
mlog.insert(0.,mycode)

highlight_style = {
    'COMMENT': {
        'foreground': '#0000dd',
        'background': '#ffffff'
    },
    'KEYWORD': {
        'foreground': '#ff77dd',
        'background': '#ffffff'
    },
    'BUILTIN': {
        'foreground': '#00dd90',
        'background': '#ffffff'
    },
    'STRING': {
        'foreground': '#00aadd',
        'background': '#ffffff'
    },
    'DEFINITION': {
        'foreground': '#dd00ff',
        'background': '#ffffff'
    },
    'SYNC': {
        'background': None,
        'foreground': None
    },
    'TODO': {
        'background': None,
        'foreground': None
    },
    'ERROR': {
        'foreground': '#000000',
        'background': '#ff7777'
    },
    'hit': {
        'foreground': '#ffffff',
        'background': '#000000'
    }
}


# ==== 使用 idlelib 自带的语法高亮 ====
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
d = ColorDelegator()
d.tagdefs = highlight_style
Percolator(mlog).insertfilter(d)

root.mainloop()
