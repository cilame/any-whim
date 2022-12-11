
jscode = r'''
function test(){
    return 123;
}
var s = 333;
function test2(){
    return s;
}
'''

# qjs.exe 需要与该脚本在同一路径下
# 两种使用 qjs 执行js代码的方式，方法均是使用 execjs 的执行获取方式
# 不过一种是需要依赖 execjs 库，另一种不需要。





import execjs._external_runtime
import execjs._runner_sources
ExternalRuntime = execjs._external_runtime.ExternalRuntime
PhantomJS = execjs._runner_sources.PhantomJS.replace('phantom.exit();', '')
middle = ExternalRuntime(
    name="quickjs",
    command=['qjs'], 
    encoding='UTF-8',
    runner_source=PhantomJS,
    tempfile=True
)
ctx = middle.compile(jscode)
v1 = ctx.call('test')
v2 = ctx.call('test2')
print('使用 execjs 依赖库方式执行')
print(v1)
print(v2)







import os
import io
import re
import json
import tempfile
from subprocess import Popen, PIPE

QuickJS = r"""
(function(program, execJS) { execJS(program) })(function() {
  return eval(#{encoded_source});
}, function(program) {
  var output;
  var print = function(string) {
    console.log('' + string);
  };
  try {
    result = program();
    print('')
    if (typeof result == 'undefined' && result !== null) {
      print('["ok"]');
    } else {
      try {
        print(JSON.stringify(['ok', result]));
      } catch (err) {
        print('["err"]');
      }
    }
  } catch (err) {
    print(JSON.stringify(['err', '' + err]));
  }
});
"""
class ProgramError(Exception):
    pass
def _json2_source():
    return 'var JSON;if(!JSON){JSON={}}(function(){function f(n){return n<10?"0"+n:n}if(typeof Date.prototype.toJSON!=="function"){Date.prototype.toJSON=function(key){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+f(this.getUTCMonth()+1)+"-"+f(this.getUTCDate())+"T"+f(this.getUTCHours())+":"+f(this.getUTCMinutes())+":"+f(this.getUTCSeconds())+"Z":null};String.prototype.toJSON=Number.prototype.toJSON=Boolean.prototype.toJSON=function(key){return this.valueOf()}}var cx=/[\\u0000\\u00ad\\u0600-\\u0604\\u070f\\u17b4\\u17b5\\u200c-\\u200f\\u2028-\\u202f\\u2060-\\u206f\\ufeff\\ufff0-\\uffff]/g,escapable=/[\\\\\\"\\x00-\\x1f\\x7f-\\x9f\\u00ad\\u0600-\\u0604\\u070f\\u17b4\\u17b5\\u200c-\\u200f\\u2028-\\u202f\\u2060-\\u206f\\ufeff\\ufff0-\\uffff]/g,gap,indent,meta={"\\b":"\\\\b","\\t":"\\\\t","\\n":"\\\\n","\\f":"\\\\f","\\r":"\\\\r",\'"\':\'\\\\"\',"\\\\":"\\\\\\\\"},rep;function quote(string){escapable.lastIndex=0;return escapable.test(string)?\'"\'+string.replace(escapable,function(a){var c=meta[a];return typeof c==="string"?c:"\\\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)})+\'"\':\'"\'+string+\'"\'}function str(key,holder){var i,k,v,length,mind=gap,partial,value=holder[key];if(value&&typeof value==="object"&&typeof value.toJSON==="function"){value=value.toJSON(key)}if(typeof rep==="function"){value=rep.call(holder,key,value)}switch(typeof value){case"string":return quote(value);case"number":return isFinite(value)?String(value):"null";case"boolean":case"null":return String(value);case"object":if(!value){return"null"}gap+=indent;partial=[];if(Object.prototype.toString.apply(value)==="[object Array]"){length=value.length;for(i=0;i<length;i+=1){partial[i]=str(i,value)||"null"}v=partial.length===0?"[]":gap?"[\\n"+gap+partial.join(",\\n"+gap)+"\\n"+mind+"]":"["+partial.join(",")+"]";gap=mind;return v}if(rep&&typeof rep==="object"){length=rep.length;for(i=0;i<length;i+=1){if(typeof rep[i]==="string"){k=rep[i];v=str(k,value);if(v){partial.push(quote(k)+(gap?": ":":")+v)}}}}else{for(k in value){if(Object.prototype.hasOwnProperty.call(value,k)){v=str(k,value);if(v){partial.push(quote(k)+(gap?": ":":")+v)}}}}v=partial.length===0?"{}":gap?"{\\n"+gap+partial.join(",\\n"+gap)+"\\n"+mind+"}":"{"+partial.join(",")+"}";gap=mind;return v}}if(typeof JSON.stringify!=="function"){JSON.stringify=function(value,replacer,space){var i;gap="";indent="";if(typeof space==="number"){for(i=0;i<space;i+=1){indent+=" "}}else{if(typeof space==="string"){indent=space}}rep=replacer;if(replacer&&typeof replacer!=="function"&&(typeof replacer!=="object"||typeof replacer.length!=="number")){throw new Error("JSON.stringify")}return str("",{"":value})}}if(typeof JSON.parse!=="function"){JSON.parse=function(text,reviver){var j;function walk(holder,key){var k,v,value=holder[key];if(value&&typeof value==="object"){for(k in value){if(Object.prototype.hasOwnProperty.call(value,k)){v=walk(value,k);if(v!==undefined){value[k]=v}else{delete value[k]}}}}return reviver.call(holder,key,value)}text=String(text);cx.lastIndex=0;if(cx.test(text)){text=text.replace(cx,function(a){return"\\\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)})}if(/^[\\],:{}\\s]*$/.test(text.replace(/\\\\(?:["\\\\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\\\\n\\r]*"|true|false|null|-?\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?/g,"]").replace(/(?:^|:|,)(?:\\s*\\[)+/g,""))){j=eval("("+text+")");return typeof reviver==="function"?walk({"":j},""):j}throw new SyntaxError("JSON.parse")}}}());'
