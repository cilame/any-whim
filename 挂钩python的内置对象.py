# 挂钩内置对象，让内置对象拥有一些更加方便的函数功能
# 比如可以实现 "asdf".md5() 直接获得该字符串的 md5 值

import ctypes
class PyObject(ctypes.Structure):
    class PyType(ctypes.Structure): pass
    ssize = ctypes.c_int64 if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_int32
    _fields_ = [
        ('ob_refcnt', ssize), 
        ('ob_type', ctypes.POINTER(PyType))
    ]
    def incref(self): self.ob_refcnt += 1
    def decref(self): self.ob_refcnt -= 1

def sign(klass, key, value):
    class SlotsProxy(PyObject):
        _fields_ = [('dict', ctypes.POINTER(PyObject))]
    _name = klass.__name__
    _dict = klass.__dict__
    proxy_dict = SlotsProxy.from_address(id(_dict))
    namespace = {}
    ctypes.pythonapi.PyDict_SetItem(
        ctypes.py_object(namespace),
        ctypes.py_object(_name),
        proxy_dict.dict,
    )
    namespace[_name][key] = value

import hashlib
def md5(self): 
    return hashlib.md5(self.encode()).hexdigest()

# 让 python 自己的内置对象自带一些更加有意思的函数
# 一般的 class 对象也可以通过这种方式实现挂钩，这种方式会比一般方式更强大，能挂钩内置对象
sign(str, 'md5', md5)

print("12345")
print("12345".md5())
