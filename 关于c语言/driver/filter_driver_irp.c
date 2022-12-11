#include "ntddk.h"

// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk x64 WIN7
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre x64 WIN7

NTKERNELAPI
NTSTATUS
NTAPI
ObReferenceObjectByName (
    IN PUNICODE_STRING  ObjectName,
    IN ULONG            Attributes,
    IN PACCESS_STATE    PassedAccessState OPTIONAL,
    IN ACCESS_MASK      DesiredAccess OPTIONAL,
    IN POBJECT_TYPE     ObjectType,
    IN KPROCESSOR_MODE  AccessMode,
    IN OUT PVOID        ParseContext OPTIONAL,
    OUT PVOID           *Object
);

extern POBJECT_TYPE *IoDriverObjectType;

// global
PDRIVER_OBJECT   g_FilterDriverObject;
PDRIVER_DISPATCH gfn_OrigReadCompleteRoutine;

NTSTATUS FilterReadCompleteRoutine(
    IN struct _DEVICE_OBJECT  *DeviceObject,
    IN struct _IRP  *Irp){
    KdPrint(("read filter ok."));
    return gfn_OrigReadCompleteRoutine(DeviceObject, Irp);
}

NTSTATUS FilterDriverQuery(){
    NTSTATUS       status;
    UNICODE_STRING usObjectName;
    RtlInitUnicodeString(&usObjectName, L"\\Driver\\Xuetr");

    status = ObReferenceObjectByName(
        &usObjectName,
        OBJ_CASE_INSENSITIVE,
        NULL,
        0,
        *IoDriverObjectType,
        KernelMode,
        NULL,
        (PVOID *)&g_FilterDriverObject
    );
    if (!NT_SUCCESS(status)){
        KdPrint(("ObReferenceObjectByName failed."));
        return status;
    }
    gfn_OrigReadCompleteRoutine = g_FilterDriverObject->MajorFunction[IRP_MJ_READ];
    g_FilterDriverObject->MajorFunction[IRP_MJ_READ] = FilterReadCompleteRoutine;
    ObDereferenceObject(g_FilterDriverObject);// 操作计数减一
    return STATUS_SUCCESS;
}

VOID UnFilterDriverQuery(){
    if (!MmIsAddressValid(g_FilterDriverObject)){
        g_FilterDriverObject->MajorFunction[IRP_MJ_READ] = gfn_OrigReadCompleteRoutine;
    }
}

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
    UnFilterDriverQuery();
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
    KdPrint(("install ok."));

    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
