from settings import *
import matplotlib.pyplot as plt
import numpy as np
import time
import cv2
import os


def get_sparse_points(frame_list):
    sparse_points_list = list()
    for frame_it in range(len(frame_list)):
        print('get_sparse_points', frame_it)
        center_points = (frame_list[frame_it][:, :, 0] > 128)
        is_point_around = np.zeros((720 + 2 * PX_MI, 1280 + 2 * PX_MI), dtype=np.uint8)
        expended_frame = np.zeros((720 + 2 * PX_MO, 1280 + 2 * PX_MO, 3), dtype=np.uint8)
        expended_frame[PX_MO: PX_MO + 720, PX_MO: PX_MO + 1280, :] = frame_list[frame_it]
        center_points[expended_frame[PX_MO: PX_MO + 720, 0: 1280, 0] <= 128] = False  # 上
        center_points[expended_frame[PX_MO: PX_MO + 720, 2 * PX_MO: 1280 + 2 * PX_MO, 0] <= 128] = False  # 下
        center_points[expended_frame[0: 720, PX_MO: 1280 + PX_MO, 0] <= 128] = False  # 左
        center_points[expended_frame[2 * PX_MO: 720 + 2 * PX_MO, PX_MO: 1280 + PX_MO, 0] <= 128] = False  # 右
        for row in range(720):
            for col in range(1280):
                if center_points[row, col]:
                    if is_point_around[row + PX_MI, col + PX_MI]:
                        center_points[row, col] = False
                    else:
                        is_point_around[row: row + 2 * PX_MI, col: col + 2 * PX_MI] = 1
        sparse_points_list.append(center_points)
    return sparse_points_list


def format_data_4_plot(sparse_points_list):
    output_data = list()
    for frame_it in range(len(sparse_points_list)):
        output_data_1frame = list()
        for row in range(720):
            for col in range(1280):
                if sparse_points_list[frame_it][row, col]:
                    output_data_1frame.append([row, col])
        output_data.append(np.array(output_data_1frame))
    return output_data


def save_pics_data(sparse_points_list):
    if not os.path.exists('data'):
        os.makedirs('data')
    f = open('data/outputs.csv', 'w')
    for frame_it in range(len(sparse_points_list)):
        for point in sparse_points_list[frame_it]:
            f.write('%d,%d,%d\n' % (frame_it, point[0], point[1]))
    f.close()


def plot_pics(sparse_points_list):
    for frame_it in range(len(sparse_points_list)):
        x_values = sparse_points_list[frame_it][:, 1]
        y_values = 720 - sparse_points_list[frame_it][:, 0]
        plt.figure(figsize=(16, 9), dpi=120)
        plt.title(u'Scatter Diagram')
        plt.xlabel(u'x')
        plt.ylabel(u'y')
        plt.scatter(x_values, y_values, marker='.', s=5)
        plt.xlim(0, 1280)
        plt.ylim(0, 720)
        # plt.show()??
        # time.sleep(2000)
        if not os.path.exists('pics'):
            os.makedirs('pics')
        plt.savefig('pics/%03d.png' % frame_it)
        plt.close()
        time.sleep(1)


def save_pics():
    # 1.读取原视频，获取逐帧数据
    video = cv2.VideoCapture(VIDEO_PATH)
    video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    frame_list = list()
    for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
        ret, frame = video.read()
        frame_list.append(frame)
    # 2.对视频中的每一帧数据进行处理，只保留距离边缘比较远的黑点
    sparse_points_list = get_sparse_points(frame_list)
    sparse_points_list = format_data_4_plot(sparse_points_list)
    # 3.用Matplotlib展示散点图，并将中心点保存在文件中，供echarts部分使用
    plot_pics(sparse_points_list)
    save_pics_data(sparse_points_list)


if __name__ == '__main__':
    save_pics()
