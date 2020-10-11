#include "variables.h"

//const string ImgPath1 = "../Test/TestVideo.png"; //��һ��ͼ
//const string ImgPath2 = "../Test/TestVideo.png"; //�ڶ���ͼ
//const int DuraMS = 1500; //ÿһ��ͼ�������ٺ���

const uint8_t BackgroundColor[3] = { 255, 255, 255 }; //������ɫ
const uint8_t LineColor[3] = {17, 152, 187}; //��������ɫ
const uint8_t AxisColor[3] = {206, 226, 240}; //�����������ɫ
const uint8_t ImageColor[3] = { 241, 246, 250 }; //ͼƬ��ɫ����ɫ

TaskManagerPrint TMPrintObj;

void StringToWchar(string s, wchar_t* wc)
{
	const char* c = s.c_str();
	int len = MultiByteToWideChar(CP_ACP, 0, c, strlen(c), NULL, 0);
	MultiByteToWideChar(CP_ACP, 0, c, strlen(c), wc, len);
	wc[len] = '\0';
}
