# 开发环境 python3，开发日期 20200315
# 依赖环境 pip3 install cryptography youtube-dl
# 图形界面设置有按钮，如果没有安装上面的任何一个依赖，你可以一键安装这两个第三方库，如已安装则不显示该按钮
# 直接执行即可使用，一个带有搜索和下载功能的图形化下载工具。

from urllib import request
from urllib.parse import urlencode
import os,sys,re,json,random,base64
def get_encryptor(key, iv=None):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    algoer = algorithms.AES(key)
    mode   = modes.CBC(iv)
    cipher = Cipher(algoer, mode, backend=default_backend())
    def enc(bitstring):
        padder    = padding.PKCS7(algoer.block_size).padder()
        bitstring = padder.update(bitstring) + padder.finalize()
        encryptor = cipher.encryptor()
        return encryptor.update(bitstring) + encryptor.finalize()
    def dec(bitstring):
        decryptor = cipher.decryptor()
        ddata     = decryptor.update(bitstring) + decryptor.finalize()
        unpadder  = padding.PKCS7(algoer.block_size).unpadder()
        return unpadder.update(ddata) + unpadder.finalize()
    class f:pass
    f.encrypt, f.decrypt = enc, dec
    return f
def get_postbody(realparams):
    def mk_rdkey():
        rdstring = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join([random.choice(rdstring) for i in range(16)])
    def get_params(rdkey, data):
        key  = '0CoJUm6Qyw8W8jud'.encode()
        iv   = '0102030405060708'.encode()
        edata = base64.b64encode(get_encryptor(key, iv).encrypt(data.encode())).decode()
        edata = base64.b64encode(get_encryptor(rdkey.encode(), iv).encrypt(edata.encode())).decode()
        return edata
    def get_encSecKey(rdkey):
        def parse_base2int(string):
            v = 0
            for i in range(0,len(string)):
                p = len(string) - i - 1
                t = ord(string[p]) << p*8
                v += t
            return v
        return hex(pow(parse_base2int(rdkey),65537,157794750267131502212476817800345498121872783333389747424011531025366277535262539913701806290766479189477533597854989606803194253978660329941980786072432806427833685472618792592200595694346872951301770580765135349259590167490536138082469680638514416594216629258349130257685001248172188325316586707301643237607))[2:]
    rdkey = mk_rdkey()
    params = get_params(rdkey, realparams)
    encSecKey = get_encSecKey(rdkey)
    return params, encSecKey
def mk_mp3_url_headers_body(songid):
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    realparams = '''{"encodeType": "aac", "ids": "[''' +str(songid)+ ''']", "level": "standard"}'''
    params,encSecKey = get_postbody(realparams)
    body = { "params": params, "encSecKey": encSecKey }
    return url,headers,body
