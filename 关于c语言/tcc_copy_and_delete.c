// 如果用gcc，<shellapi.h> 和 <winnetwk.h> 是不需要引入的，并且不需要 -lshell32
// cmd> gcc tcc_copy_and_delete.c
// cmd> tcc tcc_copy_and_delete.c

// 拷贝自身到某个地址，并将自身删除
#include <stdio.h>
#include <windows.h>
#include <shellapi.h>
#include <winnetwk.h>
#include <shlobj.h>
#pragma comment(lib, "shell32")

// 拷贝文件到某地址
char TARGET_PATHFILE[MAX_PATH] = {0};
BOOL copy_self_to_path_name(char* inputpathfile, char*targetpath, char* targetname){
    ZeroMemory(TARGET_PATHFILE, MAX_PATH);
    FILE *fp1, *fp2;
    int i;
    strcat(TARGET_PATHFILE, targetpath);
    strcat(TARGET_PATHFILE, targetname);
    if (strcmp(inputpathfile, TARGET_PATHFILE) == 0) return FALSE;
    fp1 = fopen(inputpathfile, "rb");
    fp2 = fopen(TARGET_PATHFILE, "wb");
    while((i = fgetc(fp1)) != EOF) fputc(i, fp2);
    fclose(fp1); fclose(fp2);
    return TRUE;
}
BOOL copy_self_to_path(char* inputpathfile, char*targetpath){
    char *targetname = strrchr(inputpathfile, '\\');
    return copy_self_to_path_name(inputpathfile, targetpath, targetname);
}

// 获取程序自身绝对路径，获取用户目录，获取系统路径
char SELF_PATH[MAX_PATH] = {0};
char* get_self_path(){
    ZeroMemory(SELF_PATH, MAX_PATH);
    GetModuleFileName(NULL,(LPSTR)SELF_PATH,sizeof(SELF_PATH));  
    return SELF_PATH;
}
char SELF_USER_PATH[MAX_PATH] = {0};
char* get_curr_user_path(){
    ZeroMemory(SELF_USER_PATH, MAX_PATH);
    SHGetSpecialFolderPath(0, SELF_USER_PATH, CSIDL_PROFILE, 0);
    return SELF_USER_PATH;
}
char SELF_SYSTEM_PATH[MAX_PATH] = {0};
char* get_system_path(){
    ZeroMemory(SELF_SYSTEM_PATH, MAX_PATH);
    SHGetSpecialFolderPath(0, SELF_SYSTEM_PATH, CSIDL_SYSTEM, 0);
    return SELF_SYSTEM_PATH;
}

// 删除文件自身
BOOL delete_self() {
    SHELLEXECUTEINFO sei;
    TCHAR szModule [MAX_PATH],szComspec[MAX_PATH],szParams [MAX_PATH];
    if (    (GetModuleFileName(0,szModule,MAX_PATH)!=0) &&
            (GetShortPathName(szModule,szModule,MAX_PATH)!=0) &&
            (GetEnvironmentVariable("COMSPEC",szComspec,MAX_PATH)!=0))   {
        lstrcpy(szParams,"/c del ");
        lstrcat(szParams, szModule);
        lstrcat(szParams, " > nul");
        sei.cbSize = sizeof(sei);
        sei.hwnd = 0;
        sei.lpVerb = "Open";
        sei.lpFile = szComspec;
        sei.lpParameters = szParams;
        sei.lpDirectory = 0; sei.nShow = SW_HIDE;
        sei.fMask = SEE_MASK_NOCLOSEPROCESS;
        if (ShellExecuteEx(&sei)) {
            SetPriorityClass(sei.hProcess,IDLE_PRIORITY_CLASS);
            SetPriorityClass(GetCurrentProcess(),REALTIME_PRIORITY_CLASS);
            SetThreadPriority(GetCurrentThread(),THREAD_PRIORITY_TIME_CRITICAL);
            SHChangeNotify(SHCNE_DELETE,SHCNF_PATH,szModule,0);
            return TRUE;
        }
    }
    return FALSE;
}

int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    if (copy_self_to_path(get_self_path(), get_curr_user_path())){
        delete_self();
    }
}

