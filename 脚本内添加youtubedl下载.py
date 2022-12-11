url = 'https://www.bilibili.com/video/av42557280?from=search&seid=10441521160359990716'
url = 'https://v.youku.com/v_show/id_XNDM0MjM1MzMyNA==.html'

from youtube_dl import YoutubeDL
ytdl = YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
info = ytdl.extract_info(url, download=False)

size = info['filesize']/2**20 # 单位兆
fsize = '{:>.2f}'.format(size).rstrip('0') + ' M'
print(fsize)
if size < 20:
    info = ytdl.extract_info(url, download=True)
    print(info)