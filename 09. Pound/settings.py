import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 70  # 从视频的哪一秒开始解析
END_SEC = 80  # 到视频的哪一秒结束

BKGRD_IMG_PATH = '../Origin/Pounds.png'
BKGRD_IMG_HEIGHT = 1372  # 背景图片的宽和高
BKGRD_IMG_WIDTH = 1227

DATA_LOAD_FROM_TXT = True

ROW_NUM_LEFT = 600  # 左边视频一共有多少行
COL_NUM_LEFT = 1200  # 左边视频一共有多少列
VIDEO_POS_LEFT = [0, 30]  # 左边视频的横纵坐标分别是多少
DIAM_RIGHT = 560  # 右边视频的直径是多少
VIDEO_POS_RIGHT = [295, 750]  # 右边视频的横纵坐标是多少
ALPHA_RATIO = 0.4  # 背景图片的颜色展示百分之多少
