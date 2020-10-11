#include <iostream>
#include <opencv2/opencv.hpp>
#include "total.h"

#ifdef _DEBUG
#pragma comment(lib, "opencv_world430d.lib")
#else
#pragma comment(lib, "opencv_world430.lib")
#endif

using namespace std;

cv::Mat* new_video;


double* calc_dist_inner(cv::Mat frame_data) {
	double* dist_list = new double[720 * 1280];
	int __cnt = 0;
	for (int t = 0; t < 720 * 1280; t++)
		dist_list[t] = 3000;
	for (int row = 0; row <= 719; row++) {
		for (int col = 0; col <= 1279; col++) {
			cv::Vec3b frame_1px = frame_data.at<cv::Vec3b>(row, col);
			if (frame_1px[2] < 96) {
				//说明是线条颜色，计算各个点与这个点的距离
				for (int y = max(0, row - 100); y <= min(719, row + 100); y++) {
					for (int x = max(0, col - 100); x <= min(1279, col + 100); x++) {
						double dist = sqrt((x - col) * (x - col) + (y - row) * (y - row));
						if (dist < dist_list[y * 1280 + x])
							dist_list[y * 1280 + x] = dist;
					}
				}
				//记录一下计算进度
				if (__cnt % 1000 == 0)
					cout << "calc_dist: __cnt = " << __cnt << endl;
				__cnt++;
			}
		}
	}
	return dist_list;
}

double* calc_dist(cv::Mat frame_data, bool loadtxt, bool savetxt) {
	if (loadtxt) {
		//从txt文件中读取距离数据
		double* dist_list = new double[720 * 1280];
		FILE* pfile = fopen("dist.txt", "r");
		for (int row = 0; row <= 719; row++) {
			for (int col = 0; col <= 1279; col++) {
				if (col != 1279)
					fscanf(pfile, "%lf,", &dist_list[row * 1280 + col]);
				else if (row != 719)
					fscanf(pfile, "%lf\n", &dist_list[row * 1280 + col]);
				else
					fscanf(pfile, "%lf", &dist_list[row * 1280 + col]);
			}
		}
		fclose(pfile);
		return dist_list;
	}
	else {
		double* dist_list = calc_dist_inner(frame_data);
		if (savetxt) {
			FILE* pfile = fopen("dist.txt", "w");
			for (int row = 0; row <= 719; row++) {
				for (int col = 0; col <= 1279; col++) {
					if (col != 1279)
						fprintf(pfile, "%.3lf,", dist_list[row * 1280 + col]);
					else if (row != 719)
						fprintf(pfile, "%.3lf\n", dist_list[row * 1280 + col]);
					else
						fprintf(pfile, "%.3lf", dist_list[row * 1280 + col]);
				}
			}
			fclose(pfile);
		}
		return dist_list;
	}
}

