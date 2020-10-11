#include "variables.h"

Bitmap* ChangeImgColor(string img_path)
{
	// 1.把图像从文件里导入进来
	wchar_t img_pth_wc[100];
	StringToWchar(img_path, img_pth_wc);
	Bitmap* pimage = new Bitmap(img_pth_wc);
	// 2.把文件的颜色二值化
	for (int y = 0; y <= pimage->GetHeight() - 1; y++) {
		for (int x = 0; x <= pimage->GetWidth() - 1; x++) {
			Color color_1px;
			Color color_1px2;
			bool is_border = false;
			pimage->GetPixel(x, y, &color_1px);
			pimage->GetPixel(0, 0, &color_1px2);
			//判断这个点是不是边界点
			if (y <= pimage->GetHeight() - 2) {
				Color color_px_bottom;
				pimage->GetPixel(x, y + 1, &color_px_bottom);
				if (abs(color_1px.GetR() - color_px_bottom.GetR()) >= 32)
					is_border = true;
			}
			if (x <= pimage->GetWidth() - 2) {
				Color color_px_r;
				pimage->GetPixel(x + 1, y, &color_px_r);
				if (abs(color_1px.GetR() - color_px_r.GetR()) >= 32)
					is_border = true;
			}
			// 绘制该点的颜色
			if (is_border) { // 线条颜色
				pimage->SetPixel(x, y, Color(LineColor[0], LineColor[1], LineColor[2]));
			}
			else if (color_1px.GetR() >= 224) { //图片着色颜色
				pimage->SetPixel(x, y, Color(ImageColor[0], ImageColor[1], ImageColor[2]));
			}
			else {
				pimage->SetPixel(x, y, Color(BackgroundColor[0], BackgroundColor[1], BackgroundColor[2]));
			}
		}
	}
	// 3.绘制边框和坐标
	for (int y = 0; y <= pimage->GetHeight() - 1; y++) {
		for (int x = 0; x <= pimage->GetWidth() - 1; x++) {
			if (y == 0 || y == pimage->GetHeight() - 1 || x == 0 || x == pimage->GetWidth() - 1) { //边框
				pimage->SetPixel(x, y, Color(LineColor[0], LineColor[1], LineColor[2]));
			}
			if (y % (pimage->GetHeight() / 10) == 0 || x % (pimage->GetWidth() / 10) == 0) { //坐标线
				pimage->SetPixel(x, y, Color(AxisColor[0], AxisColor[1], AxisColor[2]));
			}
		}
	}
	return pimage;
}

bool TaskManagerPrint::FindHWND1Layer(string layer_name, WNDENUMPROC lpEnumFunc)
{
	MatchSuccess = false;
	strcpy(ClassNameToMatch, layer_name.c_str());
	EnumChildWindows(TMWindow, lpEnumFunc, 0);
	if (!MatchSuccess) {
		printf("%s not found\n", layer_name.c_str());
		return false;
	}
	return true;
}

bool TaskManagerPrint::InitHWND()
{
	// 1.找到任务管理器对应的窗口，并记录这个窗口的大小
	TMWindow = FindWindow("TaskManagerWindow", "任务管理器");
	GetWindowRect(TMWindow, &TMWindowRect);
	// 2.找到下一层NativeHWNDHost对应的窗口
	if (!FindHWND1Layer("NativeHWNDHost", EnumChildWindowsCb))
		return false;
	// 3.找到下一层DirectUIHWND的窗口
	if (!FindHWND1Layer("DirectUIHWND", EnumChildWindowsCb))
		return false;
	// 4.找到下一层CtrlNotifySink的窗口
	if (!FindHWND1Layer("CtrlNotifySink", EnumCtrlNotifySinkCb))
		return false;
	// 5.找到下一层CvChartWindow的窗口
	if (!FindHWND1Layer("CvChartWindow", EnumChildWindowsCb))
		return false;
	GetWindowRect(TMWindow, &TMWindowRect);
	return true;
}

BOOL CALLBACK EnumChildWindowsCb(HWND hwnd, LPARAM lparam)
{
	char class_name[256];
	GetClassName(hwnd, class_name, 255);
	if (strcmp(TMPrintObj.ClassNameToMatch, class_name) == 0){
		// 进入这里说明找到想要的子窗口了
		TMPrintObj.TMWindow = hwnd;
		TMPrintObj.MatchSuccess = true;
		return false;  //返回false表示不用再回调了
	}
	return true;
}

BOOL CALLBACK EnumCtrlNotifySinkCb(HWND hwnd, LPARAM lparam)
{
	char class_name[256];
	GetClassName(hwnd, class_name, 255);
	if (strcmp(TMPrintObj.ClassNameToMatch, class_name) == 0) {
		// 对于“CtrlNotifySink”这个层级，还需要根据窗口的大小来判断是不是我们想要的窗口
		RECT rect;
		GetWindowRect(hwnd, &rect);
		if (rect.bottom - rect.top >= 100 && rect.right - rect.left >= 100){
			TMPrintObj.TMWindow = hwnd;
			TMPrintObj.MatchSuccess = true;
			return false;  //返回false表示不用再回调了
		}
	}
	return true;
}

void TaskManagerPrint::Show1Img(Bitmap* pbitmap)
{
	// 1.获取要绘制的窗口Graphics
	HDC hdc = GetDC(TMWindow);
	Graphics* graphics = Graphics::FromHWND(TMWindow); //Graphics::FromHDC(hdc);
	// 2.把图像画进去
	graphics->DrawImage(pbitmap, 2, 2, TMWindowRect.right - TMWindowRect.left - 4, TMWindowRect.bottom - TMWindowRect.top - 4);
}

void TaskManagerPrint::MainTask()
{
	//1.处理图片
	Bitmap** pbitmaps = new Bitmap * [FRAME_END - FRAME_START + 1]; //ChangeImgColor(ImgPath1);
	for (int frame_it = FRAME_START; frame_it <= FRAME_END; frame_it++)
	{
		char img_path[50] = { 0 };
		sprintf(img_path, "pics/%04d.png", frame_it);
		pbitmaps[frame_it - FRAME_START] = ChangeImgColor(string(img_path));
		printf("curr frame id = %d\n", frame_it);
	}
	_sleep(1500);
	for (int frame_it = FRAME_START; frame_it <= FRAME_END; frame_it++) {
		Show1Img(pbitmaps[frame_it - FRAME_START]);
		_sleep(int(1000.0 / FPS));
	}
}

int main()
{
	// 1.初始化Gdi+
	GdiplusStartupInput gdiplusStartupInput;
	ULONG_PTR gdiplusToken;
	GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
	// 2.执行画图
	int res = TMPrintObj.InitHWND();
	if (res) {
		TMPrintObj.MainTask();
	}
	// 3.结束
	GdiplusShutdown(gdiplusToken);

	system("pause");
	return 0;
}
