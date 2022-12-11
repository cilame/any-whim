#include "ntddk.h"

// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre ia64 WIN7 no_oacr
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ chk x64 WIN7
// C:\Windows\System32\cmd.exe /k D:\WinDDK\7600.16385.1\bin\setenv.bat D:\WinDDK\7600.16385.1\ fre x64 WIN7

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
    UNICODE_STRING usSymDevice;
    RtlInitUnicodeString(&usSymDevice,L"\\??\\FirstDevice");
    if(pDriverObject->DeviceObject!=NULL){
        IoDeleteDevice(pDriverObject->DeviceObject);
        IoDeleteSymbolicLink(&usSymDevice);
        KdPrint(("delete device success!"));
    }
}

NTSTATUS CreateDevice(PDRIVER_OBJECT pDriverObject){
    NTSTATUS Status;
    PDEVICE_OBJECT pDevObj;
    UNICODE_STRING usDevName;
    UNICODE_STRING usSysName;

    RtlInitUnicodeString(&usDevName,L"\\Device\\FirstDevice");
    Status = IoCreateDevice(
            pDriverObject,\
            NULL,\
            &usDevName,\
            FILE_DEVICE_UNKNOWN,\
            FILE_DEVICE_SECURE_OPEN,\
            TRUE,\
            &pDevObj);
    if(!NT_SUCCESS(Status)){
        return Status;
    }
    pDevObj->Flags |= DO_BUFFERED_IO;

    RtlInitUnicodeString(&usSysName,L"\\??\\FirstDevice");
    Status = IoCreateSymbolicLink(&usSysName,&usDevName);
    if(!NT_SUCCESS(Status)){
        IoDeleteDevice(pDevObj);
        return Status;
    }
    return STATUS_SUCCESS;
}


NTSTATUS CreateCompleteRoutine(PDEVICE_OBJECT pDeviceObject,PIRP pIrp){
    NTSTATUS Status;
    Status = STATUS_SUCCESS;
    KdPrint(("create"));
    pIrp->IoStatus.Status = Status;
    pIrp->IoStatus.Information = 0;
    IoCompleteRequest(pIrp,IO_NO_INCREMENT);
    return Status;
}
NTSTATUS CloseCompleteRoutine(PDEVICE_OBJECT pDeviceObject,PIRP pIrp){
    NTSTATUS Status;
    Status = STATUS_SUCCESS;
    KdPrint(("close"));
    pIrp->IoStatus.Status = Status;
    pIrp->IoStatus.Information = 0;
    IoCompleteRequest(pIrp,IO_NO_INCREMENT);
    return Status;
}
NTSTATUS ReadCompleteRoutine(PDEVICE_OBJECT pDeviceObject,PIRP pIrp){
    NTSTATUS Status;
    Status = STATUS_SUCCESS;
    KdPrint(("read"));
    pIrp->IoStatus.Status = Status;
    pIrp->IoStatus.Information = 0;
    IoCompleteRequest(pIrp,IO_NO_INCREMENT);
    return Status;
}
NTSTATUS WriteCompleteRoutine(PDEVICE_OBJECT pDeviceObject,PIRP pIrp){
    NTSTATUS Status;
    Status = STATUS_SUCCESS;
    KdPrint(("write"));
    pIrp->IoStatus.Status = Status;
    pIrp->IoStatus.Information = 0;
    IoCompleteRequest(pIrp,IO_NO_INCREMENT);
    return Status;
}


NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
    NTSTATUS Status;

    Status = CreateDevice(pDriverObject);
    if(!NT_SUCCESS(Status)){
        KdPrint(("create device failed!"));
    }else{
        KdPrint(("create device success!"));
        KdPrint(("%wZ",pRegistryPath));
    }

    pDriverObject->MajorFunction[IRP_MJ_CREATE] = CreateCompleteRoutine;
    pDriverObject->MajorFunction[IRP_MJ_CLOSE] = CloseCompleteRoutine;
    pDriverObject->MajorFunction[IRP_MJ_READ] = ReadCompleteRoutine;
    pDriverObject->MajorFunction[IRP_MJ_WRITE] = WriteCompleteRoutine;

    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
