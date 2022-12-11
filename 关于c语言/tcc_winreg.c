// cmd> tcc .\tcc_winreg.c -lAdvapi32
#include <windows.h>
#include <stdio.h>
#define START_RUN "C:\\Users\\Administrator\\Desktop\\ctfmon.exe"
 
int main() {
    char *Register = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
    char *Myapp = START_RUN;
    HKEY hKey;
    if(RegOpenKeyExA(HKEY_CURRENT_USER, Register, 0, KEY_ALL_ACCESS, &hKey)== ERROR_SUCCESS) {
        RegSetValueExA(hKey, "Mytest", 0, REG_SZ, (BYTE *)Myapp, strlen(Myapp));
        RegCloseKey(hKey);
        printf("succeed!\n");
    } else {
        printf("Failed!");
        return -1;
    }
    return 0;
}