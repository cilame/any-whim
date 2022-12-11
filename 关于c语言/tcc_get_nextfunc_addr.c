#include <stdio.h>
#include <windows.h>

// get_nextfunc_realaddr 用来获取这个函数后面一个函数的绝对地址
// 对于一些 shellcode 来说会有比较大的用处。
// gcc/tcc 32/64 通用的函数

void AdjustPE();
DWORD get_nextfunc_realaddr(){
    // 这个函数非常娇贵，一丝一毫也不能改。
    #ifdef _WIN64
    int _addr;
    asm("mov $., %0;":"=a"(_addr));
        #ifdef __MINGW32__
        return (DWORD)_addr+0x14; 
        #else
        return (DWORD)_addr-0xb + 0x28;
        #endif
    #else
    int _addr;
    asm("mov $., %0;":"=a"(_addr));
        #ifdef __MINGW32__
        return (DWORD)_addr-0x6 + 0x16;
        #else
        return (DWORD)_addr-0xa + 0x1d;
        #endif
    #endif
}
void AdjustPE() {
}

int main(){
    printf("%x\n", AdjustPE);
    printf("%x\n", get_nextfunc_realaddr());
}
