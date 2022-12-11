// 暂时还没有做完功能，可能在dll转移以及调试上面出现一些问题。
// 更多的是在功能上还没有想好处理的方式。

// 管道接收端
#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <string.h>
#ifdef _WIN64
    #define ULONGLONG ULONGLONG
    #define PULONGLONG PULONGLONG
#else
    #define ULONGLONG ULONG
    #define PULONGLONG PULONG
#endif
#define PIPE_NAME "\\\\.\\Pipe\\vtestv"
#define G_V_SPACE "Global\\vttttv"
#define BUF_SIZE 1024*1024

LPVOID ReadFile_from_Memory(HMODULE hModule) {
    HANDLE f,h;
    LPVOID m;
    TCHAR szCurrent[MAX_PATH] = {0};
    GetModuleFileName(hModule, szCurrent, sizeof(szCurrent)-1);
    if (strlen(szCurrent) == 0){
        h = OpenFileMapping(FILE_MAP_ALL_ACCESS, TRUE, G_V_SPACE);
        m = MapViewOfFile(h, FILE_MAP_ALL_ACCESS, 0, 0, BUF_SIZE);
    }else{
        // dll文件状态被主动加载时，这里可以考虑是否要删除文件本身。
        if ((f = CreateFileA(
                    szCurrent,GENERIC_READ,FILE_SHARE_READ,0,
                    OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL)
                ) == INVALID_HANDLE_VALUE){
            return NULL;
        }
        LPVOID pBuffer = (LPVOID)malloc(BUF_SIZE);
        ReadFile(f, pBuffer, BUF_SIZE, NULL, NULL);
        CloseHandle(f);
        h = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, BUF_SIZE, G_V_SPACE);
        m = MapViewOfFile(h, FILE_MAP_ALL_ACCESS, 0, 0, BUF_SIZE);
        memcpy((LPVOID)m, pBuffer, BUF_SIZE);
        return m;
    }

    // test log
    char somestring[125] = {0};//
    char *info = (char *)malloc(strlen(somestring) + 2);
    itoa((int)GetLastError(), somestring, 10);
    info = (char *)malloc(strlen(somestring) + 2);
    strcpy(info, somestring);
    strcat(info, " ");
    itoa(strlen(szCurrent), somestring, 10);
    strcat(info, somestring);
    MessageBox(NULL, info, "eeeeeeeeeeeeee", MB_OK);
    return m;
}




char SELF_PATH[MAX_PATH] = {0};
char* get_self_path(){
    ZeroMemory(SELF_PATH, MAX_PATH);
    GetModuleFileName(NULL,(LPSTR)SELF_PATH,sizeof(SELF_PATH));  
    return SELF_PATH;
}
char* get_info_string(){
    char *path = get_self_path();
    char cpid[25] = {0};
    itoa(GetCurrentProcessId(), cpid, 10);
    char *info = (char *)malloc(strlen(path) + strlen(cpid) + 2);
    strcpy(info, path);
    strcat(info, " ");
    strcat(info, cpid);
    return info;
}




