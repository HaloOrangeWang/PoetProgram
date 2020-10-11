import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

DIST_DATA_LOAD_FROM_TXT = True

START_SEC = 0  # 从视频的哪一秒开始解析

BACKGROUND_COLOR = [0, 0, 0]  # 背景色
LINE_COLOR = [0, 0, 255]  # 线条颜色
MOSAIC_BEGIN_TM = 2  # Mosaic开始时间
MOSAIC_MIDDLE_TM = 4  # Mosaic中段时间
MOSAIC_END_TM = 6  # Mosaic结束时间
