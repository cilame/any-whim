// 用 gcc 直接编译
// 用 tcc 编译需要注意引入 windows 的头文件地址
// cmd> tcc -I"C:\Users\...\winapi-full-for-0.9.27\include\winapi" tcc_injecter.c
// tcc_injecter.c

#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h>

BOOL LoadDll(DWORD dwProcessId,LPTSTR lpszDllName) {
    HANDLE hProcess = NULL;
    HANDLE hThread  = NULL;
    PSTR   pDllFile = NULL;
    hProcess = OpenProcess(PROCESS_ALL_ACCESS,FALSE,dwProcessId);
    if(hProcess == NULL) return FALSE;
    printf("OpenProcess %d success.\n",dwProcessId);
    int cch = 1 + strlen(lpszDllName);
    pDllFile = (PSTR)VirtualAllocEx(hProcess, NULL, cch, MEM_COMMIT, PAGE_READWRITE);
    if(pDllFile == NULL) return FALSE;
    printf("VirtualAllocEx success.\n");
    if((WriteProcessMemory(hProcess, (PVOID)pDllFile, (PVOID)lpszDllName, cch, NULL)) == FALSE) return FALSE;
    printf("WriteProcessMemory success.\n");
    PTHREAD_START_ROUTINE pfnThreadRtn = (PTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandle("kernel32"),"LoadLibraryA");
    if(pfnThreadRtn == NULL) return FALSE;
    printf("get LoadLibraryA success.\n");
    hThread = CreateRemoteThread(hProcess, NULL, 0, pfnThreadRtn, (PVOID)pDllFile, 0, NULL);
    if(hThread == NULL) return FALSE;
    printf("CreateRemoteThread success.\n");
    // WaitForSingleObject(hThread, INFINITE); // 是否等待注入任务执行完毕再继续此处后续的代码
    VirtualFreeEx(hProcess,(PVOID)pDllFile,0,MEM_RELEASE);
    CloseHandle(hThread);
    return TRUE;
}

int getPidByProcessName(char* processname) {
    PROCESSENTRY32 ProcessEntry = { 0 };
    HANDLE hProcessSnap;
    ProcessEntry.dwSize = sizeof(PROCESSENTRY32);
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    BOOL bRet = Process32First(hProcessSnap,&ProcessEntry);
    while (bRet) {
        if(strcmp(processname,ProcessEntry.szExeFile) == 0) {
            return ProcessEntry.th32ProcessID;
        }
        bRet = Process32Next(hProcessSnap,&ProcessEntry);
    }
}

void main(int argc, char* argv[]) {
    char lpDllName[MAX_PATH] = TEXT("./inject.dll");
    char processname[MAX_PATH] = TEXT("notepad.exe");
    int pid = getPidByProcessName(processname);
    LoadDll(pid,lpDllName);
}

// 下面是注入的dll写法，这样可以在dll被别的程序附加时执行执行附加时的程序
// cmd> tcc -shared inject.c
// inject.c
// #include <windows.h>
// #include <stdio.h>
// BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {
//     switch (ul_reason_for_call) {
//     case DLL_PROCESS_ATTACH:
//         MessageBox(NULL, TEXT("你好啊"), TEXT("提示"), MB_OK);
//     case DLL_THREAD_ATTACH:
//     case DLL_THREAD_DETACH:
//     case DLL_PROCESS_DETACH:
//         break;
//     }
//     return TRUE;
// }