HANDLE Find_Process(char * processname) {
    PROCESSENTRY32 ProcessEntry = { 0 };
    HANDLE hProcessSnap, proc;
    ProcessEntry.dwSize = sizeof(PROCESSENTRY32);
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    BOOL bRet = Process32First(hProcessSnap,&ProcessEntry);
    while (bRet) {
        if(strcmp(processname,ProcessEntry.szExeFile) == 0) {
            proc = OpenProcess(PROCESS_ALL_ACCESS,0,ProcessEntry.th32ProcessID);
            MessageBox(NULL, ProcessEntry.szExeFile, "x", MB_OK);
            break;
        }
        bRet = Process32Next(hProcessSnap,&ProcessEntry);
    }
    return proc;
}
typedef struct _PE_INFO {
    LPVOID  base;
    BOOL    reloc;
    LPVOID  Get_Proc;
    LPVOID  Load_DLL;
}PE_INFO , *LPE_INFO;
void AdjustPE(LPE_INFO pe) {
    PIMAGE_DOS_HEADER           dos;
    PIMAGE_NT_HEADERS           nt;
    LPVOID                      base;
    PIMAGE_IMPORT_DESCRIPTOR    import;
    PIMAGE_THUNK_DATA           Othunk,Fthunk;
    PIMAGE_BASE_RELOCATION      reloc;
    PIMAGE_TLS_DIRECTORY        tls;
    PIMAGE_TLS_CALLBACK*        CallBack;
    ULONGLONG*                  p,delta;
    BOOL        (*DLL_Entry)    (LPVOID, DWORD, LPVOID);
    LPVOID      (*Load_DLL)     (LPSTR);
    LPVOID      (*Get_Proc)     (LPVOID, LPSTR);
    base       = pe->base;
    Load_DLL   = pe->Load_DLL;
    Get_Proc   = pe->Get_Proc;
    dos        = (PIMAGE_DOS_HEADER)base;
    nt         = (PIMAGE_NT_HEADERS)(base + dos->e_lfanew);
    DLL_Entry  = base+nt->OptionalHeader.AddressOfEntryPoint;
    if(pe->reloc){
        if(nt->OptionalHeader.DataDirectory[5].VirtualAddress != 0){
            delta = (ULONGLONG)base-nt->OptionalHeader.ImageBase;
            reloc = (PIMAGE_BASE_RELOCATION)(base+nt->OptionalHeader.DataDirectory[5].VirtualAddress);
            while(reloc->VirtualAddress) {
                LPVOID  dest    = base+reloc->VirtualAddress;
                int     nEntry  = (reloc->SizeOfBlock-sizeof(IMAGE_BASE_RELOCATION))/2;
                PWORD   data    = (PWORD)((LPVOID)reloc+sizeof(IMAGE_BASE_RELOCATION));
                int i;
                for(i = 0; i<nEntry; i++,data++) {
                    if(((*data) >> 12) == 10) {
                        p = (PULONGLONG)(dest+((*data)&0xfff));
                        *p += delta;
                    }
                }
                reloc = (PIMAGE_BASE_RELOCATION)((LPVOID)reloc+reloc->SizeOfBlock);
            }
        }
    }
    if(nt->OptionalHeader.DataDirectory[1].VirtualAddress != 0){
        import = (PIMAGE_IMPORT_DESCRIPTOR)(base+nt->OptionalHeader.DataDirectory[1].VirtualAddress);
        while(import->Name) {
            LPVOID dll = (*Load_DLL)(base+import->Name);
            Othunk = (PIMAGE_THUNK_DATA)(base+import->OriginalFirstThunk);
            Fthunk = (PIMAGE_THUNK_DATA)(base+import->FirstThunk);
            if(!import->OriginalFirstThunk){
                Othunk = Fthunk;
            }
            while(Othunk->u1.AddressOfData) {
                if(Othunk->u1.Ordinal & IMAGE_ORDINAL_FLAG) {
                    *(ULONGLONG *)Fthunk = (ULONGLONG)(*Get_Proc)(dll,(LPSTR)IMAGE_ORDINAL(Othunk->u1.Ordinal));
                }
                else {
                    PIMAGE_IMPORT_BY_NAME fnm = (PIMAGE_IMPORT_BY_NAME)(base+Othunk->u1.AddressOfData);
                    *(PULONGLONG)Fthunk = (ULONGLONG)(*Get_Proc)(dll,fnm->Name);
                }
                Othunk++;
                Fthunk++;
            }
            import++;
        }
    }
    if(nt->OptionalHeader.DataDirectory[9].VirtualAddress != 0){
        tls = (PIMAGE_TLS_DIRECTORY)(base+nt->OptionalHeader.DataDirectory[9].VirtualAddress);
        if(tls->AddressOfCallBacks != 0){
            CallBack = (PIMAGE_TLS_CALLBACK *)(tls->AddressOfCallBacks);
            while(*CallBack) {
                (*CallBack)(base,DLL_PROCESS_ATTACH,NULL);
                CallBack++;
            }
        }
    }
    (*DLL_Entry)(base,DLL_PROCESS_ATTACH,NULL);
}
int AdjustPEEND(){
    return 0;
}
int inject_self_to_other(HMODULE hModule){
    HANDLE      proc;
    LPVOID      Rbase,Adj;
    DWORD       Func_Size;
    LPVOID base = ReadFile_from_Memory(hModule);
    PE_INFO     pe;
    PIMAGE_DOS_HEADER       dos;
    PIMAGE_SECTION_HEADER   sec;
    PIMAGE_NT_HEADERS       nt;
    dos  = (PIMAGE_DOS_HEADER)base;
    nt   = (PIMAGE_NT_HEADERS)(base+dos->e_lfanew);
    sec  = (PIMAGE_SECTION_HEADER)((LPVOID)nt+24+nt->FileHeader.SizeOfOptionalHeader);
    proc = Find_Process("642.exe"); // 这里被写死了，后续考虑动态处理
    pe.reloc = 0;
    if((Rbase = VirtualAllocEx(proc,(LPVOID)nt->OptionalHeader.ImageBase,
                            nt->OptionalHeader.SizeOfImage,MEM_COMMIT|MEM_RESERVE,
                            PAGE_EXECUTE_READWRITE)) == NULL) {
        pe.reloc = 1;
        if((Rbase = VirtualAllocEx(proc,NULL,nt->OptionalHeader.SizeOfImage,
                            MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE)) == NULL) {
            return 0;
        }
    }
    WriteProcessMemory(proc,Rbase,base,nt->OptionalHeader.SizeOfHeaders,NULL);
    int i;
    for(i = 0; i<nt->FileHeader.NumberOfSections; i++, sec++) {
        WriteProcessMemory(proc,Rbase+sec->VirtualAddress,
                base+sec->PointerToRawData,sec->SizeOfRawData,NULL);
    }
    pe.base = Rbase;
    Func_Size = (DWORD)((ULONGLONG)AdjustPEEND-(ULONGLONG)AdjustPE);
    pe.Get_Proc = GetProcAddress(LoadLibraryA("kernel32"), "GetProcAddress");
    pe.Load_DLL = GetProcAddress(LoadLibraryA("kernel32"), "LoadLibraryA");
    Adj = VirtualAllocEx(proc, NULL, Func_Size+sizeof(pe),
                    MEM_COMMIT|MEM_RESERVE,
                    PAGE_EXECUTE_READWRITE);
    if(Adj == NULL) return 0;
    WriteProcessMemory(proc,Adj,&pe,sizeof(pe),NULL);
    WriteProcessMemory(proc,Adj+sizeof(pe),AdjustPE,Func_Size,NULL);
    CreateRemoteThread(proc,NULL,0,(LPTHREAD_START_ROUTINE)(Adj+sizeof(pe)),Adj,0,NULL);

    // test log
    char somestring[25] = {0};
    char *info = (char *)malloc(strlen(somestring) + 2);
    info = (char *)malloc(22);
    itoa((int)GetLastError(), somestring, 10);
    strcpy(info, somestring);
    strcat(info, " ");
    itoa((int)Func_Size, somestring, 10);
    strcat(info, somestring);
    MessageBox(NULL, info, "xxx", MB_OK);
    return 0;
}

void start_pipe_server(HMODULE hModule){
    HANDLE PipeHandle;
    DWORD BytesRead;
    CHAR buffer[256] = {0};
    while (1){
        if ((PipeHandle = CreateNamedPipe(PIPE_NAME, PIPE_ACCESS_DUPLEX,
                PIPE_TYPE_BYTE|PIPE_READMODE_BYTE, 1, 0, 0, 1000, NULL)) == INVALID_HANDLE_VALUE) {
            Sleep(1000);
        }else{
            break;
        }
    }
    while (1){
        char* info0 = get_info_string();
        MessageBox(NULL, info0, TEXT("hello111"), MB_OK);
        if (  ConnectNamedPipe(PipeHandle,NULL) == 0 ||
              ReadFile(PipeHandle,buffer,sizeof(buffer),&BytesRead,NULL) <= 0 ){
            CloseHandle(PipeHandle);
            return;
        }
        char* info = get_info_string();
        MessageBox(NULL, info, TEXT("hello"), MB_OK);
        inject_self_to_other(hModule);
        break;
        if (DisconnectNamedPipe(PipeHandle) == 0) return;
    }
    CloseHandle(PipeHandle);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
        start_pipe_server(hModule);
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}