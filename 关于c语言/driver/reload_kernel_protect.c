// 快速开发 windows 内核驱动，一个脚本即可开发驱动。
// 该处代码的主要功能为重载内核，主要是绕过一些内核态的函数检测功能。
// 使用重载内核后实现的新内核空间的函数，让执行程序执行时走自己创建的内核空间的代码
// 防止一些已经被挂钩住的内核函数的检测，
// 主要的过滤逻辑在 FilterKiFastCallEntry 函数处，注意修改即可。
// 另外还需要注意最底部的 DriverEntry 函数内的注释，注意修改即可。


// 准备1：
// 在当前脚本路径内创建两个文件，配置完这两个固定的文件后续就无需再修改了。文件名字固定为 makefile 和 sources
// 
// 文件 makefile 的内容如下，只有一行即可
// !INCLUDE $(NTMAKEENV)\makefile.def
// 
// 文件 sources 的内容如下，三行内容即可，TARGETNAME 为生成的驱动名字，TARGETTYPE 固定为 DRIVER 即可，SOURCES 为该脚本的名字
// TARGETNAME=some
// TARGETTYPE=DRIVER
// SOURCES=some.c

// 准备2：
// 下载安装 WDK 运行环境；我用的是 GRMWDK_EN_7600_1.ISO
// 下载地址为 http://download.microsoft.com/download/4/A/2/4A25C7D5-EFBE-4182-B6A9-AE6850409A78/GRMWDK_EN_7600_1.ISO
// 下载安装后在命令行启动环境配置。
// 以下为配置环境的四种模式，随便选一个在命令行中执行即可，个人开发推荐第一个环境。
// 注意修改下面路径中的 “D:\WinDDK\7600.16385.1\” 为自己的 GRMWDK_EN_7600_1.ISO 安装地址
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk x64 WIN7
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre x64 WIN7
// 
// 执行后，环境配置完毕，请跳转到当前路径位置。使用配置好环境的命令行进行编译。
// 执行命令 build 即可编译。这样你的驱动就编译好了。

#include "ntddk.h"

