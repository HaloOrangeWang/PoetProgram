import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 87  # 从视频的哪一秒开始解析
END_SEC = 97  # 到视频的哪一秒结束

PX_MI = 4  # 相邻两个散点图的点间隔多少
PX_MO = 0  # 距离边缘至少多少px的点才会被显示在散点图中
