import base64
def rc4(text, key = b'default-key', mode = "encode"):
    if mode == "decode": text = base64.b64decode(text)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i%len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i, j = 0, 0
    R = []
    for c in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = c ^ (S[(S[i] + S[j]) % 256])
        R.append(t)
    if mode == "encode": return base64.b64encode(bytes(R))
    return bytes(R)

if __name__ == '__main__':
    text  = '123'.encode()
    key   = '123'.encode()
    encd = rc4(text,key,mode='encode');print(encd)
    decd = rc4(encd,key,mode='decode');print(decd)