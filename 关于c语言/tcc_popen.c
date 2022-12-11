// 通过本进程开启别的程序，并将别的程序执行结果通过管道传回显示
// 类似于 python 的 os.popen('...').read() # ...为

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

int runcmd( char* lpCmd ) {
    char buf[2048] = {0};
    DWORD len;
    HANDLE hRead, hWrite;
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    SECURITY_ATTRIBUTES sa;
    sa.nLength = sizeof( sa );
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;
    if( !CreatePipe( &hRead, &hWrite, &sa, 2048 ) ) {
        printf( "CreatePipe fail!(%#X)\n", (unsigned int)GetLastError() );
        return 1;
    }
    ZeroMemory( &si, sizeof( si ) );
    si.cb = sizeof( si );
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;
    si.hStdError = hWrite;
    si.hStdOutput = hWrite;
    if ( !CreateProcess( NULL, lpCmd, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi ) ) {
        printf( "CreateProcess fail!(%#x)\n", (unsigned int)GetLastError() );
        CloseHandle( hRead );
        CloseHandle( hWrite );
        return 1;
    }
    CloseHandle( hWrite );
    while ( ReadFile( hRead, buf, 2047, &len, NULL ) ) {
        printf( buf );
        ZeroMemory( buf, 2047 );
    }
    CloseHandle( hRead );
    return 0;
}

int main( int argc, char** argv ) {
    char cmd[256];
    printf( "input cmd:" );
    gets( cmd );
    runcmd( cmd );
    system( "pause" );
    return 0;
}