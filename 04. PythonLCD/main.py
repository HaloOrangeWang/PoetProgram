from settings import *
import numpy as np
import serial
import time
import cv2
import os


def judge_line_low_res(frame_list, loadtxt, savetxt):
    """判断在低分辨率的情况下，哪些点应当被认定为线条点"""

    def judge_line_2():
        is_line_list = list()
        low_res_x_list = np.repeat([np.arange(1280) / 1280 * COL_NUM], 720, axis=0).astype(np.uint32)
        low_res_y_list = np.repeat(np.array([[t] for t in range(720)]) / 720 * 64, 1280, axis=1).astype(np.uint32)
        px_cnt_1frame = np.zeros((64, COL_NUM), dtype=np.int32)
        for row in range(720):
            for col in range(1280):
                px_cnt_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += 1

        for frame_it in range(len(frame_list)):
            print(frame_it)
            color_sum_1frame = np.zeros((64, COL_NUM), dtype=np.int32)
            for row in range(720):
                for col in range(1280):
                    color_sum_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += frame_list[frame_it][row, col, 0]
            # color_sum_1frame[row_dx_low_res, col_dx_low_res] += frame_list[frame_it][row, col, 2]
            is_line_1frame = (color_sum_1frame / px_cnt_1frame) > COLOR_AVR_THRES
            is_line_list.append(is_line_1frame.astype(np.uint8))
        return is_line_list

    if loadtxt:
        is_line_list_2 = list()
        frame_dx = 0
        while True:
            if not os.path.exists('data/data_%d.npy' % frame_dx):
                return is_line_list_2
            is_line_list_2.append(np.load('data/data_%d.npy' % frame_dx))
            frame_dx += 1
    else:
        is_line_list_2 = judge_line_2()
        if savetxt:
            if not os.path.exists('data'):
                os.makedirs('data')
            for frame_it2 in range(len(is_line_list_2)):
                np.save('data/data_%d.npy' % frame_it2, is_line_list_2[frame_it2])
        return is_line_list_2


def transfer_to_serial(comm, is_line_list):

    def transfer_data_1frame(comm_2, is_line_1frame):
        # 1.获取要插入的数据
        data_list_1frame = [[0 for t0 in range(COL_NUM)] for t in range(8)]
        for row in range(64):
            row_in_lcd = row // 8
            row_rem_in_lcd = row % 8
            for col in range(COL_NUM):
                if is_line_1frame[row, col] == 1:
                    data_list_1frame[row_in_lcd][col] |= (1 << row_rem_in_lcd)
        # 2.将这些数据发送到串口里面
        for row in range(8):
            for col in range(COL_NUM):
                comm_2.write(bytes([1, col, 0]))  # 选择列
                comm_2.write(bytes([2, row, 0]))  # 选择行
                comm_2.write(bytes([3, data_list_1frame[row][col], 0]))
                time.sleep(0.01)
            time.sleep(0.1)

    for frame_it in range(len(is_line_list)):
        print('current frame: ', frame_it)
        comm.write(bytes([6, 0, 0]))  # LCD清空内容
        transfer_data_1frame(comm, is_line_list[frame_it])
        comm.write(bytes([5, 0, 0]))  # LCD显示内容
        time.sleep(SECS_PER_FRAME)


def main():
    assert COL_NUM <= 255
    # 1.读取原视频，获取逐帧数据
    video = cv2.VideoCapture(VIDEO_PATH)
    video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    frame_list = list()
    for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
        ret, frame = video.read()
        frame_list.append(frame)
    # 2.对视频数据进行处理，判断每一帧应该如何降低分辨率
    is_line_list = judge_line_low_res(frame_list, DATA_LOAD_FROM_TXT, (not DATA_LOAD_FROM_TXT))
    # 3.打开串口
    print('开始打开串口')
    comm = serial.Serial('COM2', 115200, timeout=1)
    if not comm.isOpen():
        raise RuntimeError('串口打不开')
    # 4.将数据输出到串口调试助手中
    transfer_to_serial(comm, is_line_list)


if __name__ == '__main__':
    main()
