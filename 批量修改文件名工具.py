# -*- coding=utf-8 -*-

import os, re
import shutil
import tkinter
import tkinter.ttk as ttk
from tkinter import scrolledtext

Text = scrolledtext.ScrolledText
Frame = tkinter.Frame
Entry = tkinter.Entry
Button = ttk.Button
Label = ttk.Label

top = tkinter.Tk()

f0 = Frame(top)
f1 = Frame(top)
f2 = Frame(top)
f0.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)
f1.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
f2.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)


t1 = Text(f1, width=50, height=50)
t2 = Text(f2, width=50, height=50)
t1.pack(expand=True, fill=tkinter.BOTH)
t2.pack(expand=True, fill=tkinter.BOTH)

def change_func(*content):
    path = en1.get().rstrip('\\/ \n')
    if os.path.isdir(path):
        t1.delete(0., tkinter.END)
        t1.insert(0., '\n'.join(os.listdir(path)))
        if not en2.get().strip():
            en2.delete(0, tkinter.END)
            en2.insert(0, path+'_new')

def change_end():
    li1 = t1.get(0., tkinter.END).strip().splitlines()
    li2 = t2.get(0., tkinter.END).strip().splitlines()
    assert len(li1) == len(li2)
    pat1 = en1.get().strip()
    pat2 = en2.get().strip()
    if not os.path.isdir(pat2):
        os.makedirs(pat2)
    for name1, name2 in zip(li1, li2):
        pa1 = os.path.join(pat1, name1)
        pa2 = os.path.join(pat2, name2)
        print(pa1, pa2)
        shutil.copyfile(pa1, pa2)

def check_end():
    change_func()
    ex1 = en3.get()
    ex2 = en4.get()
    tx1 = t1.get(0., tkinter.END).strip()
    t2.delete(0., tkinter.END)
    t2.insert(0., re.sub(ex1, ex2, tx1))
    print('ok')

# 修改地址
f01 = Frame(f0)
f02 = Frame(f0)
f03 = Frame(f0)
f04 = Frame(f0)
f05 = Frame(f0)
f01.pack(expand=True, fill=tkinter.BOTH)
f02.pack(expand=True, fill=tkinter.BOTH)
f03.pack(expand=True, fill=tkinter.BOTH)
f04.pack(expand=True, fill=tkinter.BOTH)
f05.pack(expand=True, fill=tkinter.BOTH)

la1 = Label(f01, text='修改地址')
en1 = Entry(f01)
la1.pack(side=tkinter.LEFT)
en1.pack(expand=True, fill=tkinter.BOTH)
en1.bind('<Return>', change_func)

la2 = Label(f02, text='输出地址')
en2 = Entry(f02)
la2.pack(side=tkinter.LEFT)
en2.pack(expand=True, fill=tkinter.BOTH)

la3 = Label(f03, text='正则替换')
en3 = Entry(f03)
en4 = Entry(f03)
la3.pack(side=tkinter.LEFT)
en3.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
en4.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
bt1 = Button(f04, text='生成新的文件名列表', command=check_end)
bt1.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
bt2 = Button(f04, text='使用新的文件名修改', command=change_end)
bt2.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
en3.insert(0, '.*')
en4.insert(0, r'prefix_\g<0>')

top.mainloop()