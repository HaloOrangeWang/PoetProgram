from settings import *
import numpy as np
import pymongo
import time
import cv2
import os


def init_mongo():
    """mongodb初始化: 创建数据库和集合"""
    mongo_client = pymongo.MongoClient(MONGO_HOST)
    mongo_db = mongo_client[DB_NAME]
    mongo_col = mongo_db['YilMain']
    if 'YilMain' in mongo_db.list_collection_names():  # 如果这个集合已经存在了，则清空这个集合
        mongo_col.delete_many({})
    mongo_col.insert_one({"_id": DOC_ID})
    return mongo_col


def judge_line_low_res(frame_list, loadtxt, savetxt):
    """判断在低分辨率的情况下，哪些点应当被认定为线条点"""

    def judge_line_2():
        is_line_list = list()
        low_res_x_list = np.repeat([np.arange(1280) / 1280 * COL_NUM], 720, axis=0).astype(np.uint32)
        low_res_y_list = np.repeat(np.array([[t] for t in range(720)]) / 720 * ROW_NUM, 1280, axis=1).astype(np.uint32)
        px_cnt_1frame = np.zeros((ROW_NUM, COL_NUM), dtype=np.int32)
        for row in range(720):
            for col in range(1280):
                px_cnt_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += 1

        for frame_it in range(len(frame_list)):
            print(frame_it)
            color_sum_1frame = np.zeros((ROW_NUM, COL_NUM), dtype=np.int32)
            for row in range(720):
                for col in range(1280):
                    color_sum_1frame[low_res_y_list[row, col], low_res_x_list[row, col]] += frame_list[frame_it][row, col, 0]
            # color_sum_1frame[row_dx_low_res, col_dx_low_res] += frame_list[frame_it][row, col, 2]
            is_line_1frame = (color_sum_1frame / px_cnt_1frame) > COLOR_AVR_THRES
            is_line_list.append(is_line_1frame.astype(np.uint8))
        return is_line_list

    if loadtxt:
        is_line_list_2 = list()
        frame_dx = 0
        while True:
            if not os.path.exists('data/data_%d.txt' % frame_dx):
                return is_line_list_2
            is_line_list_2.append(np.loadtxt('data/data_%d.txt' % frame_dx))
            frame_dx += 1
    else:
        is_line_list_2 = judge_line_2()
        if savetxt:
            if not os.path.exists('data'):
                os.makedirs('data')
            for frame_it2 in range(len(is_line_list_2)):
                np.savetxt('data/data_%d.txt' % frame_it2, is_line_list_2[frame_it2])
        return is_line_list_2


def save_data(mongo_col, is_line_list):

    def save_data_1frame(mongo_col_2, is_line_1frame):
        # 1.获取要插入的数据
        data_dic_1frame = dict()
        for row in range(ROW_NUM):
            label = 'F%03d' % row
            sql_str_tmp = ''
            for col in range(COL_NUM):
                if is_line_1frame[row, col] == 0:
                    sql_str_tmp += ' '
                else:
                    sql_str_tmp += '#'
            data_dic_1frame[label] = sql_str_tmp
        # 2.将这个数据插入到Mongodb中
        mongo_doc = {'_id': DOC_ID}
        new_data = {"$set": data_dic_1frame}
        mongo_col_2.update_one(mongo_doc, new_data)

    for frame_it in range(len(is_line_list)):
        save_data_1frame(mongo_col, is_line_list[frame_it])
        time.sleep(SECS_PER_FRAME)


def main():
    # 1.初始化mongodb集合
    mongo_col = init_mongo()
    # 2.读取原视频，获取逐帧数据
    video = cv2.VideoCapture(VIDEO_PATH)
    video.set(cv2.CAP_PROP_POS_FRAMES, int(START_SEC * FPS))
    frame_list = list()
    for frame_it in range(int(START_SEC * FPS), int(END_SEC * FPS)):
        ret, frame = video.read()
        frame_list.append(frame)
    # 3.对视频数据进行处理，判断每一帧应该如何降低分辨率
    is_line_list = judge_line_low_res(frame_list, DATA_LOAD_FROM_TXT, (not DATA_LOAD_FROM_TXT))
    # 4.保存数据
    # raise Exception
    save_data(mongo_col, is_line_list)


if __name__ == '__main__':
    main()
