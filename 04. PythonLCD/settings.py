import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 41  # 从视频的哪一秒开始解析
END_SEC = 45  # 到视频的哪一秒结束

COLOR_AVR_THRES = 192  # 当一个区域内颜色的平均值低于某个数值时，即认为这个区域对应的点是一个线条点
DATA_LOAD_FROM_TXT = False

COL_NUM = 114  # LCD点阵屏中的视频一共有多少列
SECS_PER_FRAME = 2  # 每一帧数据在点阵屏中展示多少秒
