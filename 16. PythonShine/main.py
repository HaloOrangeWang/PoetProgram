from settings import *
import numpy as np
import time
import cv2


def calc_dist(frame_data, loadtxt=False, savetxt=True):
    """计算一张图像中所有点与最近的线段点的距离"""

    def calc_txt_2():
        dist_list = np.zeros(shape=(720, 1280)) + 3000
        x_list = np.repeat([[t for t in range(1280)]], 720, axis=0)
        y_list = np.repeat([[t] for t in range(720)], 1280, axis=1)
        black_dx_list_2 = np.argwhere(frame_data[:, :, 2] <= 64)  # 原图像中哪些点是黑色的
        black_dx_list = np.ndarray(shape=black_dx_list_2.shape, dtype=black_dx_list_2.dtype)
        black_dx_list[:, 0] = black_dx_list_2[:, 1]
        black_dx_list[:, 1] = black_dx_list_2[:, 0]
        for black_dx_it in range(len(black_dx_list)):
            # for black_dx in black_dx_list:
            black_dx = black_dx_list[black_dx_it]
            if black_dx_it % 1000 == 0:
                print(black_dx_it)
            dist_list = np.minimum(dist_list, np.sqrt(np.square(x_list - black_dx[0]) + np.square(y_list - black_dx[1])))
        return dist_list

    if loadtxt:
        # 直接从txt里面读
        return np.loadtxt('dist.txt')
    else:
        # 计算距离
        dist_list = calc_txt_2()
        if savetxt:
            np.savetxt('dist.txt', dist_list)


def calc_color_by_dist(frame_data, dist_data, bkgrd_thers):
    """
    根据背景中每个点与其最近的线段点之间的距离，来充实背景
    :param dist_data: 每个点与其最近的线段点之间的距离的数据
    :param bkgrd_thers: 当距离超过多少之后，就使用背景色了
    :return: 每个节点应该显示的颜色
    """
    # dist_data = dist_data.T
    use_color_data = np.zeros([720, 1280, 3], dtype=np.uint8)
    use_color_data[310: 410, :, :] = 1
    if bkgrd_thers <= 0:
        return frame_data
    # 处理dist_data，将值限制在0-bkgrd_thres中，且扩展为3维数组，便于后续的RGB运算
    dist_data = np.minimum(dist_data, bkgrd_thers)
    dist_data = np.expand_dims(dist_data, axis=2)
    dist_data = np.repeat(dist_data, 3, axis=2)
    # 进行RGB运算
    color_data = BACKGROUND_COLOR * (dist_data / bkgrd_thers) + LINE_COLOR * ((bkgrd_thers - dist_data) / bkgrd_thers)
    color_data = color_data * use_color_data + frame_data * (1 - use_color_data)
    return color_data.astype(np.uint8)


def get_new_video(video):
    """将旧的视频内容，进行变色/闪光等处理之后，生成新的视频内容"""
    new_video_data = list()
    # 开始闪光之后，获取开始闪光的frame，并进行闪光处理
    ret, shine_beg_frame = video.read()
    dist_data = calc_dist(shine_beg_frame, DIST_DATA_LOAD_FROM_TXT, (not DIST_DATA_LOAD_FROM_TXT))
    for frame_it in range(int(SHINE_DURA_TM * FPS)):
        ret, frame_data = video.read()
        if frame_it <= 0.5 * SHINE_DURA_TM * FPS:
            dist_thres = 20 * frame_it / (0.5 * SHINE_DURA_TM * FPS)
        else:
            dist_thres = 20 * ((SHINE_DURA_TM * FPS - frame_it) / (0.5 * SHINE_DURA_TM * FPS))
        new_frame = calc_color_by_dist(frame_data, dist_data, int(dist_thres))
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
