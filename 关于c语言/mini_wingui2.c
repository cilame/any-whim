// 纯c开发窗口功能的模板，仅含有少量窗口该有的功能，能实现的功能： Label, button, Text.
// 纯c编写的 windows 窗口有一个最大的好处就是工具体积可以非常小，
// 用 gcc 编译下面内容仅有一百多kb，若是用 tcc 编译甚至能只有几kb
// 另外，如果使用 gcc 编译需要多加一些参数

// >gcc <thisfile> -mwindows -lgdi32
// >tcc <thisfile>

#include <windows.h>
#include <stdio.h>

#define window_X 100
#define window_Y 100
#define window_W 300
#define window_H 150
// 控件使用的ID
#define ID_BTN1 1
#define ID_BTN2 2
#define ID_BTN3 3
#define ID_LAB1 4
#define ID_TXT1 5
static HWND hwndChild[50]; // 控件数量，大一点没关系，只要比你定义的控件数量大即可
// 按钮功能实现
void btn1_func(){
    MessageBox(0,"btn1","btn1",0);
}
void btn2_func(){
    MessageBox(0,"btn2","btn2",0);
}
void btn3_func(){
    static TCHAR *szBuffer;
    static int   iLength;
    iLength = GetWindowTextLength(hwndChild[ID_TXT1]);
    szBuffer = malloc(iLength*2);
    GetWindowText( hwndChild[ID_TXT1], szBuffer, iLength + 1 );
    MessageBox(0,szBuffer,"btn3",0); // 将 ID_TXT1 控件中的文本拿到并使用 messagebox 弹窗展示出来
    free(szBuffer);
}
int _WindowSwitch( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam ){
    HINSTANCE hInst;
    switch( message ) {
        case WM_CREATE:
            hInst = ((LPCREATESTRUCT) lParam) -> hInstance;
            int style_btn   = WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON;
            int style_entry = WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_AUTOVSCROLL;
            int style_label = WS_CHILD | WS_VISIBLE | SS_CENTER;
            hwndChild[ID_BTN1] = CreateWindow( TEXT("button"), TEXT("button 1"), style_btn, 0,0,0,0, hwnd, (HMENU)ID_BTN1, hInst, NULL);
            hwndChild[ID_BTN2] = CreateWindow( TEXT("button"), TEXT("button 2"), style_btn, 0,0,0,0, hwnd, (HMENU)ID_BTN2, hInst, NULL);
            hwndChild[ID_BTN3] = CreateWindow( TEXT("button"), TEXT("button 3"), style_btn, 0,0,0,0, hwnd, (HMENU)ID_BTN3, hInst, NULL);
            hwndChild[ID_LAB1] = CreateWindow( TEXT("static"), TEXT("input"), style_label, 0,0,0,0, hwnd, (HMENU)ID_LAB1, hInst, NULL );
            hwndChild[ID_TXT1] = CreateWindow( TEXT("edit"), NULL, style_entry, 0,0,0,0, hwnd, (HMENU)ID_TXT1, hInst, NULL );
            return 0;
        case WM_SIZE:
            //////////////////////////////    x,  y,  w,   h
            MoveWindow( hwndChild[ID_BTN1],   0,  0, 80,  25, TRUE ); 
            MoveWindow( hwndChild[ID_BTN2],   0, 25, 80,  25, TRUE ); // 在这里注释掉约等于关闭该控件
            MoveWindow( hwndChild[ID_LAB1], 100,  0, 80,  25, TRUE ); // 在这里注释掉约等于关闭该控件
            MoveWindow( hwndChild[ID_TXT1], 100, 25, 80,  25, TRUE ); // 在这里注释掉约等于关闭该控件
            MoveWindow( hwndChild[ID_BTN3], 100, 50, 80,  25, TRUE ); // 在这里注释掉约等于关闭该控件
            return 0;
        case WM_PAINT:
            return 0;
        case WM_COMMAND:
            switch(LOWORD(wParam)) {
                case ID_BTN1:
                    btn1_func();
                    return 0;
                case ID_BTN2:
                    btn2_func();
                    return 0;
                case ID_BTN3:
                    btn3_func();
                    return 0;
            }
            return 0;
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
    }
}








// 简单的热键处理，这里的示例为 Ctrl+Home 组合键快速切换是否显示窗口，Ctrl+End 退出程序两个热键。
DWORD  WINAPI _RegistHotKey( LPARAM lParam ){
    MSG  msg = { 0 };
    char str[256];
    RegisterHotKey(NULL, 0x24, MOD_CONTROL, VK_HOME);
    RegisterHotKey(NULL, 0x25, MOD_CONTROL, VK_END);
    while (GetMessage(&msg, 0, 0, 0)){
        if (WM_HOTKEY == msg.message){
            if (VK_HOME == HIWORD(msg.lParam) && MOD_CONTROL == LOWORD(msg.lParam)){
                if (IsWindowVisible((HANDLE)lParam)){
                    ShowWindow((HANDLE)lParam, SW_HIDE);
                }else{
                    ShowWindow((HANDLE)lParam, SW_RESTORE);
                }
            }
            if (VK_END == HIWORD(msg.lParam) && MOD_CONTROL == LOWORD(msg.lParam)){
                PostMessage((HANDLE)lParam, WM_QUIT, 0, 0);
            }
        }
    }
}
// 后面的内容是固定基本上除了尺寸其他都不需要修改。
LRESULT CALLBACK WndProc( HWND, UINT, WPARAM, LPARAM);
int WINAPI WinMain( HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow ){
    static TCHAR szAppName[] = TEXT( "v" );
    static HWND  hwnd;
    MSG      msg;
    WNDCLASS wndclass;
    wndclass.lpfnWndProc   = WndProc;
    wndclass.style         = CS_HREDRAW | CS_VREDRAW;
    wndclass.hInstance     = hInstance;
    wndclass.cbClsExtra    = 0;
    wndclass.cbWndExtra    = 0;
    wndclass.hbrBackground = CreateSolidBrush(RGB(236, 233, 216));
    wndclass.hCursor       = LoadCursor( NULL, IDC_ARROW );
    wndclass.hIcon         = LoadIcon( NULL, IDI_APPLICATION );
    wndclass.lpszClassName = szAppName;
    wndclass.lpszMenuName  = NULL;
    if (!RegisterClass(&wndclass)) {
        MessageBox( NULL, TEXT("cannot create regist window."), TEXT("error"), MB_OK | MB_ICONERROR );
        return 0;
    }
    hwnd = CreateWindow( szAppName, TEXT("v"), WS_OVERLAPPEDWINDOW & ~WS_SIZEBOX & ~WS_MAXIMIZEBOX & ~WS_MINIMIZEBOX,
        window_X, window_Y,
        window_W, window_H,
        NULL, NULL, hInstance, NULL );
    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)_RegistHotKey, hwnd, 0, 0);
    ShowWindow( hwnd, iCmdShow );
    UpdateWindow( hwnd );
    while (GetMessage(&msg, NULL, 0, 0)){
        TranslateMessage( &msg );
        DispatchMessage( &msg );
    }
    RemoveMenu(GetSystemMenu(hwnd, 0), SC_CLOSE, MF_BYCOMMAND);
    return msg.wParam;
}
LRESULT CALLBACK WndProc( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam ) {
    _WindowSwitch( hwnd, message, wParam, lParam );
    return DefWindowProc( hwnd, message, wParam, lParam );
}