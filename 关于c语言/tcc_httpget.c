// c语言实现简单的get请求
// cmd> gcc .\tcc_httpget.c -lws2_32
// cmd> tcc .\tcc_httpget.c -I"C:\Users\...\winapi-full-for-0.9.27\include\winapi" -lws2_32

#include <stdio.h>
#include <winsock2.h>
#include <windows.h>

char* getip(char* url){
    WSADATA wsaData;
    WSAStartup(MAKEWORD(1,1), &wsaData);
    HOSTENT *pHost = gethostbyname(url);
    if(NULL != pHost) {
        return inet_ntoa(*((struct in_addr *)pHost->h_addr)) ;
    }
    return "none";
}

int sendinfo(char* method, char* url, char* body, int port) {
    // 通过dns获取url的ip地址
    char *ipstr = getip(url);
    if(strcmp(ipstr, "none") == 0) return 0;
    SOCKET ssocket = INVALID_SOCKET;
    SOCKADDR_IN sockaddr_in = {0};
    char send_message[4096] = {0};
    char resp_message[4096] = {0};
    char *pRcv = resp_message;
    int numb = 0;
    int conn = SOCKET_ERROR;
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 0), &wsaData);
    // 生成请求头，请求类似如下内容，除了GET..这一行，示例的其余行都非必须，一般视情况而定，结尾接上 \r\n\r\n
    // 如果是POST请求则在headers后接 \n\n 然后接上编码后的body然后再接上 \r\n\r\n
    // GET http://www.baidu.com HTTP/1/1
    // accept-encoding: gzip, deflate
    // accept-language: zh-CN,zh;q=0.9
    // accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    // user-agent: Chrome/68.0.3440.75 Safari/537.36
    strcat(send_message, method);
    strcat(send_message, " http://");
    strcat(send_message, url);
    strcat(send_message, " HTTP/1.1\n");
    strcat(send_message, "accept-language: zh-CN,zh;q=0.9\n");
    strcat(send_message, "accept: */*\n");
    strcat(send_message, "\n");
    strcat(send_message, body);
    strcat(send_message, "\r\n\r\n");
    sockaddr_in.sin_family = AF_INET;
    sockaddr_in.sin_port = htons(port);
    sockaddr_in.sin_addr.s_addr = inet_addr(ipstr);
    ssocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    conn = connect(ssocket, (SOCKADDR*)&sockaddr_in, sizeof(SOCKADDR));
    if(conn == SOCKET_ERROR) {
        return 0;
    }
    else {
        send(ssocket, (char*)send_message, sizeof(send_message),0);
        while(1) {
            pRcv += recv(ssocket, pRcv, 2048, 0);
            if(numb == 0 || numb == -1)
                break;
        }
        closesocket(ssocket);
    }
    printf("%s\n", resp_message);
    return 0;
}

int get(char* url){
    sendinfo("GET", url, "", 80);
}

int post(char* url, char* body){
    sendinfo("POST", url, body, 80);
}

int main(){
    get("www.baidu.com");
}