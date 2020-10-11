import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 104  # 从视频的哪一秒开始解析
END_SEC = 115  # 到视频的哪一秒结束

BKGRD_IMG_PATH = 'imgs/001-Grassland01.png'
BKGRD_IMG_HEIGHT = 32  # 背景图片的宽和高
BKGRD_IMG_WIDTH = 32

ROW_NUM = 720  # 左边视频一共有多少行
COL_NUM = 1280  # 左边视频一共有多少列

ALPHA_RATIO = 0.4  # 背景图片的颜色展示百分之多少