#define WORD  USHORT
#define DWORD ULONG
#ifndef _NTIMAGE_
#define _NTIMAGE_
#define IMAGE_DOS_SIGNATURE                 0x5A4D
#define IMAGE_OS2_SIGNATURE                 0x454E
#define IMAGE_OS2_SIGNATURE_LE              0x454C
#define IMAGE_VXD_SIGNATURE                 0x454C
#define IMAGE_NT_SIGNATURE                  0x00004550
#define IMAGE_FILE_MACHINE_AM33       0x1d3
#define IMAGE_FILE_MACHINE_AMD64      0x8664
#define IMAGE_FILE_MACHINE_ARM        0x1c0
#define IMAGE_FILE_MACHINE_EBC        0xebc
#define IMAGE_FILE_MACHINE_I386       0x14c
#define IMAGE_FILE_MACHINE_IA64       0x200
#define IMAGE_FILE_MACHINE_M32R       0x9041
#define IMAGE_FILE_MACHINE_MIPS16     0x266
#define IMAGE_FILE_MACHINE_MIPSFPU    0x366
#define IMAGE_FILE_MACHINE_MIPSFPU16  0x466
#define IMAGE_FILE_MACHINE_POWERPC    0x1f0
#define IMAGE_FILE_MACHINE_POWERPCFP  0x1f1
#define IMAGE_FILE_MACHINE_R4000      0x166
#define IMAGE_FILE_MACHINE_SH3        0x1a2
#define IMAGE_FILE_MACHINE_SH3E       0x01a4
#define IMAGE_FILE_MACHINE_SH3DSP     0x1a3
#define IMAGE_FILE_MACHINE_SH4        0x1a6
#define IMAGE_FILE_MACHINE_SH5        0x1a8
#define IMAGE_FILE_MACHINE_THUMB      0x1c2
#define IMAGE_FILE_MACHINE_WCEMIPSV2  0x169
#define IMAGE_FILE_MACHINE_R3000      0x162
#define IMAGE_FILE_MACHINE_R10000     0x168
#define IMAGE_FILE_MACHINE_ALPHA      0x184
#define IMAGE_FILE_MACHINE_ALPHA64    0x0284
#define IMAGE_FILE_MACHINE_AXP64      IMAGE_FILE_MACHINE_ALPHA64
#define IMAGE_FILE_MACHINE_CEE        0xC0EE
#define IMAGE_FILE_MACHINE_TRICORE    0x0520
#define IMAGE_FILE_MACHINE_CEF        0x0CEF
typedef struct _IMAGE_DOS_HEADER {
    USHORT e_magic;
    USHORT e_cblp;
    USHORT e_cp;
    USHORT e_crlc;
    USHORT e_cparhdr;
    USHORT e_minalloc;
    USHORT e_maxalloc;
    USHORT e_ss;
    USHORT e_sp;
    USHORT e_csum;
    USHORT e_ip;
    USHORT e_cs;
    USHORT e_lfarlc;
    USHORT e_ovno;
    USHORT e_res[4];
    USHORT e_oemid;
    USHORT e_oeminfo;
    USHORT e_res2[10];
    LONG e_lfanew;
} IMAGE_DOS_HEADER, *PIMAGE_DOS_HEADER;
typedef struct _IMAGE_EXPORT_DIRECTORY {
    ULONG Characteristics;
    ULONG TimeDateStamp;
    USHORT MajorVersion;
    USHORT MinorVersion;
    ULONG Name;
    ULONG Base;
    ULONG NumberOfFunctions;
    ULONG NumberOfNames;
    ULONG AddressOfFunctions;
    ULONG AddressOfNames;
    ULONG AddressOfNameOrdinals;
} IMAGE_EXPORT_DIRECTORY, *PIMAGE_EXPORT_DIRECTORY;
typedef struct _IMAGE_RESOURCE_DATA_ENTRY {
    ULONG OffsetToData;
    ULONG Size;
    ULONG CodePage;
    ULONG Reserved;
} IMAGE_RESOURCE_DATA_ENTRY, *PIMAGE_RESOURCE_DATA_ENTRY;
typedef struct {
    ULONG   Size;
    ULONG   TimeDateStamp;
    USHORT  MajorVersion;
    USHORT  MinorVersion;
    ULONG   GlobalFlagsClear;
    ULONG   GlobalFlagsSet;
    ULONG   CriticalSectionDefaultTimeout;
    ULONG   DeCommitFreeBlockThreshold;
    ULONG   DeCommitTotalFreeThreshold;
    ULONG   LockPrefixTable;
    ULONG   MaximumAllocationSize;
    ULONG   VirtualMemoryThreshold;
    ULONG   ProcessHeapFlags;
    ULONG   ProcessAffinityMask;
    USHORT  CSDVersion;
    USHORT  Reserved1;
    ULONG   EditList;
    ULONG   SecurityCookie;
    ULONG   SEHandlerTable;
    ULONG   SEHandlerCount;
} IMAGE_LOAD_CONFIG_DIRECTORY32, *PIMAGE_LOAD_CONFIG_DIRECTORY32;
typedef struct {
    ULONG      Size;
    ULONG      TimeDateStamp;
    USHORT     MajorVersion;
    USHORT     MinorVersion;
    ULONG      GlobalFlagsClear;
    ULONG      GlobalFlagsSet;
    ULONG      CriticalSectionDefaultTimeout;
    ULONGLONG  DeCommitFreeBlockThreshold;
    ULONGLONG  DeCommitTotalFreeThreshold;
    ULONGLONG  LockPrefixTable;
    ULONGLONG  MaximumAllocationSize;
    ULONGLONG  VirtualMemoryThreshold;
    ULONGLONG  ProcessAffinityMask;
    ULONG      ProcessHeapFlags;
    USHORT     CSDVersion;
    USHORT     Reserved1;
    ULONGLONG  EditList;
    ULONGLONG  SecurityCookie;
    ULONGLONG  SEHandlerTable;
    ULONGLONG  SEHandlerCount;
} IMAGE_LOAD_CONFIG_DIRECTORY64, *PIMAGE_LOAD_CONFIG_DIRECTORY64;
#ifdef _WIN64
typedef IMAGE_LOAD_CONFIG_DIRECTORY64     IMAGE_LOAD_CONFIG_DIRECTORY;
typedef PIMAGE_LOAD_CONFIG_DIRECTORY64    PIMAGE_LOAD_CONFIG_DIRECTORY;
#else
typedef IMAGE_LOAD_CONFIG_DIRECTORY32     IMAGE_LOAD_CONFIG_DIRECTORY;
typedef PIMAGE_LOAD_CONFIG_DIRECTORY32    PIMAGE_LOAD_CONFIG_DIRECTORY;
#endif
typedef struct _IMAGE_BASE_RELOCATION {
    ULONG VirtualAddress;
    ULONG SizeOfBlock;
    USHORT TypeOffset[1];
} IMAGE_BASE_RELOCATION, *PIMAGE_BASE_RELOCATION;
typedef struct _IMAGE_RESOURCE_DIRECTORY {
    ULONG Characteristics;
    ULONG TimeDateStamp;
    USHORT MajorVersion;
    USHORT MinorVersion;
    USHORT NumberOfNamedEntries;
    USHORT NumberOfIdEntries;
} IMAGE_RESOURCE_DIRECTORY, *PIMAGE_RESOURCE_DIRECTORY;
typedef struct _IMAGE_RESOURCE_DIRECTORY_STRING {
    USHORT Length;
    CHAR NameString[ANYSIZE_ARRAY];
} IMAGE_RESOURCE_DIRECTORY_STRING, *PIMAGE_RESOURCE_DIRECTORY_STRING;
#define IMAGE_SIZEOF_SHORT_NAME              8
#define IMAGE_SIZEOF_SECTION_HEADER          40
typedef struct _IMAGE_SECTION_HEADER {
    UCHAR Name[IMAGE_SIZEOF_SHORT_NAME];
    union
    {
        ULONG PhysicalAddress;
        ULONG VirtualSize;
    } Misc;
    ULONG VirtualAddress;
    ULONG SizeOfRawData;
    ULONG PointerToRawData;
    ULONG PointerToRelocations;
    ULONG PointerToLinenumbers;
    USHORT NumberOfRelocations;
    USHORT NumberOfLinenumbers;
    ULONG Characteristics;
} IMAGE_SECTION_HEADER, *PIMAGE_SECTION_HEADER;
#define IMAGE_SCN_CNT_CODE                   0x00000020
#define IMAGE_SCN_CNT_INITIALIZED_DATA       0x00000040
#define IMAGE_SCN_CNT_UNINITIALIZED_DATA     0x00000080
#define IMAGE_SCN_LNK_NRELOC_OVFL            0x01000000
#define IMAGE_SCN_MEM_DISCARDABLE            0x02000000
#define IMAGE_SCN_MEM_NOT_CACHED             0x04000000
#define IMAGE_SCN_MEM_NOT_PAGED              0x08000000
#define IMAGE_SCN_MEM_SHARED                 0x10000000
#define IMAGE_SCN_MEM_EXECUTE                0x20000000
#define IMAGE_SCN_MEM_READ                   0x40000000
#define IMAGE_SCN_MEM_WRITE                  0x80000000
#define IMAGE_SIZEOF_FILE_HEADER             20
typedef struct _IMAGE_FILE_HEADER {
    USHORT Machine;
    USHORT NumberOfSections;
    ULONG TimeDateStamp;
    ULONG PointerToSymbolTable;
    ULONG NumberOfSymbols;
    USHORT SizeOfOptionalHeader;
    USHORT Characteristics;
} IMAGE_FILE_HEADER, *PIMAGE_FILE_HEADER;
#define IMAGE_FILE_RELOCS_STRIPPED           0x0001
#define IMAGE_FILE_EXECUTABLE_IMAGE          0x0002
#define IMAGE_FILE_LINE_NUMS_STRIPPED        0x0004
#define IMAGE_FILE_LOCAL_SYMS_STRIPPED       0x0008
#define IMAGE_FILE_AGGRESIVE_WS_TRIM         0x0010
#define IMAGE_FILE_LARGE_ADDRESS_AWARE       0x0020
#define IMAGE_FILE_BYTES_REVERSED_LO         0x0080
#define IMAGE_FILE_32BIT_MACHINE             0x0100
#define IMAGE_FILE_DEBUG_STRIPPED            0x0200
#define IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP   0x0400
#define IMAGE_FILE_NET_RUN_FROM_SWAP         0x0800
#define IMAGE_FILE_SYSTEM                    0x1000
#define IMAGE_FILE_DLL                       0x2000
#define IMAGE_FILE_UP_SYSTEM_ONLY            0x4000
#define IMAGE_FILE_BYTES_REVERSED_HI         0x8000
#define IMAGE_NUMBEROF_DIRECTORY_ENTRIES    16
typedef struct _IMAGE_DATA_DIRECTORY {
    ULONG   VirtualAddress;
    ULONG   Size;
} IMAGE_DATA_DIRECTORY, *PIMAGE_DATA_DIRECTORY;
typedef struct _IMAGE_OPTIONAL_HEADER {
    USHORT  Magic;
    UCHAR   MajorLinkerVersion;
    UCHAR   MinorLinkerVersion;
    ULONG   SizeOfCode;
    ULONG   SizeOfInitializedData;
    ULONG   SizeOfUninitializedData;
    ULONG   AddressOfEntryPoint;
    ULONG   BaseOfCode;
    ULONG   BaseOfData;
    ULONG   ImageBase;
    ULONG   SectionAlignment;
    ULONG   FileAlignment;
    USHORT  MajorOperatingSystemVersion;
    USHORT  MinorOperatingSystemVersion;
    USHORT  MajorImageVersion;
    USHORT  MinorImageVersion;
    USHORT  MajorSubsystemVersion;
    USHORT  MinorSubsystemVersion;
    ULONG   Win32VersionValue;
    ULONG   SizeOfImage;
    ULONG   SizeOfHeaders;
    ULONG   CheckSum;
    USHORT  Subsystem;
    USHORT  DllCharacteristics;
    ULONG   SizeOfStackReserve;
    ULONG   SizeOfStackCommit;
    ULONG   SizeOfHeapReserve;
    ULONG   SizeOfHeapCommit;
    ULONG   LoaderFlags;
    ULONG   NumberOfRvaAndSizes;
    IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES];
} IMAGE_OPTIONAL_HEADER32, *PIMAGE_OPTIONAL_HEADER32;
typedef struct _IMAGE_ROM_OPTIONAL_HEADER {
    USHORT Magic;
    UCHAR  MajorLinkerVersion;
    UCHAR  MinorLinkerVersion;
    ULONG  SizeOfCode;
    ULONG  SizeOfInitializedData;
    ULONG  SizeOfUninitializedData;
    ULONG  AddressOfEntryPoint;
    ULONG  BaseOfCode;
    ULONG  BaseOfData;
    ULONG  BaseOfBss;
    ULONG  GprMask;
    ULONG  CprMask[4];
    ULONG  GpValue;
} IMAGE_ROM_OPTIONAL_HEADER, *PIMAGE_ROM_OPTIONAL_HEADER;
typedef struct _IMAGE_OPTIONAL_HEADER64 {
    USHORT      Magic;
    UCHAR       MajorLinkerVersion;
    UCHAR       MinorLinkerVersion;
    ULONG       SizeOfCode;
    ULONG       SizeOfInitializedData;
    ULONG       SizeOfUninitializedData;
    ULONG       AddressOfEntryPoint;
    ULONG       BaseOfCode;
    ULONGLONG   ImageBase;
    ULONG       SectionAlignment;
    ULONG       FileAlignment;
    USHORT      MajorOperatingSystemVersion;
    USHORT      MinorOperatingSystemVersion;
    USHORT      MajorImageVersion;
    USHORT      MinorImageVersion;
    USHORT      MajorSubsystemVersion;
    USHORT      MinorSubsystemVersion;
    ULONG       Win32VersionValue;
    ULONG       SizeOfImage;
    ULONG       SizeOfHeaders;
    ULONG       CheckSum;
    USHORT      Subsystem;
    USHORT      DllCharacteristics;
    ULONGLONG   SizeOfStackReserve;
    ULONGLONG   SizeOfStackCommit;
    ULONGLONG   SizeOfHeapReserve;
    ULONGLONG   SizeOfHeapCommit;
    ULONG       LoaderFlags;
    ULONG       NumberOfRvaAndSizes;
    IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES];
} IMAGE_OPTIONAL_HEADER64, *PIMAGE_OPTIONAL_HEADER64;
#define IMAGE_NT_OPTIONAL_HDR32_MAGIC      0x10b
#define IMAGE_NT_OPTIONAL_HDR64_MAGIC      0x20b
#define IMAGE_ROM_OPTIONAL_HDR_MAGIC       0x107
#ifdef _WIN64
typedef IMAGE_OPTIONAL_HEADER64             IMAGE_OPTIONAL_HEADER;
typedef PIMAGE_OPTIONAL_HEADER64            PIMAGE_OPTIONAL_HEADER;
#define IMAGE_NT_OPTIONAL_HDR_MAGIC         IMAGE_NT_OPTIONAL_HDR64_MAGIC
#else
typedef IMAGE_OPTIONAL_HEADER32             IMAGE_OPTIONAL_HEADER;
typedef PIMAGE_OPTIONAL_HEADER32            PIMAGE_OPTIONAL_HEADER;
#define IMAGE_NT_OPTIONAL_HDR_MAGIC         IMAGE_NT_OPTIONAL_HDR32_MAGIC
#endif
typedef struct _IMAGE_NT_HEADERS64 {
    ULONG Signature;
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER64 OptionalHeader;
} IMAGE_NT_HEADERS64, *PIMAGE_NT_HEADERS64;

