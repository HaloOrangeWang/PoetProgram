from settings import *
import time
import cv2
import os


def show_pics():
    # 1.把图片都load进来
    img_list = []
    frame_cnt = 0
    while True:
        if os.path.exists('pics/%03d.png' % frame_cnt):
            img_list.append(cv2.imread('pics/%03d.png' % frame_cnt))
            frame_cnt += 1
        else:
            break
    # 2.展示这些图片
    cv2.namedWindow("Yil", 0)
    cv2.resizeWindow("Yil", 1280, 720)
    time.sleep(20)
    for frame in range(frame_cnt):
        cv2.imshow("Yil", img_list[frame])
        cv2.waitKey(int(1000 / FPS))
    time.sleep(100)


if __name__ == '__main__':
    show_pics()
