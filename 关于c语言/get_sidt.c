
#include "windows.h"
#include "stdio.h"

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

ULONG GetInterruptFuncAddress(ULONG InterruptIndex){
    IDTR idtr;
    IDTENTRY *idt_entry;
    ULONG ret;
    // asm("sidt %eax");
    asm("sidt %0"::"m"(&idtr));
    printf("0x%016lx\n", (ULONG)idtr);
    idt_entry = (IDTENTRY*)MAKELONG(idtr.IDT_Lowbase, idtr.IDT_Highbase);
    printf("0x%016lx\n", (ULONG)idt_entry);
    ret = MAKELONG(idt_entry[InterruptIndex].LowOffset, idt_entry[InterruptIndex].HiOffset);
    printf("0x%016lx\n", (ULONG)ret);
    return ret;
}

int main(int argc, char const *argv[]) {
    printf("hello world.\n");
    ULONG s = GetInterruptFuncAddress(3);
    printf("%d\n", (int)s);
    return 0;
}