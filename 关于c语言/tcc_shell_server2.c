#include <winsock2.H>
#include <windows.h>
#include <stdio.h>
#include <process.h>
#pragma comment(lib, "ws2_32")
#define CMDBUF 1024*40

// 定义接收反弹 shell 的端口
#define HOOK_PORT 6000

void ReceiveThread(LPVOID lPvoid) {
    SOCKET socketNew = (SOCKET)lPvoid;
    while(1) {
        char receiveBuf[CMDBUF]; // 这里定义大一点否则回传的日志过大会出现问题。
        int len = recv(socketNew, receiveBuf, sizeof(receiveBuf), 0);
        if(len <= 0) {
            closesocket(socketNew);
            printf("socket error...%d\n", len);
            ExitThread(0);
        }
        receiveBuf[len] = 0;
        printf("%s",receiveBuf);
    }
}
void SendThread(LPVOID lPvoid) {
    SOCKET socketNew = (SOCKET)lPvoid;
    char sendBuf[CMDBUF];
    while(1) {
        gets(sendBuf);
        if(SOCKET_ERROR == send(socketNew,sendBuf,strlen(sendBuf),0)) {
            printf("Send Error\n");
            ExitThread(0);
        }
    }
}

void SocketThread(LPVOID lPvoid) {
    SOCKET socketNew = (SOCKET)lPvoid;
    _beginthread(ReceiveThread, 0, (LPVOID)socketNew);
    _beginthread(SendThread, 0, (LPVOID)socketNew);
}

int main(int argc,char **argv) {
    WORD myVersionRequest;
    WSADATA wsaData;
    myVersionRequest = MAKEWORD(2, 3);
    int err;
    err = WSAStartup(myVersionRequest,&wsaData);
    if (!err){
        printf("WSAStartup open.\n");
    }else{
        printf("WSAStartup error!\n");
        return 1;
    }
    SOCKET serSocket = socket(AF_INET, SOCK_STREAM, 0);
    SOCKADDR_IN addr;
    addr.sin_family           = AF_INET;
    addr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
    addr.sin_port             = htons(HOOK_PORT);
    bind(serSocket,(SOCKADDR*)&addr, sizeof(SOCKADDR));
    listen(serSocket,5);
    SOCKADDR_IN clientsocket;
    int len = sizeof(SOCKADDR);
    while(1) {
        SOCKET socketNew = accept(serSocket,(SOCKADDR*)&clientsocket,&len);
        printf("new connection is coming....\n");
        _beginthread(SocketThread, 0, (LPVOID)socketNew);
    }
    return 1;
}