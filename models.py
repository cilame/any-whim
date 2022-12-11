#coding=utf-8
import tkinter
import tkinter.ttk as ttk
import os
import requests
import zipfile
import idlelib
import threading
import shutil

def run_in_idle():
    filepath = globals().get("filepath")
    _pythonw = os.path.join(idlelib.__file__.split('lib',1)[0],'pythonw.exe')
    _idlepyw = os.path.join(idlelib.__file__.rsplit('\\',1)[0],'idle.pyw')
    cmd = [_pythonw,_idlepyw]
    if filepath:
        tarpath = './models/__temp__/' + filepath.rsplit('/',1)[1]
        shutil.copy(filepath,tarpath)
        cmd.append(tarpath)
        os.popen(' '.join(cmd))
    else:
        os.popen(' '.join(cmd))

def download_models():
    if not os.path.isdir('./models') or\
       not os.path.isfile('./models/models.ini'):
        print('not have ini file: ./models/models.ini')
        return
    download['text'] = '正在下载...'
    url = open('./models/models.ini').read().split('=',1)[1].strip()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)'}
    r = requests.get(url,headers=headers)
    filename = url.rsplit('/',1)[1]
    with open(filename,'wb') as f:
        f.write(r.content)
    try:
        zip_file = zipfile.ZipFile(filename)
        for names in zip_file.namelist():
            zip_file.extract(names,"./models")
        zip_file.close()
        os.remove(filename)
    finally:
        download['text'] = '模板下载'
        load_local_file_tree('./models',tree)

def download_models_thread():
    t = threading.Thread(target=download_models) 
    t.setDaemon(True) 
    t.start()

def load_local_file_tree(local_dir,tree,local_node=None):
    next_nodes = []
    for idx,i in enumerate(os.listdir(local_dir)):
        if (i == 'models.ini' or i == "__temp__") and not local_node:
            continue
        abs_path = '/'.join([local_dir,i])
        next_node = local_node if local_node else ""
        if os.path.isdir(abs_path):
            node = tree.insert(next_node,idx,text=i)
            next_nodes.append((abs_path,node))
        elif os.path.isfile(abs_path):
            tree.insert(next_node,idx,text=i,values=abs_path)
    for abs_path,node in next_nodes:
        load_local_file_tree(abs_path,tree,node)


def show_code(filepath):
    size = os.path.getsize(filepath)
    text.delete(0.,"end")
    if size < 5*2**20:
        for idx,i in enumerate(open(filepath,encoding="utf-8").readlines()):
            text.insert(tkinter.END,i)
    else:
        text.insert(0.,"file is too large. (codefile size limit: 5M).")

def tree_on_select(event):
    items = tree.selection()
    if len(items) != 1:
        print (items)
        return
    else:
        global filepath
        filepath = ' '.join(tree.item(items[0],"values"))
        if filepath:
            print(filepath)
            show_code(filepath)

def init():
    if not os.path.isdir('./models'): os.mkdir('./models')
    if not os.path.isdir('./models/__temp__'): os.mkdir('./models/__temp__')
    if not os.path.isfile('./models/models.ini'):
        with open('./models/models.ini','w') as f:
            f.write("url = https://github.com/cilame/samples/archive/master.zip")

if __name__ == "__main__":
    init()
    tk = tkinter.Tk()
    tree = ttk.Treeview(tk)
    text = tkinter.Text(tk,width=80)
    button = tkinter.Button(tk,text="用idle打开\n附件",command=run_in_idle)
    download  = tkinter.Button(tk,text="下载",command=download_models_thread)
    tree.pack(side="left",fill="both")
    text.pack(side="left",fill="both")
    button.pack(side="top",fill="x")
    download.pack(side="top",fill="x")
    tree.bind("<<TreeviewSelect>>", tree_on_select)
    load_local_file_tree('./models',tree)
    tk.mainloop()
