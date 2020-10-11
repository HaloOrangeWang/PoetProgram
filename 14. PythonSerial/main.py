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
        low_res_y_list = np.repeat(np.array([[t] for t in range(720)]) / 720 * ROW_NUM, 1280, axis=1).astype(np.uint32)
        px_cnt_1frame = np.zeros((ROW_NUM, COL_NUM), dtype=np.int32)
        for row in range(720):
            for col in range(1280):
                px_cnt_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += 1

        for frame_it in range(len(frame_list)):
            print(frame_it)
            color_sum_1frame = np.zeros((ROW_NUM, COL_NUM), dtype=np.int32)
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
        data_list_1frame = []
        for row in range(ROW_NUM):
            comm_str_tmp = bytearray()
            for col in range(COL_NUM):
                if is_line_1frame[row, col] == 0:
                    comm_str_tmp.extend(b' ')
                else:
                    comm_str_tmp.extend(b'#')
            comm_str_tmp.extend(b'\r\n')
            data_list_1frame.append(bytes(comm_str_tmp))
        # 2.将这些数据发送到串口里面
        for row in data_list_1frame:
            comm_2.write(row)
            time.sleep(0.03)

    comm.write(b'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n')
    time.sleep(1)
    for frame_it in range(len(is_line_list)):
        transfer_data_1frame(comm, is_line_list[frame_it])
        time.sleep(SECS_PER_FRAME)


def main():
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
    comm = serial.Serial('COM2', 460800, timeout=1)
    if not comm.isOpen():
        raise RuntimeError('串口打不开')
    # 4.将数据输出到串口调试助手中
    transfer_to_serial(comm, is_line_list)


if __name__ == '__main__':
    main()
