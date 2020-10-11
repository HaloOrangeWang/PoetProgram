from settings import *
import numpy as np
import time
import cv2
import os


def sl(pos):
    def sl_inner(func):
        def call(loadtxt, savetxt, *args):
            if loadtxt:
                new_frame_list_2 = list()
                frame_dx = 0
                while True:
                    if not os.path.exists('data/data_%s_%d.npy' % (pos, frame_dx)):
                        return new_frame_list_2
                    new_frame_list_2.append(np.load('data/data_%s_%d.npy' % (pos, frame_dx)))
                    frame_dx += 1
            else:
                new_frame_list_2 = func(*args)
                if savetxt:
                    if not os.path.exists('data'):
                        os.makedirs('data')
                    for frame_it2 in range(len(new_frame_list_2)):
                        np.save('data/data_%s_%d.npy' % (pos, frame_it2), new_frame_list_2[frame_it2])
                return new_frame_list_2
        return call
    return sl_inner


@sl('left')
def get_new_video_left(frame_list):
    new_frame_list = list()
    low_res_x_list = np.repeat([np.arange(1280) / 1280 * COL_NUM_LEFT], 720, axis=0).astype(np.uint32)
    low_res_y_list = np.repeat(np.array([[t] for t in range(720)]) / 720 * ROW_NUM_LEFT, 1280, axis=1).astype(np.uint32)
    px_cnt_1frame = np.zeros((ROW_NUM_LEFT, COL_NUM_LEFT), dtype=np.int32)
    for row in range(720):
        for col in range(1280):
            px_cnt_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += 1
    px_cnt_1frame = np.expand_dims(px_cnt_1frame, axis=2)
    px_cnt_1frame = np.repeat(px_cnt_1frame, 3, axis=2)

    for frame_it in range(len(frame_list)):
        print('left', frame_it)
        color_sum_1frame = np.zeros((ROW_NUM_LEFT, COL_NUM_LEFT, 3), dtype=np.int32)
        for row in range(720):
            for col in range(1280):
                color_sum_1frame[low_res_y_list[row, col], low_res_x_list[row, col], :] += frame_list[frame_it][row, col, :]
        new_frame = (color_sum_1frame / px_cnt_1frame).astype(np.uint8)
        new_frame_list.append(new_frame)
        del color_sum_1frame
    return new_frame_list


@sl('right')
def get_new_video_right(frame_list, bkgrd_img):
    new_frame_list = list()
    low_res_x_list = np.repeat([np.arange(720) / 720 * DIAM_RIGHT], 720, axis=0).astype(np.uint32)
    low_res_y_list = low_res_x_list.T
    px_cnt_1frame = np.zeros((DIAM_RIGHT, DIAM_RIGHT), dtype=np.int32)
    use_bkgrd = np.zeros((DIAM_RIGHT, DIAM_RIGHT), dtype=np.int32)
    for row in range(720):
        for col in range(720):
            px_cnt_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += 1
    px_cnt_1frame = np.expand_dims(px_cnt_1frame, axis=2)
    px_cnt_1frame = np.repeat(px_cnt_1frame, 3, axis=2)
    circle_center = (DIAM_RIGHT - 1) / 2
    for row in range(DIAM_RIGHT):
        for col in range(DIAM_RIGHT):
            if np.sqrt((row - circle_center) * (row - circle_center) + (col - circle_center) * (col - circle_center)) <= (DIAM_RIGHT / 2):
                use_bkgrd[row, col] = False
            else:
                use_bkgrd[row, col] = True

    for frame_it in range(len(frame_list)):
        print('right', frame_it)
        color_sum_1frame = np.zeros((DIAM_RIGHT, DIAM_RIGHT, 3), dtype=np.int32)
        for row in range(720):
            for col in range(720):
                color_sum_1frame[low_res_y_list[row, col], low_res_x_list[row, col], :] += frame_list[frame_it][row, col + 420, :]
        new_frame = (color_sum_1frame / px_cnt_1frame).astype(np.uint8)
        for row in range(DIAM_RIGHT):
            for col in range(DIAM_RIGHT):
                if use_bkgrd[row, col]:
                    new_frame[row, col, :] = bkgrd_img[VIDEO_POS_RIGHT[1] + row, VIDEO_POS_RIGHT[0] + col, :]
        new_frame_list.append(new_frame)
        del color_sum_1frame
    return new_frame_list


def get_new_video(video_left, video_right, bkgrd_img):
    new_video = []
    for frame_it in range(len(video_left)):
        print(frame_it)
        video_1frame = bkgrd_img.copy()
        video_1frame_left_old = video_1frame[VIDEO_POS_LEFT[1]: VIDEO_POS_LEFT[1] + ROW_NUM_LEFT, VIDEO_POS_LEFT[0]: VIDEO_POS_LEFT[0] + COL_NUM_LEFT]
        video_1frame_right_old = video_1frame[VIDEO_POS_RIGHT[1]: VIDEO_POS_RIGHT[1] + DIAM_RIGHT, VIDEO_POS_RIGHT[0]: VIDEO_POS_RIGHT[0] + DIAM_RIGHT]
        video_1frame[VIDEO_POS_LEFT[1]: VIDEO_POS_LEFT[1] + ROW_NUM_LEFT, VIDEO_POS_LEFT[0]: VIDEO_POS_LEFT[0] + COL_NUM_LEFT] = (video_1frame_left_old * ALPHA_RATIO + video_left[frame_it] * (1 - ALPHA_RATIO)).astype(np.uint8)
        video_1frame[VIDEO_POS_RIGHT[1]: VIDEO_POS_RIGHT[1] + DIAM_RIGHT, VIDEO_POS_RIGHT[0]: VIDEO_POS_RIGHT[0] + DIAM_RIGHT] = (video_1frame_right_old * ALPHA_RATIO + video_right[frame_it] * (1 - ALPHA_RATIO)).astype(np.uint8)
        del video_1frame_left_old
        del video_1frame_right_old
        new_video.append(video_1frame)
    return new_video


def main():
    # 1.读取背景图片和视频
    bkgrd_img = cv2.imread(BKGRD_IMG_PATH)  # 背景图片
    video = cv2.VideoCapture(VIDEO_PATH)
    video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    frame_list = list()
    for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
        ret, frame = video.read()
        frame_list.append(frame)
    # 2.对左侧和右侧的视频数据进行降低分辨率的处理，右侧的视频做成圆形
    video_left = get_new_video_left(DATA_LOAD_FROM_TXT, (not DATA_LOAD_FROM_TXT), frame_list)
    video_right = get_new_video_right(DATA_LOAD_FROM_TXT, (not DATA_LOAD_FROM_TXT), frame_list, bkgrd_img)
    # 3.将新的视频内容和背景图片贴在一起，得到要显示的视频内容
    new_video_data = get_new_video(video_left, video_right, bkgrd_img)
    # 4.将新视频展示出来
    cv2.namedWindow("Yil", 0)
    cv2.resizeWindow("Yil", 720, 720)
    time.sleep(15)
    for frame in new_video_data:
        cv2.imshow("Yil", frame)
        cv2.waitKey(int(1000 / FPS))
    time.sleep(100)


if __name__ == '__main__':
    main()