def encode_unicode_codepoints(str):
    codepoint_format = '\\u{0:04x}'.format
    def codepoint(m):
        return codepoint_format(ord(m.group(0)))
    return re.sub('[^\x00-\x7f]', codepoint, str)
def _compile(source):
    runner_source = QuickJS
    replacements = {
        '#{source}': lambda: source,
        '#{encoded_source}': lambda: json.dumps(
            "(function(){ " +
            encode_unicode_codepoints(source) +
            " })()"
        ),
        '#{json2_source}': _json2_source,
    }
    pattern = "|".join(re.escape(k) for k in replacements)
    runner_source = re.sub(pattern, lambda m: replacements[m.group(0)](), runner_source)
    return runner_source
def _extract_result(output):
    output = output.replace("\r\n", "\n").replace("\r", "\n")
    output_last_line = output.split("\n")[-2]
    ret = json.loads(output_last_line)
    if len(ret) == 1:
        ret = [ret[0], None]
    status, value = ret
    if status == "ok":
        return value
    else:
        raise ProgramError(value)
def evaljs(source):
    (fd, filename) = tempfile.mkstemp(prefix='execjs', suffix='.js')
    os.close(fd)
    try:
        with io.open(filename, "w+", encoding='UTF8') as fp:
            fp.write(_compile(source))
        cmd = ['./qjs.exe'] + [filename]
        p = None
        try:
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=None, universal_newlines=True)
            stdoutdata, stderrdata = p.communicate()
            ret = p.wait()
        finally:
            del p
        return _extract_result(stdoutdata)
    finally:
        os.remove(filename)
class execjs:
    @staticmethod
    def compile(source):
        return execjs.Context(source)
    class Context:
        def __init__(self, source):
            self.source = source
        def call(self, identifier, *args):
            args = json.dumps(args)
            _source = "{identifier}.apply(this, {args})".format(identifier=identifier, args=args)
            data = "''" if not _source.strip() else "'('+" + json.dumps(_source, ensure_ascii=True) + "+')'"
            _source = 'return eval({data})'.format(data=data)
            rsource = '\n'.join([self.source, _source])
            return evaljs(rsource)




ctx = execjs.compile(jscode)
v1 = ctx.call('test')
v2 = ctx.call('test2')
print('使用无依赖库方式执行')
print(v1)
print(v2)