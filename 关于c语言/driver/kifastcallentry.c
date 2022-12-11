#include "ntddk.h"
#pragma pack(1)
typedef struct ServiceDescriptorEntry {
    unsigned int *ServiceTableBase;
    unsigned int *ServiceCounterTableBase;
    unsigned int NumberOfServices;
    unsigned char *ParamTableBase;
} ServiceDescriptorTableEntry_t, *PServiceDescriptorTableEntry_t;
#pragma pack()
__declspec(dllimport) ServiceDescriptorTableEntry_t KeServiceDescriptorTable;
ULONG g_ntcreatefile;
ULONG g_fastcall_hookpointer;
ULONG g_goto_origfunc;
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
VOID FilterKiFastCallEntry(ULONG ServiceTableBase, ULONG NumberOfServices) {
    if (ServiceTableBase == (ULONG)KeServiceDescriptorTable.ServiceTableBase) {
        if (NumberOfServices == 190) {
            KdPrint(("%s", (char*)PsGetCurrentProcess() + 0x16c));
        }
    }
}
__declspec(naked)
VOID NewKiFastCallEntry() {
    __asm{
        pushad
        pushfd
        push eax
        push edi
        call FilterKiFastCallEntry
        popfd
        popad
        sub esp, ecx
        shr ecx, 2
        jmp g_goto_origfunc
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
    RtlInitUnicodeString(&usFileName, L"\\??\\C:\\Windows\\System32\\ntkrnlpa.exe");
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

VOID DriverUnload(IN PDRIVER_OBJECT pDriverObject) {
    UnHookKiFastCallEntry();
}
NTSTATUS DriverEntry(IN PDRIVER_OBJECT pDriverObject, IN PUNICODE_STRING RegistryPath) {
    HookKiFastCallEntry();
    pDriverObject->DriverUnload = DriverUnload;
    return STATUS_SUCCESS;
}