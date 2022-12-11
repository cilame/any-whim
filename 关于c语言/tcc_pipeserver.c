// 管道接收端

#include <windows.h>
#include <stdio.h>

#define PIPE_NAME "\\\\.\\Pipe\\vtestv"

void start_pipe_server(){
    HANDLE PipeHandle;
    DWORD BytesRead;
    CHAR buffer[256] = {0};
    if ((PipeHandle = CreateNamedPipe(PIPE_NAME,PIPE_ACCESS_DUPLEX,PIPE_TYPE_BYTE|PIPE_READMODE_BYTE,1,0,0,1000,NULL)) == INVALID_HANDLE_VALUE){
        printf("CreateNamedPipe failed with error %x \n",GetLastError());
        return;
    }
    printf("Server is now running \n");
    while (1){
        if (ConnectNamedPipe(PipeHandle,NULL) == 0){
            printf("ConnectNamePipe failed with error %x \n",GetLastError());
            CloseHandle(PipeHandle);
            return;
        }
        if(ReadFile(PipeHandle,buffer,sizeof(buffer),&BytesRead,NULL) <= 0){
            printf("ReadFile failed with error %x \n",GetLastError());
            CloseHandle(PipeHandle);
            return;
        }
        printf("byteread = %d,buffer = %s \n",BytesRead,buffer);
        if (DisconnectNamedPipe(PipeHandle) == 0){
            printf("DisconnectNamedPipe failed with error %x \n",GetLastError());
            return;
        }
    }
    CloseHandle(PipeHandle);
}
 
void main() {
    start_pipe_server();
}