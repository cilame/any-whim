Function = new Proxy(Function, {
    construct: function(T, L, N){
        if (typeof L[0] == 'string'){
            L[0] = L[0].replace(' Buffer ', ' aslkdjfaklsdjf ')
            L[0] = L[0].replace('process["argv"][0]["indexOf"]("node")', '-1')
            L[0] = L[0].replace('typeof module != "object";', 'true')
        }
        return Reflect.construct(T, L, N)
    }
})

var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
function atob(input) {
    var str = (String (input)).replace (/[=]+$/, ''); // #31: ExtendScript bad parse of /=
    if (str.length % 4 === 1) {
        throw new InvalidCharacterError ("'atob' failed: The string to be decoded is not correctly encoded.");
    }
    for (
        var bc = 0, bs, buffer, idx = 0, output = '';
        buffer = str.charAt (idx++);
        ~buffer && (bs = bc % 4 ? bs * 64 + buffer : buffer, bc++ % 4) ? output += String.fromCharCode (255 & bs >> (-2 * bc & 6)) : 0
    ) {
        buffer = chars.indexOf (buffer);
    }
    return output;
};
Window = function () {
};
Window.prototype = {
    navigator: {
        cookieEnabled: true,
        language: "zh-CN",
        userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37",
        appVersion:"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37"
    },
    document: {
        cookie:"",
        createElement: function (x) {
            if (x == 'canvas') {
                return {
                    getContext: function () {
                        return {
                            fillText:
                                function () {
                                },
                            fillRect: function () {
                            }
                        }
                    },
                    toDataURL: function () {
                        return "data:image/png;base64,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"
                    }
                }
            }
        },
        getElementById:function (){}
    },
    length: 0,
    decodeURI: decodeURI,
    history:{
        scrollRestoration:"auto",
        length:5,
        state:null
    },
    eval: eval,
    innerHeight: 734,
    outerHeight: 734,
    innerWidth: 1280,
    outerWidth: 1280,
    Math: Math,
    location: {
        href: ""
    },
    Function:Function,
};
top = new Window();
window = new Proxy(new Window(), {
    get: function (x, y) {
        return x[y]
    },
    set(target, p, value, receiver) {
        target[p] = value
    }
});
delete global;
document = window.document;
navigator = window.navigator;
Storage = function (){};
Storage.prototype = {
    setItem:function (x,y){
        this[x] = y
    },
    getItem:function (x){
        return this[x]
    },
    removeItem:function (x){
        delete this[x]
    }
};
sessionStorage = new Storage();
localStorage = new Storage();
closed = false;
top.location.href = "https://www.zhipin.com/web/common/security-check.html?seed=h7vwjxliib4vmnjN%2FH%2BPXDRF1PK6sE%2BgMhxMvyDXXxI%3D&name=3bff01f6&ts=1622826970587&callbackUrl=%2Fc101280600-p100901%2F&srcReferer=https%3A%2F%2Fwww.zhipin.com%2F";
top.location.hostname = "www.zhipin.com";
window.window = window;
window.window.window.toString = function (){
    return "[object Window]"
};
window.top = top;
function setInterval() {};
setInterval.toString = function() {
    return "function setInterval() { [native code] }"
};
function clearTimeout(){};