def mk_search_url_headers_body(searchkey):
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    realparams = {"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":searchkey,"type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}
    params,encSecKey = get_postbody(json.dumps(realparams))
    body = { "params": params, "encSecKey": encSecKey }
    return url,headers,body
def mk_user_playlist_url_headers_body(uid):
    url = 'https://music.163.com/weapi/v6/playlist/detail'
    headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    realparams = '''{"id":"'''+str(uid)+'''","offset":"0","total":"true","limit":"1000","n":"1000","csrf_token":"6f9063dc4f9580c3122056aa52321bb4"}'''
    params, encSecKey = get_postbody(realparams)
    body = { "params": params, "encSecKey": encSecKey }
    return url,headers,body
def mypost(url, headers, body):
    r = request.Request(url, method='POST')
    for k, v in headers.items():
        if k.lower() == 'accept-encoding': continue
        r.add_header(k, v)
    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    opener = request.build_opener(request.ProxyHandler(proxies))
    return opener.open(r, data=urlencode(body).encode('utf-8')).read()
def get_playlist_by_playlistid(uid):
    url,headers,body = mk_user_playlist_url_headers_body(uid)
    jsondata = json.loads(mypost(url, headers, body))
    infos = []
    for i in jsondata['playlist']['tracks']:
        d = {}
        d["id"]   = i.get("id")
        d['name'] = '[{}]-[{}]-[{}]'.format(i.get("name"), '/'.join([i.get('name') for i in i.get("ar")]), i.get("al").get('name'))
        d['name'] = re.sub(r'[/\\:\*"<>\|\?]', '_', d['name']).strip()
        infos.append(d)
    return infos
def get_mp3_attr_by_songid(songid):
    url,headers,body = mk_mp3_url_headers_body(songid)
    return json.loads(mypost(url, headers, body))['data'][0]['url']
def get_infos_by_searchkey(searchkey):
    url,headers,body = mk_search_url_headers_body(searchkey)
    jsondata = json.loads(mypost(url, headers, body))
    infos = []
    for i in jsondata['result']['songs']:
        d = {}
        d["id"]   = i.get("id")
        d['name'] = '[{}]-[{}]-[{}]'.format(i.get("name"), '/'.join([i.get('name') for i in i.get("ar")]), i.get("al").get('name'))
        d['name'] = re.sub(r'[/\\:\*"<>\|\?]', '_', d['name']).strip()
        infos.append(d)
    return infos
# 尝试一个函数多次
def dosomething(func, *a, times=0, **kw):
    try:
        info = func(*a, **kw)
        assert info is not None
        return info
    except:
        import traceback
        print('retry:{}\n{}'.format(times, traceback.format_exc()))
        if times < 5: dosomething(func, *a, times=times+1, **kw)
        else: print('error retry times:{}'.format(times))
import tkinter
import tkinter.messagebox
from tkinter import scrolledtext
from tkinter.font import Font
t = tkinter.Tk()
ft = Font(family='Consolas',size=10)
f1 = tkinter.Frame(); f1.pack(expand=True,fill=tkinter.X)
f2 = tkinter.Frame(); f2.pack(expand=True,fill=tkinter.X)
f3 = tkinter.Frame(); f3.pack(expand=True,fill=tkinter.X)
f4 = tkinter.Frame(); f4.pack(expand=True,fill=tkinter.X)
f5 = tkinter.Frame(); f5.pack(expand=True,fill=tkinter.X)
def _show_playlist(infos):
    for i in infos:
        info = '[id]{:<13}{}'.format(i.get('id'), i.get('name'))
        lbx.insert("end", info)
    lbd['text'] = lbd['text'].split(':')[0]+':'+str(lbx.size())
def _update_listbox(func, entry):
    lbx.delete(0, tkinter.END)
    msg = entry.get().strip()
    if msg: 
        print('正在搜索'); _show_playlist(dosomething(func, msg)); print('搜索结束')
    else:
        print('请输入正确的内容')
config = {'curr': None}
def search_btn(*a):       _update_listbox(get_infos_by_searchkey, e1);     lbs['text'] = './music/default'
def get_playlist_btn(*a): _update_listbox(get_playlist_by_playlistid, e2); lbs['text'] = './music/playlistID_'+e2.get().strip()
def download_by_lbx_content(lbx_content):
    from youtube_dl import YoutubeDL
    playlist_id = lbs['text'].replace('./music/','')
    _id = re.findall(r'\[id\](\d+)', lbx_content)[0]
    _name = re.findall(r'\[id\]\d+(.*$)', lbx_content)[0].strip()
    url = dosomething(get_mp3_attr_by_songid, _id)
    localpath = os.path.dirname(os.path.realpath(sys.argv[0]))
    savepath = localpath+'/music/{}/{}.mp3'.format(playlist_id, _name)
    ytdl = YoutubeDL({'outtmpl': savepath})
    info = dosomething(ytdl.extract_info, url, download=True)
    return _id, savepath
def download_retry(download_failed):
    if len(download_failed):
        if tkinter.messagebox.askokcancel('下载', '还有没有下载完毕的歌曲，是否重试下载失败的歌曲'):
            for ls in download_failed:
                (idx, content), (_id, savepath) = ls
                download_by_lbx_content(content)
        else:
            return download_failed
    for ls in download_failed:
        (idx, content), (_id, savepath) = ls
        if os.path.isfile(savepath):
            download_failed.remove(ls)
    return download_retry(download_failed)
def download_all(*a):
    list_download = []
    for idx in range(lbx.size()):
        content = lbx.get(idx)
        list_download.append([(idx, content), download_by_lbx_content(content)])
    download_success = []
    download_failed = []
    for ls in list_download:
        (idx, content), (_id, savepath) = ls
        download_success.append(ls) if os.path.isfile(savepath) else download_failed.append(ls)
    print('列表下载，下载成功的数量:{}, 下载失败的数量:{}'.format(len(download_success), len(download_failed)))
    download_failed = download_retry(download_failed)
    for ls in download_failed:
        (idx, content), (_id, savepath) = ls
        print('下载失败歌曲：{} === {}'.format(_id, content))
def double_click(*a):
    content = lbx.get(lbx.curselection())
    download_by_lbx_content(content)
def pipinstall_all(*a):
    import os, sys
    pip3_exe = os.path.join(os.path.split(sys.executable)[0], r'Scripts', r'pip3.exe')
    libs = 'cryptography youtube-dl'
    try:    cmd = 'start powershell -NoExit "{}" install {} -i https://pypi.douban.com/simple/'.format(pip3_exe, libs); os.system(cmd)
    except: cmd = 'start cmd /k "{}" install {} -i https://pypi.douban.com/simple/'.format(pip3_exe, libs); os.system(cmd)
lb = tkinter.Label(f1,text='输入关键词点击搜索(回车)，双击需要的歌曲即可下载'); lb.pack(side=tkinter.LEFT)
e1 = tkinter.Entry(f1); e1.pack(side=tkinter.LEFT); e1.bind("<Return>", search_btn)
bt = tkinter.Button(f1,text='搜索歌曲', command=search_btn); bt.pack(side=tkinter.RIGHT)
lb = tkinter.Label(f2,text='输入歌单id点击搜索(回车)以获取歌单里面收藏的音乐'); lb.pack(side=tkinter.LEFT)
e2 = tkinter.Entry(f2); e2.pack(side=tkinter.LEFT); e2.bind("<Return>", get_playlist_btn)
bt = tkinter.Button(f2,text='搜索歌单', command=get_playlist_btn); bt.pack(side=tkinter.RIGHT)
lbd = tkinter.Label(f3,text='当前搜索到歌曲的数量:0'); lbd.pack(side=tkinter.LEFT)
__ = tkinter.Label(f3,text='保存文件夹:'); __.pack(side=tkinter.LEFT)
lbs = tkinter.Label(f3,text='./music/default'); lbs.pack(side=tkinter.LEFT)
try:
    # 检查依赖安装情况，如果已经安装则不会显示安装库的按钮
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    from youtube_dl import YoutubeDL
except:
    bt = tkinter.Button(f3,text='安装依赖库(豆瓣源)', command=pipinstall_all); bt.pack(side=tkinter.RIGHT)
bt = tkinter.Button(f3,text='下载列表中的全部歌曲', command=download_all); bt.pack(side=tkinter.RIGHT)
lbx = tkinter.Listbox(f4,width=100,height=25,font=ft); lbx.pack(expand=True,fill=tkinter.X); lbx.bind('<Double-Button-1>', double_click)
lb = tkinter.Label(f5,text='日志'); lb.pack()
tx = scrolledtext.ScrolledText(f5,height=13); tx.pack(expand=True,fill=tkinter.X)
class mystdout:
    def write(msg): tx.insert(tkinter.END, msg.rstrip()+'\n'); tx.see(tkinter.END); tx.update()
    def flush(): 
        try:tx.see(tkinter.END); tx.update()
        except:pass
sys.stdout = mystdout
t.title('网易音乐批量下载器【若下载失败多重试几次，实在下载不到的估计因为版权抹掉了】')
t.bind('<Escape>',lambda *a: t.quit())
t.mainloop()