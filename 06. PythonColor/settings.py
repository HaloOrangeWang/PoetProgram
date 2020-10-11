import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 44  # 从视频的哪一秒开始解析
END_SEC = 55  # 到视频的哪一秒结束

BACKGROUND_COLOR = [0, 0, 0]  # 背景色
# LINE_COLOR = [0, 0, 255]  # 线条颜色
