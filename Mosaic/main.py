from settings import *
import numpy as np
import time
import cv2


def calc_black_ratio(frame_data, frame_no, loadtxt, savetxt):
    """计算一张图中每个像素点"""

    def get_weight_matrix():
        weight_mat_in = []
        for y in range(100):
            weight_mat_in.append(np.zeros(2120))
        for y in range(1080):
            if y <= 99:
                weight_edge = 4 - 0.02 * y
                weight_middle = 2 - 0.01 * y
                step = (weight_edge - weight_middle) / 100
            elif y <= 979:
                weight_edge = 2
                weight_middle = 1
                step = 0.01
            else:
                weight_edge = 2 + 0.02 * (y - 979)
                weight_middle = 1 + 0.01 * (y - 979)
                step = (weight_edge - weight_middle) / 100
            weight_mat_1line = list(np.zeros(100))
            weight_mat_1line.extend(list(np.arange(weight_edge, weight_middle + 0.000001, -step)))
            weight_mat_1line.extend(list(np.ones(1720) * weight_middle))
            weight_mat_1line.extend(list(np.arange(weight_middle + step, weight_edge + step - 0.000001, step)))
            weight_mat_1line.extend(list(np.zeros(100)))
            weight_mat_in.append(weight_mat_1line)
        for y in range(100):
            weight_mat_in.append(np.zeros(2120))
        return np.array(weight_mat_in, dtype=np.float32)

    def get_black_ratio():
        weight_mat = get_weight_matrix()
        black_ratio_mat_in = np.zeros((1280, 2120))

        black_dx_list = np.argwhere(frame_data[:, :, 2] <= 128)  # 原图像中哪些点是黑色的
        for black_dx_it in range(len(black_dx_list)):
            black_dx = black_dx_list[black_dx_it]
            if black_dx_it % 1000 == 0:
                print(black_dx_it)
            black_ratio_mat_in[black_dx[0]: black_dx[0] + 200, black_dx[1]: black_dx[1] + 200] += weight_mat[black_dx[0]: black_dx[0] + 200, black_dx[1]: black_dx[1] + 200]
        return black_ratio_mat_in[100: 1180, 100: 2020]

    if loadtxt:
        # 直接从txt里面读
        return np.loadtxt('black_ratio_%d.txt' % frame_no)
    else:
        # 计算距离
        black_ratio_mat = get_black_ratio()
        if savetxt:
            np.savetxt('black_ratio_%d.txt' % frame_no, black_ratio_mat)
        return black_ratio_mat


def change_color(frame_data):
    """显示一帧的视频内容"""
    # 判断frame的每一个格子是不是背景
    is_bkgrd = (frame_data[:, :, 2] >= 128)
    is_bkgrd = np.expand_dims(is_bkgrd, axis=2)
    is_bkgrd = np.repeat(is_bkgrd, 3, axis=2)
    # 进行RGB运算
    color_data = BACKGROUND_COLOR * is_bkgrd + LINE_COLOR * (~is_bkgrd)
    return color_data.astype(np.uint8)


def calc_mosaic_color(frame_data, black_ratio_mat, mosaic_weight):
    """
    计算Mosaic处理之后的各个点的颜色
    :param frame_data: Mosaic处理之前的帧数据
    :param black_ratio_mat: 每个点周围有多少线条点
    :param mosaic_weight: mosaic权重
    :return: mosaic处理之后每个节点应该显示的颜色
    """
    # 1.计算这一帧每个节点的线条颜色比例
    not_bkgrd = (frame_data[:, :, 2] < 128)
    mosaic_line_ratio = black_ratio_mat / 40000
    line_ratio = not_bkgrd * (1 - mosaic_weight) + mosaic_line_ratio * mosaic_weight
    # 2.计算这一帧的具体颜色
    line_ratio = np.expand_dims(line_ratio, axis=2)
    line_ratio = np.repeat(line_ratio, 3, axis=2)
    color_data = BACKGROUND_COLOR * (1 - line_ratio) + LINE_COLOR * line_ratio
    return color_data.astype(np.uint8)


def get_new_video(video):
    """将旧的视频内容，进行mosaic处理之后，生成新的视频内容"""
    new_video_data = list()
    # 开始Mosaic之前，用简单的变色处理
    for frame_it in range(int(MOSAIC_BEGIN_TM * FPS)):
        ret, frame = video.read()
        new_frame = change_color(frame)
        new_video_data.append(new_frame)
    # 开始Mosaic，获取开始Mosaic的frame，并进行Mosaic处理
    ret, mosaic_beg_frame = video.read()
    black_ratio_mat = calc_black_ratio(mosaic_beg_frame, 1, DIST_DATA_LOAD_FROM_TXT, (not DIST_DATA_LOAD_FROM_TXT))
    for frame_it in range(int(MOSAIC_BEGIN_TM * FPS), int(MOSAIC_MIDDLE_TM * FPS)):
        mosaic_weight = (frame_it - int(MOSAIC_BEGIN_TM * FPS)) / (int(MOSAIC_MIDDLE_TM * FPS) - int(MOSAIC_BEGIN_TM * FPS))
        new_frame = calc_mosaic_color(mosaic_beg_frame, black_ratio_mat, mosaic_weight)
        new_video_data.append(new_frame)
    # 结束Mosaic，获取结束Mosaic的frame，并进行Mosaic处理
    for frame_it in range(int(MOSAIC_BEGIN_TM * FPS), int(MOSAIC_END_TM * FPS)):
        video.read()
    ret, mosaic_end_frame = video.read()
    black_ratio_mat = calc_black_ratio(mosaic_end_frame, 2, DIST_DATA_LOAD_FROM_TXT, (not DIST_DATA_LOAD_FROM_TXT))
    for frame_it in range(int(MOSAIC_MIDDLE_TM * FPS), int(MOSAIC_END_TM * FPS)):
        mosaic_weight = (int(MOSAIC_END_TM * FPS) - frame_it) / (int(MOSAIC_END_TM * FPS) - int(MOSAIC_MIDDLE_TM * FPS))
        new_frame = calc_mosaic_color(mosaic_end_frame, black_ratio_mat, mosaic_weight)
        new_video_data.append(new_frame)
    return new_video_data


def main():
    # 1.读取MP4文件
    video = cv2.VideoCapture(VIDEO_PATH)
    # 2.略过开头的帧，设置视频大小
    video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    cv2.namedWindow("cam_1", 0)
    cv2.resizeWindow("cam_1", 1280, 720)
    # 3.生成颜色变换之后的新视频，并展示出来
    new_video_data = get_new_video(video)
    for frame in new_video_data:
        cv2.imshow("cam_1", frame)
        cv2.waitKey(int(1000 / FPS))
    time.sleep(100)


if __name__ == '__main__':
    main()
