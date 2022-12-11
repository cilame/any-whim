配置好Python3.6和pip3
安装EPEL和IUS软件源

```bash
# 旧的下载链接
# https://centos7.iuscommunity.org/ius-release.rpm
# 最新的下载链接
# https://repo.ius.io/ius-release-el7.rpm

# 这里是多行处理(不覆盖原来python2的python和pip名字，以python3,pip3使用python3)
# 安装 python36u-devel 是为了处理某些安装异常，例如 twisted。
yum install epel-release -y
yum install https://repo.ius.io/ius-release-el7.rpm -y
yum install python36u -y
yum install python36u-pip -y
yum install gcc -y
yum install python36u-devel -y
ln -s /bin/python3.6 /bin/python3
ln -s /bin/pip3.6 /bin/pip3

# 用python3覆盖原python和pip名字（强烈不建议覆盖，因为yum工具使用的是py2，所以修改后会导致yum使用异常）
# rm -f /bin/python ; rm -f /bin/pip ; ln -s /bin/python3 /bin/python; ln -s /bin/pip3 /bin/pip

# 关于ss
# pip3 install shadowsocks ; systemctl stop firewalld.service ; systemctl disable firewalld.service
# ssserver -p 6666 -k vilame -d start

# 关于连接ss端口进行下载
# sslocal -s xxx.xxx.xxx.xxx -p 6666 -b 127.0.0.1 -l 1080 -k vilame -d start
# you-get -s 127.0.0.1:1080 --skip-existing-file-size-check url1,url2,url3...
# youtube-dl --proxy socks5://127.0.0.1:1080/ url1,url2,url3...
```

安装ffmpeg

```bash
# centos7
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
sudo yum install ffmpeg ffmpeg-devel -y

# centos6
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el6/x86_64/nux-dextop-release-0-2.el6.nux.noarch.rpm
sudo yum install ffmpeg ffmpeg-devel -y
```

使用squid安装http代理

```bash
# 无密码
yum install squid -y
# 在配置文件 /etc/squid/squid.conf 的 http_access deny all 之前写入下面内容
http_access allow all
http_port 6666
# 命令行启动，和开机启动
systemctl start squid
systemctl enable squid
# 请求时候需要使用 http://xxx.xxx.xxx.xxx:1234 这样的结构来请求

# 带密码
yum install squid -y
yum install httpd-tools -y
mkdir /etc/squid/ ; htpasswd -bc /etc/squid/passwords uname pword
# 用 which ncsa_auth 命令找到该工具的地址，配合上面的密码存储地址使用
# 在配置文件 /etc/squid/squid.conf 中的 http_access deny all 之前写入下面的内容（包括配置端口）
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwords
acl auth_user proxy_auth REQUIRED
http_access allow auth_user
http_access allow all
http_port 6666
# 再在命令行内键入如下命令启动服务，开机启动
systemctl start squid
systemctl enable squid
# 后续请注意例如阿里云之类的端口需要在账户的防火墙策略内打开。
# 请求时候需要使用 http://uname:pword@xxx.xxx.xxx.xxx:1234 这样的结构来请求
```

centos7安装chrome以及chromedriver环境使用selenium

```bash
yum -y install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
yum -y install unzip
wget http://chromedriver.storage.googleapis.com/70.0.3538.16/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm -f chromedriver_linux64.zip

# 注意，当你使用 selenium 的时候记得添加一些参数，网上说是下面三个
# 但是经过测试至少需要添加前两个参数才能正常运行，chromedriver 的测试版本为 70.0.3538.16。
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
```