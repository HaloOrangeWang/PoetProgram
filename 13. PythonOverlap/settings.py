import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 96  # 从视频的哪一秒开始解析
END_SEC = 102  # 到视频的哪一秒结束

BACKGROUND_COLOR = [0, 0, 0]  # 背景色
# LINE_COLOR = [0, 0, 255]  # 线条颜色

CHANGE_METHOD_TM = 2  # 何时（第几秒）切换策略

DELAY_FRAMES = 10  # 延时多少帧
DECAY_RATIO = 0.5  # 延时帧的衰减指数
