// 注意，编译工具编译的环境，32位的 shellcode 只能使用 32位编译出来的工具
#include <stdio.h>
#include <windows.h>
#pragma comment(lib, "user32")
int main(int argc, char const *argv[]) {
    HANDLE hFile = CreateFileA(argv[1], GENERIC_READ, 0, NULL, OPEN_ALWAYS, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE){
        printf("error:%d\n", GetLastError());
        return -1;
    }
    DWORD dwSize;
    dwSize = GetFileSize(hFile, NULL);
    LPVOID lpAddress = VirtualAlloc(NULL, dwSize, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    if (lpAddress == NULL){
        printf("error:%d\n", GetLastError());
        CloseHandle(hFile);
        return -1;
    }
    DWORD dwRead;
    ReadFile(hFile, lpAddress, dwSize, &dwRead, 0);
    ((void(*)(void))lpAddress)();
    MessageBoxA(NULL,"this box is show means that shellcode dnot kill this execute.", "test", 0);
    return 0;
}