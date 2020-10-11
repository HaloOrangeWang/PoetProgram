import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath']  # 视频路径
FPS = JSON_CONFIG['Fps']  # 视频帧速率

# START_SEC = 101  # 从视频的哪一秒开始解析
# END_SEC = 106  # 到视频的哪一秒结束
START_SEC = 105  # 从视频的哪一秒开始解析
END_SEC = 106  # 到视频的哪一秒结束

COLOR_AVR_THRES = 192  # 当一个区域内颜色的平均值低于某个数值时，即认为这个区域对应的点是一个线条点
DATA_LOAD_FROM_TXT = False

ROW_NUM = 63  # 串口调试助手中的视频一共有多少行
COL_NUM = 224  # 串口调试助手中的视频一共有多少列
SECS_PER_FRAME = 5  # 每一帧数据在串口调试助手中展示多少秒

BAUD_RATE = 460800  # 波特率
