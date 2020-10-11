import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 146  # 从视频的哪一秒开始解析
END_SEC = 150  # 到视频的哪一秒结束

BACKGROUND_COLOR = [0, 0, 0]  # 背景色

CHANGE_METHOD_TM = 2  # 何时（第几秒）切换策略

DELAY_FRAMES = 12  # 最多延时多少帧
DECAY_RATIO = 0.7  # 延时帧的衰减指数
