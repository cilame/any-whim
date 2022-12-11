// 管道发送端

#include <windows.h>
#include <stdio.h>

#define PIPE_NAME "\\\\.\\Pipe\\vtestv"

void send_pipe(char* message){
    HANDLE PipeHandle;
    DWORD BytesWritten;
    if (WaitNamedPipe(PIPE_NAME, NMPWAIT_WAIT_FOREVER) == 0){
        printf("CreateNamedPipe failed with error %x \n",GetLastError());
        return;
    }
    if ((PipeHandle = CreateFile(
                            PIPE_NAME, GENERIC_READ | GENERIC_WRITE, 
                            0 ,
                            (LPSECURITY_ATTRIBUTES)NULL, 
                            OPEN_EXISTING, 
                            FILE_ATTRIBUTE_NORMAL, 
                            (HANDLE)NULL)
                        ) == INVALID_HANDLE_VALUE) {
        printf("CreateFile failed with error %x \n",GetLastError());
        return;
    }
    if (WriteFile(PipeHandle, message, strlen(message), &BytesWritten, NULL) == 0){
        printf("WriteFile failed with error %x \n",GetLastError());
        CloseHandle(PipeHandle);
        return;
    }
    printf("Wrote %d bytes \n", BytesWritten);
    CloseHandle(PipeHandle);
}

void main() {
    send_pipe("nihaoa xiongdi.");
}