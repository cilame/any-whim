// 编写 shellcode 的代码需要注意的是
// 1) 不能直接使用函数获取函数的地址，需要通过一定的汇编获取 Kernel32 的地址
// 2) 后续找到 GetProcAddress LoadLibraryA 这两个函数的地址后续基本就需要这两个函数进行处理必要函数的获取
// 3) 使用那些函数的时候也需要注意，需要从函数声明的地方获取结构声明，所有“函数声明”不会影响生成的代码的顺序。
// 4) 另外 shellcode 的编写中注意不能使用任何全局变量，并且函数内“字符串声明”的方式只能使用 char[] 来实现，
//    这是为了避免字符串由于编译器优化被放到其他地方从而 shellcode 不完整。

#include <stdio.h>
#include <windows.h>

DWORD getKernel32();
FARPROC _GetProcAddress(HMODULE hModuleBase);
void ShellcodeStart();
void ShellcodeEntry();
void ShellcodeEnd();
void CreateShellcode();


// create shellcode bin.
int main(){
    CreateShellcode();
}
void CreateShellcode(){
    HANDLE hBin = CreateFileA("sh.bin", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
    DWORD dwSize;
    DWORD dwWrite;
    if (hBin == INVALID_HANDLE_VALUE){
        printf("%s error:%d\n", "create sh.bin fail.", GetLastError());
        return;
    }
    dwSize = (DWORD)ShellcodeEnd - (DWORD)ShellcodeStart;
    WriteFile(hBin, ShellcodeStart, dwSize, &dwWrite, NULL);
}







// shellcode
__declspec(naked) void ShellcodeStart(){
    __asm{
        call ShellcodeEntry
    }
}
// init function struct.
typedef FARPROC (WINAPI* FN_GetProcAddress)(
    HMODULE hModule,
    LPCSTR lpProcName
);
typedef HMODULE (WINAPI* FN_LoadLibraryA)(
    LPCSTR lpLibFileName
);
typedef int (WINAPI* FN_MessageBoxA)(
    HWND hWnd ,
    LPCSTR lpText,
    LPCSTR lpCaption,
    UINT uType);
typedef HANDLE (WINAPI* FN_CreateFileA)(
    LPCSTR lpFileName,
    DWORD dwDesiredAccess,
    DWORD dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD dwCreationDisposition,
    DWORD dwFlagsAndAttributes,
    HANDLE hTemplateFile
    );
typedef struct _FUNCTION {
    FN_GetProcAddress   fn_GetProcAddress;
    FN_LoadLibraryA     fn_LoadLibraryA;
    FN_CreateFileA      fn_CreateFileA;
    FN_MessageBoxA      fn_MessageBoxA;
}FUNCTION, *PFUNCTION;
void InitFunctions(PFUNCTION pFn){
    char szLoadLibraryA[] = {'L','o','a','d','L','i','b','r','a','r','y','A','\0'};
    char szUser32[] = {'u','s','e','r','3','2','\0'};
    char szMessageBoxA[] = {'M','e','s','s','a','g','e','B','o','x','A','\0'};
    char szKernel32[] = {'k','e','r','n','e','l','3','2','\0'};
    char szCreateFileA[] = {'C','r','e','a','t','e','F','i','l','e','A','\0'};
    pFn->fn_GetProcAddress  = (FN_GetProcAddress)_GetProcAddress((HMODULE)getKernel32());
    pFn->fn_LoadLibraryA    = (FN_LoadLibraryA)pFn->fn_GetProcAddress((HMODULE)getKernel32(), szLoadLibraryA);
    pFn->fn_MessageBoxA     = (FN_MessageBoxA)pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szUser32), szMessageBoxA);
    pFn->fn_CreateFileA     = (FN_CreateFileA)pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCreateFileA);
}
// work funciton
void WKCreateFile(PFUNCTION pFn){
    char szFileName[] = {'.','/','1','.','t','x','t','\0'};
    pFn->fn_CreateFileA(szFileName,GENERIC_WRITE,0,NULL,CREATE_ALWAYS,0,NULL);
}
void WKMessageBox(PFUNCTION pFn){
    pFn->fn_MessageBoxA(NULL,NULL,NULL,NULL);
}
// shellcode main
void ShellcodeEntry(){
    FUNCTION fn;
    InitFunctions(&fn);
    WKCreateFile(&fn);
    WKMessageBox(&fn);
}
// get kernel32 and get GetProcAddress.
__declspec(naked) DWORD getKernel32(){
    __asm{
        mov eax, fs:[30h]
        mov eax, [eax+0ch]
        mov eax, [eax+14h]
        mov eax, [eax]
        mov eax, [eax]
        mov eax, [eax+10h]
    }
}
FARPROC _GetProcAddress(HMODULE hModuleBase){
    PIMAGE_DOS_HEADER lpDosHeader = (PIMAGE_DOS_HEADER)hModuleBase;
    PIMAGE_NT_HEADERS32 lpNtHeader = (PIMAGE_NT_HEADERS32)((DWORD)lpDosHeader + lpDosHeader->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY lpExports;
    PDWORD  lpdwFunName;
    PWORD   lpwOrd;
    PDWORD  lpdwFunAddr;
    DWORD   dwLoop;
    FARPROC pRet;
    char* pFunName;
    if (!lpNtHeader -> OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].Size){
        return NULL;
    }

    if (!lpNtHeader -> OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress){
        return NULL;
    }
    lpExports   = (PIMAGE_EXPORT_DIRECTORY)((DWORD)hModuleBase + (DWORD)lpNtHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    lpdwFunName = (PDWORD)((DWORD)hModuleBase + (DWORD)lpExports->AddressOfNames);
    lpwOrd      = (PWORD)((DWORD)hModuleBase  + (DWORD)lpExports->AddressOfNameOrdinals);
    lpdwFunAddr = (PDWORD)((DWORD)hModuleBase + (DWORD)lpExports->AddressOfFunctions);
    dwLoop      = 0;
    pRet        = NULL;
    for (;dwLoop <= lpExports->NumberOfNames - 1; dwLoop++){
        pFunName = (char*)(lpdwFunName[dwLoop] + (DWORD)hModuleBase);
        if (    pFunName[0] == 'G' &&
                pFunName[1] == 'e' &&
                pFunName[2] == 't' &&
                pFunName[3] == 'P' &&
                pFunName[4] == 'r' &&
                pFunName[5] == 'o' &&
                pFunName[6] == 'c' &&
                pFunName[7] == 'A' &&
                pFunName[8] == 'd' &&
                pFunName[9] == 'd' &&
                pFunName[10] == 'r' &&
                pFunName[11] == 'e' &&
                pFunName[12] == 's' &&
                pFunName[13] == 's'     ){
            pRet = (FARPROC)(lpdwFunAddr[lpwOrd[dwLoop]] + (DWORD)hModuleBase);
            break;
        }
    }
    return pRet;
}
void ShellcodeEnd(){
}