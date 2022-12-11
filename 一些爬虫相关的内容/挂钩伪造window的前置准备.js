!function(){
    var $toString = Function.toString
    var v_Object_defineProperty = Object.defineProperty
    var cacheI = []
    var cacheS = []
    var idxI = [].indexOf.bind(cacheI)
    var pushI = [].push.bind(cacheI)
    var pushS = [].push.bind(cacheS)
    Object.defineProperty(Function.prototype, 'toString', {
        "enumerable": !1, "configurable": !0, "writable": !0,
        "value": function toString() {
            return typeof this == 'function' && cacheS[idxI(this)] || $toString.call(this);
        }
    })
    function safe_func(func, name, string){
        if (-1 == idxI(func)){
            if (name){ v_Object_defineProperty(func, 'name', {value: name, writable: false, enumerable: false, configurable: true}) }
            pushI(func)
            pushS(string ? string : `function ${name || func.name || ''}() { [native code] }`)
        }
        return func
    };
    safe_func(Function.prototype.toString, 'toString')
    var v_Object_defineProperty = Object.defineProperty
    var v_Function_toString = Function.prototype.toString
    var v_push = Date.call.bind(Date.call, [].push)
    var v_indexOf = Date.call.bind(Date.call, [].indexOf)
    var v_cache_r = []
    var v_cache_b = []
    var v_oldFunction = Function
    var v_newFunction = function Function(){
        if (!global.window){
            throw Error('pls init global.window') // 这里非常容易忘，总之强制加上
        }
        var rfunc = v_oldFunction.apply(this, arguments)
        var bfunc = global.window ? rfunc.bind(global.window) : rfunc
        safe_func(bfunc, rfunc.name, v_Function_toString.call(rfunc))
        v_push(v_cache_r, rfunc)
        v_push(v_cache_b, bfunc)
        return bfunc
    }
    var v_idx;
    var v_newbind = function bind(a){
        if ((v_idx = v_indexOf(v_cache_b, this)) != -1){
            return v_bind.apply(v_cache_r[idx], arguments)
        }
        return v_bind.apply(this, arguments)
    }
    safe_func(v_newFunction)
    safe_func(v_newbind)
    Function.prototype.constructor = v_newFunction
    Function = v_newFunction
    Function.prototype = v_oldFunction.prototype
    var v_bind = Function.prototype.bind
    Function.prototype.bind = v_newbind
}()