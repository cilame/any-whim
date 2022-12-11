// 挂钩系统中断表
// 
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk x64 WIN7
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre x64 WIN7

#include "ntddk.h"

#define WORD  USHORT
#define DWORD ULONG
#define MAKELONG(a,b) ((LONG)(((WORD)((DWORD_PTR)(a) & 0xffff)) | ((DWORD)((WORD)((DWORD_PTR)(b) & 0xffff))) << 16))
typedef struct _IDTR {
    USHORT IDT_Limit;
    USHORT IDT_Lowbase;
    USHORT IDT_Highbase;
}IDTR, *PIDTR;
typedef struct _IDTENTRY{
    unsigned short LowOffset;
    unsigned short selector;
    unsigned char retention:5;
    unsigned char zero1:3;
    unsigned char gate_type:1;
    unsigned char zero2:1;
    unsigned char interrupt_gate_size:1;
    unsigned char zero3:1;
    unsigned char zero4:1;
    unsigned char DPL:2;
    unsigned char P:1;
    unsigned short HiOffset;
}IDTENTRY, *PIDTENTRY;
ULONG g_InterruptFunc3;

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
VOID __stdcall FilterInterruptFunc3(){
    KdPrint(("curr process:%s", (char *)PsGetCurrentProcess()+0x16c));
}
__declspec(naked)
VOID NewInterruptFunc3(){
    __asm{
        pushad
        pushfd
        push fs
        push 0x30
        pop fs
        call FilterInterruptFunc3
        pop fs
        popfd
        popad
        jmp g_InterruptFunc3
    }
}
ULONG GetInterruptFuncAddress(ULONG InterruptIndex){
    IDTR idtr;
    IDTENTRY *idt_entry;
    __asm{
        SIDT idtr
    }
    idt_entry = (IDTENTRY*)MAKELONG(idtr.IDT_Lowbase, idtr.IDT_Highbase);
    return MAKELONG(idt_entry[InterruptIndex].LowOffset, idt_entry[InterruptIndex].HiOffset);
}
VOID SetInterrupt(ULONG InterruptIndex, ULONG NewInterruptFunc){
    UNICODE_STRING  usFuncName;
    ULONG           u_fnKeSetTimeIncrement;
    ULONG           *u_KiProcessorBlock;
    ULONG           idx;
    IDTENTRY        *pIdtEntry;
    RtlInitUnicodeString(&usFuncName, L"KeSetTimeIncrement");
    u_fnKeSetTimeIncrement = (ULONG)MmGetSystemRoutineAddress(&usFuncName);
    if (!MmIsAddressValid((PVOID)u_fnKeSetTimeIncrement)){
        return;
    }
    u_KiProcessorBlock = *(ULONG**)(u_fnKeSetTimeIncrement + 44);
    idx = 0;
    while (u_KiProcessorBlock[idx]){
        pIdtEntry = *(IDTENTRY**)(u_KiProcessorBlock[idx]-0xe8);
        g_InterruptFunc3 = MAKELONG(pIdtEntry[3].LowOffset, pIdtEntry[3].HiOffset);
        PageProtectOff();
        pIdtEntry[InterruptIndex].LowOffset = (unsigned short)((ULONG)NewInterruptFunc & 0xffff);
        pIdtEntry[InterruptIndex].HiOffset = (unsigned short)((ULONG)NewInterruptFunc >> 16);
        PageProtectOn();
        idx++;
    }
}
VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
    SetInterrupt(3, g_InterruptFunc3);
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
    g_InterruptFunc3 = GetInterruptFuncAddress(3);
    SetInterrupt(3, (ULONG)NewInterruptFunc3);
    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
