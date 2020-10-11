import numpy as np
import turtle
import time
import cv2


def main():
    # 1.读取原图
    img = cv2.imread('../Origin/TurtleImg.png')
    # 2.对原图进行处理，提取线条边缘，并做Hough变换
    edges = cv2.Canny(img, 50, 150)
    hough_lines = cv2.HoughLinesP(edges, 2, np.pi / 180, 10)  # , 20)
    hough_lines = hough_lines.astype(np.int32)  # 转成1280*720的形式

    is_draw = np.zeros((len(hough_lines)), dtype=np.uint8)
    last_draw_dx = 0  # 上一次画了HoughLine的哪一条线
    last_draw_x_y = [hough_lines[0][0][2], hough_lines[0][0][3]]  # 上一个HoughLine直线结束时的横纵坐标
    # 3.turtle初始化
    turtle.screensize(1280, 720)
    turtle.setup(1305, 745, startx=0, starty=0)
    turtle.pensize(2)
    turtle.pencolor('blue')
    turtle.speed(10)
    turtle.up()
    turtle.goto(hough_lines[0][0][0] - 640, 360 - hough_lines[0][0][1])
    turtle.down()
    turtle.goto(hough_lines[0][0][2] - 640, 360 - hough_lines[0][0][3])
    is_draw[0] = 1
    # 4.用turtle画出hough变换的结果
    while True:
        if all(is_draw):
            break
        next_draw_dx = None  # 接下来应该画HoughLine的哪一条线
        min_dist = np.inf  # 这条线的起始点和上一条线的终点的距离
        for line_it in range(len(hough_lines)):
            if not is_draw[line_it]:
                next_draw_x_y = [hough_lines[line_it][0][0], hough_lines[line_it][0][1]]
                dist = abs(next_draw_x_y[0] - last_draw_x_y[0]) + abs(next_draw_x_y[1] - last_draw_x_y[1])
                if dist < min_dist:
                    min_dist = dist
                    next_draw_dx = line_it
        if min_dist == 0:
            turtle.goto(hough_lines[next_draw_dx][0][2] - 640, 360 - hough_lines[next_draw_dx][0][3])
            is_draw[next_draw_dx] = 1
            last_draw_dx = next_draw_dx  # 上一次画了HoughLine的哪一条线
            last_draw_x_y = [hough_lines[next_draw_dx][0][2], hough_lines[next_draw_dx][0][3]]  # 上一个HoughLine直线结束时的横纵坐标
        else:
            turtle.up()
            turtle.goto(hough_lines[next_draw_dx][0][0] - 640, 360 - hough_lines[next_draw_dx][0][1])
            turtle.down()
            turtle.goto(hough_lines[next_draw_dx][0][2] - 640, 360 - hough_lines[next_draw_dx][0][3])
            is_draw[next_draw_dx] = 1
            last_draw_dx = next_draw_dx  # 上一次画了HoughLine的哪一条线
            last_draw_x_y = [hough_lines[next_draw_dx][0][2], hough_lines[next_draw_dx][0][3]]  # 上一个HoughLine直线结束时的横纵坐标
    turtle.hideturtle()
    time.sleep(110)


if __name__ == '__main__':
    main()
