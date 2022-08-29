import argparse
from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
import json
import math
from multiprocessing.pool import ThreadPool
import os
import os
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPauseAnimation, Qt, QThreadPool
from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPoint,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QSize,
    QTimer,
    Qt,
)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import * # pyright: ignore
#import bcrypt
#from cryptography.fernet import Fernet

from pathlib import Path

app = QtWidgets.QApplication(sys.argv)

with open("style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)
        

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        
        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(0, -30, 500, 30)
        self.alert_label.setStyleSheet("")
        
        self.setWindowTitle("Crazy Suite")

        self.setWindowIcon(QtGui.QIcon('Logo.ico'))
        

        
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_sign_in_button.clicked.connect(lambda:self.switch_page(1))
        self.start_register_button.clicked.connect(lambda:self.switch_page(2))
        
        self.back_to_start_from_sign_in.clicked.connect(lambda:self.switch_page(0))
        self.back_to_start_from_register.clicked.connect(lambda:self.switch_page(0))
        
        self.sign_in_sign_in_button.clicked.connect(self.on_sign_in_sign_in_button_clicked)
        self.register_submit_button.clicked.connect(self.on_register_submit_button_clicked)
        
    def on_sign_in_sign_in_button_clicked(self):
        print(self.sign_in_username_text.text(),self.sign_in_password_text.text())
        
    def on_register_submit_button_clicked(self):
        register_email, register_username, register_password, register_password_confirm = self.register_email_text.text(), self.register_username_text.text(), self.register_password_text.text(), self.register_password_confirm_text.text(),
        print(register_email, register_username, register_password, register_password_confirm)
        
    def switch_page(self, to):
        self.pages.setCurrentIndex(to)


    def alert(self, message,severity):
            print(message)
            if severity == 0:
                color = "red"
            elif severity == 1:
                color = "#ffbf00"
            elif severity == 2:
                color = "green"
            else:
                color = "red"

            x = self.alert_label.x()
            y = self.alert_label.y()
            if x == 0 and y == -30:
                self.alert_label.setText(message)
                self.alert_label.setStyleSheet(f"background-color: {color};"
                                                "font-size: 16px;")
                self.anim = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
                self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
                self.anim.setEndValue(QPoint(0, 0))
                self.anim.setDuration(1500)
                self.anim_2 = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
                self.anim_2.setEndValue(QPoint(0, -30))
                self.anim_2.setDuration(2000)
                self.delay = QPauseAnimation(5000)
                self.anim_group = QSequentialAnimationGroup()
                self.anim_group.addAnimation(self.anim)
                self.anim_group.addAnimation(self.delay)
                self.anim_group.addAnimation(self.anim_2)
                
                self.anim_group.start()
            else:
                self.return_ = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
                self.return_.setEndValue(QPoint(0, -20))
                self.return_.setDuration(1000)
                self.return_.start()



app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()

