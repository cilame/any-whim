# 直接执行即可测试

# 功能：快速定位复杂 js 代码中的函数部分的字符串
# 因为代码很短，复制使用即可，按照测试的写法写即可。
# 开发于 python3 ，是对已经存在库的内部函数的挂钩式处理后增加了自己想要的功能

# 依赖， pip install pyjsparser
# 如果你安装过了 js2py ，那么这个库就已经安装了。

import pyjsparser

class PyJsHooker:
    Identifier = 3 # pyjsparser.pyjsparserdata.Token.Identifier
    func_stack = []
    func_count = {}
    func_local = []
    def _expect_hook(self, value):
        index = len(PyJsHooker.func_stack)
        if self.lookahead['value'] == '{':
            if index not in PyJsHooker.func_count:
                PyJsHooker.func_count[index] = 1
            else:
                PyJsHooker.func_count[index] += 1
        if self.lookahead['value'] == '}':
            PyJsHooker.func_count[index] -= 1
        if index in PyJsHooker.func_count and PyJsHooker.func_count[index] == 0 and self.lookahead['value'] == '}':
            if PyJsHooker.func_stack:
                (name, start), end = PyJsHooker.func_stack.pop(), self.lookahead
                name = name['value'] if name['type'] == PyJsHooker.Identifier else '[Anonymous function]'
                PyJsHooker.func_local.append((name, start['start'], end['end']))
        return PyJsHooker._bak_expect(self, value)
    def _expectKeyword_hook(self, w):
        orFunc = self.lookahead
        isFunc = True if self.lookahead['value'] == 'function' else False
        r = PyJsHooker._bak_expectKeyword(self, w)
        crFunc = self.lookahead
        if isFunc:
            name = crFunc if crFunc['type'] == PyJsHooker.Identifier else None
            PyJsHooker.func_stack.append([crFunc, orFunc])
        return r
    _bak_expect = pyjsparser.PyJsParser.expect
    _bak_expectKeyword = pyjsparser.PyJsParser.expectKeyword
    pyjsparser.PyJsParser.expect = _expect_hook
    pyjsparser.PyJsParser.expectKeyword = _expectKeyword_hook
    def __init__(self):
        self.parser = pyjsparser.PyJsParser()

    def parse(self, script):
        PyJsHooker.func_stack = []
        PyJsHooker.func_count = {}
        PyJsHooker.func_local = []
        self.parser.parse(script)
        return PyJsHooker.func_local


if __name__ == '__main__':
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
    }

    var a = 123;'''
    s = PyJsHooker()

    for local in s.parse(script):
        name, start, end = local
        v = script[start:end]
        print('===================================')
        print('function name:{}, start:{}, end:{}'.format(name, start, end))
        print('-----------------------------------')
        print(v)