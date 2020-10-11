#ifndef VARIABLES_H_
#define VARIABLES_H_

#include <string>
#include <Windows.h>
#include <ObjIdl.h>
#include <gdiplus.h>
#include <gdiplusgraphics.h>

#pragma comment(lib, "gdiplus.lib")

using namespace std;
using namespace Gdiplus;
using namespace std;

#define FRAME_START 425  //从哪一帧起始
#define FRAME_END 699  //到哪一帧结束
#define FPS 25  //帧率是多少

//extern const string ImgPath1; //第一张图
//extern const string ImgPath2; //第二张图
//extern const int DuraMS;
extern const uint8_t BackgroundColor[3];
extern const uint8_t LineColor[3];
extern const uint8_t AxisColor[3];
extern const uint8_t ImageColor[3];


BOOL CALLBACK EnumChildWindowsCb(HWND hwnd, LPARAM lparam); //查找HWND时的回调函数
BOOL CALLBACK EnumCtrlNotifySinkCb(HWND hwnd, LPARAM lparam); //查找CtrlNotifySink的处理比较特殊，单独写一个函数

class TaskManagerPrint
{
public:
	bool InitHWND(); //找到任务管理器对应的HWND
	void MainTask();
private:
	bool FindHWND1Layer(string layer_name, WNDENUMPROC lpEnumFunc); //查找1个层级的HWND
	void Show1Img(Bitmap* pbitmap); //用任务管理器展示一张图片
public:
	HWND TMWindow; //任务管理器对应的窗口是哪个
	RECT TMWindowRect; //绘图窗口的坐标、长宽数据
	char ClassNameToMatch[256]; //当前回调函数中，应当match哪个名称的HWND
	bool MatchSuccess; //上一次回调函数是否Match到了
};

extern TaskManagerPrint TMPrintObj;

void StringToWchar(string s, wchar_t* wc);

#endif