typedef struct _IMAGE_NT_HEADERS {
    ULONG Signature;
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER32 OptionalHeader;
} IMAGE_NT_HEADERS32, *PIMAGE_NT_HEADERS32;
#ifdef _WIN64
typedef IMAGE_NT_HEADERS64                  IMAGE_NT_HEADERS;
typedef PIMAGE_NT_HEADERS64                 PIMAGE_NT_HEADERS;
#else
typedef IMAGE_NT_HEADERS32                  IMAGE_NT_HEADERS;
typedef PIMAGE_NT_HEADERS32                 PIMAGE_NT_HEADERS;
#endif
#define IMAGE_FIRST_SECTION( NtHeader ) ((PIMAGE_SECTION_HEADER)        \
    ((ULONG_PTR)(NtHeader) +                                            \
     FIELD_OFFSET( IMAGE_NT_HEADERS, OptionalHeader ) +                 \
     ((NtHeader))->FileHeader.SizeOfOptionalHeader   \
    ))
#define IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE          0x0040
#define IMAGE_DLLCHARACTERISTICS_FORCE_INTEGRITY       0x0080
#define IMAGE_DLLCHARACTERISTICS_NX_COMPAT             0x0100
#define IMAGE_DLLCHARACTERISTICS_NO_ISOLATION          0x0200
#define IMAGE_DLLCHARACTERISTICS_NO_SEH                0x0400
#define IMAGE_DLLCHARACTERISTICS_NO_BIND               0x0800
#define IMAGE_DLLCHARACTERISTICS_WDM_DRIVER            0x2000
#define IMAGE_DLLCHARACTERISTICS_TERMINAL_SERVER_AWARE 0x8000
#define IMAGE_DIRECTORY_ENTRY_EXPORT          0
#define IMAGE_DIRECTORY_ENTRY_IMPORT          1
#define IMAGE_DIRECTORY_ENTRY_RESOURCE        2
#define IMAGE_DIRECTORY_ENTRY_EXCEPTION       3
#define IMAGE_DIRECTORY_ENTRY_SECURITY        4
#define IMAGE_DIRECTORY_ENTRY_BASERELOC       5
#define IMAGE_DIRECTORY_ENTRY_DEBUG           6
#define IMAGE_DIRECTORY_ENTRY_ARCHITECTURE    7
#define IMAGE_DIRECTORY_ENTRY_GLOBALPTR       8
#define IMAGE_DIRECTORY_ENTRY_TLS             9
#define IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG    10
#define IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT   11
#define IMAGE_DIRECTORY_ENTRY_IAT            12
#define IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT   13
#define IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR 14
typedef struct _IMAGE_IMPORT_BY_NAME {
    USHORT  Hint;
    UCHAR   Name[1];
} IMAGE_IMPORT_BY_NAME, *PIMAGE_IMPORT_BY_NAME;
typedef struct _IMAGE_THUNK_DATA64 {
    union {
        ULONGLONG ForwarderString;
        ULONGLONG Function;
        ULONGLONG Ordinal;
        ULONGLONG AddressOfData;
    } u1;
} IMAGE_THUNK_DATA64, *PIMAGE_THUNK_DATA64;
typedef struct _IMAGE_THUNK_DATA32 {
    union {
        ULONG ForwarderString;
        ULONG Function;
        ULONG Ordinal;
        ULONG AddressOfData;
    } u1;
} IMAGE_THUNK_DATA32, *PIMAGE_THUNK_DATA32;
#define IMAGE_ORDINAL_FLAG64 0x8000000000000000ULL
#define IMAGE_ORDINAL_FLAG32 0x80000000
#define IMAGE_ORDINAL64(Ordinal) (Ordinal & 0xffff)
#define IMAGE_ORDINAL32(Ordinal) (Ordinal & 0xffff)
#define IMAGE_SNAP_BY_ORDINAL64(Ordinal) ((Ordinal & IMAGE_ORDINAL_FLAG64) != 0)
#define IMAGE_SNAP_BY_ORDINAL32(Ordinal) ((Ordinal & IMAGE_ORDINAL_FLAG32) != 0)
typedef
VOID
(NTAPI *PIMAGE_TLS_CALLBACK) (
    PVOID DllHandle,
    ULONG Reason,
    PVOID Reserved
);
typedef struct _IMAGE_TLS_DIRECTORY64 {
    ULONGLONG   StartAddressOfRawData;
    ULONGLONG   EndAddressOfRawData;
    ULONGLONG   AddressOfIndex;
    ULONGLONG   AddressOfCallBacks;
    ULONG   SizeOfZeroFill;
    ULONG   Characteristics;
} IMAGE_TLS_DIRECTORY64, *PIMAGE_TLS_DIRECTORY64;
typedef struct _IMAGE_TLS_DIRECTORY32 {
    ULONG   StartAddressOfRawData;
    ULONG   EndAddressOfRawData;
    ULONG   AddressOfIndex;
    ULONG   AddressOfCallBacks;
    ULONG   SizeOfZeroFill;
    ULONG   Characteristics;
} IMAGE_TLS_DIRECTORY32, *PIMAGE_TLS_DIRECTORY32;
#ifdef _WIN64
#define IMAGE_ORDINAL_FLAG              IMAGE_ORDINAL_FLAG64
#define IMAGE_ORDINAL(Ordinal)          IMAGE_ORDINAL64(Ordinal)
typedef IMAGE_THUNK_DATA64              IMAGE_THUNK_DATA;
typedef PIMAGE_THUNK_DATA64             PIMAGE_THUNK_DATA;
#define IMAGE_SNAP_BY_ORDINAL(Ordinal)  IMAGE_SNAP_BY_ORDINAL64(Ordinal)
typedef IMAGE_TLS_DIRECTORY64           IMAGE_TLS_DIRECTORY;
typedef PIMAGE_TLS_DIRECTORY64          PIMAGE_TLS_DIRECTORY;
#else
#define IMAGE_ORDINAL_FLAG              IMAGE_ORDINAL_FLAG32
#define IMAGE_ORDINAL(Ordinal)          IMAGE_ORDINAL32(Ordinal)
typedef IMAGE_THUNK_DATA32              IMAGE_THUNK_DATA;
typedef PIMAGE_THUNK_DATA32             PIMAGE_THUNK_DATA;
#define IMAGE_SNAP_BY_ORDINAL(Ordinal)  IMAGE_SNAP_BY_ORDINAL32(Ordinal)
typedef IMAGE_TLS_DIRECTORY32           IMAGE_TLS_DIRECTORY;
typedef PIMAGE_TLS_DIRECTORY32          PIMAGE_TLS_DIRECTORY;
#endif
#endif
#define IMAGE_REL_BASED_ABSOLUTE 0
#define IMAGE_REL_BASED_HIGH 1
#define IMAGE_REL_BASED_LOW 2
#define IMAGE_REL_BASED_HIGHLOW 3
#define IMAGE_REL_BASED_HIGHADJ 4
#define IMAGE_REL_BASED_MIPS_JMPADDR 5
#define IMAGE_REL_BASED_MIPS_JMPADDR16 9
#define IMAGE_REL_BASED_IA64_IMM64 9
#define IMAGE_REL_BASED_DIR64 10
typedef struct _LDR_DATA_TABLE_ENTRY {
    LIST_ENTRY InLoadOrderLinks;
    LIST_ENTRY InMemoryOrderLinks;
    LIST_ENTRY InInitializationOrderLinks;
    PVOID DllBase;
    PVOID EntryPoint;
    ULONG SizeOfImage;
    UNICODE_STRING FullDllName;
    UNICODE_STRING BaseDllName;
    ULONG Flags;
    USHORT LoadCount;
    USHORT TlsIndex;
    union {
        LIST_ENTRY HashLinks;
        struct {
            PVOID SectionPointer;
            ULONG CheckSum;
        };
    };
    union {
        struct {
            ULONG TimeDateStamp;
        };
        struct {
            PVOID LoadedImports;
        };
    };
} LDR_DATA_TABLE_ENTRY,*PLDR_DATA_TABLE_ENTRY;
#pragma pack(1)
typedef struct ServiceDescriptorEntry {
    unsigned int *ServiceTableBase;
    unsigned int *ServiceCounterTableBase;
    unsigned int NumberOfServices;
    unsigned char *ParamTableBase;
} ServiceDescriptorTableEntry_t, *PServiceDescriptorTableEntry_t;
#pragma pack()
typedef NTSTATUS (*NTCREATEFILE)(
    OUT PHANDLE  FileHandle,
    IN ACCESS_MASK  DesiredAccess,
    IN POBJECT_ATTRIBUTES  ObjectAttributes,
    OUT PIO_STATUS_BLOCK  IoStatusBlock,
    IN PLARGE_INTEGER  AllocationSize  OPTIONAL,
    IN ULONG  FileAttributes,
    IN ULONG  ShareAccess,
    IN ULONG  CreateDisposition,
    IN ULONG  CreateOptions,
    IN PVOID  EaBuffer  OPTIONAL,
    IN ULONG  EaLength
    );
