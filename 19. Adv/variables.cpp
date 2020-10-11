#include "total.h"

string VIDEO_PATH = "../Test/TestVideo.mp4"; //视频路径
double FPS = 30.3; //视频帧速率

bool DIST_DATA_LOAD_FROM_TXT = true;

double START_SEC = 0; //从视频的哪一秒开始解析

uint8_t BACKGROUND_COLOR[3] = { 104, 135, 142 }; //背景色
uint8_t LINE_COLOR[3] = { 0, 0, 255 }; //线条颜色

int BKGRD_THRES = 30; //当距离超过多少之后，就使用背景色了
int SHINE_WIDTH = 200; //闪光的宽度是多少
