// 直接编译运行即可测试，开发环境为 win7/64 位。
// tcc/gcc 均可直接编译运行，
// 部分其他测试内容在该代码最底部 main 函数里面解开注释函数即可测试。
// 
// 这里在原有加密的基础上添加了保存秘钥为字符串的功能
// 可以将秘钥保存为 base64字符串，也可以使用秘钥的base64字符串加载成秘钥的结构直接使用来加解密
// 之所以用base64是为了复制粘贴秘钥的方便。详细请看 main 函数中的部分测试函数中的内容。

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
unsigned char *base64_encode(unsigned char *str, long str_len){
    long len;
    unsigned char *res;
    int i,j;
    unsigned char *base64_table="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    if(str_len % 3 == 0)
        len=str_len/3*4;
    else
        len=(str_len/3+1)*4;
    res = malloc(sizeof(unsigned char)*len+1);
    res[len] = '\0';
    for(i=0,j=0;i<len-2;j+=3,i+=4){
        res[i]   = base64_table[str[j]>>2];
        res[i+1] = base64_table[(str[j]&0x3)<<4 | (str[j+1]>>4)];
        res[i+2] = base64_table[(str[j+1]&0xf)<<2 | (str[j+2]>>6)];
        res[i+3] = base64_table[str[j+2]&0x3f];
    }
    switch(str_len % 3){
        case 1:
            res[i-2]='=';
            res[i-1]='=';
            break;
        case 2:
            res[i-1]='=';
            break;
    }
    return res;
}
unsigned char *base64_decode(unsigned char *code){
    int table[]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62,0,0,0,
                 63,52,53,54,55,56,57,58,59,60,61,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,
                 22,23,24,25,0,0,0,0,0,0,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51};
    long len, str_len;
    unsigned char *res;
    int i,j;
    len = strlen(code);
    if(strstr(code,"=="))
        str_len = len/4*3-2;
    else if(strstr(code,"="))
        str_len = len/4*3-1;
    else
        str_len=len/4*3;
    res = malloc(sizeof(unsigned char)*str_len+1);
    res[str_len]='\0';
    for(i=0,j=0;i < len-2;j+=3,i+=4){
        res[j]   =  ((unsigned char)table[code[i]])<<2    | (((unsigned char)table[code[i+1]])>>4);
        res[j+1] = (((unsigned char)table[code[i+1]])<<4) | (((unsigned char)table[code[i+2]])>>2);
        res[j+2] = (((unsigned char)table[code[i+2]])<<6) | ((unsigned char)table[code[i+3]]);
    }
    return res;
}
#ifndef __BIGNUM_H__
#define __BIGNUM_H__
#include <stdint.h>
typedef uint64_t dbn_t;
typedef uint32_t bn_t;
typedef uint16_t bnh_t;
#define BN_DIGIT_BITS               32  
#define BN_HALF_DIGIT_BITS          16  
#define BN_DIGIT_LEN                4   
#define BN_MAX_DIGITS               65  
#define BN_MAX_DIGIT                0xFFFFFFFF
#define BN_MAX_HALF_DIGIT           0xFFFF
#define LOW_HALF(x)                 ((x) & BN_MAX_HALF_DIGIT)
#define HIGH_HALF(x)                (((x) >> BN_HALF_DIGIT_BITS) & BN_MAX_HALF_DIGIT)
#define TO_HIGH_HALF(x)             (((bn_t)(x)) << BN_HALF_DIGIT_BITS)
#define DIGIT_MSB(x)                (uint32_t)(((x) >> (BN_DIGIT_BITS - 1)) & 0x01)
#define DIGIT_2MSB(x)               (uint32_t)(((x) >> (BN_DIGIT_BITS - 2)) & 0x03)
void bn_decode(bn_t *bn, uint32_t digits, uint8_t *hexarr, uint32_t size);
void bn_encode(uint8_t *hexarr, uint32_t size, bn_t *bn, uint32_t digits);
void bn_assign(bn_t *a, bn_t *b, uint32_t digits);          
void bn_assign_zero(bn_t *a, uint32_t digits);              
void bn_assign_2exp(bn_t *a, uint32_t b, uint32_t digits);  
bn_t bn_add(bn_t *a, bn_t *b, bn_t *c, uint32_t digits);    
bn_t bn_sub(bn_t *a, bn_t *b, bn_t *c, uint32_t digits);    
void bn_mul(bn_t *a, bn_t *b, bn_t *c, uint32_t digits);    
void bn_div(bn_t *a, bn_t *b, bn_t *c, uint32_t cdigits, bn_t *d, uint32_t ddigits);
bn_t bn_shift_l(bn_t *a, bn_t *b, uint32_t c, uint32_t digits); 
bn_t bn_shift_r(bn_t *a, bn_t *b, uint32_t c, uint32_t digits); 
void bn_mod(bn_t *a, bn_t *b, uint32_t bdigits, bn_t *c, uint32_t cdigits); 
void bn_mod_mul(bn_t *a, bn_t *b, bn_t *c, bn_t *d, uint32_t digits);       
void bn_mod_exp(bn_t *a, bn_t *b, bn_t *c, uint32_t cdigits, bn_t *d, uint32_t ddigits); 
void bn_mod_inv(bn_t *a, bn_t *b, bn_t *c, uint32_t digits);    
void bn_gcd(bn_t *a, bn_t *b, bn_t *c, uint32_t digits);        
int bn_cmp(bn_t *a, bn_t *b, uint32_t digits);                  
int bn_is_zero(bn_t *a, uint32_t digits);                       
uint32_t bn_bits(bn_t *a, uint32_t digits);                     
uint32_t bn_digits(bn_t *a, uint32_t digits);                   
#define BN_ASSIGN_DIGIT(a, b, digits)   {bn_assign_zero(a, digits); a[0] = b;}
#define BN_EQUAL(a, b, digits)          (!bn_cmp(a, b, digits))
#define BN_EVEN(a, digits)              (((digits) == 0) || !(a[0] & 0x01))
#endif  
#include <string.h>
extern void print_bn(char *TAG, bn_t *bn, uint32_t bn_size);
static bn_t bn_sub_digit_mul(bn_t *a, bn_t *b, bn_t c, bn_t *d, uint32_t digits);
static bn_t bn_add_digit_mul(bn_t *a, bn_t *b, bn_t c, bn_t *d, uint32_t digits);
static uint32_t bn_digit_bits(bn_t a);
void bn_decode(bn_t *bn, uint32_t digits, uint8_t *hexarr, uint32_t size){
    bn_t t;
    int j;
    uint32_t i, u;
    for(i=0,j=size-1; i<digits && j>=0; i++) {
        t = 0;
        for(u=0; j>=0 && u<BN_DIGIT_BITS; j--, u+=8) {
            t |= ((bn_t)hexarr[j]) << u;
        }
        bn[i] = t;
    }
    for(; i<digits; i++) {
        bn[i] = 0;
    }
}
void bn_encode(uint8_t *hexarr, uint32_t size, bn_t *bn, uint32_t digits){
    bn_t t;
    int j;
    uint32_t i, u;
    for(i=0,j=size-1; i<digits && j>=0; i++) {
        t = bn[i];
        for(u=0; j>=0 && u<BN_DIGIT_BITS; j--, u+=8) {
            hexarr[j] = (uint8_t)(t >> u);
        }
    }
    for(; j>=0; j--) {
        hexarr[j] = 0;
    }
}
void bn_assign(bn_t *a, bn_t *b, uint32_t digits){
    uint32_t i;
    for(i=0; i<digits; i++) {
        a[i] = b[i];
    }
}
void bn_assign_zero(bn_t *a, uint32_t digits){
    uint32_t i;
    for(i=0; i<digits; i++) {
        a[i] = 0;
    }
}
void bn_assign_2exp(bn_t *a, uint32_t b, uint32_t digits){
    bn_assign_zero(a, digits);
    if(b >= (digits * BN_DIGIT_BITS)) {
        return;     
    }
    a[b/BN_DIGIT_BITS] = (bn_t)1 << (b % BN_DIGIT_BITS);
}
bn_t bn_add(bn_t *a, bn_t *b, bn_t *c, uint32_t digits){
    bn_t ai, carry;
    uint32_t i;
    carry = 0;
    for(i=0; i<digits; i++) {
        if((ai = b[i] + carry) < carry) {
            ai = c[i];
        } else if((ai += c[i]) < c[i]) {
            carry = 1;
        } else {
            carry = 0;
        }
        a[i] = ai;
    }
    return carry;
}
bn_t bn_sub(bn_t *a, bn_t *b, bn_t *c, uint32_t digits){
    bn_t ai, borrow;
    uint32_t i;
    borrow = 0;
    for(i=0; i<digits; i++) {
        if((ai = b[i] - borrow) > (BN_MAX_DIGIT - borrow)) {
            ai = BN_MAX_DIGIT - c[i];
        } else if((ai -= c[i]) > (BN_MAX_DIGIT - c[i])) {
            borrow = 1;
        } else {
            borrow = 0;
        }
        a[i] = ai;
    }
    return borrow;
}
void bn_mul(bn_t *a, bn_t *b, bn_t *c, uint32_t digits){
    bn_t t[2*BN_MAX_DIGITS];
    uint32_t bdigits, cdigits, i;
    bn_assign_zero(t, 2*digits);
    bdigits = bn_digits(b, digits);
    cdigits = bn_digits(c, digits);
    for(i=0; i<bdigits; i++) {
        t[i+cdigits] += bn_add_digit_mul(&t[i], &t[i], b[i], c, cdigits);
    }
    bn_assign(a, t, 2*digits);
    memset((uint8_t *)t, 0, sizeof(t));
}
void bn_div(bn_t *a, bn_t *b, bn_t *c, uint32_t cdigits, bn_t *d, uint32_t ddigits){
    dbn_t tmp;
    bn_t ai, t, cc[2*BN_MAX_DIGITS+1], dd[BN_MAX_DIGITS];
    int i;
    uint32_t dddigits, shift;
    dddigits = bn_digits(d, ddigits);
    if(dddigits == 0)
        return;
    shift = BN_DIGIT_BITS - bn_digit_bits(d[dddigits-1]);
    bn_assign_zero(cc, dddigits);
    cc[cdigits] = bn_shift_l(cc, c, shift, cdigits);
    bn_shift_l(dd, d, shift, dddigits);
    t = dd[dddigits-1];
    bn_assign_zero(a, cdigits);
    i = cdigits - dddigits;
    for(; i>=0; i--) {
        if(t == BN_MAX_DIGIT) {
            ai = cc[i+dddigits];
        } else {
            tmp = cc[i+dddigits-1];
            tmp += (dbn_t)cc[i+dddigits] << BN_DIGIT_BITS;
            ai = tmp / (t + 1);
        }
        cc[i+dddigits] -= bn_sub_digit_mul(&cc[i], &cc[i], ai, dd, dddigits);
        while(cc[i+dddigits] || (bn_cmp(&cc[i], dd, dddigits) >= 0)) {
            ai++;
            cc[i+dddigits] -= bn_sub(&cc[i], &cc[i], dd, dddigits);
        }
        a[i] = ai;
    }
    bn_assign_zero(b, ddigits);
    bn_shift_r(b, cc, shift, dddigits);
    memset((uint8_t *)cc, 0, sizeof(cc));
    memset((uint8_t *)dd, 0, sizeof(dd));
}
bn_t bn_shift_l(bn_t *a, bn_t *b, uint32_t c, uint32_t digits){
    bn_t bi, carry;
    uint32_t i, t;
    if(c >= BN_DIGIT_BITS)
        return 0;
    t = BN_DIGIT_BITS - c;
    carry = 0;
    for(i=0; i<digits; i++) {
        bi = b[i];
        a[i] = (bi << c) | carry;
        carry = c ? (bi >> t) : 0;
    }
    return carry;
}
bn_t bn_shift_r(bn_t *a, bn_t *b, uint32_t c, uint32_t digits){
    bn_t bi, carry;
    int i;
    uint32_t t;
    if(c >= BN_DIGIT_BITS)
        return 0;
    t = BN_DIGIT_BITS - c;
    carry = 0;
    i = digits - 1;
    for(; i>=0; i--) {
        bi = b[i];
        a[i] = (bi >> c) | carry;
        carry = c ? (bi << t) : 0;
    }
    return carry;
}
void bn_mod(bn_t *a, bn_t *b, uint32_t bdigits, bn_t *c, uint32_t cdigits){
    bn_t t[2*BN_MAX_DIGITS] = {0};
    bn_div(t, a, b, bdigits, c, cdigits);
    memset((uint8_t *)t, 0, sizeof(t));
}
void bn_mod_mul(bn_t *a, bn_t *b, bn_t *c, bn_t *d, uint32_t digits){
    bn_t t[2*BN_MAX_DIGITS];
    bn_mul(t, b, c, digits);
    bn_mod(a, t, 2*digits, d, digits);
    memset((uint8_t *)t, 0, sizeof(t));
}
void bn_mod_exp(bn_t *a, bn_t *b, bn_t *c, uint32_t cdigits, bn_t *d, uint32_t ddigits){
    bn_t bpower[3][BN_MAX_DIGITS], ci, t[BN_MAX_DIGITS];
    int i;
    uint32_t ci_bits, j, s;
    bn_assign(bpower[0], b, ddigits);
    bn_mod_mul(bpower[1], bpower[0], b, d, ddigits);
    bn_mod_mul(bpower[2], bpower[1], b, d, ddigits);
    BN_ASSIGN_DIGIT(t, 1, ddigits);
    cdigits = bn_digits(c, cdigits);
    i = cdigits - 1;
    for(; i>=0; i--) {
        ci = c[i];
        ci_bits = BN_DIGIT_BITS;
        if(i == (int)(cdigits - 1)) {
            while(!DIGIT_2MSB(ci)) {
                ci <<= 2;
                ci_bits -= 2;
            }
        }
        for(j=0; j<ci_bits; j+=2) {
            bn_mod_mul(t, t, t, d, ddigits);
            bn_mod_mul(t, t, t, d, ddigits);
            if((s = DIGIT_2MSB(ci)) != 0) {
                bn_mod_mul(t, t, bpower[s-1], d, ddigits);
            }
            ci <<= 2;
        }
    }
    bn_assign(a, t, ddigits);
    memset((uint8_t *)bpower, 0, sizeof(bpower));
    memset((uint8_t *)t, 0, sizeof(t));
}
void bn_mod_inv(bn_t *a, bn_t *b, bn_t *c, uint32_t digits){
    bn_t q[BN_MAX_DIGITS], t1[BN_MAX_DIGITS], t3[BN_MAX_DIGITS], w[2*BN_MAX_DIGITS];
    bn_t u1[BN_MAX_DIGITS], u3[BN_MAX_DIGITS], v1[BN_MAX_DIGITS], v3[BN_MAX_DIGITS];
    int u1_sign;
    BN_ASSIGN_DIGIT(u1, 1, digits);
    bn_assign_zero(v1, digits);
    bn_assign(u3, b, digits);
    bn_assign(v3, c, digits);
    u1_sign = 1;
    while(!bn_is_zero(v3, digits)) {
        bn_div(q, t3, u3, digits, v3, digits);
        bn_mul(w, q, v1, digits);
        bn_add(t1, u1, w, digits);
        bn_assign(u1, v1, digits);
        bn_assign(v1, t1, digits);
        bn_assign(u3, v3, digits);
        bn_assign(v3, t3, digits);
        u1_sign = -u1_sign;
    }
    if(u1_sign < 0) {
        bn_sub(a, c, u1, digits);
    } else {
        bn_assign(a, u1, digits);
    }
    memset((uint8_t *)q, 0, sizeof(q));
    memset((uint8_t *)t1, 0, sizeof(t1));
    memset((uint8_t *)t3, 0, sizeof(t3));
    memset((uint8_t *)u1, 0, sizeof(u1));
    memset((uint8_t *)u3, 0, sizeof(u3));
    memset((uint8_t *)v1, 0, sizeof(v1));
    memset((uint8_t *)v3, 0, sizeof(v3));
    memset((uint8_t *)w, 0, sizeof(w));
}
void bn_gcd(bn_t *a, bn_t *b, bn_t *c, uint32_t digits){
    bn_t t[BN_MAX_DIGITS], u[BN_MAX_DIGITS], v[BN_MAX_DIGITS];
    bn_assign(u, b, digits);
    bn_assign(v, c, digits);
    while(!bn_is_zero(v, digits)) {
        bn_mod(t, u, digits, v, digits);
        bn_assign(u, v, digits);
        bn_assign(v, t, digits);
    }
    bn_assign(a, u, digits);
    memset((uint8_t *)t, 0, sizeof(t));
    memset((uint8_t *)u, 0, sizeof(u));
    memset((uint8_t *)v, 0, sizeof(v));
}
int bn_cmp(bn_t *a, bn_t *b, uint32_t digits){
    int i;
    for(i=digits-1; i>=0; i--) {
        if(a[i] > b[i])     return 1;
        if(a[i] < b[i])     return -1;
    }
    return 0;
}
int bn_is_zero(bn_t *a, uint32_t digits){
    uint32_t i;
    for(i=0; i<digits; i++) {
        if(a[i]) {
            return 0;
        }
    }
    return 1;
}
uint32_t bn_bits(bn_t *a, uint32_t digits){
    if((digits = bn_digits(a, digits)) == 0) {
        return 0;
    }
    return ((digits - 1) * BN_DIGIT_BITS + bn_digit_bits(a[digits-1]));
}
uint32_t bn_digits(bn_t *a, uint32_t digits){
    int i;
    for(i=digits-1; i>=0; i--) {
        if(a[i])    break;
    }
    return (i + 1);
}
static bn_t bn_add_digit_mul(bn_t *a, bn_t *b, bn_t c, bn_t *d, uint32_t digits){
    dbn_t result;
    bn_t carry, rh, rl;
    uint32_t i;
    if(c == 0)
        return 0;
    carry = 0;
    for(i=0; i<digits; i++) {
        result = (dbn_t)c * d[i];
        rl = result & BN_MAX_DIGIT;
        rh = (result >> BN_DIGIT_BITS) & BN_MAX_DIGIT;
        if((a[i] = b[i] + carry) < carry) {
            carry = 1;
        } else {
            carry = 0;
        }
        if((a[i] += rl) < rl) {
            carry++;
        }
        carry += rh;
    }
    return carry;
}
static bn_t bn_sub_digit_mul(bn_t *a, bn_t *b, bn_t c, bn_t *d, uint32_t digits){
    dbn_t result;
    bn_t borrow, rh, rl;
    uint32_t i;
    if(c == 0)
        return 0;
    borrow = 0;
    for(i=0; i<digits; i++) {
        result = (dbn_t)c * d[i];
        rl = result & BN_MAX_DIGIT;
        rh = (result >> BN_DIGIT_BITS) & BN_MAX_DIGIT;
        if((a[i] = b[i] - borrow) > (BN_MAX_DIGIT - borrow)) {
            borrow = 1;
        } else {
            borrow = 0;
        }
        if((a[i] -= rl) > (BN_MAX_DIGIT - rl)) {
            borrow++;
        }
        borrow += rh;
    }
    return borrow;
}
static uint32_t bn_digit_bits(bn_t a){
    uint32_t i;
    for(i=0; i<BN_DIGIT_BITS; i++) {
        if(a == 0)  break;
        a >>= 1;
    }
    return i;
}
#ifndef __RSA_H__
#define __RSA_H__
#include <stdint.h>
#define RSA_MIN_MODULUS_BITS                508
#define RSA_MAX_MODULUS_BITS                2048
#define RSA_MAX_MODULUS_LEN                 ((RSA_MAX_MODULUS_BITS + 7) / 8)
#define RSA_MAX_PRIME_BITS                  ((RSA_MAX_MODULUS_BITS + 1) / 2)
#define RSA_MAX_PRIME_LEN                   ((RSA_MAX_PRIME_BITS + 7) / 8)
#define ERR_WRONG_DATA                      0x1001
#define ERR_WRONG_LEN                       0x1002
typedef struct {
    uint32_t bits;
    uint8_t  modulus[RSA_MAX_MODULUS_LEN];
    uint8_t  exponent[RSA_MAX_MODULUS_LEN];
} rsa_pk_t;
typedef struct {
    uint32_t bits;
    uint8_t  modulus[RSA_MAX_MODULUS_LEN];
    uint8_t  public_exponet[RSA_MAX_MODULUS_LEN];
    uint8_t  exponent[RSA_MAX_MODULUS_LEN];
    uint8_t  prime1[RSA_MAX_PRIME_LEN];
    uint8_t  prime2[RSA_MAX_PRIME_LEN];
    uint8_t  prime_exponent1[RSA_MAX_PRIME_LEN];
    uint8_t  prime_exponent2[RSA_MAX_PRIME_LEN];
    uint8_t  coefficient[RSA_MAX_PRIME_LEN];
} rsa_sk_t;
int rsa_get_sk_from_file(char *file, rsa_sk_t *sk);
int rsa_generate_keys(rsa_pk_t *pk, rsa_sk_t *sk, uint32_t key_bits);
int rsa_public_encrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_pk_t *pk);
int rsa_public_decrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_pk_t *pk);
int rsa_private_encrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_sk_t *sk);
int rsa_private_decrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_sk_t *sk);
#endif  
#include <string.h>
#include <stdio.h>
void initialize_rand(void);
void generate_rand(uint8_t *block, uint32_t block_len);
int generate_prime(bn_t *a, bn_t *lower, bn_t *upper, bn_t *d, uint32_t digits);
static int rsa_filter(bn_t *a, uint32_t adigits, bn_t *b, uint32_t bdigits);
static int relatively_prime(bn_t *a, uint32_t adigits, bn_t *b, uint32_t bdigits);
static int public_block_operation(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_pk_t *pk);
static int private_block_operation(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_sk_t *sk);
int rsa_get_sk_from_file(char *file, rsa_sk_t *sk){
    FILE *fp;
    fp = fopen(file, "r");
    if(fp == NULL) {
        return -1;
    }
    fread((uint8_t *)sk, 1, sizeof(rsa_sk_t), fp);
    fclose(fp);
    return 0;
}
int rsa_generate_keys(rsa_pk_t *pk, rsa_sk_t *sk, uint32_t key_bits){
    int status;
    uint32_t ndigits, pbits, pdigits, qbits;
    bn_t n[BN_MAX_DIGITS], d[BN_MAX_DIGITS], e[BN_MAX_DIGITS], p[BN_MAX_DIGITS], q[BN_MAX_DIGITS];
    bn_t dp[BN_MAX_DIGITS], dq[BN_MAX_DIGITS], phi_n[BN_MAX_DIGITS], q_inv[BN_MAX_DIGITS];
    bn_t p_minus1[BN_MAX_DIGITS], q_minus1[BN_MAX_DIGITS];
    bn_t t[BN_MAX_DIGITS], u[BN_MAX_DIGITS], v[BN_MAX_DIGITS];
    if((key_bits < RSA_MIN_MODULUS_BITS) || (key_bits > RSA_MAX_MODULUS_BITS))
        return ERR_WRONG_LEN;
    ndigits = (key_bits + BN_DIGIT_BITS - 1) / BN_DIGIT_BITS;
    pdigits = (ndigits + 1) / 2;
    pbits = (key_bits + 1) / 2;
    qbits = key_bits - pbits;
    initialize_rand();
    BN_ASSIGN_DIGIT(e, (bn_t)65537, ndigits);
    bn_assign_2exp(t, pbits-1, pdigits);
    bn_assign_2exp(u, pbits-2, pdigits);
    bn_add(t, t, u, pdigits);
    BN_ASSIGN_DIGIT(v, 1, pdigits);
    bn_sub(v, t, v, pdigits);
    bn_add(u, u, v, pdigits);
    BN_ASSIGN_DIGIT(v, 2, pdigits);
    do {
        status = generate_prime(p, t, u, v, pdigits);
        if(status != 0) {
            return status;
        }
    } while(!rsa_filter(p, pdigits, e, 1));
    bn_assign_2exp(t, qbits-1, pdigits);
    bn_assign_2exp(u, qbits-2, pdigits);
    bn_add(t, t, u, pdigits);
    BN_ASSIGN_DIGIT(v, 1, pdigits);
    bn_sub(v, t, v, pdigits);
    bn_add(u, u, v, pdigits);
    BN_ASSIGN_DIGIT(v, 2, pdigits);
    do {
        status = generate_prime(q, t, u, v, pdigits);
        if(status != 0) {
            return status;
        }
    } while(!rsa_filter(q, pdigits, e, 1));
    if(bn_cmp(p, q, pdigits) < 0) {
        bn_assign(t, p, pdigits);
        bn_assign(p, q, pdigits);
        bn_assign(q, t, pdigits);
    }
    bn_mul(n, p, q, pdigits);
    bn_mod_inv(q_inv, q, p, pdigits);
    BN_ASSIGN_DIGIT(t, 1, pdigits);
    bn_sub(p_minus1, p, t, pdigits);
    bn_sub(q_minus1, q, t, pdigits);
    bn_mul(phi_n, p_minus1, q_minus1, pdigits);
    bn_mod_inv(d, e, phi_n, ndigits);
    bn_mod(dp, d, ndigits, p_minus1, pdigits);
    bn_mod(dq, d, ndigits, q_minus1, pdigits);
    pk->bits = sk->bits = key_bits;
    bn_encode(pk->modulus, RSA_MAX_MODULUS_LEN, n, ndigits);
    bn_encode(pk->exponent, RSA_MAX_MODULUS_LEN, e, 1);
    memcpy((uint8_t *)sk->modulus, (uint8_t *)pk->modulus, RSA_MAX_MODULUS_LEN);
    memcpy((uint8_t *)sk->public_exponet, (uint8_t *)pk->exponent, RSA_MAX_MODULUS_LEN);
    bn_encode(sk->exponent, RSA_MAX_MODULUS_LEN, d, ndigits);
    bn_encode(sk->prime1, RSA_MAX_PRIME_LEN, p, pdigits);
    bn_encode(sk->prime2, RSA_MAX_PRIME_LEN, q, pdigits);
    bn_encode(sk->prime_exponent1, RSA_MAX_PRIME_LEN, dp, pdigits);
    bn_encode(sk->prime_exponent2, RSA_MAX_PRIME_LEN, dq, pdigits);
    bn_encode(sk->coefficient, RSA_MAX_PRIME_LEN, q_inv, pdigits);
    memset((uint8_t *)d, 0, sizeof(d));
    memset((uint8_t *)dp, 0, sizeof(dp));
    memset((uint8_t *)dq, 0, sizeof(dq));
    memset((uint8_t *)p, 0, sizeof(p));
    memset((uint8_t *)q, 0, sizeof(q));
    memset((uint8_t *)phi_n, 0, sizeof(phi_n));
    memset((uint8_t *)q_inv, 0, sizeof(q_inv));
    memset((uint8_t *)p_minus1, 0, sizeof(p_minus1));
    memset((uint8_t *)q_minus1, 0, sizeof(q_minus1));
    memset((uint8_t *)t, 0, sizeof(t));
    return 0;
}
int rsa_public_encrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_pk_t *pk){
    int status;
    uint8_t byte, pkcs_block[RSA_MAX_MODULUS_LEN];
    uint32_t i, modulus_len;
    modulus_len = (pk->bits + 7) / 8;
    if(in_len + 11 > modulus_len) {
        return ERR_WRONG_LEN;
    }
    pkcs_block[0] = 0;
    pkcs_block[1] = 2;
    for(i=2; i<modulus_len-in_len-1; i++) {
        do {
            generate_rand(&byte, 1);
        } while(byte == 0);
        pkcs_block[i] = byte;
    }
    pkcs_block[i++] = 0;
    memcpy((uint8_t *)&pkcs_block[i], (uint8_t *)in, in_len);
    status = public_block_operation(out, out_len, pkcs_block, modulus_len, pk);
    byte = 0;
    memset((uint8_t *)pkcs_block, 0, sizeof(pkcs_block));
    return status;
}
int rsa_public_decrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_pk_t *pk){
    int status;
    uint8_t pkcs_block[RSA_MAX_MODULUS_LEN];
    uint32_t i, modulus_len, pkcs_block_len;
    modulus_len = (pk->bits + 7) / 8;
    if(in_len > modulus_len)
        return ERR_WRONG_LEN;
    status = public_block_operation(pkcs_block, &pkcs_block_len, in, in_len, pk);
    if(status != 0)
        return status;
    if(pkcs_block_len != modulus_len)
        return ERR_WRONG_LEN;
    if((pkcs_block[0] != 0) || (pkcs_block[1] != 1))
        return ERR_WRONG_DATA;
    for(i=2; i<modulus_len-1; i++) {
        if(pkcs_block[i] != 0xFF)   break;
    }
    if(pkcs_block[i++] != 0)
        return ERR_WRONG_DATA;
    *out_len = modulus_len - i;
    if(*out_len + 11 > modulus_len)
        return ERR_WRONG_DATA;
    memcpy((uint8_t *)out, (uint8_t *)&pkcs_block[i], *out_len);
    memset((uint8_t *)pkcs_block, 0, sizeof(pkcs_block));
    return status;
}
int rsa_private_encrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_sk_t *sk){
    int status;
    uint8_t pkcs_block[RSA_MAX_MODULUS_LEN];
    uint32_t i, modulus_len;
    modulus_len = (sk->bits + 7) / 8;
    if(in_len + 11 > modulus_len)
        return ERR_WRONG_LEN;
    pkcs_block[0] = 0;
    pkcs_block[1] = 1;
    for(i=2; i<modulus_len-in_len-1; i++) {
        pkcs_block[i] = 0xFF;
    }
    pkcs_block[i++] = 0;
    memcpy((uint8_t *)&pkcs_block[i], (uint8_t *)in, in_len);
    status = private_block_operation(out, out_len, pkcs_block, modulus_len, sk);
    memset((uint8_t *)pkcs_block, 0, sizeof(pkcs_block));
    return status;
}
int rsa_private_decrypt(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_sk_t *sk){
    int status;
    uint8_t pkcs_block[RSA_MAX_MODULUS_LEN];
    uint32_t i, modulus_len, pkcs_block_len;
    modulus_len = (sk->bits + 7) / 8;
    if(in_len > modulus_len){
        return ERR_WRONG_LEN;
    }
    status = private_block_operation(pkcs_block, &pkcs_block_len, in, in_len, sk);
    if(status != 0)
        return status;
    if(pkcs_block_len != modulus_len)
        return ERR_WRONG_LEN;
    if((pkcs_block[0] != 0) || (pkcs_block[1] != 2))
        return ERR_WRONG_DATA;
    for(i=2; i<modulus_len-1; i++) {
        if(pkcs_block[i] == 0)  break;
    }
    i++;
    if(i >= modulus_len)
        return ERR_WRONG_DATA;
    *out_len = modulus_len - i;
    if(*out_len + 11 > modulus_len)
        return ERR_WRONG_DATA;
    memcpy((uint8_t *)out, (uint8_t *)&pkcs_block[i], *out_len);
    memset((uint8_t *)pkcs_block, 0, sizeof(pkcs_block));
    return status;
}
static int public_block_operation(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_pk_t *pk){
    uint32_t edigits, ndigits;
    bn_t c[BN_MAX_DIGITS], e[BN_MAX_DIGITS], m[BN_MAX_DIGITS], n[BN_MAX_DIGITS];
    bn_decode(m, BN_MAX_DIGITS, in, in_len);
    bn_decode(n, BN_MAX_DIGITS, pk->modulus, RSA_MAX_MODULUS_LEN);
    bn_decode(e, BN_MAX_DIGITS, pk->exponent, RSA_MAX_MODULUS_LEN);
    ndigits = bn_digits(n, BN_MAX_DIGITS);
    edigits = bn_digits(e, BN_MAX_DIGITS);
    if(bn_cmp(m, n, ndigits) >= 0) {
        return ERR_WRONG_DATA;
    }
    bn_mod_exp(c, m, e, edigits, n, ndigits);
    *out_len = (pk->bits + 7) / 8;
    bn_encode(out, *out_len, c, ndigits);
    memset((uint8_t *)c, 0, sizeof(c));
    memset((uint8_t *)m, 0, sizeof(m));
    return 0;
}
static int private_block_operation(uint8_t *out, uint32_t *out_len, uint8_t *in, uint32_t in_len, rsa_sk_t *sk){
    uint32_t cdigits, ndigits, pdigits;
    bn_t c[BN_MAX_DIGITS], cp[BN_MAX_DIGITS], cq[BN_MAX_DIGITS];
    bn_t dp[BN_MAX_DIGITS], dq[BN_MAX_DIGITS], mp[BN_MAX_DIGITS], mq[BN_MAX_DIGITS];
    bn_t n[BN_MAX_DIGITS], p[BN_MAX_DIGITS], q[BN_MAX_DIGITS], q_inv[BN_MAX_DIGITS], t[BN_MAX_DIGITS];
    bn_decode(c, BN_MAX_DIGITS, in, in_len);
    bn_decode(n, BN_MAX_DIGITS, sk->modulus, RSA_MAX_MODULUS_LEN);
    bn_decode(p, BN_MAX_DIGITS, sk->prime1, RSA_MAX_PRIME_LEN);
    bn_decode(q, BN_MAX_DIGITS, sk->prime2, RSA_MAX_PRIME_LEN);
    bn_decode(dp, BN_MAX_DIGITS, sk->prime_exponent1, RSA_MAX_PRIME_LEN);
    bn_decode(dq, BN_MAX_DIGITS, sk->prime_exponent2, RSA_MAX_PRIME_LEN);
    bn_decode(q_inv, BN_MAX_DIGITS, sk->coefficient, RSA_MAX_PRIME_LEN);
    cdigits = bn_digits(c, BN_MAX_DIGITS);
    ndigits = bn_digits(n, BN_MAX_DIGITS);
    pdigits = bn_digits(p, BN_MAX_DIGITS);
    if(bn_cmp(c, n, ndigits) >= 0)
        return ERR_WRONG_DATA;
    bn_mod(cp, c, cdigits, p, pdigits);
    bn_mod(cq, c, cdigits, q, pdigits);
    bn_mod_exp(mp, cp, dp, pdigits, p, pdigits);
    bn_assign_zero(mq, ndigits);
    bn_mod_exp(mq, cq, dq, pdigits, q, pdigits);
    if(bn_cmp(mp, mq, pdigits) >= 0) {
        bn_sub(t, mp, mq, pdigits);
    } else {
        bn_sub(t, mq, mp, pdigits);
        bn_sub(t, p, t, pdigits);
    }
    bn_mod_mul(t, t, q_inv, p, pdigits);
    bn_mul(t, t, q, pdigits);
    bn_add(t, t, mq, ndigits);
    *out_len = (sk->bits + 7) / 8;
    bn_encode(out, *out_len, t, ndigits);
    memset((uint8_t *)c, 0, sizeof(c));
    memset((uint8_t *)cp, 0, sizeof(cp));
    memset((uint8_t *)cq, 0, sizeof(cq));
    memset((uint8_t *)dp, 0, sizeof(dp));
    memset((uint8_t *)dq, 0, sizeof(dq));
    memset((uint8_t *)mp, 0, sizeof(mp));
    memset((uint8_t *)mq, 0, sizeof(mq));
    memset((uint8_t *)p, 0, sizeof(p));
    memset((uint8_t *)q, 0, sizeof(q));
    memset((uint8_t *)q_inv, 0, sizeof(q_inv));
    memset((uint8_t *)t, 0, sizeof(t));
    return 0;
}
static int rsa_filter(bn_t *a, uint32_t adigits, bn_t *b, uint32_t bdigits){
    int status;
    bn_t a_minus1[BN_MAX_DIGITS], t[BN_MAX_DIGITS];
    BN_ASSIGN_DIGIT(t, 1, adigits);
    bn_sub(a_minus1, a, t, adigits);
    status = relatively_prime(a_minus1, adigits, b, bdigits);
    memset((uint8_t *)a_minus1, 0, sizeof(a_minus1));
    return status;
}
static int relatively_prime(bn_t *a, uint32_t adigits, bn_t *b, uint32_t bdigits){
    int status;
    bn_t t[BN_MAX_DIGITS], u[BN_MAX_DIGITS];
    bn_assign_zero(t, adigits);
    bn_assign(t, b, bdigits);
    bn_gcd(t, a, t, adigits);
    BN_ASSIGN_DIGIT(u, 1, adigits);
    status = BN_EQUAL(t, u, adigits);
    memset((uint8_t *)t, 0, sizeof(t));
    return status;
}
#ifndef __PRIME_H__
#define __PRIME_H__
#include <stdint.h>
#endif  
#include <string.h>
#include <stdlib.h>
#include <time.h>
const uint8_t SMALL_PRIMES[] = {3, 5, 7, 11};
#define SMALL_PRIME_COUNT 4
static int probable_prime(bn_t *a, uint32_t digits);
static int small_factor(bn_t *a, uint32_t digits);
static int fermat_test(bn_t *a, uint32_t digits);
void initialize_rand(void){
    srand((unsigned)time(NULL));
}
void generate_rand(uint8_t *block, uint32_t block_len){
    uint32_t i;
    for(i=0; i<block_len; i++) {
        block[i] = rand();
    }
}
int generate_prime(bn_t *a, bn_t *lower, bn_t *upper, bn_t *d, uint32_t digits){
    uint8_t block[BN_MAX_DIGITS*BN_DIGIT_LEN];
    bn_t t[BN_MAX_DIGITS], u[BN_MAX_DIGITS];
    generate_rand(block, digits*BN_DIGIT_LEN);
    bn_decode(a, digits, block, digits*BN_DIGIT_LEN);
    bn_sub(t, upper, lower, digits);
    BN_ASSIGN_DIGIT(u, 1, digits);
    bn_add(t, t, u, digits);
    bn_mod(a, a, digits, t, digits);
    bn_add(a, a, lower, digits);
    bn_mod(t, a, digits, d, digits);
    bn_sub(a, a, t, digits);
    bn_add(a, a, u, digits);
    if(bn_cmp(a, lower, digits) < 0) {
        bn_add(a, a, d, digits);
    }
    if(bn_cmp(a, upper, digits) > 0) {
        bn_sub(a, a, d, digits);
    }
    bn_assign(t, upper, digits);
    bn_sub(t, t, d, digits);
    while(!probable_prime(a, digits)) {
        if(bn_cmp(a, t, digits) > 0) {
            return ERR_WRONG_DATA;
        }
        bn_add(a, a, d, digits);
    }
    return 0;
}
static int probable_prime(bn_t *a, uint32_t digits){
    return (!small_factor(a, digits) && fermat_test(a, digits));
}
static int small_factor(bn_t *a, uint32_t digits){
    int status;
    bn_t t[1];
    uint32_t i;
    status = 0;
    for(i=0; i<SMALL_PRIME_COUNT; i++) {
        BN_ASSIGN_DIGIT(t, SMALL_PRIMES[i], 1);
        if((digits == 1) && BN_EQUAL(a, t, 1)) {
            break;
        }
        bn_mod(t, a, digits, t, 1);
        if(bn_is_zero(t, 1)) {
            status = 1;
            break;
        }
    }
    i = 0;
    memset((uint8_t *)t, 0, sizeof(t));
    return status;
}
static int fermat_test(bn_t *a, uint32_t digits){
    int status;
    bn_t t[BN_MAX_DIGITS], u[BN_MAX_DIGITS];
    BN_ASSIGN_DIGIT(t, 2, digits);
    bn_mod_exp(u, t, a, digits, a, digits);
    status = BN_EQUAL(t, u, digits);
    memset((uint8_t *)u, 0, sizeof(u));
    return status;
}
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void print_bn_arr(char *TAG, uint8_t *array, int len){
    int i = 0;
    printf("%s", TAG);
    while(array[i] == 0) {
        i++;
    }
    for(; i<len; i++) {
        printf("%02X", array[i]);
    }
    printf("\n");
}
void print_array(char *TAG, uint8_t *array, int len){
    int i;
    printf("%s[%d]: ", TAG, len);
    for(i=0; i<len; i++) {
        printf("%02X", array[i]);
    }
    printf("\n");
}
void print_pk(rsa_pk_t *pk){
    printf("PK[%d]:\n", pk->bits);
    print_bn_arr("  modulus: ", pk->modulus, RSA_MAX_MODULUS_LEN);
    print_bn_arr("  exponent: ", pk->exponent, RSA_MAX_MODULUS_LEN);
}
void print_sk(rsa_sk_t *sk){
    printf("SK[%d]:\n", sk->bits);
    print_bn_arr("  modulus: ", sk->modulus, RSA_MAX_MODULUS_LEN);
    print_bn_arr("  public_exponet: ", sk->public_exponet, RSA_MAX_MODULUS_LEN);
    print_bn_arr("  exponent: ", sk->exponent, RSA_MAX_MODULUS_LEN);
    print_bn_arr("  prime1: ", sk->prime1, RSA_MAX_PRIME_LEN);
    print_bn_arr("  prime2: ", sk->prime2, RSA_MAX_PRIME_LEN);
    print_bn_arr("  primeExponent1: ", sk->prime_exponent1, RSA_MAX_PRIME_LEN);
    print_bn_arr("  primeExponent2: ", sk->prime_exponent2, RSA_MAX_PRIME_LEN);
    print_bn_arr("  coefficient: ", sk->coefficient, RSA_MAX_PRIME_LEN);
}
static void write_sk(char *file, rsa_sk_t *sk){
    FILE *fp;
    fp = fopen(file, "w");
    if(fp == NULL) {
        printf("CAN NOT OPEN FILE\n");
        return;
    }
    fwrite((uint8_t *)sk, 1, sizeof(rsa_sk_t), fp);
    fclose(fp);
}
char* save_pk_base64(rsa_pk_t pk){
    char v[516];
    char *r;
    for (int i = 0; i < 516; ++i){
        v[i] = ((unsigned char*)&pk)[i];
    }
    r = base64_encode(v, 516);
    return r;
}
char* save_sk_base64(rsa_sk_t sk){
    char v[1412];
    char *r;
    for (int i = 0; i < 1412; ++i){
        v[i] = ((unsigned char*)&sk)[i];
    }
    r = base64_encode(v, 1412);
    return r;
}
rsa_pk_t load_pk_from_base64(char* s){
    char *r;
    rsa_pk_t pk;
    r = base64_decode(s);
    for (int i = 0; i < 516; ++i){
        ((unsigned char*)&pk)[i] = r[i];
    }
    return pk;
}
rsa_sk_t load_sk_from_base64(char* s){
    char *r;
    rsa_sk_t sk;
    r = base64_decode(s);
    for (int i = 0; i < 1412; ++i){
        ((unsigned char*)&sk)[i] = r[i];
    }
    return sk;
}
// 通过对 char* 数据切割，生成目标长度生成固定分段，然后返回 char* 的加密数据
unsigned char* rsa_encrypt(char* edata, int datalen, rsa_pk_t *pk, int* edatalen){
    int splitnum, onepeace, allength, onesplit;
    int ret;
    int keylen;
    unsigned char *res;
    uint8_t output[256];
    uint8_t input[256];
    unsigned int outputLen;
    keylen = pk->bits;
    onesplit = keylen/8-11;
    onepeace = keylen/8;
    splitnum = (datalen+(onesplit-1))/onesplit;
    allength = onepeace * splitnum;
    *edatalen = allength;
    res = malloc(allength);
    unsigned int left, right;
    for (int i = 0; i < splitnum; ++i) {
        memset(input, 0, 256);
        left = i*onesplit;
        right = (i+1)*onesplit<datalen ? (i+1)*onesplit : datalen;
        for (int j = left; j < right; ++j) {
            input[j-left] = edata[j];
        }
        ret = rsa_public_encrypt(output, &outputLen, input, right-left, pk);
        left = i*onepeace;
        right = (i+1)*onepeace<allength ? (i+1)*onepeace : allength;
        for (int j = left; j < right; ++j) {
            res[j] = output[j-left];
        }
        printf("enc: %d/%d\n", i+1, splitnum); // 显示进度
    }
    return res;
}
unsigned char* rsa_decrypt(char* ddata, int datalen, rsa_sk_t *sk, int* ddatalen){
    int splitnum, onepeace, tplength, onesplit;
    int allength = 0;
    int keylen;
    unsigned int outputLen;
    unsigned char *res;
    uint8_t output[256];
    uint8_t input[256];
    keylen = sk->bits;
    onesplit = keylen/8-11;
    onepeace = keylen/8;
    splitnum = datalen/onepeace;
    tplength = onesplit * splitnum;
    res = malloc(tplength);
    unsigned int left, right;
    for (int i = 0; i < splitnum; ++i) {
        memset(input, 0, 256);
        left = i*onepeace;
        right = (i+1)*onepeace;
        for (int j = left; j < right; ++j) {
            input[j-left] = ddata[j];
        }
        rsa_private_decrypt(output, &outputLen, input, onepeace, sk);
        *ddatalen += outputLen;
        left = i*onesplit;
        right = (i+1)*onesplit;
        for (int j = left; j < right; ++j) {
            res[j] = output[j-left];
        }
        printf("dec: %d/%d\n", i+1, splitnum); // 显示进度
    }
    return res;
}
int get_file_size(FILE * file_handle){
    unsigned int current_read_position = ftell(file_handle);
    int file_size;
    fseek(file_handle, 0, SEEK_END);
    file_size = ftell(file_handle);
    fseek(file_handle, current_read_position, SEEK_SET);
    return file_size;
}