#define __Max(a,b)  a>b?a:b
PVOID g_lpVirtualPointer;
ULONG g_ntcreatefile;
ULONG g_fastcall_hookpointer;
ULONG g_goto_origfunc;
ULONG g_new_kernel_inc;

ServiceDescriptorTableEntry_t *g_pnew_service_table;






















__declspec(dllimport) ServiceDescriptorTableEntry_t KeServiceDescriptorTable;
void PageProtectOn() {
    __asm {
        mov  eax, cr0
        or   eax, 10000h
        mov  cr0, eax
        sti
    }
}
void PageProtectOff() {
    __asm {
        cli
        mov  eax, cr0
        and  eax, not 10000h
        mov  cr0, eax
    }
}
ULONG SearchHookPointer(ULONG StartAddress) {
    ULONG i = 0;
    UCHAR *p = (UCHAR *)StartAddress;
    for (i = 0; i < 200; i++) {
        if (*p == 0x2b && 
            *(p + 1) == 0xe1 && 
            *(p + 2) == 0xc1 && 
            *(p + 3) == 0xe9 && 
            *(p + 4) == 0x02) {
            return (ULONG)p;
        }
        p--;
    }
    return 0;
}
ULONG FilterKiFastCallEntry(ULONG ServiceTableBase, ULONG NumberOfServices, ULONG OrigFuncAddress) {
    ULONG ProcessObj;
    ProcessObj = *(ULONG*)((ULONG)PsGetCurrentThread()+0x150);
    if (ServiceTableBase == (ULONG)KeServiceDescriptorTable.ServiceTableBase) {
        if (strstr((char*)ProcessObj+0x16c, "llydbg") != 0){
            // 让自己用来调试的软件走新的通道，使得能够轻松绕过各种 hook 反调试
            // 另外需要注意的是，该驱动要早于 ssdt 被修改前加载，这样新的 ssdt 表地址才会准确，否则可能会导致蓝屏
            // KdPrint(("Numb:%X Orig:%X INC:%X plus:%X", NumberOfServices, OrigFuncAddress, g_new_kernel_inc, (OrigFuncAddress + g_new_kernel_inc)));
            return g_pnew_service_table->ServiceTableBase[NumberOfServices];
        }
    }
    return OrigFuncAddress;
}
__declspec(naked) VOID NewKiFastCallEntry() {
    __asm{
        pushad
        pushfd
        push    edx
        push    eax
        push    edi
        call    FilterKiFastCallEntry
        mov     [esp+0x18],eax
        popfd
        popad
        sub     esp,ecx
        shr     ecx,2
        jmp     g_goto_origfunc
    }
}
VOID CoverKiFastCallEntry(ULONG HookPointer) {
    ULONG u_temp;
    UCHAR str_jmp_code[5];
    str_jmp_code[0] = 0xE9;
    u_temp = (ULONG)NewKiFastCallEntry - 5 - HookPointer;
    *(ULONG*)&str_jmp_code[1] = u_temp;
    PageProtectOff();
    RtlCopyMemory((PVOID)HookPointer, str_jmp_code, 5);
    PageProtectOn();
}
NTSTATUS NewCreateFile(
    OUT PHANDLE  FileHandle,
    IN ACCESS_MASK  DesiredAccess,
    IN POBJECT_ATTRIBUTES  ObjectAttributes,
    OUT PIO_STATUS_BLOCK  IoStatusBlock,
    IN PLARGE_INTEGER  AllocationSize  OPTIONAL,
    IN ULONG  FileAttributes,
    IN ULONG  ShareAccess,
    IN ULONG  CreateDisposition,
    IN ULONG  CreateOptions,
    IN PVOID  EaBuffer  OPTIONAL,
    IN ULONG  EaLength
    ) {
    ULONG u_call_retaddr;
    __asm{
        pushad
        mov eax, [ebp + 0x4]
        mov u_call_retaddr, eax
        popad
    }
    g_fastcall_hookpointer = SearchHookPointer(u_call_retaddr);
    if (0 == g_fastcall_hookpointer){
        KdPrint(("SearchHookPointer failed."));
    }else{
        KdPrint(("SearchHookPointer success."));
    }
    g_goto_origfunc = g_fastcall_hookpointer + 5;
    CoverKiFastCallEntry(g_fastcall_hookpointer);
    PageProtectOff();
    KeServiceDescriptorTable.ServiceTableBase[66] = (unsigned int)g_ntcreatefile;
    PageProtectOn();
    return ((NTCREATEFILE)g_ntcreatefile)(
        FileHandle, 
        DesiredAccess, 
        ObjectAttributes,
        IoStatusBlock, 
        AllocationSize, 
        FileAttributes, 
        ShareAccess, 
        CreateDisposition, 
        CreateOptions,
        EaBuffer, 
        EaLength
    );
}
VOID HookKiFastCallEntry() {
    HANDLE              hFile;
    OBJECT_ATTRIBUTES   ObjAttr;
    IO_STATUS_BLOCK     IoStatusBlock;
    UNICODE_STRING      usFileName;
    RtlInitUnicodeString(&usFileName, L"\\??\\C:\\Windows\\System32\\ntoskrnl.exe");
    InitializeObjectAttributes(
        &ObjAttr,
        &usFileName,
        OBJ_CASE_INSENSITIVE,
        NULL,
        NULL
    );
    g_ntcreatefile = KeServiceDescriptorTable.ServiceTableBase[66];
    PageProtectOff();
    KeServiceDescriptorTable.ServiceTableBase[66] = (unsigned int)NewCreateFile;
    PageProtectOn();
    ZwCreateFile(
        &hFile,
        FILE_ALL_ACCESS,
        &ObjAttr,
        &IoStatusBlock,
        NULL,
        FILE_ATTRIBUTE_NORMAL,
        FILE_SHARE_READ,
        FILE_OPEN,
        FILE_NON_DIRECTORY_FILE,
        NULL,
        0
    );
    if (NT_SUCCESS(hFile)){
        ZwClose(hFile);
    }
}
VOID UnHookKiFastCallEntry() {
    UCHAR str_origfuncode[5] = { 0x2b, 0xe1, 0xc1, 0xe9, 0x02 };
    if (g_fastcall_hookpointer == 0 ){
        return;
    }
    PageProtectOff();
    RtlCopyMemory((PVOID)g_fastcall_hookpointer, str_origfuncode, 5);
    PageProtectOn();
}
VOID RelocModule(PVOID pNewImage, PVOID pOrigImage){
    ULONG                   Index;
    ULONG                   uRelocTableSize;
    USHORT                  TypeValue;
    USHORT                  *pwOffsetArrayAddress;
    ULONG                   uTypeOffsetArraySize;
    ULONG                   uRelocOffset;
    ULONG                   uRelocAddress;
    PIMAGE_DOS_HEADER       pImageDosHeader;
    PIMAGE_NT_HEADERS       pImageNtHeader;
    IMAGE_DATA_DIRECTORY    ImageDataDirectory;
    IMAGE_BASE_RELOCATION   *pImageBaseRelocation;
    pImageDosHeader = (PIMAGE_DOS_HEADER)pNewImage;
    pImageNtHeader = (PIMAGE_NT_HEADERS)((ULONG)pNewImage + pImageDosHeader->e_lfanew);
    uRelocOffset = (ULONG)pOrigImage - pImageNtHeader->OptionalHeader.ImageBase;
    ImageDataDirectory = pImageNtHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC];
    pImageBaseRelocation = (PIMAGE_BASE_RELOCATION)((ULONG)ImageDataDirectory.VirtualAddress + (ULONG)pNewImage);
    uRelocTableSize = ImageDataDirectory.Size;
    while (uRelocTableSize){
        uTypeOffsetArraySize = (pImageBaseRelocation->SizeOfBlock - sizeof(ULONG)*2)/sizeof(USHORT);
        pwOffsetArrayAddress = pImageBaseRelocation->TypeOffset;
        for (Index = 0; Index < uTypeOffsetArraySize; Index++) {
            TypeValue = pwOffsetArrayAddress[Index];
            if (TypeValue >> 12 == IMAGE_REL_BASED_HIGHLOW ){
                uRelocAddress = (TypeValue & 0xFFF) + pImageBaseRelocation->VirtualAddress + (ULONG)pNewImage;
                if (!MmIsAddressValid((PVOID)uRelocAddress)){
                    continue;
                }
                *(ULONG*)uRelocAddress += uRelocOffset;
            }
        }
        uRelocTableSize -= pImageBaseRelocation->SizeOfBlock;
        pImageBaseRelocation = (IMAGE_BASE_RELOCATION*)(
            (ULONG)pImageBaseRelocation + (ULONG)pImageBaseRelocation->SizeOfBlock);
    }
}
VOID SetNewSSDT(PVOID pNewImage, PVOID pOrigImage, ServiceDescriptorTableEntry_t **pNewSeviceTable) {
    ULONG                           u_index;
    ULONG                           u_offset;
    ServiceDescriptorTableEntry_t   *pnew_ssdt;
    g_new_kernel_inc = (ULONG)pNewImage - (ULONG)pOrigImage;
    pnew_ssdt = (ServiceDescriptorTableEntry_t *)((ULONG)&KeServiceDescriptorTable + g_new_kernel_inc);
    if (!MmIsAddressValid(pnew_ssdt)){
        KdPrint(("pNewSSDT"));
        return;
    }
    pnew_ssdt->NumberOfServices = KeServiceDescriptorTable.NumberOfServices;
    u_offset = (ULONG)KeServiceDescriptorTable.ServiceTableBase - (ULONG)pOrigImage;
    pnew_ssdt->ServiceTableBase = (unsigned int*)((ULONG)pNewImage + u_offset);
    if (!MmIsAddressValid(pnew_ssdt->ServiceTableBase)) {
        KdPrint(("pNewSSDT->ServiceTableBase:%X",pnew_ssdt->ServiceTableBase));
        return;
    }
    for (u_index = 0;u_index<pnew_ssdt->NumberOfServices;u_index++) {
        pnew_ssdt->ServiceTableBase[u_index] += g_new_kernel_inc;
    }
    u_offset = (ULONG)KeServiceDescriptorTable.ParamTableBase - (ULONG)pOrigImage;
    pnew_ssdt->ParamTableBase = (unsigned char*)((ULONG)pNewImage + u_offset);
    if (!MmIsAddressValid(pnew_ssdt->ParamTableBase)) {
        KdPrint(("pNewSSDT->ParamTableBase"));
        return;
    }
    RtlCopyMemory(pnew_ssdt->ParamTableBase,KeServiceDescriptorTable.ParamTableBase,pnew_ssdt->NumberOfServices*sizeof(char));
    *pNewSeviceTable = pnew_ssdt;
    KdPrint(("set new ssdt success."));
}
NTSTATUS ReadFileToMemory(wchar_t* filename, PVOID* lpVirtualAddress, PVOID pOrigImage){
    NTSTATUS                status;
    UNICODE_STRING          ufilename;
    HANDLE                  hFile;
    LARGE_INTEGER           FileOffset;
    OBJECT_ATTRIBUTES       ObjAttr;
    IO_STATUS_BLOCK         IoStatusBlock;
    IMAGE_DOS_HEADER        ImageDosHeader;
    IMAGE_NT_HEADERS        ImageNtHeader;
    IMAGE_SECTION_HEADER    *pImageSectionHeader;
    IMAGE_DATA_DIRECTORY    ImageDataDirectory;
    ULONG                   Index;
    PVOID                   lpVirtualPointer;
    ULONG                   SecVirtualAddress, SizeOfSection;
    ULONG                   PointerToRawData;
    if (!MmIsAddressValid(filename)){
        return STATUS_UNSUCCESSFUL;
    }
    RtlInitUnicodeString(&ufilename, filename);
    InitializeObjectAttributes(
        &ObjAttr,
        &ufilename,
        OBJ_CASE_INSENSITIVE,
        NULL,
        NULL
    );
    status = ZwCreateFile(
        &hFile,
        FILE_ALL_ACCESS,
        &ObjAttr,
        &IoStatusBlock,
        NULL,
        FILE_ATTRIBUTE_NORMAL,
        FILE_SHARE_READ,
        FILE_OPEN,
        FILE_NON_DIRECTORY_FILE,
        NULL,
        0
    );
    if (!NT_SUCCESS(status)){
        KdPrint(("ZwCreatFile Failed."));
        return status;
    }
    // 读取 DOS headers.
    FileOffset.QuadPart = 0;
    status = ZwReadFile(
        hFile,
        NULL,
        NULL,
        NULL,
        &IoStatusBlock,
        &ImageDosHeader,
        sizeof(IMAGE_DOS_HEADER),
        &FileOffset,
        NULL
    );
    if (!NT_SUCCESS(status)){
        KdPrint(("ZwReadFile dos Failed."));
        ZwClose(hFile);
        return status;
    }
    // 读取 nt headers.
    FileOffset.QuadPart = ImageDosHeader.e_lfanew;
    status = ZwReadFile(
        hFile,
        NULL,
        NULL,
        NULL,
        &IoStatusBlock,
        &ImageNtHeader,
        sizeof(IMAGE_NT_HEADERS),
        &FileOffset,
        NULL
    );
    if (!NT_SUCCESS(status)){
        KdPrint(("ZwReadFile nt Failed."));
        ZwClose(hFile);
        return status;
    }
    // 申请区段内存空间，读取区段
    pImageSectionHeader = ExAllocatePool(
        NonPagedPool, 
        sizeof(IMAGE_SECTION_HEADER)*ImageNtHeader.FileHeader.NumberOfSections
    );
    if (pImageSectionHeader == 0){
        KdPrint(("ExAllocatePool pImageSectionHeader Failed."));
        ZwClose(hFile);
        return STATUS_UNSUCCESSFUL;
    }
    FileOffset.QuadPart += sizeof(IMAGE_NT_HEADERS);
    status = ZwReadFile(
        hFile,
        NULL,
        NULL,
        NULL,
        &IoStatusBlock,
        pImageSectionHeader,
        sizeof(IMAGE_SECTION_HEADER)*ImageNtHeader.FileHeader.NumberOfSections,
        &FileOffset,
        NULL
    );
    if (!NT_SUCCESS(status)){
        KdPrint(("ZwReadFile nt Failed."));
        ExFreePool(pImageSectionHeader);
        ZwClose(hFile);
        return status;
    }
    lpVirtualPointer = ExAllocatePool(
        NonPagedPool, 
        ImageNtHeader.OptionalHeader.SizeOfImage
    );
    if (lpVirtualPointer == 0){
        KdPrint(("ExAllocatePool lpVirtualPointer Failed."));
        ExFreePool(pImageSectionHeader);
        ZwClose(hFile);
        return STATUS_UNSUCCESSFUL;
    }
    // 拷贝数据到内存空间
    memset(lpVirtualPointer, 0, ImageNtHeader.OptionalHeader.SizeOfImage);
    RtlCopyMemory(
        lpVirtualPointer, 
        &ImageDosHeader, 
        sizeof(IMAGE_DOS_HEADER)
    );
    RtlCopyMemory(
        (PVOID)((ULONG)lpVirtualPointer+ImageDosHeader.e_lfanew), 
        &ImageNtHeader, 
        sizeof(IMAGE_NT_HEADERS)
    );
    RtlCopyMemory(
        (PVOID)((ULONG)lpVirtualPointer+ImageDosHeader.e_lfanew+sizeof(IMAGE_NT_HEADERS)), 
        pImageSectionHeader, 
        sizeof(IMAGE_SECTION_HEADER)*ImageNtHeader.FileHeader.NumberOfSections
    );
    for (Index = 0; Index < ImageNtHeader.FileHeader.NumberOfSections; Index++) {
        SecVirtualAddress = pImageSectionHeader[Index].VirtualAddress;
        SizeOfSection = __Max(  pImageSectionHeader[Index].SizeOfRawData,
                                pImageSectionHeader[Index].Misc.VirtualSize );
        PointerToRawData = pImageSectionHeader[Index].PointerToRawData;
        FileOffset.QuadPart = PointerToRawData;
        status = ZwReadFile(
            hFile,
            NULL,
            NULL,
            NULL,
            &IoStatusBlock,
            (PVOID)((ULONG)lpVirtualPointer+SecVirtualAddress),
            SizeOfSection,
            &FileOffset,
            NULL
        );
        if (!NT_SUCCESS(status)){
            KdPrint(("read failed is pImageSectionHeader[%d]", Index));
            ExFreePool(pImageSectionHeader);
            ExFreePool(lpVirtualPointer);
            ZwClose(hFile);
            return status;
        }
    }
    RelocModule(lpVirtualPointer, pOrigImage);
    SetNewSSDT(lpVirtualPointer, pOrigImage,&g_pnew_service_table);
    ExFreePool(pImageSectionHeader);
    *lpVirtualAddress = lpVirtualPointer;
    ZwClose(hFile);
    return status;
}

