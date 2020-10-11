#include "variables.h"
#include <Windows.h>
#include <stdio.h>
#include <opencv2/opencv.hpp>

#ifdef _DEBUG
#pragma comment(lib, "opencv_world430d.lib")
#else
#pragma comment(lib, "opencv_world430.lib")
#endif

#define EDGE_THRES 100

HANDLE hComm;
const string ImgPath = "../Origin/VisualScopePng.png";
uint8_t edge_data[720][1280];
int trace_data[4][1280];

bool InitComm()
{
	//初始化串口
	hComm = CreateFile("COM1", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);// FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, NULL);
	if (hComm == INVALID_HANDLE_VALUE) {
		printf("open serial failed.\n");
		return false;
	}
	if (!SetupComm(hComm, 10240, 10240)) {
		printf("Setup Comm failed.\n");
		return false;
	}

	COMMTIMEOUTS timeOuts;
	timeOuts.ReadIntervalTimeout = 1000;
	timeOuts.ReadTotalTimeoutMultiplier = 1000;
	timeOuts.ReadTotalTimeoutConstant = 10000;
	timeOuts.WriteTotalTimeoutMultiplier = 1000;
	timeOuts.WriteTotalTimeoutConstant = 5000;
	if (!SetCommTimeouts(hComm, &timeOuts)) {
		printf("set comm timeout failed.\n");
		return false;
	}

	DCB dcb;
	GetCommState(hComm, &dcb);
	dcb.BaudRate = CBR_115200;
	dcb.ByteSize = 8;
	dcb.Parity = NOPARITY;
	dcb.StopBits = ONESTOPBIT;
	if (!SetCommState(hComm, &dcb)) {
		printf("set comm state failed.\n");
		return false;
	}
	return true;
}

void GetEdge(const cv::Mat img_data)
{
	// 1.获取边缘点
	memset(edge_data, 0, sizeof(uint8_t) * 720 * 1280);
	for (int row = 0; row <= 719; row++) {
		for (int col = 0; col <= 1279; col++) {
			cv::Vec3b data_1px = img_data.at<cv::Vec3b>(row, col);
			if (row <= 6) {
				cv::Vec3b data_1px_down00 = img_data.at<cv::Vec3b>(row + 6, col);
				cv::Vec3b data_1px_down01 = img_data.at<cv::Vec3b>(row + 3, col);
				if (abs(data_1px[0] - data_1px_down00[0]) >= EDGE_THRES || abs(data_1px[0] - data_1px_down01[0]) >= EDGE_THRES) {
					edge_data[row][col] = 1;
				}
			}
			else if (row >= 714) {
				cv::Vec3b data_1px_up20 = img_data.at<cv::Vec3b>(row - 6, col);
				cv::Vec3b data_1px_up21 = img_data.at<cv::Vec3b>(row - 3, col);
				if (abs(data_1px[0] - data_1px_up20[0]) >= EDGE_THRES || abs(data_1px[0] - data_1px_up21[0]) >= EDGE_THRES) {
					edge_data[row][col] = 1;
				}
			}
			else {
				cv::Vec3b data_1px_up10 = img_data.at<cv::Vec3b>(row - 6, col);
				cv::Vec3b data_1px_down10 = img_data.at<cv::Vec3b>(row + 6, col);
				cv::Vec3b data_1px_up11 = img_data.at<cv::Vec3b>(row - 3, col);
				cv::Vec3b data_1px_down11 = img_data.at<cv::Vec3b>(row + 3, col);
				if (abs(data_1px[0] - data_1px_up10[0]) >= EDGE_THRES || abs(data_1px[0] - data_1px_down10[0]) >= EDGE_THRES
					|| abs(data_1px[0] - data_1px_up11[0]) >= EDGE_THRES || abs(data_1px[0] - data_1px_down11[0]) >= EDGE_THRES || abs(data_1px_up11[0] - data_1px_down11[0]) >= EDGE_THRES) {
					edge_data[row][col] = 1;
				}
				//if (col == 55 && row >= 530 && row <= 560) {
				//	printf("row = %d, %d, up0 = %d, up1 = %d, down0 = %d, down1 = %d\n", row, data_1px[0], data_1px_up10[0], data_1px_up11[0], data_1px_down10[0], data_1px_down11[0]);
				//}
			}
		}
	}
	// 2.连续N个点是边缘点的情况下，只取中间的一个
	for (int col = 0; col <= 1279; col++) {
		int start_row_dx = -1;
		int end_row_dx = -1;
		for (int row = 0; row <= 719; row++) {
			if (edge_data[row][col] == 1 && start_row_dx == -1) {
				start_row_dx = row;
			}
			else if ((edge_data[row][col] == 0 && start_row_dx != -1)) {
				end_row_dx = row - 1;
				for (int row0 = start_row_dx; row0 <= end_row_dx; row0++) {
					if (row0 != int((start_row_dx + end_row_dx) / 2)) {
						edge_data[row0][col] = 0;
					}
				}
				start_row_dx = -1;
				end_row_dx = -1;
			}
			if ((row == 719 && start_row_dx != -1)) {
				end_row_dx = 719;
				for (int row0 = start_row_dx; row0 <= end_row_dx; row0++) {
					if (row0 != int((start_row_dx + end_row_dx) / 2)) {
						edge_data[row][col] = 0;
					}
				}
				start_row_dx = -1;
				end_row_dx = -1;
			}
		}
	}
}

