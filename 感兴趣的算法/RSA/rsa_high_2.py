# rsa 高位攻击基础
# https://sagecell.sagemath.org/

# rsa 高位攻击，爆破处理
n = 0x9d3a1a28ecb1bd245dd86b18dc4c5b729f23778710005118836129f08e31d6516de8ab47db1b3b7f660f50d283b1e9f2c06e7836136e4c0159f5d2b05771861d3ce6aa8715932eadc1cc0f380909a1961018340f7393142f9c177b1187151f97ac8cdc4ad17fa59a0f39d192af555f27de9cc800846eb2ca6ce78f87c0c0fbf47828328392b81771af624389fd779d130d80739bb7a608961125ba3f1800c766440fa70bfd3f834294d47d7ed9cfffd6d14ae18310f6c1d6d8f88b6c5d72a0b45608b4e21bbb8e314220ed7a2d6a8c95454e571c71b50f1d6a823778ca47131f5b889a1ed1957248bee8c4ac66872a5fd58a121560a27bad4958f1c763f2ffddL
px:"(p>>?)<<?" = 0xda5df16f286dbc825cd0c8ee48aa26ac27338a75172c5b92351f14d083216f7e91b9355e27cf930646fbbda6058dec3c4ddf751f36df5556359fbe671f9b947b4c79cadfdbb27b00
c = 0x1f2deea59244b14e53c72465febc2064172a35245842fa83ebff313344bed35ee8af8c3f8f61e6f498fa1fd35e63998a573d7717905f72ec01de0b0529eaab10eb0b0c2ca06e9d6e4245e748fd74f4f756a86e379559793389a3ae6c421d51bb78331a487fc3c3e68971e3e26991ab34ce2a2c07ffd5a5a1e215e766b51fb2d6aab63c2dafa3c87d0a5eb79b634740e1fca7a727de997958839bda684e19acad93cae4abfd1c8cc3684419f83696fe4840f3253e7c038adb13a1382667cf7e17ef55c1e950ea474594102e660e36a23bfd3fd830d1c18a434d0b34bed98308399a894dcab909d68bcab7c7ac990974a4f6ed7d612abb7044f6734eaaebcdc0b5L
e = 0x10001
pbits = len(bin(n)[2:]) // 2
for i in range(0,127):
    p4 = px + int(hex(i),16)
    kbits = pbits - p4.nbits()
    print(i, pbits, p4.nbits(), kbits) # 需要爆破的位数
    p4 = p4 << kbits
    PR.<x> = PolynomialRing(Zmod(n))
    f = x + p4
    roots = f.small_roots(X=2^kbits, beta=0.4)
    if roots:
        p = p4 + int(roots[0])
        print("p: ", hex(int(p)))
        assert n % p == 0
        q = n // int(p)
        print("q: ", hex(int(q)))
        d = inverse_mod(e, (p-1)*(q-1))
        m = int(pow(c, d, n))
        print(bytes.fromhex(hex(m)[2:]))
        break