PLDR_DATA_TABLE_ENTRY SearchDriver(PDRIVER_OBJECT pDriverObject, wchar_t *strDriverName){
    LDR_DATA_TABLE_ENTRY *pDataTableEntry;
    LDR_DATA_TABLE_ENTRY *pCheckTableEntry;
    UNICODE_STRING       usMuduleName;
    PLIST_ENTRY          pList;
    pDataTableEntry = (LDR_DATA_TABLE_ENTRY *)pDriverObject->DriverSection;
    if (!pDataTableEntry){
        return 0;
    }
    RtlInitUnicodeString(&usMuduleName, strDriverName);
    pList = pDataTableEntry->InLoadOrderLinks.Flink;
    while (pList != &pDataTableEntry->InLoadOrderLinks){
        pCheckTableEntry = (LDR_DATA_TABLE_ENTRY *)pList;
        if (0 == RtlCompareUnicodeString(&usMuduleName, &pCheckTableEntry->BaseDllName, FALSE)){
            KdPrint(("find table entry: %wZ", &pCheckTableEntry->FullDllName));
            return pCheckTableEntry;
        }
        pList = pList->Flink;
    }
    return 0;
}







VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
    if (g_lpVirtualPointer){
        ExFreePool(g_lpVirtualPointer);
        UnHookKiFastCallEntry();
    }
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
    LDR_DATA_TABLE_ENTRY   *pLdrDataTableEntry;
    pLdrDataTableEntry = SearchDriver(pDriverObject, L"ntoskrnl.exe"); // 这里不跟随下面的注释修改，固定即可。
    if (pLdrDataTableEntry){
        // 一个十分重要的点就是在这里的读取的程序需要考虑该电脑是否支持 PAE 模式，选则错了模式基本距离蓝屏不远了。
        // 如果没使用 PAE 模式则加载文件 L"\\??\\C:\\Windows\\System32\\ntoskrnl.exe"
        // 如果使用了 PAE 模式则加载文件 L"\\??\\C:\\Windows\\System32\\ntkrnlpa.exe"
        // 多核情况不太清楚，这里给出一点描述用于后续开发，简单来说是同一套源代码根据编译选项的不同而编译出四个可执行文件，看机器选择：
        // ntoskrnl - 单处理器，不支持PAE
        // ntkrnlpa - 单处理器，支持PAE
        // ntkrnlmp - 多处理器，不支持PAE
        // ntkrpamp - 多处理器，支持PAE
        ReadFileToMemory(L"\\??\\C:\\Windows\\System32\\ntoskrnl.exe", &g_lpVirtualPointer, pLdrDataTableEntry->DllBase);
        g_new_kernel_inc = (ULONG)g_lpVirtualPointer - (ULONG)pLdrDataTableEntry->DllBase;
        KdPrint(("g_lpVirtualPointer:%X", g_lpVirtualPointer));
        KdPrint(("pLdrDataTableEntry->DllBase:%X", pLdrDataTableEntry->DllBase));
        KdPrint(("g_new_kernel_inc:%X", g_new_kernel_inc));
        HookKiFastCallEntry();
    }
    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