void Calc4Traces()
{
	int trace_first_dx[4] = { -1, -1, -1, -1 };
	int trace_last_dx[4] = { -1, -1, -1, -1 };
	for (int col = 0; col <= 1279; col++) {
		for (int t = 0; t <= 3; t++) {
			trace_data[t][col] = -1;
		}
	}
	for (int col = 1; col <= 1279; col++) {
		for (int row = 0; row <= 719; row++) {
			if (edge_data[row][col] == 1) {
				// 1.先找可不可以使用现成的trace_data进行轨迹跟踪
				bool trace_found = false;
				for (int t = 0; t <= 3; t++) {
					if (trace_data[t][col - 1] >= row - 15 && trace_data[t][col - 1] <= row + 15) {
						trace_data[t][col] = row;
						trace_last_dx[t] = col;
						trace_found = true;
						if (trace_first_dx[t] == -1)
							trace_first_dx[t] = col;
						break;
					}
				}
				// 2.开辟一个新的trace
				if (!trace_found) {
					for (int t = 0; t <= 3; t++) {
						if (trace_data[t][col - 1] == -1) {
							trace_data[t][col] = row;
							trace_last_dx[t] = col;
							if (trace_first_dx[t] == -1)
								trace_first_dx[t] = col;
							break;
						}
					}
				}
			}
		}
	}
	for (int t = 0; t <= 3; t++) {
		for (int col = trace_first_dx[t]; col <= trace_last_dx[t]; col++) {
			if (trace_data[t][col] == -1 && trace_data[t][col + 30] != -1)
				trace_data[t][col] = trace_data[t][col - 1];
		}
	}
}

int main()
{
	// 1.读取图片，并获取图片在每个x位置处的边缘（不使用canny算法）
	cv::Mat img_data = cv::imread(ImgPath);
	GetEdge(img_data);
	Calc4Traces();
	// 2.初始化串口
	if (!InitComm()) {
		system("pause");
		return 0;
	}

	for (int col = 0; col <= 1279; col++) {
		int show_val[4];
		for (int t = 0; t <= 3; t++) {
			if (trace_data[t][col] == -1)
				show_val[t] = -1;
			else
				show_val[t] = 720 - trace_data[t][col];
		}
		GetData(show_val[0], show_val[1], show_val[2], show_val[3]);
		OutPut_Data();
		_sleep(10);
	}

	system("pause");
	return 0;
}