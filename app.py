import numpy as np
import cv2, sys, os
from PyQt5.QtCore import Qt
from __init__ import __version__
from mainui import MainUI
from PyQt5.QtGui import  QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QGraphicsPixmapItem

class Select:
    def __init__(self):
        self.mainWindow = MainUI()
        self.mainWindow.setupUi()

        self.image_path = ""
        self.image_list = []
        self.image_idx = 0

        self.mainWindow.closeEvent = self.window_close
        self.mainWindow.action_open_img_dir.triggered.connect(self.open_img_dir)
        self.mainWindow.action_version.triggered.connect(self.menu_version)
        self.mainWindow.btn_prev.clicked.connect(lambda: self.image_option("prev"))
        self.mainWindow.btn_next.clicked.connect(lambda: self.image_option("next"))

        self.mainWindow.show()

    def open_img_dir(self):
        tmp_path = QFileDialog.getExistingDirectory(self.mainWindow, "选择图片所在文件夹")
        if tmp_path:
            self.reset_param()
            self.image_path = tmp_path
            self.image_list = [im for im in os.listdir(self.image_path) if im.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.tif', '.tiff', '.gif', '.webp', '.jfif'))]
            # self.image_list = sorted(self.image_list, key=lambda x: int(x.split('.')[0]))
            self.image_list.sort()
            self.mainWindow.label_img_idx_total.setText(str(len(self.image_list)))
            self.img_show("first")
    
    def img_show(self, option):
        if self.image_path and self.image_list:
            try:
                frame = QPixmap(os.path.join(self.image_path, self.image_list[self.image_idx]))
                self.mainWindow.graphicsView.image = frame
                self.mainWindow.graphicsView.image_item = QGraphicsPixmapItem(frame)

                if option == "first":
                    self.mainWindow.graphicsView.loadImage()
                if option == "update":
                    self.mainWindow.graphicsView.update_image()
                self.mainWindow.label_img_idx_now.setText(f"{self.image_idx + 1}")
                self.mainWindow.label_img_name.setText(self.image_list[self.image_idx])
            except Exception as e:
                self.showMsg("错误提示", f"err: {str(e)}")

    def image_option(self, option: str):
        if self.image_path and self.image_list:
            if option == "prev":
                if self.image_idx - 1 >= 0:
                    self.image_idx -= 1

            if option == "next":
                if self.image_idx < len(self.image_list) - 1:
                    self.image_idx += 1
            self.img_show("update")

    def reset_param(self):
        self.image_path = ""
        self.image_list = []
        self.image_idx = 0

    def window_close(self, event):
        event.ignore()
        self.mainWindow.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint) # 最小化到托盘

    def menu_version(self):
        reply = QMessageBox(QMessageBox.Information, "版本", __version__, QMessageBox.NoButton, self.mainWindow)
        reply.addButton("确定", QMessageBox.YesRole)
        reply.addButton("取消", QMessageBox.NoRole)
        reply.exec_()

    def showMsg(self, title: str, msg: str):
        reply = QMessageBox(QMessageBox.Warning, title, msg, QMessageBox.NoButton, self.mainWindow)
        reply.addButton("确定", QMessageBox.YesRole)
        reply.addButton("取消", QMessageBox.NoRole)
        reply.exec_()

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    select = Select()
    sys.exit(app.exec_())

if __name__ == "__main__":
        main()
