// 某些 dev-tools(F12) 的反调试代码
setTimeout(function adbg() {
  var d = new Image;
  Object.defineProperty(d, "id", {get: function() {
      alert(123);
  }})
  console.log(d);
  console.clear();
  setTimeout(adbg, 200);
}, 200);






// eval Function Function.constructor 三种执行字符串脚本的挂钩
(function(){
  eval_string = window.eval.toString()
  eval_tostring = window.eval.toString.toString()
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- eval(*) -----\n" + args);
      return target.apply(thisArg, args) } }
  const handler_tostring = { apply: function (target, thisArg, args){ return eval_string; } }
  const handler_totostring = { apply: function (target, thisArg, args){ return eval_tostring; } }
  window.eval = new Proxy(window.eval, handler);
  window.eval.toString = new Proxy(window.eval.toString, handler_tostring);
  window.eval.toString.toString = new Proxy(window.eval.toString.toString, handler_totostring);
})();
(function(){
  Function_string = window.Function.toString()
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- Function(*) -----\n" + args);
      return target.apply(thisArg, args) } }
  const handler_tostring = { apply: function (target, thisArg, args){ return Function_string; } }
  window.Function = new Proxy(window.Function, handler);
  window.Function.toString = new Proxy(window.Function.toString, handler_tostring);
})();
Function.prototype.__defineGetter__('constructor', function() { return function(...args) {
    // debugger;
    console.log('----- Function constructor(*) -----\n', ...args); 
    return Function(...args); }; });







// 挂钩 XMLHttpRequest. 设置请求头和发起请求的时机
(function(){
  XMLHttpRequest_prototype_open_str = XMLHttpRequest.prototype.open.toString()
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- XMLHttpRequest_open -----\n", args)
      return target.apply(thisArg, args) } }
  const handler_tostring = { apply: function (target, thisArg, args){ return XMLHttpRequest_prototype_open_str; } }
  XMLHttpRequest.prototype.open = new Proxy(XMLHttpRequest.prototype.open, handler);
  XMLHttpRequest.prototype.open.toString = new Proxy(XMLHttpRequest.prototype.open.toString, handler_tostring);
})();
(function(){
  XMLHttpRequest_prototype_setRequestHeader_str = XMLHttpRequest.prototype.setRequestHeader.toString()
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- XMLHttpRequest_setRequestHeader -----\n", args)
      return target.apply(thisArg, args) } }
  const handler_tostring = { apply: function (target, thisArg, args){ return XMLHttpRequest_prototype_setRequestHeader_str; } }
  XMLHttpRequest.prototype.setRequestHeader = new Proxy(XMLHttpRequest.prototype.setRequestHeader, handler);
  XMLHttpRequest.prototype.setRequestHeader.toString = new Proxy(XMLHttpRequest.prototype.setRequestHeader.toString, handler_tostring);
})();







// 挂钩生成cookie设置时机，但是这里是有问题的，这里如果挂钩，之后都将无法设置真实的 cookie 键值
(function(){
  var _cookie = document.__lookupSetter__('cookie');
  var _cookie_set = function(c) {
    if (/RM4hZBv0dDon443M/.test(c)){
      // debugger;
    }
    console.log('----- cookie.set -----\n', c);
    _cookie = c;
    return _cookie;
  }
  var mycookie = document.cookie;
  document.__defineSetter__("cookie", _cookie_set);
  document.__defineGetter__("cookie", function() {return _cookie;} );
  Object.getOwnPropertyNames(String.prototype).filter(k => !!String.prototype[k].call).map(function(a){
    if (!/^caller$|^callee$|^arguments$/.test(a)){
      document.cookie[a] = mycookie[a];
    }
  });
  document.cookie.toString = function (){ return mycookie.toString() };
})();








// 挂钩一些对象的参数，特别是该值为列表，也会挂钩该列表对象的push函数
var hook_set = (function(pname, pobject){
  var win_param = pobject.__lookupSetter__(pname);
  var win_param_set = function(c) {
    console.log('----- ' + pname + '.set -----\n', c);
    win_param = c;
    if (win_param instanceof Array){
      (function(){
        pobject_push_str = win_param.push.toString()
        const handler = { apply: function (target, thisArg, args){
          // debugger;
          console.log("----- " + pname + " Array.push -----\n", args)
          return target.apply(thisArg, args) } }
        const handler_tostring = { apply: function (target, thisArg, args){ return pobject_push_str; } }
        win_param.push = new Proxy(win_param.push, handler);
        win_param.push.toString = new Proxy(win_param.push.toString, handler_tostring);
      })();
    }
    return win_param;
  }
  pobject.__defineSetter__(pname, win_param_set);
  pobject.__defineGetter__(pname, function() {return win_param;} );
});
hook_set('_$ss', window)
hook_set('_$pr', window)










// 挂钩打印函数
_console_log = console.log;
console.log = function(...args){
  if (args && args[0] == '有时候控制台输出太多无意义内容会影响性能，可以hook对部分字符串进行不打印'){
    return 
  }
  _console_log(...args);
}

