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

function gen_prime(bitlen){
    var n = (1<<(bitlen-1)) + Math.random() * ((1<<(bitlen-1)) * 0.9) | 1
    while (1){
        n += 2
        if (isprime_mr(n)){
            return n
        }
    }
}

function ex_gcd(a, b){
    if (b == 0){
        return [1, 0, a]
    }
    var z = ex_gcd(b, a%b)
    var x = z[0]
    var y = z[1]
    var r = z[2]
    var t = x
    var x = y
    var y = t - (a / b | 0) * y
    return [x, y, r]
}

function make_primes(l){
    var e = 65537
    if (l % 2 == 1){ throw Error('must be even.') }
    while(1){
        var p = gen_prime(l / 2)
        var q = gen_prime(l / 2)
        var n = p * q
        if ((n.toString(2).length == l) && p != q){
            break
        }
    }
    return [n, p, q]
}

function modinv(a, m) {
    var z = ex_gcd(a, m)
    var x = z[0]
    var y = z[1]
    var g = z[2]
    if (g != 1){
        throw Error('inver not exist.')
    }else{
        if (x > 0){
            return x % m
        }else{
            while (x < 0){
                x += m
            }
            return x
        }
    }
}

function lcm(a, b){
    return a * b / ex_gcd(a, b)[2]
}


var z = make_primes(12)
var n = z[0]
var p = z[1]
var q = z[2]
var n2 = n * n
var lamb = lcm(p-1, q-1)
var x = modinv((quickpow(n + 1, lamb, n2) - 1) / n, n)
console.log(n2, lamb, x)




function encrypt(m){
    return (n * m + 1) % n2
}

function add(a, b){
    return (a * b) % n2
}

function mult(a, b){
    return quickpow(a, b, n2)
}

function decrypt(c){
    return ((quickpow(c, lamb, n2) - 1) / n * x) % n
}




// 适用于运算结果在 1000 以内的整数算法 (+*)
e1 = encrypt(1)
e2 = encrypt(2)
e3 = encrypt(3)
console.log(e1, e2, e3)

// 1 + 2 + 3
e4 = add(add(e1, e2), e3)
c4 = decrypt(e4)

// (1+2+3) * 5
e5 = mult(e4, 5)
c5 = decrypt(e5)

console.log('n2:', n2)
console.log('e4:', e4)
console.log('c4:', c4)
console.log('e5:', e5)
console.log('c5:', c5)