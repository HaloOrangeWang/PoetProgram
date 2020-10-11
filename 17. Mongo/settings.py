import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

START_SEC = 118  # 从视频的哪一秒开始解析
END_SEC = 124  # 到视频的哪一秒结束

COLOR_AVR_THRES = 192  # 当一个区域内颜色的平均值低于某个数值时，即认为这个区域对应的点是一个线条点
DATA_LOAD_FROM_TXT = True

MONGO_HOST = 'mongodb://localhost:27017/'
DB_NAME = 'Yil'
DOC_ID = '39330059'  # 文档id

ROW_NUM = 54  # 数据表一共有多少行
COL_NUM = 192  # 数据表一共有多少列
SECS_PER_FRAME = 1  # 每一帧数据在数据库中展示多少秒
