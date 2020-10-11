#include "variables.h"

//const string ImgPath1 = "../Test/TestVideo.png"; //第一张图
//const string ImgPath2 = "../Test/TestVideo.png"; //第二张图
//const int DuraMS = 1500; //每一张图持续多少毫秒

const uint8_t BackgroundColor[3] = { 255, 255, 255 }; //背景颜色
const uint8_t LineColor[3] = {17, 152, 187}; //线条的颜色
const uint8_t AxisColor[3] = {206, 226, 240}; //横纵坐标的颜色
const uint8_t ImageColor[3] = { 241, 246, 250 }; //图片着色的颜色

TaskManagerPrint TMPrintObj;

void StringToWchar(string s, wchar_t* wc)
{
	const char* c = s.c_str();
	int len = MultiByteToWideChar(CP_ACP, 0, c, strlen(c), NULL, 0);
	MultiByteToWideChar(CP_ACP, 0, c, strlen(c), wc, len);
	wc[len] = '\0';
}