static int test_enc_dec_long_char_list(void){
    // 长的 char* 的加解密基本上也同等于对文件的加解密了，因为本质上读取文件后的数据就可以用 char* 和一个长度来表示。
    int edatalen = 0;
    int ddatalen = 0;
    char *encdata, *decdata, *temp;
    char *b64_pk = "AAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMm9HZKm2be/sZKiepYFEVBuoKRtIlv5r61q3vv/ftuUyR1iLYLgHNh+DUJ1ey2aqZqtoQt9tkOoAR35IM7oq0kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAB";
    char *b64_sk = "AAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMm9HZKm2be/sZKiepYFEVBuoKRtIlv5r61q3vv/ftuUyR1iLYLgHNh+DUJ1ey2aqZqtoQt9tkOoAR35IM7oq0kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfhNXMPhfJeuB0Q8Dp0/Bc0+/yyJ9D5fqR2l7s2cH47dpMsUmw314Q/t1ECPpA0J3pWxqHzIQr9EtDsdUd+a6AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/K8tIavNY1Bfhm9qiaHzXz4g1ZA4rVAUVW+Tzd7FkJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAyeb0yEEm+LLiafqJDB99Twl7uu1vxqAmR/gZym6JkEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABz9X8q/HAK87KnL5Y2TNhFTzB1OJtAftu6oXkPvNN+cQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMaki4sGxvADF84LJ5Ec3i3H98sW1lVGtcMzLzTCgmfBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAApNCySAGU65NiL6dTOKv9UHXBy0h7oYhUrnfglRvP2Dz=";
    char *endata = "1234567890123456789012345612345678901234567890123456123456789012345678901234561234567890123456789012345612345678901234567890123456";
    // rsa_pk_t 和 rsa_sk_t 对象内都包含了 keylen 的秘钥长度信息，所以加载的时候
    rsa_pk_t pk = load_pk_from_base64(b64_pk);
    rsa_sk_t sk = load_sk_from_base64(b64_sk);
    encdata = rsa_encrypt(endata, strlen(endata), &pk, &edatalen);
    decdata = rsa_decrypt(encdata, edatalen, &sk, &ddatalen);
    print_array("ORI DATA(HEX):", endata, strlen(endata));
    print_array("ENC DATA(HEX):", encdata, edatalen);
    print_array("DEC DATA(HEX):", decdata, ddatalen);
    temp = malloc(ddatalen+1);
    memset(temp, 0, ddatalen+1);
    memcpy(temp, decdata, ddatalen);
    printf("ORI: %s\n", endata);
    printf("DEC: %s\n", temp);
}
static int test_save_struct_in_base64(void){
    int keylen = 512;
    rsa_pk_t pk;
    rsa_sk_t sk;
    rsa_generate_keys(&pk, &sk, keylen);
    char *b64_pk;
    char *b64_sk;
    b64_pk = save_pk_base64(pk);
    b64_sk = save_sk_base64(sk);
    printf("pk_base64: %s\n\n", b64_pk);
    printf("sk_base64: %s\n\n", b64_sk);
    return 0;
}
static int test_load_struct_from_base64(void){
    char *b64_pk = "AAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMm9HZKm2be/sZKiepYFEVBuoKRtIlv5r61q3vv/ftuUyR1iLYLgHNh+DUJ1ey2aqZqtoQt9tkOoAR35IM7oq0kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAB";
    char *b64_sk = "AAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMm9HZKm2be/sZKiepYFEVBuoKRtIlv5r61q3vv/ftuUyR1iLYLgHNh+DUJ1ey2aqZqtoQt9tkOoAR35IM7oq0kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfhNXMPhfJeuB0Q8Dp0/Bc0+/yyJ9D5fqR2l7s2cH47dpMsUmw314Q/t1ECPpA0J3pWxqHzIQr9EtDsdUd+a6AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/K8tIavNY1Bfhm9qiaHzXz4g1ZA4rVAUVW+Tzd7FkJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAyeb0yEEm+LLiafqJDB99Twl7uu1vxqAmR/gZym6JkEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABz9X8q/HAK87KnL5Y2TNhFTzB1OJtAftu6oXkPvNN+cQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMaki4sGxvADF84LJ5Ec3i3H98sW1lVGtcMzLzTCgmfBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAApNCySAGU65NiL6dTOKv9UHXBy0h7oYhUrnfglRvP2Dz=";
    rsa_pk_t pk = load_pk_from_base64(b64_pk);
    rsa_sk_t sk = load_sk_from_base64(b64_sk);
    print_pk(&pk);
    print_sk(&sk);
    uint8_t output[256];
    uint8_t endata[256] = "test1111";
    uint8_t dedata[256];
    unsigned int outputLen, dedataLen, endataLen;
    endataLen = strlen(endata);
    rsa_public_encrypt (output, &outputLen, endata, endataLen, &pk);
    rsa_private_decrypt(dedata, &dedataLen, output, outputLen, &sk);
    print_array("=== PK  ENC", output, outputLen);
    print_array("=== src MSG", endata, endataLen);
    print_array("=== SK  DEC", dedata, dedataLen);
    char *temp;
    temp = malloc(dedataLen+1);
    memset(temp, 0, dedataLen+1);
    memcpy(temp, dedata, dedataLen);
    printf("DECLEN: %d; DEC: %s\n", dedataLen, temp);
    return 0;
}
static int test_enc_dec_in_onepeace(void){
    int ret;
    int keylen = 1024; // 512/1024/2048
    rsa_pk_t pk;
    rsa_sk_t sk;
    // 由于使用了 pksc1 ，padding 占用了 11 个位置，所以，加密数据的长度只能为 (keylen/8)-11。
    // 例如秘钥长度为 512 的就只能加密的字符长度为 (512/8)-11=53 。1024->117。2048->245。
    uint8_t endata[256] = "==12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890==";
    uint8_t output[256];
    uint8_t dedata[256];
    unsigned int outputLen, endataLen, dedataLen;
    // 生成公钥和私钥，建议使用时将公私钥保存成 base64 字符串，这样非常方便复制粘贴使用
    // 上面也提供了保存秘钥到 base64 字符串的函数，也有将 秘钥base64 字符串读取成数据结构使用的方式，使用起来也比较方便
    ret = rsa_generate_keys(&pk, &sk, keylen);
    print_sk(&sk);
    endataLen = strlen((const char *)endata);
 // rsa_public_encrypt (output, &outputLen, endata, endataLen, &sk); // 使用 sk 也能加密因为 sk 包含了公钥
    rsa_public_encrypt (output, &outputLen, endata, endataLen, &pk);
    rsa_private_decrypt(dedata, &dedataLen, output, outputLen, &sk);
    print_array("=== PK  ENC", output, outputLen);
    print_array("=== src MSG", endata, endataLen);
    print_array("=== SK  DEC", dedata, dedataLen);
    char *temp;
    temp = malloc(dedataLen+1);
    memset(temp, 0, dedataLen+1);
    memcpy(temp, dedata, dedataLen);
    printf("DECLEN: %d; DEC: %s\n", dedataLen, temp);
    return 0;
}
static int test_all_enc_dec_a_file(void){
    int keylen = 1024;
    rsa_pk_t pk;
    rsa_sk_t sk;
    char *b64_pk;
    char *b64_sk;

    // // 初始化秘钥
    // rsa_generate_keys(&pk, &sk, keylen);
    // b64_pk = save_pk_base64(pk);
    // b64_sk = save_sk_base64(sk);
    // // 将秘钥结构体保存成base64字符串
    // printf("pk_base64: %s\n\n", b64_pk);
    // printf("sk_base64: %s\n\n", b64_sk);

    // 直接从保存的base64字符串加载秘钥，节省初始化时间
    b64_pk = "AAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuaW1hyWp0UL9NLFzcxXBEVGrT42hNqb9m57wbztxz7vdNnS0o50qBdcZ62dHFJN/VMYacpFBw1/tmBeXNvJD+2+593rJ+Zy/XV5hYRgSU7X5PuVkXBZ/bxOoagRa9VOcgxY3gsOQELvLylnrESNxdDt7aOVNa6l80lFkAweYU50AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAB";
    b64_sk = "AAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuaW1hyWp0UL9NLFzcxXBEVGrT42hNqb9m57wbztxz7vdNnS0o50qBdcZ62dHFJN/VMYacpFBw1/tmBeXNvJD+2+593rJ+Zy/XV5hYRgSU7X5PuVkXBZ/bxOoagRa9VOcgxY3gsOQELvLylnrESNxdDt7aOVNa6l80lFkAweYU50AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC3RJAsp5C6JXCDaT54eRxMdZwxf7aLllS8IS5oEH3tPh9GV/XPoyJN+6f5zM3N0UIdNSf8u8r5DaUmxPshYg6a5IVHC5/R2trJmB+twh31eNITvD2ql9rXI1ggl5h2WQQFWWkYkwZthKBwgmbYlN5BgzWnzoicodSytZpn/ks8XQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADqZFdL9pFX8U3tZqHrUMcgyt3jwUWSkZN9HZTZ/PFlupiaNDqaTSlpIMTv2sBJc1duEOnToMkRoLB2uOOBeoN/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMrC/gyOOg+xWecam7a+D4+pvsOYWoA4RHYQHw/T+5sgU6lIMwrtfNej283Z/9rTACD6L/pGh8uXV95kNYR/RuMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsJTpg2v9cXB0Ud6ZK6uOaPEMm1H2tQYBRCfuBQ/fWNFrt/iTEb4B7ZZnZ3+4j11ax6vsTKf78tDJQJfnpZsDxwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnIyA6eDGI2ejKjP5FdcY3KsKhqoS9fx7n0xDL01Ubik/buw3vLAwO65f/0fZq3JOHygL8wiRwDdRuHtWdr5uVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwHTInkycwUT1h8Iso4UVpiJzk0vpR8So+VTdEYELzxcaBiqVpzDrGD2a6PZvp0zdh7XBe2VTIRdkrkw0zpuf=";
    pk = load_pk_from_base64(b64_pk);
    sk = load_sk_from_base64(b64_sk);

    // 下面是将文件 filename 加密后保存成 savename 文件，名字自行调整进行测试
    int filesize, edatalen, ddatalen;
    char *filename = "./test.rar";
    char *fildata, *encdata, *decdata;
    FILE *fp;
    fp = fopen(filename, "rb");
    filesize = get_file_size(fp);
    fildata = (char *)malloc(filesize);
    fread(fildata, 1, filesize, fp);
    fclose(fp);

    encdata = rsa_encrypt(fildata, filesize, &pk, &edatalen);
 // decdata = rsa_decrypt(encdata, edatalen, &sk, &ddatalen); // 解密

    FILE *tp;
    char *savename = "./asdfasdf";
    tp = fopen(savename, "wb");
    fwrite(encdata, edatalen, 1, tp);
    fclose(tp);
}








int main(int argc, char const *argv[]){
    // test_save_struct_in_base64();
    // test_load_struct_from_base64();
    test_enc_dec_long_char_list();
    // test_enc_dec_in_onepeace();
    // test_all_enc_dec_a_file(); // 使用时请关注这个函数里面的实现
    return 0;
}