from settings import *
from PyQt5.QtGui import QPainter, QFont, QPalette, QImage, QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer
import traceback


def run_with_exc(f):
    """运行时捕捉异常并用messagebox显示出来"""

    def call(window, *args, **kwargs):
        try:
            return f(window, *args, **kwargs)
        except Exception as e:
            exc_info = traceback.format_exc()
            QMessageBox.about(window, 'Traceback', exc_info)
    return call


class GameWindow(QMainWindow):
    def __init__(self, frame_cnt):
        super().__init__()
        # 初始化，load数据
        self.img_list = []
        self.cter_img_list = []
        self.npc_img_list = []
        for frame_it in range(frame_cnt):
            self.img_list.append(QImage('data/%03d.png' % frame_it))
        for t in range(4):
            self.cter_img_list.append(QImage('imgs/001-Fighter01_big.png').copy(t * 96, 288, 96, 144))
            self.npc_img_list.append(QImage('imgs/066-Beast04.png').copy(t * 96, 96, 96, 96))
        self.dialog_img = QImage('imgs/001-Blue01.png').copy(130, 66, 28, 28)
        self.tri_img = [QImage('imgs/001-Blue01.png').copy(160, 64, 16, 16), QImage('imgs/001-Blue01.png').copy(160, 80, 16, 16)]
        # 准备图形界面
        self.init_ui()
        self.frame_cnt = frame_cnt
        self.curr_frame = 0  # 当前处于第几帧
        # 设置播放新帧的定时器
        self.frame_timer = QTimer(self)
        self.frame_timer.timeout.connect(self.on_new_frame)
        self.frame_timer.start(40)

    def init_ui(self):
        # 设置窗口主题、大小和背景图片
        self.setObjectName('MainWindow')
        self.setFixedSize(1300, 740)
        # 设置背景view
        self.bkgrd = QGraphicsView(self)
        self.bkgrd.setFixedSize(1280, 720)
        self.bkgrd.move(10, 10)
        self.bkgrd.setStyleSheet("background:transparent;border:none;")
        bkgrd_pixmap = QPixmap.fromImage((self.img_list[0]))
        bkgrd_pixmap.fromImage(self.img_list[0])
        self.bkgrd_scene = QGraphicsScene()
        self.bkgrd_scene.addItem(QGraphicsPixmapItem(bkgrd_pixmap))
        self.bkgrd.setScene(self.bkgrd_scene)
        # 小人
        self.character = QGraphicsView(self)
        self.character.setFixedSize(96, 144)
        self.character.move(0, 500)
        self.character.setStyleSheet("background:transparent;border:none;")
        cter_pixmap = QPixmap.fromImage((self.cter_img_list[0]))
        cter_pixmap.fromImage(self.img_list[0])
        self.cter_scene = QGraphicsScene()
        self.cter_scene.addItem(QGraphicsPixmapItem(cter_pixmap))
        self.character.setScene(self.cter_scene)
        # NPC
        self.npc = QGraphicsView(self)
        self.npc.setFixedSize(96, 96)
        self.npc.move(1050, 530)
        self.npc.setStyleSheet("background:transparent;border:none;")
        npc_pixmap = QPixmap.fromImage((self.npc_img_list[0]))
        self.npc_scene = QGraphicsScene()
        self.npc_scene.addItem(QGraphicsPixmapItem(npc_pixmap))
        self.npc.setScene(self.npc_scene)
        # 对话框
        self.dialog = QGraphicsView(self)
        self.dialog.setFixedSize(1248, 208)
        self.dialog.move(26, 496)
        dialog_pixmap = QPixmap.fromImage(self.dialog_img)
        palette = QPalette()
        palette.setBrush(self.dialog.backgroundRole(), QBrush(dialog_pixmap))
        self.dialog.setPalette(palette)
        self.dialog.hide()
        self.label = QLabel(self)
        self.label.setFont(QFont("宋体", 24, 40))
        self.label.setFixedSize(1000, 100)
        self.label.move(60, 496)
        self.label.setText("啦啦啦啦啦")
        self.label.hide()
        # 对话框下面的小三角
        self.tri = QGraphicsView(self)
        self.tri.setFixedSize(16, 16)
        self.tri.move(632, 696)
        self.tri.setStyleSheet("background:transparent;border:none;")
        tri_pixmap = QPixmap.fromImage(self.tri_img[0])
        self.tri_scene = QGraphicsScene()
        self.tri_scene.addItem(QGraphicsPixmapItem(tri_pixmap))
        self.tri.setScene(self.tri_scene)
        self.tri.hide()

        # 显示界面
        self.show()

    def on_new_frame(self):
        self.curr_frame += 1
        # 更新背景
        bkgrd_pixmap = QPixmap.fromImage((self.img_list[self.curr_frame]))
        self.bkgrd_scene.clear()
        self.bkgrd_scene.addItem(QGraphicsPixmapItem(bkgrd_pixmap))
        # 更新小人
        if self.curr_frame % 6 == 0:
            cter_pixmap = QPixmap.fromImage((self.cter_img_list[int(self.curr_frame % 24 // 6)]))
            self.cter_scene.clear()
            self.cter_scene.addItem(QGraphicsPixmapItem(cter_pixmap))
            npc_pixmap = QPixmap.fromImage((self.npc_img_list[int(self.curr_frame % 24 // 6)]))
            self.npc_scene.clear()
            self.npc_scene.addItem(QGraphicsPixmapItem(npc_pixmap))
        if self.curr_frame % 12 == 0:
            tri_pixmap = QPixmap.fromImage((self.tri_img[int(self.curr_frame % 24 // 12)]))
            self.tri_scene.clear()
            self.tri_scene.addItem(QGraphicsPixmapItem(tri_pixmap))
        if self.curr_frame <= 95:
            self.character.move(self.curr_frame * 10, 500)
        # 更新对话框
        if self.curr_frame == 100:
            self.dialog.show()
            self.label.show()
            self.tri.show()
        if self.curr_frame == 192:
            self.dialog.hide()
            self.label.hide()
            self.tri.hide()
        if self.curr_frame == self.frame_cnt - 1:  # 已达最后一帧
            self.frame_timer.stop()
