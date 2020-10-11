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

#define FRAME_START 425  //����һ֡��ʼ
#define FRAME_END 699  //����һ֡����
#define FPS 25  //֡���Ƕ���

//extern const string ImgPath1; //��һ��ͼ
//extern const string ImgPath2; //�ڶ���ͼ
//extern const int DuraMS;
extern const uint8_t BackgroundColor[3];
extern const uint8_t LineColor[3];
extern const uint8_t AxisColor[3];
extern const uint8_t ImageColor[3];


BOOL CALLBACK EnumChildWindowsCb(HWND hwnd, LPARAM lparam); //����HWNDʱ�Ļص�����
BOOL CALLBACK EnumCtrlNotifySinkCb(HWND hwnd, LPARAM lparam); //����CtrlNotifySink�Ĵ���Ƚ����⣬����дһ������

class TaskManagerPrint
{
public:
	bool InitHWND(); //�ҵ������������Ӧ��HWND
	void MainTask();
private:
	bool FindHWND1Layer(string layer_name, WNDENUMPROC lpEnumFunc); //����1���㼶��HWND
	void Show1Img(Bitmap* pbitmap); //�����������չʾһ��ͼƬ
public:
	HWND TMWindow; //�����������Ӧ�Ĵ������ĸ�
	RECT TMWindowRect; //��ͼ���ڵ����ꡢ��������
	char ClassNameToMatch[256]; //��ǰ�ص������У�Ӧ��match�ĸ����Ƶ�HWND
	bool MatchSuccess; //��һ�λص������Ƿ�Match����
};

extern TaskManagerPrint TMPrintObj;

void StringToWchar(string s, wchar_t* wc);

#endif
