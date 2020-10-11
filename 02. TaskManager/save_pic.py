# 先把视频解析成图片，便于C++程序读取

import json
import cv2
import os


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 133  # 从视频的哪一秒开始解析
END_SEC = 142  # 到视频的哪一秒结束

video = cv2.VideoCapture(VIDEO_PATH)
video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
    ret, frame = video.read()
    if not os.path.exists('pics'):
        os.makedirs('pics')
    cv2.imwrite('pics/%04d.png' % frame_it, frame)
