from settings import *
import time
import cv2
import os


def divide_video_data(frame_list):
    imgs = [[[None for t in range(COL_NUM)] for t1 in range(ROW_NUM)] for t2 in range(len(frame_list))]

    for frame_it in range(len(frame_list)):
        for row in range(ROW_NUM):
            for col in range(COL_NUM):
                left_x = IMG_LEFT_MARGIN + col * (IMG_WIDTH + IMG_X_INTERVAL)
                top_y = IMG_TOP_MARGIN + row * (IMG_WIDTH + IMG_Y_INTERVAL)
                if left_x + IMG_WIDTH >= 1921:
                    raise ValueError('图片宽度超限')
                if top_y + IMG_WIDTH >= 1081:
                    raise ValueError('图片高度超限')
                imgs[frame_it][row][col] = frame_list[frame_it][top_y: top_y + IMG_WIDTH, left_x: left_x + IMG_WIDTH]
    return imgs


def save_imgs(imgs):
    for frame_it in range(len(imgs)):
        # 1.新建文件夹，并清空该文件夹
        if not os.path.exists('output/%d' % frame_it):
            os.makedirs('output/%d' % frame_it)
        else:
            pass
            # for filename in os.listdir('output'):
            #     os.remove('output/' + filename)
        # 2.保存新帧的文件
        for row in range(ROW_NUM):
            for col in range(COL_NUM):
                # if os.path.exists('output/img_%d_%d.png' % (row, col)):
                #     os.remove('output/img_%d_%d.png' % (row, col))
                cv2.imwrite('output/%d/img_%d_%d.png' % (frame_it, row, col), imgs[frame_it][row][col])
        # 3.等待一段时间
        # time.sleep(SECS_PER_FRAME)


def main():
    # 1.读取原视频，获取逐帧数据
    video = cv2.VideoCapture(VIDEO_PATH)
    video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    frame_list = list()
    for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
        ret, frame = video.read()
        frame_list.append(frame)
    # 2.对视频数据拆成若干张图片，并保存出来
    video_imgs = divide_video_data(frame_list)
    save_imgs(video_imgs)


if __name__ == '__main__':
    main()
