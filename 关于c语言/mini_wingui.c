// 纯c开发窗口功能的模板，仅含有少量窗口该有的功能，能实现的功能： Label, button, Text.
// 纯c编写的 windows 窗口有一个最大的好处就是工具体积可以非常小，
// 用 gcc 编译下面内容仅有一百多kb，若是用 tcc 编译甚至能只有几kb
// 另外，如果使用 gcc 编译需要多加一些参数

// >gcc <thisfile> -mwindows -lgdi32
// >tcc <thisfile>

#include <windows.h>
#include <stdio.h>

// 控件使用的ID
#define ID_EDITBOX 1
#define ID_TXTINPT 2
#define ID_SAVEBTN 3
#define ID_CLSBTN  4
static HWND hwndChild[50]; // 控件数量，大一点没关系，只要比你定义的控件数量大即可
int CreateChildWindow(HWND hwnd, HWND *hwndChild, LPARAM lParam) {
    HINSTANCE hInst = ((LPCREATESTRUCT) lParam) -> hInstance;
    int style_editt = WS_CHILD | WS_VISIBLE | ES_LEFT | ES_MULTILINE | ES_AUTOHSCROLL | ES_AUTOVSCROLL;
    int style_edite = WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_AUTOVSCROLL;
    int style_btn   = WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON;
    hwndChild[ID_EDITBOX] = CreateWindow( TEXT("edit"), NULL, style_editt, 0,0,0,0, hwnd, (HMENU)ID_EDITBOX, hInst, NULL );
    hwndChild[ID_TXTINPT] = CreateWindow( TEXT("edit"), NULL, style_edite, 0,0,0,0, hwnd, (HMENU)ID_TXTINPT, hInst, NULL );
    hwndChild[ID_SAVEBTN] = CreateWindow( TEXT("button"), TEXT("mslog"), style_btn, 0,0,0,0, hwnd, (HMENU)ID_SAVEBTN, hInst, NULL);
    hwndChild[ID_CLSBTN]  = CreateWindow( TEXT("button"), TEXT("clear"), style_btn, 0,0,0,0, hwnd, (HMENU)ID_CLSBTN,  hInst, NULL);
    return 0;
}

// 功能函数，用于实现类似按钮的功能处理。
// 开发的功能函数需要在 _WindowSwitch 函数前面定义，且需在 _WindowSwitch 内部使用
int ShowInputContent( TCHAR *Input, TCHAR *content ) {
    char str[256];
    snprintf(str, 256, "%s", Input);
    MessageBox(NULL, str, "title", MB_OK | MB_ICONINFORMATION);
    return 0;
}

int _WindowSwitch( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam ){
    HDC          hdc;
    PAINTSTRUCT  ps;
    RECT         rect;
    static TCHAR *szBuffer;
    static TCHAR szInput[256];
    static TCHAR szLineNum[32];
    static int   iLength;
    int iLineCount, iCharCount;
    switch( message ) {
        case WM_CREATE:
            CreateChildWindow( hwnd, hwndChild, lParam );
            return 0;
        case WM_SIZE:
            GetClientRect(hwnd, &rect);
            // 绘制窗口的位置
            // 文本编辑窗留出底部的 35 像素位置用于放置各个操作相关的元素
            MoveWindow( hwndChild[ID_EDITBOX], 0, 0, rect.right, rect.bottom-35, TRUE );
            MoveWindow( hwndChild[ID_TXTINPT], 60,  rect.bottom-35, 200, 20, TRUE );
            MoveWindow( hwndChild[ID_SAVEBTN], 280, rect.bottom-35, 50,  25, TRUE );
            MoveWindow( hwndChild[ID_CLSBTN ], 340, rect.bottom-35, 50,  25, TRUE );
            return 0;
        case WM_PAINT:
            // 用于展示文本，类似 Label 功能
            GetClientRect(hwnd, &rect);
            hdc = BeginPaint( hwnd, &ps );
            TextOut( hdc, 20, rect.bottom-30, "input:", lstrlen("input:") );
            TextOut( hdc, 400, rect.bottom-30, szLineNum, lstrlen(szLineNum) );
            EndPaint( hwnd, &ps );
            return 0;
        case WM_COMMAND:
            switch(LOWORD(wParam)) {
                case ID_EDITBOX:
                    switch(HIWORD(wParam)) {
                        case EN_UPDATE:
                            // 获取到文本更新消息的同时将 Label 展示内容进行更新
                            iLineCount = SendMessage( hwndChild[ID_EDITBOX], EM_GETLINECOUNT, 0, 0 );
                            iCharCount = GetWindowTextLength( hwndChild[ID_EDITBOX] );
                            wsprintf(szLineNum, "line: %03i char number: %03i", iLineCount, iCharCount);
                            InvalidateRect(hwnd, NULL, FALSE);
                            break;
                        }
                    return 0;
                case ID_SAVEBTN:
                    // 获取编辑窗内容的长度，并分配一定长度内存用于
                    // 获取编辑窗的内容
                    // 获取文件名字窗的内容
                    iLength = GetWindowTextLength(hwndChild[ID_EDITBOX]);
                    szBuffer = malloc(iLength*2);
                    GetWindowText( hwndChild[ID_EDITBOX], szBuffer, iLength + 1 );
                    GetWindowText( hwndChild[ID_TXTINPT], szInput, 256 );
                    ShowInputContent( szInput, szBuffer );
                    return 0;
                case ID_CLSBTN:
                    SetWindowText( hwndChild[ID_EDITBOX], TEXT("") );
                    return 0;
            }
            return 0;
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
    }
}








// 简单的热键处理，这里的示例为 Home 组合键快速切换是否显示窗口，Ctrl+End 退出程序两个热键。
DWORD  WINAPI _RegistHotKey( LPARAM lParam ){
    MSG  msg = { 0 };
    char str[256];
    RegisterHotKey(NULL, 0x24, 0,           VK_HOME);
    RegisterHotKey(NULL, 0x25, MOD_CONTROL, VK_END);
    while (GetMessage(&msg, 0, 0, 0)){
        if (WM_HOTKEY == msg.message){
            // 组合热键的判断方式
            if (VK_HOME == HIWORD(msg.lParam)){
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
// 后面的内容是固定不需要修改的
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
    hwnd = CreateWindow( szAppName, TEXT("vwindow"), WS_OVERLAPPEDWINDOW,
        100, 100,
        600, 200,
        NULL, NULL, hInstance, NULL );
    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)_RegistHotKey, hwnd, 0, 0);
    ShowWindow( hwnd, iCmdShow );
    UpdateWindow( hwnd );
    while (GetMessage(&msg, NULL, 0, 0)){
        TranslateMessage( &msg );
        DispatchMessage( &msg );
    }
    return msg.wParam;
}
LRESULT CALLBACK WndProc( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam ) {
    _WindowSwitch( hwnd, message, wParam, lParam );
    return DefWindowProc( hwnd, message, wParam, lParam );
}