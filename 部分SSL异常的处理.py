# 当服务器过旧的时候可能会出现一些密钥策略的问题。
# 出现 SSL 的异常，不太了解怎么回事，不过针对不同的语言用下面的方法就能解决。


# 【scrapy】
# 异常：
# Traceback (most recent call last):
#   File "d:\python\python36\lib\site-packages\scrapy\core\downloader\middleware.py", line 43, in process_request
#     defer.returnValue((yield download_func(request=request,spider=spider)))
# twisted.web._newclient.ResponseNeverReceived: [<twisted.python.failure.Failure OpenSSL.SSL.Error: [('SSL routines', 'tls_process_ske_dhe', 'dh key too small')]>]
# 解决方法：增加以下代码即可
from twisted.internet.ssl import AcceptableCiphers
from scrapy.core.downloader import contextfactory
contextfactory.DEFAULT_CIPHERS = AcceptableCiphers.fromOpenSSLCipherString('DEFAULT:!DH')


# 【requests】
# 异常：
# requests.exceptions.SSLError: HTTPSConnectionPool(host='www.ispl.cn', port=443): Max retries exceeded with url: /ispl/servlet/ProductList_Public?tmp=1&valid=1&pageIndex=1 (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 'tls_process_ske_dhe', 'dh key too small')],)",),))
# 解决方法：增加以下代码即可
try:
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


# 【urllib】
# 异常：
# urllib.error.URLError: <urlopen error [SSL: SSL_NEGATIVE_LENGTH] dh key too small (_ssl.c:847)>
# 解决方法：增加以下代码
import ssl
ssl._DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'