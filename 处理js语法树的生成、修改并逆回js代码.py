# 完全依赖 js2py

# 通过生成语法树，快速修改内部的某些混肴处理，从而简化代码
# 直接使用 js2py 非常方便，因为其内部已经自带了一些 js 库的 python 化代码
# 使用其中的 escodegen 模块就可以重新将语法树重构成代码。代码如下。

script = '''// test_code
function func(a,b){
    function ffff(){
        var sadf = "12312{31}23";
        var fffasdf = "123123123", aaa;
        var qqq = {"123123":123123};
        return 133;
    }

    (function(){
            console.log(ffff);
        })();

    return a+b;
};
try{
    function nihao(){
        console.log('nihao');
    }
    console.log(123);
} catch (_0x59ca51){
    console.log(456+123);
}

var a = 123;'''

import json
import pyjsparser
s = pyjsparser.parse(script)
v = json.dumps(s, indent=4)
print('========================================')
print(v)
s['body'][0]['id']['name'] = '傻逼了' # 修改一个函数名


import js2py.py_node_modules.escodegen as escodegen
escodegen = escodegen.var.get('escodegen')
v = escodegen.get('generate')(s) # 用树重新生成js代码
print('========================================')
print(v.to_python())