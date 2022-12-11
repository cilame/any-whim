#include "ntddk.h"

#pragma(1)
typedef struct ServiceDescriptorEntry{
    unsigned int *ServiceTableBase;
    unsigned int *ServiceCounterTableBase;
    unsigned int NumberOfServices;
    unsigned char *ParamTableBase;
} ServiceDescriptorTableEntry_t, *PServiceDescriptorTableEntry;
#pragma()

__declspec(dllimport)ServiceDescriptorTableEntry_t KeServiceDescriptorTable;

void PageProtectOff(){
    __asm{
        cli
        mov eax,cr0
        and eax,not 10000h
        mov cr0,eax
    }
}

void PageProtectOn(){
    __asm{
        mov eax,cr0
        or eax,10000h
        mov cr0,eax
        sti
    }
}

ULONG g_ntopenkey;
ULONG g_jmp_orig_ntopenkey;
UCHAR g_orig_funcode[5];

VOID FilterNtOpenKey(){
    KdPrint(("%s",(char*)PsGetCurrentProcess()+0x16c));
}

__declspec(naked)
void NewNtOpenKey(){
    __asm{
        pushad
        call FilterNtOpenKey
        popad
        pop eax
        mov edi,edi
        push ebp
        mov ebp,esp
        jmp g_jmp_orig_ntopenkey
    }
}

void HookNtOpenKey(){
    ULONG u_jmp_temp;
    UCHAR jmp_code[5];

    g_ntopenkey = KeServiceDescriptorTable.ServiceTableBase[182];
    g_jmp_orig_ntopenkey = g_ntopenkey + 5;

    u_jmp_temp = (ULONG)NewNtOpenKey - g_ntopenkey - 5;
    jmp_code[0] = 0xE8;
    *(ULONG*)&jmp_code[1] = u_jmp_temp;

    PageProtectOff();
    RtlCopyMemory(g_orig_funcode,(PVOID)g_ntopenkey,5);
    RtlCopyMemory((PVOID)g_ntopenkey,jmp_code,5);
    PageProtectOn();
}

void UnHookOpenKey(){
    PageProtectOff();
    RtlCopyMemory((PVOID)g_ntopenkey,g_orig_funcode,5);
    PageProtectOn();
}

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
    UnHookOpenKey();
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
    HookNtOpenKey();
    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
