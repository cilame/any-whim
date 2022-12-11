// 非常注意的是，这里的 gcc 使用的 mingw 和旧版本生成的代码不兼容。
// 这里使用的是 gcc (x86_64-win32-seh-rev0, Built by MinGW-W64 project) 8.1.0
// 对于我来说，这里的 gcc 会更好更新，能支持更新的语法，例如 naked 之类的。
// 不过在 32 位程序的交叉编译上就很有问题。不像是 tcc 那么稳。如果需要兼容 32 位的代码实现-
// 请使用 gcc 的旧版本（我之前是在devcpp下载安装后自带那个），并且使用 tcc_autocreate_she11code.c 的代码实现。
// 不过我也没想到的是，gcc 不同的版本竟然编译出的东西执行效果居然是不同的，困扰了我这个萌新一周。
//     不过不用担心的是，这个不同版本的影响只影响了汇编的部分，其他部分代码都是正常的。
//     这部分的异同你需要去找找看这里的代码和给出文件的对比代码里面的“汇编实现”究竟有什么不同即可。
// 这里的编译支持高版本的gcc（目前只编译成功64位，32位的交叉编译出现严重错误）

#include <stdio.h>
#include <windows.h>

HMODULE getKernel32();
FARPROC getProcAddress(HMODULE hModuleBase);
void ShellcodeStart();
void ShellcodeEntry();
void ShellcodeEnd();
void CreateShellcode();

// create shellcode bin.
// int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
#ifdef _WIN64
int main(int argc, char const *argv[]) {
    printf("kernel32:       %016llx\n", getKernel32());
    printf("GetProcAddress: %016llx\n", getProcAddress((HMODULE)getKernel32()));
    CreateShellcode();
}
#else
int main(int argc, char const *argv[]) {
    printf("kernel32:       %016lx\n", getKernel32());
    printf("GetProcAddress: %016lx\n", getProcAddress((HMODULE)getKernel32()));
    CreateShellcode();
}
#endif
void CreateShellcode(){
    HANDLE hBin = CreateFileA("sh.bin", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
    DWORD dwSize;
    DWORD dwWrite;
    if (hBin == INVALID_HANDLE_VALUE){
        printf("%s error:%d\n", "create sh.bin fail.", GetLastError());
        return;
    }
    dwSize = ShellcodeEnd - ShellcodeStart;
    WriteFile(hBin, ShellcodeStart, dwSize, &dwWrite, NULL);
    printf("ShellcodeSize:  %16d\n", dwWrite);
}







// shellcode
__declspec(naked) void ShellcodeStart(){
	#ifdef __MINGW32__
	asm("jmp ShellcodeEntry");
	#else
	ShellcodeEntry(); // TINYC use this
	#endif
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
    UINT uType
);
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
    pFn->fn_GetProcAddress  = (FN_GetProcAddress)getProcAddress((HMODULE)getKernel32());
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
    pFn->fn_MessageBoxA(NULL,NULL,NULL,0);
}
// shellcode main
void ShellcodeEntry(){
    FUNCTION fn;
    InitFunctions(&fn);
    WKCreateFile(&fn);
    WKMessageBox(&fn);
}
// get kernel32 and get GetProcAddress.
#ifdef _WIN64
__declspec(naked) HMODULE getKernel32(){
    asm("mov %gs:(0x60), %rax");
    asm("mov 0x18(%rax), %rax");
    asm("mov 0x20(%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov 0x20(%rax), %rax");
	#ifdef __MINGW32__
	asm("ret"); // TINYC dnot need this
	#endif
}
#else
__declspec(naked) HMODULE getKernel32(){
    asm("mov %fs:(0x30), %eax");
    asm("mov 0x0c(%eax), %eax");
    asm("mov 0x14(%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov 0x10(%eax), %eax");
	#ifdef __MINGW32__
	asm("ret"); // TINYC dnot need this
	#endif
}
#endif
FARPROC getProcAddress(HMODULE hModuleBase){
    LPBYTE lpBaseAddr = (LPBYTE)hModuleBase;
    PIMAGE_DOS_HEADER lpDosHdr = (PIMAGE_DOS_HEADER)lpBaseAddr;
    PIMAGE_NT_HEADERS pNtHdrs = (PIMAGE_NT_HEADERS)(lpBaseAddr + lpDosHdr->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY pExportDir = (PIMAGE_EXPORT_DIRECTORY)(lpBaseAddr + pNtHdrs->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    LPDWORD pNameArray = (LPDWORD)(lpBaseAddr + pExportDir->AddressOfNames);
    LPDWORD pAddrArray = (LPDWORD)(lpBaseAddr + pExportDir->AddressOfFunctions);
    LPWORD pOrdArray = (LPWORD)(lpBaseAddr + pExportDir->AddressOfNameOrdinals);
    FARPROC GetProcAddressAPI;
    for (UINT i = 0; i < pExportDir->NumberOfNames; i++){
        LPSTR pFuncName = (LPSTR)(lpBaseAddr + pNameArray[i]);
        if (    pFuncName[0] == 'G' &&
                pFuncName[1] == 'e' &&
                pFuncName[2] == 't' &&
                pFuncName[3] == 'P' &&
                pFuncName[4] == 'r' &&
                pFuncName[5] == 'o' &&
                pFuncName[6] == 'c' &&
                pFuncName[7] == 'A' &&
                pFuncName[8] == 'd' &&
                pFuncName[9] == 'd' &&
                pFuncName[10] == 'r' &&
                pFuncName[11] == 'e' &&
                pFuncName[12] == 's' &&
                pFuncName[13] == 's'     ){
            GetProcAddressAPI = (FARPROC)(lpBaseAddr + pAddrArray[pOrdArray[i]]);
            return GetProcAddressAPI;
        }
    }
    return NULL;
}
void ShellcodeEnd(){
}