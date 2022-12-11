// 编译成 dll 提供给 python 调用(.\build_golang_to_dll_4_python.go)
// go build -buildmode=c-shared -o mydll.dll .\build_golang_to_dll_4_python.go

// 使用 python 调用该 dll(.\test.py)
// import ctypes
// s2 = ctypes.CDLL('./mydll.dll')
// add = s2.addstr
// add.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
// add.restype = ctypes.c_char_p
// Encrypt3DES = s2._Encrypt3DES
// Encrypt3DES.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
// Encrypt3DES.restype = ctypes.c_char_p
// print(add(b'asdfasdfasdf',b'asdfasdfasdf'))
// v = Encrypt3DES(b'87654321hgfedcbaopqrstuv11',b'87654321hgfedcbaopqrstuv')
// print(len(v))
// import base64
// v = base64.b64encode(v)
// print(v)

package main
 
import (
	"C"
	"bytes"
	"crypto/des"
	"crypto/cipher"
	"fmt"
	"unsafe"
)
 
func padding(src []byte,blocksize int) []byte {
	padnum:=blocksize-len(src)%blocksize
	pad:=bytes.Repeat([]byte{byte(padnum)},padnum)
	return append(src,pad...)
}
 
func unpadding(src []byte) []byte {
	n:=len(src)
	unpadnum:=int(src[n-1])
	return src[:n-unpadnum]
}
 
//export Encrypt3DES
func Encrypt3DES(src []byte,key []byte) []byte {
	fmt.Println(src, key)
	block,_:=des.NewTripleDESCipher(key)
	src=padding(src,block.BlockSize())
	blockmode:=cipher.NewCBCEncrypter(block,key[:block.BlockSize()])
	blockmode.CryptBlocks(src,src)
	return src
}

//export _Encrypt3DES
func _Encrypt3DES(src,key *C.char) *C.char {
	_src 	:= ([]byte)(C.GoString(src))
	_key 	:= ([]byte)(C.GoString(key))
	block,_ := des.NewTripleDESCipher(_key)
	_src=padding(_src,block.BlockSize())
	blockmode:=cipher.NewCBCEncrypter(block,_key[:block.BlockSize()])
	blockmode.CryptBlocks(_src,_src)
	return C.CString(C.GoString((*C.char)(unsafe.Pointer(&_src[0]))))
}


//export Decrypt3DES
func Decrypt3DES(src []byte,key []byte) []byte {
	block,_:=des.NewTripleDESCipher(key)
	blockmode:=cipher.NewCBCDecrypter(block,key[:block.BlockSize()])
	blockmode.CryptBlocks(src,src)
	src=unpadding(src)
	return src
}

//export addstr
func addstr(a,b *C.char) *C.char {
	merge := C.GoString(a) + C.GoString(b)
	return C.CString(merge)
}

func main()  {
	x:=[]byte("87654321hgfedcbaopqrstuv11")
	key:=[]byte("87654321hgfedcbaopqrstuv")
	x1:=Encrypt3DES(x,key)
	x2:=Decrypt3DES(x1,key)
	fmt.Println(x1)
	fmt.Println(x2)
	fmt.Println(string(x2))
	fmt.Println()


	_x := (*C.char)(unsafe.Pointer(&x[0]))
	_key := (*C.char)(unsafe.Pointer(&key[0]))
	s := ([]byte)(C.GoString(_x))
	v := ([]byte)(C.GoString(_key))
	fmt.Println(s, v)
	k := _Encrypt3DES(_x, _key)
	fmt.Println(k)
	r := ([]byte)(C.GoString(k))
	fmt.Println(123)
	fmt.Println(r)
	// fmt.Println(string(r))



	fmt.Println(addstr(_x,_key), 123)
}