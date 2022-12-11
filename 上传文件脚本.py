# coding=utf8
import base64
from flask import Flask, request
app = Flask(__name__)

file_html = r'''
<html>
<head>
<script type="text/javascript">

function formSubmit() {
  function cback(){
    try{
      document.getElementById("decode").value = xml.response;
    }catch{
      document.getElementById("decode").value = '正在传输数据，请等待';
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
  var v = document.getElementById("file_test_interface").value;
  var href = '/file_test_interface?filename=' + v.substring(v.lastIndexOf("\\")+1);
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

@app.route('/')
def index():
    return file_html

@app.route('/file_test_interface', methods=['POST'])
def file_test_interface():
    try:
        filename = request.args.get('filename')
        # print(request.get_data().decode().split('base64,'))
        file = request.get_data().decode().split('base64,')[-1]
        filedata = base64.b64decode(file)
        # 这里返回的是字符串，通常用于解析二进制内容后返回字符串类型数据
        with open(filename, 'wb') as f:
            f.write(filedata)
        return '传输数据成功.'
    except:
        import traceback; traceback.print_exc()
        return "传输数据失败."

if __name__ == '__main__':
    app.run("0.0.0.0", port=12333)