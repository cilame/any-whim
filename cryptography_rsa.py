import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization
NoEncryption  = serialization.NoEncryption
Encoding      = serialization.Encoding
PrivateFormat = serialization.PrivateFormat
PublicFormat  = serialization.PublicFormat
load_der_public_key  = serialization.load_der_public_key
load_der_private_key = serialization.load_der_private_key
load_pem_public_key  = serialization.load_pem_public_key
load_pem_private_key = serialization.load_pem_private_key

# 自己生成的公钥私钥（可以生成二进制模式），创建保存模式字符串数据
private_key = rsa.generate_private_key( public_exponent=65537, key_size=512, backend=default_backend() )
public_key  = private_key.public_key()
encd = Encoding.PEM # (PEM/DER) # DER模式为二进制模式
pubk = public_key. public_bytes (encd, PublicFormat.PKCS1)
prik = private_key.private_bytes(encd, PrivateFormat.PKCS8, NoEncryption())
print(pubk.decode() if encd == Encoding.PEM else base64.b64encode(pubk).decode())
print(prik.decode() if encd == Encoding.PEM else base64.b64encode(prik).decode())

# 使用已有的二进制加载成公私钥，进行加解密
pubk = 'MEgCQQDJ0W1Gl1sCOOzYntjk0iHt/lIxp6ichM+QSZ0Xd6ZXSVND2lqU/NDNwHaXhck8OieIDsf5cJ9oD9/vUKQRHwDBAgMBAAE='
prik = 'MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAydFtRpdbAjjs2J7Y5NIh7f5SMaeonITPkEmdF3emV0lTQ9palPzQzcB2l4XJPDoniA7H+XCfaA/f71CkER8AwQIDAQABAkEAiekCs2paVnpv3tctf6/YX7makTPwlIRtEjw7jP3GPX41HKmTG+7d42AiD2PeW9r0wVcNHypYpfWTIfIrLoVTwQIhAP8sXWjWbb/Tdu/XHRCox5sILZTPUGHkn8sqcPIa0+4vAiEAynjPcZNguxUwKRkXsv+XxSKc+oO3G04gRmO2MCy1tA8CIFOiTttVrJL61Di34KbdKs79VzM237m2HUmRl4NCl8OxAiBcSym0igvD++qSMV/+NkhGknqgLz5ecgSAUZ+Q4jCJvQIgW7sfITectR2WccMpDlPiLrinbKFeBaQPDqdRqlPhgK0='
pubk = base64.b64decode(pubk.encode())
prik = base64.b64decode(prik.encode())
public_key  = load_der_public_key(  pubk, default_backend() )
private_key = load_der_private_key( prik, None, default_backend() )

# 测试 private_key， public_key 的加解密功能
message = b"encrypted data"
ciphertext = public_key.encrypt(  message,    padding.PKCS1v15() )
plaintext  = private_key.decrypt( ciphertext, padding.PKCS1v15() )
print(message)
print(ciphertext) # 暂时还不太清楚为什么用同样的公钥加解密得到的加密参数都不一样，但是解密是正常的，可能存在一些规定格式的处理
print(plaintext)


