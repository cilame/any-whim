#include<d3d9.h>  

// Useless in gcc/g++
// #pragma comment(lib, "d3d9.lib")

// please put "<d3dpath>\Lib\x64" and "<d3dpath>\Include" in env path.
// next use "g++ <thisfile>.cpp -ld3d9" to make this file.

#define WINDOW_CLASS "UGPDX"  
#define WINDOW_NAME  "Drawing Lines"  

BOOL InitializeD3D(HWND hWnd, BOOL fullscreen);
BOOL InitializeObjects();
void RenderScene();
void Shutdown();

LPDIRECT3D9 g_D3D = NULL;
LPDIRECT3DDEVICE9 g_D3DDevice = NULL;
LPDIRECT3DVERTEXBUFFER9 g_VertexBuffer = NULL;

typedef struct {
    float x, y, z, rhw;
    unsigned long color;
} stD3DVertex;
#define D3DFVF_VERTEX (D3DFVF_XYZRHW | D3DFVF_DIFFUSE)   

LRESULT WINAPI MsgProc(HWND hWnd, UINT msg, WPARAM wp, LPARAM lp){
    switch (msg){
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
        break;
    case WM_KEYUP:
        if (wp == VK_ESCAPE) PostQuitMessage(0);
        break;
    }
    return DefWindowProc(hWnd, msg, wp, lp);
}

int WINAPI WinMain(HINSTANCE hInst, HINSTANCE prevhInst,
    LPSTR cmdLine, int show){
    WNDCLASSEX wc = { sizeof(WNDCLASSEX), CS_CLASSDC, MsgProc,
        0, 0, GetModuleHandle(NULL), NULL, LoadCursor(NULL,IDC_ARROW),
        NULL, NULL, WINDOW_CLASS, NULL };
    RegisterClassEx(&wc);
    HWND hWnd = CreateWindow(WINDOW_CLASS, WINDOW_NAME,
        WS_OVERLAPPEDWINDOW, 100, 100,
        640, 480, GetDesktopWindow(), NULL,
        wc.hInstance, NULL);
    if (InitializeD3D(hWnd, FALSE)){ 
        ShowWindow(hWnd, SW_SHOWDEFAULT);
        UpdateWindow(hWnd);
        MSG msg;
        ZeroMemory(&msg, sizeof(msg));
        while (msg.message != WM_QUIT){
            if (PeekMessage(&msg, NULL, 0U, 0U, PM_REMOVE)){
                TranslateMessage(&msg);
                DispatchMessage(&msg);
            }
            else
                RenderScene();
        }
    }
    Shutdown();
    UnregisterClass(WINDOW_CLASS, wc.hInstance);
    return 0;
}

BOOL InitializeD3D(HWND hWnd, BOOL fullscreen){
    D3DDISPLAYMODE displayMode;
    g_D3D = Direct3DCreate9(D3D_SDK_VERSION);
    if (g_D3D == NULL) return FALSE;
    if (FAILED(IDirect3D9_GetAdapterDisplayMode(g_D3D,D3DADAPTER_DEFAULT,
        &displayMode))) return FALSE;
    D3DPRESENT_PARAMETERS d3dpp;
    ZeroMemory(&d3dpp, sizeof(d3dpp));
    if (fullscreen){
        d3dpp.Windowed = FALSE;
        d3dpp.BackBufferWidth = 640;
        d3dpp.BackBufferHeight = 480;
    }
    else
        d3dpp.Windowed = TRUE;
    d3dpp.SwapEffect = D3DSWAPEFFECT_DISCARD;
    d3dpp.BackBufferFormat = displayMode.Format;
    if (FAILED(IDirect3D9_CreateDevice(g_D3D,D3DADAPTER_DEFAULT,
        D3DDEVTYPE_HAL, hWnd, D3DCREATE_HARDWARE_VERTEXPROCESSING,
        &d3dpp, &g_D3DDevice))) return FALSE;
    if (!InitializeObjects()) return FALSE;
    return TRUE;
}

BOOL InitializeObjects(){
    unsigned long col = D3DCOLOR_XRGB(255, 255, 255);
    stD3DVertex objData[] ={
        { 420.0f, 150.0f, 0.5f, 1.0f, col, },
        { 420.0f, 350.0f, 0.5f, 1.0f, col, },
        { 220.0f, 150.0f, 0.5f, 1.0f, col, },
        { 220.0f, 350.0f, 0.5f, 1.0f, col, },
    };
    if (FAILED(IDirect3DDevice9_CreateVertexBuffer(g_D3DDevice,sizeof(objData), 0,
        D3DFVF_VERTEX, D3DPOOL_DEFAULT, &g_VertexBuffer,
        NULL))) return FALSE;
    void *ptr;
    if (FAILED(IDirect3DVertexBuffer9_Lock(g_VertexBuffer,0, sizeof(objData),
        (void**)&ptr, 0))) return FALSE;
    memcpy(ptr, objData, sizeof(objData));
    IDirect3DVertexBuffer9_Unlock(g_VertexBuffer);
    return TRUE;
}

void RenderScene(){
    IDirect3DDevice9_Clear(g_D3DDevice,0, NULL, D3DCLEAR_TARGET,
        D3DCOLOR_XRGB(0, 0, 0), 1.0f, 0);
    IDirect3DDevice9_BeginScene(g_D3DDevice);
    IDirect3DDevice9_SetStreamSource(g_D3DDevice,0, g_VertexBuffer, 0,
        sizeof(stD3DVertex));
    IDirect3DDevice9_SetFVF(g_D3DDevice,D3DFVF_VERTEX);
    IDirect3DDevice9_DrawPrimitive(g_D3DDevice,D3DPT_LINELIST, 0, 2);
    IDirect3DDevice9_EndScene(g_D3DDevice);
    IDirect3DDevice9_Present(g_D3DDevice,NULL, NULL, NULL, NULL);
}

void Shutdown(){
    if (g_D3DDevice != NULL) IDirect3DDevice9_Release(g_D3DDevice);
    if (g_D3D != NULL) IDirect3D9_Release(g_D3D);
    if (g_VertexBuffer != NULL) IDirect3DVertexBuffer9_Release(g_VertexBuffer);
    g_D3DDevice = NULL;
    g_D3D = NULL;
    g_VertexBuffer = NULL;
}