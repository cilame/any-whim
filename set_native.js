
// by Ossian
// 算是完美hook toString的一个方法 妙啊，当然要完美挂钩，这个函数必须最开始就运行，否则可能还是会被检测到。
;(function(){
    "use strict";
    const $toString = Function.toString;
    const myFunction_toString_symbol = Symbol('('.concat('', ')_', (Math.random() + '').toString(36)));
    const myToString = function() {
        return typeof this == 'function' && this[myFunction_toString_symbol] || $toString.call(this);
    };
    function set_native(func, key, value) {
        return Object.defineProperty(func, key, {
            "enumerable": false,
            "configurable": true,
            "writable": true,
            "value": value
        })
    };
    delete Function.prototype['toString'];
    set_native(Function.prototype, "toString", myToString);
    set_native(Function.prototype.toString, myFunction_toString_symbol, "function toString() { [native code] }");
    (typeof global=='undefined'?window:global).func_set_natvie = function(func){
        return set_native(func, myFunction_toString_symbol, `function ${myFunction_toString_symbol,func.name || ''}() { [native code] }`);
    };
})();




// 根据上面的原理改造的 toString 保护函数，这样不用入侵每一个函数体，给那个函数对象增加东西
var saf;
;(function(){
  var $toString = Function.toString
    , cacheI = []
    , cacheS = []
    , idxI = [].indexOf.bind(cacheI)
    , pushI = [].push.bind(cacheI)
    , pushS = [].push.bind(cacheS)
  Object.defineProperty(Function.prototype, 'toString', {
    "enumerable": !1, 
    "configurable": !0, 
    "writable": !0,
    "value": function toString() {
      return typeof this == 'function' && cacheS[idxI(this)] || $toString.call(this);
    }
  })
  function safe_func(func, name){
    if (-1 == idxI(func)){
      pushI(func)
      pushS(`function ${name || func.name || ''}() { [native code] }`)
    }
    return func
  };
  safe_func(Function.prototype.toString)
  saf = safe_func
})();





// 一个旧的检测 native 函数的方式，依赖于 Object.toString 方法是原始方法。若不是，则无法确认检测内容是否真实。
;(function() {
    var toString = Object.prototype.toString;
    var fnToString = Function.prototype.toString;
    var reHostCtor = /^\[object .+?Constructor\]$/;
    // 使用 `Object#toString` 是因为一般他不会被污染 
    var reNative = RegExp('^' + 
            String(toString)
            .replace(/[.*+?^${}()|[\]\/\\]/g, '\\$&')
            .replace(/toString|(function).*?(?=\\\()| for .+?(?=\\\])/g, '$1.*?')
            + '$');
    function isNative(value) {
        var type = typeof value;
        if (type == 'function'){
            return reNative.test(fnToString.call(value))
        }else{
            return (value && type == 'object' && reHostCtor.test(toString.call(value))) || false;
        }
    }
    (typeof global=='undefined'?window:global).isNative = isNative;
}());






//调用方法:
function setTimeout() {};
func_set_natvie(setTimeout);
console.log(setTimeout.toString());
console.log(setTimeout.toString + '');

//单独创建 不做hook 则会返回本来的字符串:
function myfunction() {
    123123123
};
console.log(myfunction.toString());
console.log(myfunction.toString + '');

console.log(isNative(myfunction))
console.log(isNative(setTimeout))