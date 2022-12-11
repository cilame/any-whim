def extractall(self, path=None, members=None, pwd=None):
    if members is None: members = self.namelist()
    path = os.getcwd() if path is None else os.fspath(path)
    for zipinfo in members:
        try:    _zipinfo = zipinfo.encode('cp437').decode('gbk')
        except: _zipinfo = zipinfo.encode('utf-8').decode('utf-8')
        if _zipinfo.endswith('/') or _zipinfo.endswith('\\'):
            myp = os.path.join(path, _zipinfo)
            if not os.path.isdir(myp):
                os.makedirs(myp)
        else:
            myp = os.path.join(path, _zipinfo)
            youp = os.path.join(path, zipinfo)
            self.extract(zipinfo, path)
            os.rename(youp, myp)

import zipfile
zipfile.ZipFile.extractall = extractall


zfile = 'zip文件地址.zip'
with zipfile.ZipFile(zfile) as zip_ref:
    zip_ref.extractall(zfile.replace(".zip",""))