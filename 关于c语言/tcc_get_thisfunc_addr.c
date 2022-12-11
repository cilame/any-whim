#include <stdio.h>
#include <windows.h>

// get_thisfunc_realaddr 用来获取这个函数自己的地址
// 对于一些 shellcode 来说会有比较大的用处。
// gcc/tcc 32/64 通用的函数

DWORD get_thisfunc_realaddr(){
    // 这个函数非常娇贵，一丝一毫也不能改。
    #ifdef _WIN64
    int _addr;
    asm("mov $., %0;":"=a"(_addr));
        #ifdef __MINGW32__
        return (DWORD)_addr-0x8; 
        #else
        return (DWORD)_addr-0xb;
        #endif
    #else
    int _addr;
    asm("mov $., %0;":"=a"(_addr));
        #ifdef __MINGW32__
        return (DWORD)_addr-0x6;
        #else
        return (DWORD)_addr-0xa;
        #endif
    #endif
}

int main(){
    printf("%x\n", get_thisfunc_realaddr);
    printf("%x\n", get_thisfunc_realaddr());
}