cv::Mat calc_dist_by_dist_and_x(cv::Mat frame_data, double* dist_data, int shine_left_x) {
	cv::Mat color_data = cv::Mat(720, 1280, CV_8UC3);
	for (int row = 0; row <= 719; row++) {
		for (int col = 0; col <= 1279; col++) {
			//1.如果当前点是线条的话，就直接返回线条颜色了
			if (dist_data[row * 1280 + col] == 0) {
				color_data.at<cv::Vec3b>(row, col) = cv::Vec3b(LINE_COLOR[0], LINE_COLOR[1], LINE_COLOR[2]);
				continue;
			}
			//2.对于背景点，先计算使用线条颜色的权重
			double line_color_weight;
			double line_color_weight_x;
			if (col >= shine_left_x && col <= shine_left_x + SHINE_WIDTH) {
				line_color_weight_x = 1.0;
			}
			else if (col >= shine_left_x - 50 && col < shine_left_x) {
				line_color_weight_x = (col - (shine_left_x - 50)) / 50.0;
			}
			else if (col > shine_left_x + SHINE_WIDTH && col <= shine_left_x + SHINE_WIDTH + 50) {
				line_color_weight_x = (shine_left_x + SHINE_WIDTH + 50 - col) / 50.0;
			}
			else {
				line_color_weight_x = 0;
			}
			if (dist_data[row * 1280 + col] >= BKGRD_THRES)
				line_color_weight = 0;
			else
				line_color_weight = (BKGRD_THRES - dist_data[row * 1280 + col]) * line_color_weight_x / BKGRD_THRES;
			//3.计算背景点的颜色RGB值
			if (line_color_weight == 0) {
				cv::Vec3b frame_1px = frame_data.at<cv::Vec3b>(row, col);
				color_data.at<cv::Vec3b>(row, col) = cv::Vec3b(static_cast<uint8_t>(frame_1px[0]), static_cast<uint8_t>(frame_1px[1]), static_cast<uint8_t>(frame_1px[2]));
			}else{
				color_data.at<cv::Vec3b>(row, col) = cv::Vec3b(
					static_cast<uint8_t>(BACKGROUND_COLOR[0] * (1 - line_color_weight) + LINE_COLOR[0] * line_color_weight),
					static_cast<uint8_t>(BACKGROUND_COLOR[1] * (1 - line_color_weight) + LINE_COLOR[1] * line_color_weight),
					static_cast<uint8_t>(BACKGROUND_COLOR[2] * (1 - line_color_weight) + LINE_COLOR[2] * line_color_weight));
			}
		}
	}
	return color_data;
}

cv::Mat change_color(cv::Mat frame_data) {
	cv::Mat color_data = cv::Mat(720, 1280, CV_8UC3);
	for (int row = 0; row <= 719; row++) {
		for (int col = 0; col <= 1279; col++) {
			cv::Vec3b frame_1px = frame_data.at<cv::Vec3b>(row, col);
			if (frame_1px[2] >= 128) { //说明是背景色
				color_data.at<cv::Vec3b>(row, col) = cv::Vec3b(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]);
			}
			else { //说明是线条颜色
				color_data.at<cv::Vec3b>(row, col) = cv::Vec3b(LINE_COLOR[0], LINE_COLOR[1], LINE_COLOR[2]);
			}
		}
	}
	return color_data;
}

int get_new_video(vector<cv::Mat> frame_list)
{
	uint64_t frame_cnt = frame_list.size();
	int new_frame_dx = 0;
	new_video = new cv::Mat[frame_cnt];
	//2.开始闪光之后，获取开始闪光的frame，并进行闪光处理
	cv::Mat shine_beg_frame = frame_list[25];
	double* dist_data = calc_dist(shine_beg_frame, DIST_DATA_LOAD_FROM_TXT, (!DIST_DATA_LOAD_FROM_TXT));
	for (int frame_it = 0; frame_it <= int(frame_list.size()) - 1; frame_it++) {
		int shine_left_x = frame_it * 1280 / int(frame_list.size());
		new_video[new_frame_dx] = calc_dist_by_dist_and_x(frame_list[frame_it], dist_data, shine_left_x);
		new_frame_dx++;
	}
	return new_frame_dx - 1;
}

int main()
{
	//1.读取视频素材
	vector<cv::Mat> frame_list(105);
	for (int frame_it = 3445; frame_it <= 3549; frame_it++) {
		char img_path[50] = { 0 };
		sprintf(img_path, "pics/%04d.png", frame_it);
		frame_list[frame_it - 3445] = cv::imread(img_path);
	}
	//2.略过开头的帧，设置视频大小
	cv::namedWindow("YIL", 0);
	cv::resizeWindow("YIL", 1280, 720);
	//3.生成颜色变换之后的新视频，并展示出来

	int frame_cnt = get_new_video(frame_list);

	for (int frame_it = 0; frame_it < frame_cnt; frame_it++) {
		cout << frame_it << endl;
		cv::imshow("YIL", new_video[frame_it]);
		cv::waitKey(int(1000 / FPS));
	}

	cout << "Finished!" << endl;
	getchar();
	return 0;
}
