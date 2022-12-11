// D-H 密钥交换算法

function quickpow(m, n, k){
    var r = 1;
    while(n > 0) {
        if(n & 1)
            r = (r * m) % k;
        n = n >> 1 ;
        m = (m * m) % k;
    }
    return r;
}

// miller-rabin 算法素性检测
function isprime_mr(a,b){
    if (!b){
        b = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    }
    if (a == 2){
        return true
    }
    if (a % 2 == 0 || a == 1){
        return false
    }
    for (var i = 0; i < b.length; i++) {
        var x = b[i]
        var t = a - 1
        while (t % 2 == 0){
            var v = quickpow(x, t, a)
            if (!(v == 0 ||
                  v == 1 ||
                  v == a-1 )){
                return false
            }else{
                if (v == 0 ||
                    v == a-1){
                    break
                }
                t = (t / 2) | 0
            }
        }
    }
    return true
}

function gen_prime(x){
    while (!isprime_mr(++x)){}
    return x
}

function get_generator(n){
    var k = random_limit(0.6, 0.7, n)
    for (var i = k; i < n; i++) {
        if (quickpow(i, k, n) != 1){
            return i
        }
    }
}

function random_limit(x, y, p){
    return (Math.random() * (p * (y - x)) + p * x) | 0
}


var o = 123456
var p = gen_prime(o) // 从数字开始向后迭代，获取一个素数
var a = get_generator(p) // 从数字中间开始向后迭代，获取一个原根
console.log(p)
console.log(a)

var x = random_limit(0.6, 0.7, (p - 1))
var y = random_limit(0.8, 0.9, (p - 1))

console.log('生成随机数 x,y')
console.log(x)
console.log(y)

var ex = quickpow(a, x, p)
var ey = quickpow(a, y, p)

console.log('生成计算数 ex,ey')
console.log(ex)
console.log(ey)


var dx = quickpow(ey, x, p)
var dy = quickpow(ex, y, p)
console.log('生成交换后的密钥 dx,dy')
console.log(dx)
console.log(dy)



// 可以公开的就是 (p, a, ex, ey)
// 双方各自保存各自的随机值


