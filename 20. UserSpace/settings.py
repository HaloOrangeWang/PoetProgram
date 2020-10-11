import json


def get_json_config():
    with open('../Manifest.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


JSON_CONFIG = get_json_config()
VIDEO_PATH = '../' + JSON_CONFIG['VideoPath1080']  # 视频路径
FPS = JSON_CONFIG['Fps1080']  # 视频帧速率

START_SEC = 141  # 从视频的哪一秒开始解析
END_SEC = 146  # 到视频的哪一秒结束

ROW_NUM = 3  # 串口调试助手中的视频一共有多少行
COL_NUM = 5  # 串口调试助手中的视频一共有多少列

IMG_WIDTH = 300  # 每张图片的边长
IMG_X_INTERVAL = 100  # 大图片切分成小图片后，横轴间隔
IMG_Y_INTERVAL = 50  # 大图片切分成小图片后，纵轴间隔
IMG_TOP_MARGIN = 40  # 大图片的最上方多少个像素舍弃
IMG_LEFT_MARGIN = 10  # 大图片的最左方多少个像素舍弃

SECS_PER_FRAME = 2  # 每一帧数据在文件夹中展示多少秒
