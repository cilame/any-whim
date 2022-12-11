// 使用 tcc 编译时需要注意添加特定的 lib 链接库，因为 tcc 自动会链接库只有少数几个。
// cmd> gcc ./tcc_adjust_privileges.c
// cmd> tcc ./tcc_adjust_privileges.c

#include <stdio.h>
#include <windows.h>
#pragma comment(lib, "Advapi32")

BOOL AdjustPrivileges() {
    HANDLE hToken = NULL;
    TOKEN_PRIVILEGES tp;
    TOKEN_PRIVILEGES oldtp;
    DWORD dwSize = sizeof(TOKEN_PRIVILEGES);
    LUID luid;
    OpenProcessToken(GetCurrentProcess(), TOKEN_ALL_ACCESS, &hToken);
    if (!LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &luid)) {
        CloseHandle(hToken);
        return FALSE;
    }
    ZeroMemory(&tp, sizeof(tp));
    tp.PrivilegeCount = 1;
    tp.Privileges[0].Luid = luid;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    if (!AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(TOKEN_PRIVILEGES), &oldtp, &dwSize)) {
        CloseHandle(hToken);
        return FALSE;
    }
    CloseHandle(hToken);
    return TRUE;
}

int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    if(AdjustPrivileges()){
        MessageBox ( NULL, TEXT ("success, AdjustPrivileges!"), TEXT ("AdjustPrivileges"), MB_OK ) ;
    }
    return 0;
}