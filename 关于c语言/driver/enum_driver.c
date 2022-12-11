#include "ntddk.h"

// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk x64 WIN7
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre x64 WIN7

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

VOID EnumDriver(PDRIVER_OBJECT pDriverObject){
    LDR_DATA_TABLE_ENTRY *pDataTableEntry;
    LDR_DATA_TABLE_ENTRY *pCheckTableEntry;
    PLIST_ENTRY          pList;
    pDataTableEntry = (LDR_DATA_TABLE_ENTRY *)pDriverObject->DriverSection;
    if (!pDataTableEntry){
        return;
    }

    pList = pDataTableEntry->InLoadOrderLinks.Flink;
    while (pList != &pDataTableEntry->InLoadOrderLinks){
        pCheckTableEntry = (LDR_DATA_TABLE_ENTRY *)pList;
        KdPrint(("%wZ", &pCheckTableEntry->FullDllName));
        pList = pList->Flink;
    }
}

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
    KdPrint(("install ok."));
    EnumDriver(pDriverObject);
    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
