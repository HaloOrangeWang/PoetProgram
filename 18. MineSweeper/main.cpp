#include "variables.h"
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <vector>
#include <opencv2/opencv.hpp>

#ifdef _DEBUG
#pragma comment(lib, "opencv_world430d.lib")
#else
#pragma comment(lib, "opencv_world430.lib")
#endif

vector<cv::Mat> frame_list;

vector<int*> JudgeLineLowRes(vector<cv::Mat> frame_list)
{
	int px_cnt_1frame[ROW_NUM * COL_NUM];
	memset(px_cnt_1frame, 0, sizeof(int) * ROW_NUM * COL_NUM);
	for (int row = 0; row <= 719; row++) {
		for (int col = 0; col <= 1279; col++) {
			const int low_res_x = int(col / 1280.0 * COL_NUM);
			const int low_res_y = int(row / 720.0 * ROW_NUM);
			px_cnt_1frame[low_res_y * COL_NUM + low_res_x] += 1;
		}
	}
	vector<int*> is_line_list;
	for (int frame_it = 0; frame_it <= frame_list.size() - 1; frame_it++) {
		printf("frame no: %d\n", frame_it);
		int color_sum_1frame[ROW_NUM * COL_NUM];
		int* is_line_1frame = new int[ROW_NUM * COL_NUM];
		for (int t = 0; t <= ROW_NUM * COL_NUM - 1; t++) {
			color_sum_1frame[t] = 0;
			is_line_1frame[t] = 0;
		}
		for (int row = 0; row <= 719; row++) {
			for (int col = 0; col <= 1279; col++) {
				const int low_res_x = int(col / 1280.0 * COL_NUM);
				const int low_res_y = int(row / 720.0 * ROW_NUM);
				cv::Vec3b data_1px = frame_list[frame_it].at<cv::Vec3b>(row, col);
				color_sum_1frame[low_res_y * COL_NUM + low_res_x] += data_1px[0];
			}
		}
		for (int t = 0; t <= ROW_NUM * COL_NUM - 1; t++) {
			if (color_sum_1frame[t] / px_cnt_1frame[t] > COLOR_AVR_THRES)
				is_line_1frame[t] = 1;
			else
				is_line_1frame[t] = 0;
		}
		is_line_list.push_back(is_line_1frame);
	}
	return is_line_list;
}

int GetWindowLoc(RECT window_loc)
{
	if (window_loc.top >= 400) {
		if (window_loc.left >= 1000)
			return 5;
		else if (window_loc.left >= 500)
			return 4;
		else
			return 3;
	}
	else {
		if (window_loc.left >= 1000)
			return 2;
		else if (window_loc.left >= 500)
			return 1;
		else
			return 0;
	}
}

bool InitHWND()
{
	//获取6个扫雷窗口
	//1.先获取第一个扫雷窗口
	HWND mine_window_1 = FindWindow("扫雷", "扫雷");
	if (mine_window_1 == nullptr) {
		printf("failed to find minesweeper program #1.\n");
		return false;
	}
	RECT mine_window_loc;
	GetWindowRect(mine_window_1, &mine_window_loc);
	int window_dx = GetWindowLoc(mine_window_loc);
	MineWindows[window_dx] = mine_window_1;
	HWND mine_window_old = mine_window_1;
	for (int t = 1; t <= 5; t++) {
		HWND mine_window_next = FindWindowEx(NULL, mine_window_old, "扫雷", "扫雷");
		if (mine_window_next == nullptr) {
			printf("failed to find minesweeper program #%d.\n", t + 1);
			return false;
		}
		RECT mine_window_loc_2;
		GetWindowRect(mine_window_next, &mine_window_loc_2);
		int window_dx = GetWindowLoc(mine_window_loc_2);
		if (MineWindows[window_dx] != nullptr) {
			printf("failed to get location of minesweeper program #%d.\n", t + 1);
			return false;
		}
		MineWindows[window_dx] = mine_window_next;
		mine_window_old = mine_window_next;
	}
	return true;
}

void DrawMineSweeper(vector<int*> is_line_list)
{
	for (int frame_it = 0; frame_it <= is_line_list.size() - 1; frame_it++) {
		// 按下红旗
		for (int row = 0; row <= ROW_NUM - 1; row++) {
			for (int col = 0; col <= COL_NUM - 1; col++) {
				if (is_line_list[frame_it][row * COL_NUM + col] == 1) {
					int window_id = 3 * int(row / 24) + int(col / 30);
					int row_in_window = row % 24;
					int col_in_window = col % 30;
					SendMessage(MineWindows[window_id], WM_RBUTTONDOWN, 0, MAKELPARAM(20 + col_in_window * 16, 60 + row_in_window * 16));
				}
			}
		}
		_sleep(SECS_PER_FRAME * 1000);
		// 取出红旗
		for (int row = 0; row <= ROW_NUM - 1; row++) {
			for (int col = 0; col <= COL_NUM - 1; col++) {
				if (is_line_list[frame_it][row * COL_NUM + col] == 1) {
					int window_id = 3 * int(row / 24) + int(col / 30);
					int row_in_window = row % 24;
					int col_in_window = col % 30;
					SendMessage(MineWindows[window_id], WM_RBUTTONDOWN, 0, MAKELPARAM(20 + col_in_window * 16, 60 + row_in_window * 16));
				}
			}
		}
	}
}

int main()
{
	// 1.找到扫雷的窗口
	if (!InitHWND()) {
		system("pause");
		return 0;
	}
	// 2.读取原视频，获取逐帧数据
	/*cv::VideoCapture video(VIDEO_PATH);
	if (!video.isOpened()) {
		printf("打开MP4文件失败!\n");
		getchar();
		return 0;
	}
	video.set(cv::CAP_PROP_POS_FRAMES, int(START_SEC * FPS));
	for (int framt_it = int(START_SEC * FPS); framt_it < int(END_SEC * FPS); framt_it++) {
		cv::Mat frame;
		video.read(frame);
		frame_list.push_back(frame);
	}*/
	vector<cv::Mat> frame_list(250);
	for (int frame_it = 3075; frame_it <= 3324; frame_it++) {
		char img_path[50] = { 0 };
		sprintf(img_path, "pics/%04d.png", frame_it);
		frame_list[frame_it - 3075] = cv::imread(img_path);
	}
	// 3.对视频进行数据处理
	vector<int*> is_line_list = JudgeLineLowRes(frame_list);
	// 4.将处理后的数据显示在扫雷窗口中
	DrawMineSweeper(is_line_list);

	system("pause");
	return 0;

}