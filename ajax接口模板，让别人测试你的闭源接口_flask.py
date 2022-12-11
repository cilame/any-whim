import base64
from urllib.parse import unquote
from flask import Flask, request
app = Flask(__name__)

str_html = r'''
<html>
<head>
<script type="text/javascript">

function formSubmit() {
  function cback(){
    try{
      document.getElementById("decode").value = xml.response;
    }catch{
      document.getElementById("decode").value = '启动接口失败';
    }
  }
  function POST(url, headers, body){
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = cback;
    xml.open('POST', url, true);
    Object.keys(headers).map((eachKey)=>{ xml.setRequestHeader(eachKey, headers[eachKey]); })
    xml.send(Object.keys(body).map((eachKey)=>{ return encodeURIComponent(eachKey) + '=' + encodeURIComponent(body[eachKey]); }).join('&'));
    return xml;
  }
  var info = document.getElementById("str_test_Interface").value
  var href = '/str_test_Interface'
  var xml = POST(href, {}, {'info':info})
}
</script>
</head>

<body>
<textarea id="str_test_Interface" size="20" style="width:1500px;height:300px"></textarea>
<br />
<button onclick="formSubmit()">提交字符串</button>
<br />
<textarea id="decode" size="20" style="width:1500px;height:300px"></textarea>
</body>
</html>
'''

file_html = r'''
<html>
<head>
<script type="text/javascript">

function formSubmit() {
  function cback(){
    try{
      document.getElementById("decode").value = xml.response;
    }catch{
      document.getElementById("decode").value = '启动接口失败';
    }
  }
  function POST(url, headers, file){
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = cback;
    xml.open('POST', url, true);
    Object.keys(headers).map((eachKey)=>{ xml.setRequestHeader(eachKey, headers[eachKey]); })
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function(e){
      xml.send(e.target.result);
    };
    return xml;
  }
  var info = document.getElementById("file_test_interface").files[0]
  var href = '/file_test_interface'
  var xml = POST(href, {}, info)
}
</script>
</head>

<body>
<form enctype='multipart/form-data' method='POST'>
    <input type="file" name="file" id="file_test_interface" />
</form>
<br />
<button onclick="formSubmit()">提交文件</button>
<br />
<textarea id="decode" size="20" style="width:1500px;height:300px"></textarea>
</body>
</html>
'''

img_html = r'''
<html>
<head>
<script type="text/javascript">

function formSubmit() {
  function cback(){
    try{
      document.getElementById("image").src = xml.response;
    }catch{
      console.log('...');
    }
  }
  function POST(url, headers, file){
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = cback;
    xml.open('POST', url, true);
    Object.keys(headers).map((eachKey)=>{ xml.setRequestHeader(eachKey, headers[eachKey]); })
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function(e){
      xml.send(e.target.result);
    };
    return xml;
  }
  var info = document.getElementById("img_test_interface").files[0]
  var href = '/img_test_interface'
  var xml = POST(href, {}, info)
}
</script>
</head>

<body>
<form enctype='multipart/form-data' method='POST'>
    <input type="file" name="file" id="img_test_interface" />
</form>
<br />
<button onclick="formSubmit()">提交图片</button>
<br />
<img id="image"></img>
</body>
</html>
'''

@app.route('/strtest')
def strtest():
    return str_html

@app.route('/filetest')
def filetest():
    return file_html

@app.route('/imgtest')
def imgtest():
    return img_html

# 以下接口，如果是文件或图片接口只需要传递二进制的 base64 编码即可。
# 如果是字符串 strinfo ，则按照右侧格式化传递字符串即可 "info={}".format(base64.b64encode(strinfo))
# 总之稍微 chrome 调试以下即知。

@app.route('/str_test_Interface', methods=['POST'])
def str_test_Interface():
    try:
        info = unquote(request.data.decode()).split('=',1)[-1]
        return info
    except:
        return "启动接口失败."

@app.route('/file_test_interface', methods=['POST'])
def file_test_interface():
    try:
        file = request.get_data().decode().split('base64,')[-1]
        filedata = base64.b64decode(file)
        # 这里返回的是字符串，通常用于解析二进制内容后返回字符串类型数据
        return '获取文件二进制成功'
    except:
        return "启动接口失败."

@app.route('/img_test_interface', methods=['POST'])
def img_test_interface():
    try:
        file = request.get_data().decode().split('base64,')[-1]
        filedata = base64.b64decode(file)
        # 这里返回图片的方式直接用 base64 这种，会更加方便
        # 通常用于返回新绘制的图片数据
        return 'data:;base64,{}'.format(base64.b64encode(filedata).decode())
    except:
        return "启动接口失败."

if __name__ == '__main__':
    app.run()