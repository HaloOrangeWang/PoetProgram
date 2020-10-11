from settings import *
from window import GameWindow
from PyQt5.QtWidgets import QApplication
import numpy as np
import time
import sys
import cv2
import os


def get_new_video_left(frame_list):
    new_frame_list = list()
    background_color = np.array([0, 0, 0])
    line_color = np.array([255, 255, 255])
    # low_res_x_list = np.repeat([np.arange(1280) / 1280 * COL_NUM], 720, axis=0).astype(np.uint32)
    # low_res_y_list = np.repeat(np.array([[t] for t in range(720)]) / 720 * ROW_NUM, 1280, axis=1).astype(np.uint32)
    # px_cnt_1frame = np.zeros((ROW_NUM, COL_NUM), dtype=np.int32)
    # for row in range(720):
    #     for col in range(1280):
    #         px_cnt_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += 1
    # px_cnt_1frame = np.expand_dims(px_cnt_1frame, axis=2)
    # px_cnt_1frame = np.repeat(px_cnt_1frame, 3, axis=2)

    for frame_it in range(len(frame_list)):
        print('frame no. ', frame_it)
        is_line = (frame_list[frame_it][:, :, 0] > 224)
        is_line[440: 650, 960: 1160] = False
        is_line = np.expand_dims(is_line, axis=2)
        is_line = np.repeat(is_line, 3, axis=2)
        new_frame = (background_color * (1 - is_line) + line_color * is_line).astype(np.uint8)
        del is_line
        # color_sum_1frame = np.zeros((ROW_NUM, COL_NUM, 3), dtype=np.int32)
        # for row in range(720):
        #     for col in range(1280):
        #         color_sum_1frame[low_res_y_list[row, col], low_res_x_list[row, col], :] += frame_list[frame_it][row, col, :]
        # new_frame = color_sum_1frame / px_cnt_1frame
        new_frame_list.append(new_frame)
    return new_frame_list


def expand_bkgrd_img(bkgrd_img):
    img_output = np.zeros((720, 1280, 3), dtype=np.uint8)
    n_col = int(1280 / BKGRD_IMG_WIDTH)
    n_row = int(720 / BKGRD_IMG_HEIGHT)
    col_rem = 1280 - n_col * BKGRD_IMG_WIDTH
    row_rem = 720 - n_row * BKGRD_IMG_HEIGHT
    for row in range(n_row):
        for col in range(n_col):
            img_output[row * BKGRD_IMG_HEIGHT: (row + 1) * BKGRD_IMG_HEIGHT, col * BKGRD_IMG_WIDTH: (col + 1) * BKGRD_IMG_WIDTH, :] = bkgrd_img
    for row in range(n_row):
        img_output[row * BKGRD_IMG_HEIGHT: (row + 1) * BKGRD_IMG_HEIGHT, 1280 - col_rem:, :] = bkgrd_img[:, :col_rem, :]
    for col in range(n_col):
        img_output[720 - row_rem:, col * BKGRD_IMG_WIDTH: (col + 1) * BKGRD_IMG_WIDTH, :] = bkgrd_img[:row_rem, :, :]
    img_output[720 - row_rem:, 1280 - col_rem:, :] = bkgrd_img[:row_rem, :col_rem, :]
    return img_output


def get_new_video(video_old, bkgrd_img):
    new_video = []
    for frame_it in range(len(video_old)):
        video_1frame = (video_old[frame_it] * (1 - ALPHA_RATIO) + bkgrd_img * ALPHA_RATIO).astype(np.uint8)
        new_video.append(video_1frame)
    return new_video


def main():
    # 1.读取视频
    # video = cv2.VideoCapture(VIDEO_PATH)
    # video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    # frame_list = list()
    # for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
    #     ret, frame = video.read()
    #     frame_list.append(frame)
    # # 2.读取背景图片，并对背景图片进行复制，使其扩充到1280*720大小
    # bkgrd_img = cv2.imread(BKGRD_IMG_PATH)  # 背景图片
    # bkgrd_img = bkgrd_img[96: 128, 32: 64, :]
    # bkgrd_img = expand_bkgrd_img(bkgrd_img)
    # # 3.将视频和背景图片结合起来
    # new_video_data = get_new_video_left(frame_list)
    # new_video_data = get_new_video(new_video_data, bkgrd_img)
    # if not os.path.exists('data'):
    #     os.makedirs('data')
    # for frame_it in range(len(new_video_data)):
    #     cv2.imwrite('data/%03d.png' % frame_it, new_video_data[frame_it])
    # time.sleep(2)
    # raise Exception
    # 4.打开窗口，将图片显示到窗口中
    app = QApplication(sys.argv)
    ex = GameWindow(275)
    # ex = GameWindow(len(new_video_data))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
