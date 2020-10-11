#include <string>
#include <Windows.h>

using namespace std;

const string VIDEO_PATH = "Origin.mp4";
const float FPS = 25;

const float START_SEC = 103;
const float END_SEC = 113;

const float COLOR_AVR_THRES = 192;

const int ROW_NUM = 48;
const int COL_NUM = 90;
const float SECS_PER_FRAME = 3;
HWND MineWindows[6]{ nullptr, nullptr, nullptr, nullptr, nullptr, nullptr };  //É¨À×´°¿Ú
