from settings import *
import numpy as np
import time
import cv2


def judge_line(frame_list):
    """对视频的每一帧进行二值化处理。判断每一帧的每一个像素是背景还是线条"""
    is_line_list = list()
    for frame_it in range(len(frame_list)):
        is_line = (frame_list[frame_it][:, :, 0] > 224)
        is_line_list.append(is_line)
    return is_line_list


def get_color(is_line_list):
    """
    根据线条的比例，确定新视频每一帧的颜色（线条色*比例+背景色*（1-比例））
    :param line_ratio_list: 每一帧线条色的比例
    :return: 新视频每一帧的颜色
    """
    new_video_data = list()
    # 1.生成线条色，线条色的生成方式就直接写在代码里面
    line_color = np.zeros((720, 1280, 3), dtype=np.uint8)
    for col in range(1280):
        if col <= 426:
            line_color[:, col, 0] = int(255 * (426 - col) / 426)
            line_color[:, col, 1] = int(255 * col / 426)
            line_color[:, col, 2] = 0
        elif col <= 852:
            line_color[:, col, 0] = 0
            line_color[:, col, 1] = int(255 * (852 - col) / 426)
            line_color[:, col, 2] = int(255 * (col - 426) / 426)
        else:
            line_color[:, col, 0] = int(255 * (col - 852) / 426)
            line_color[:, col, 1] = 0
            line_color[:, col, 2] = int(255 * (852 - col) / 426)

    # 2.生成新视频的颜色
    for frame_it in range(len(is_line_list)):
        line_color_inner = np.zeros((720, 1280, 3), dtype=np.uint8)
        line_color_inner[:, frame_it * 3: 1280, :] = line_color[:, :1280 - frame_it * 3, :]
        line_color_inner[:, :frame_it * 3, :] = line_color[:, 1280 - frame_it * 3:, :]
        is_line = np.expand_dims(is_line_list[frame_it], axis=2)
        is_line = np.repeat(is_line, 3, axis=2)
        new_frame = BACKGROUND_COLOR * (1 - is_line) + line_color_inner * is_line
        new_video_data.append(new_frame.astype(np.uint8))
    return new_video_data


def get_new_video(video):
    # 1.确定使用原视频中的哪些帧
    frame_list = list()
    for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
        ret, frame = video.read()
        frame_list.append(frame)
    # 2.根据视频中的这些帧，通过延时的效果生成新帧
    is_line_list = judge_line(frame_list)  # 对原视频进行二值化
    new_video_data = get_color(is_line_list)  # 根据线条色比例，对新视频进行上色
    return new_video_data


def main():
    # 1.读取MP4文件
    video = cv2.VideoCapture(VIDEO_PATH)
    # 2.略过开头的帧，设置视频大小
    video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    cv2.namedWindow("YIL", 0)
    cv2.resizeWindow("YIL", 1280, 720)
    # 3.生成颜色变换之后的新视频，并展示出来
    new_video_data = get_new_video(video)
    for frame in new_video_data:
        cv2.imshow("YIL", frame)
        cv2.waitKey(int(1000 / FPS))
    time.sleep(100)


if __name__ == '__main__':
    main()
