#include "total.h"

string VIDEO_PATH = "../Test/TestVideo.mp4"; //��Ƶ·��
double FPS = 30.3; //��Ƶ֡����

bool DIST_DATA_LOAD_FROM_TXT = true;

double START_SEC = 0; //����Ƶ����һ�뿪ʼ����

uint8_t BACKGROUND_COLOR[3] = { 104, 135, 142 }; //����ɫ
uint8_t LINE_COLOR[3] = { 0, 0, 255 }; //������ɫ

int BKGRD_THRES = 30; //�����볬������֮�󣬾�ʹ�ñ���ɫ��
int SHINE_WIDTH = 200; //����Ŀ���Ƕ���
