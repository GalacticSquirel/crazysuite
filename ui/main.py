import argparse
from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
import json
import math
from multiprocessing.pool import ThreadPool
import os
import os
from re import template
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


app = QApplication(sys.argv)
with open("style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)
        

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(500, 700))
        self.setWindowTitle("Crazy Suite")
        widget = QWidget()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowIcon(QtGui.QIcon('Logo.ico'))


        self.stackedLayout = QStackedLayout()
        
        self.stackedLayout.addWidget(self.start_page())
        self.stackedLayout.addWidget(self.login_page())
        self.stackedLayout.addWidget(self.sign_up_page())
        self.stackedLayout.addWidget(self.main_page())
        
        layout.addLayout(self.stackedLayout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    
    def start_page(self):
        #Start Page
        self.start = QWidget()
        self.start_layout = QGridLayout()
        
        self.welcome_label = QLabel("Welcome to Crazy Suite")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 30px;")

        self.start_layout.addWidget(self.welcome_label, 0,0)

        self.log_in_button = QPushButton("Sign In")
        self.log_in_button.clicked.connect(lambda:self.switchPage(1))
        self.start_layout.addWidget(self.log_in_button, 1,0)
        
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(lambda:self.switchPage(2))
        self.start_layout.addWidget(self.register_button, 2,0)

        #TEMP

        self.main_button = QPushButton("Main")
        self.main_button.clicked.connect(lambda:self.switchPage(3))
        self.start_layout.addWidget(self.main_button, 3,0)

        #TEMP
        
        self.start.setLayout(self.start_layout)
        
        return self.start
    
    
    def login_page(self):
        # Login

        self.login = QWidget()
        self.login_layout = QGridLayout()

        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(0, -30, 500, 30)
        self.alert_label.setStyleSheet("")
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_label = QLabel("Sign In")
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_label.setStyleSheet("font-size: 30px;")
        self.login_layout.addWidget(self.login_label, 0,0)

        self.username_login_table = QLineEdit()
        self.username_login_table.setPlaceholderText("Username")
        self.login_layout.addWidget(self.username_login_table, 1,0)

        self.password_login_table = QLineEdit()
        self.password_login_table.setPlaceholderText("Password")
        self.login_layout.addWidget(self.password_login_table, 2,0)

        self.login_form_button = QPushButton("Sign In") # Database connection needed
        self.login_layout.addWidget(self.login_form_button, 3,0)
        self.login_form_button.clicked.connect(self.login_form_processor)

        self.back_button = QPushButton("Back")
        self.login_layout.addWidget(self.back_button)
        self.back_button.clicked.connect(lambda:self.switchPage(0))
        
        self.login.setLayout(self.login_layout)

        return self.login

    def sign_up_page(self):
        # Signup

        self.sign_up = QWidget()
        self.sign_up_layout = QGridLayout()

        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(0, -30, 500, 30)
        self.alert_label.setStyleSheet("")
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sign_up_label = QLabel("Register")
        self.sign_up_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sign_up_label.setStyleSheet("font-size: 30px;")
        self.sign_up_layout.addWidget(self.sign_up_label, 0,0)

        self.email_sign_up_table = QLineEdit()
        self.email_sign_up_table.setPlaceholderText("Email")
        self.sign_up_layout.addWidget(self.email_sign_up_table, 1,0)

        self.username_sign_up_table = QLineEdit()
        self.username_sign_up_table.setPlaceholderText("Username")
        self.sign_up_layout.addWidget(self.username_sign_up_table, 2,0)

        self.password_sign_up_table = QLineEdit()
        self.password_sign_up_table.setPlaceholderText("Password")
        self.sign_up_layout.addWidget(self.password_sign_up_table, 3,0)

        self.password_confirm_sign_up_table = QLineEdit()
        self.password_confirm_sign_up_table.setPlaceholderText("Confirm Password")
        self.sign_up_layout.addWidget(self.password_confirm_sign_up_table, 4,0)


        self.sign_up_form_button = QPushButton("Register") # Database connection needed
        self.sign_up_layout.addWidget(self.sign_up_form_button, 5,0)
        self.sign_up_form_button.clicked.connect(self.sign_up_form_processor)

        self.back_button = QPushButton("Back")
        self.sign_up_layout.addWidget(self.back_button)
        self.back_button.clicked.connect(lambda:self.switchPage(0))
        
        self.sign_up.setLayout(self.sign_up_layout)

        return self.sign_up

    def main_page(self):
        self.main = QWidget()
        self.main_layout = QGridLayout()

        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(0, -30, 500, 30)
        self.alert_label.setStyleSheet("")
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_label = QLabel("Welcome To Crazy Suite")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_label.setStyleSheet("font-size: 30px;")
        self.main_layout.addWidget(self.main_label, 0,0)

        self.owned_products_label = QLabel("Products:", self)
        self.main_layout.addWidget(self.owned_products_label, 1,0)

        # self.owned_products = QHBoxLayout()
        # self.template_owned_product = 
        # self.owned_products.addItem(self.template_owned_product)

        self.main.setLayout(self.main_layout)

        return self.main
    
    def switchPage(self, to):
        self.stackedLayout.setCurrentIndex(to)
    
    def login_form_processor(self):
        username = self.username_login_table.text()
        password = self.password_login_table.text()
    
    def sign_up_form_processor(self):
        email = self.email_sign_up_table.text()
        username = self.username_sign_up_table.text()
        password = self.password_sign_up_table.text()
        confirm_password = self.password_confirm_sign_up_table.text()

    # def UI(self):
    #     spacing = 20
        
    #     self.alert_label = QLabel("", self)
    #     self.alert_label.setGeometry(0, -30, 500, 30)
    #     self.alert_label.setStyleSheet("")
    #     self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    #     self.title_card = QLabel("Welcome to Crazy Suite", self)
    #     self.title_card.setStyleSheet("font-size: 30px;")
    #     self.title_card.setGeometry(90, 40 + spacing, 320, 55)
    #     self.title_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    #     self.select_label = QLabel("No Folder Selected Yet", self)
    #     self.select_label.setGeometry(10, 95 + spacing, 480, 45)
    #     self.select_label.setStyleSheet("font-size: 3vw;")
    #     self.select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    #     self.passcode_label = QLabel("Enter Passphrase For Encryption:", self)
    #     self.passcode_label.setGeometry(140, 140 + (spacing * 2) , 220, 30)
    #     self.passcode_label.setStyleSheet("font-size: 15px;")
    #     self.passcode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    #     self.passcode = QLineEdit("",self)
    #     self.passcode.setGeometry(140, 170 + (spacing * 3), 220, 30)
    #     self.passcode.setMaxLength(20)
    #     self.passcode.setEchoMode(QLineEdit.EchoMode.Password)
    #     #self.passcode.textChanged.connect(self.line_edited)
        
    #     self.button = QPushButton('', self)
    #     self.button.setGeometry(330, 170 + (spacing * 3), 30, 30)
    #     #self.button.clicked.connect(self.show_pass)
    #     self.button.setIcon(QtGui.QIcon('eye.png'))
    #     self.button.setIconSize(QtCore.QSize(20,30))
    #     self.button.setCheckable(True)
        
    #     self.slider_label = QLabel("Level Of Encryption:", self)
    #     self.slider_label.setGeometry(60, 198 + (spacing * 4), 160, 30)
    #     self.slider_label.setStyleSheet("font-size: 15px;")
    #     self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    #     self.slider_num = QLabel("1", self)
    #     self.slider_num.setGeometry(410, 198 + (spacing * 4), 20, 30)
    #     self.slider_num.setStyleSheet("font-size: 15px;")
    #     self.slider_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    #     self.slider = QSlider(Qt.Orientation.Horizontal, self)
    #     self.slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    #     self.slider.setGeometry(240, 200 + (spacing * 4), 160, 30)
    #     #self.slider.valueChanged[int].connect(self.slider_update) 
    #     self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
    #     self.slider.setMinimum(1)
    #     self.slider.setMaximum(10)
    
    #     self.encrypt_button = QPushButton('Encrypt', self)
    #     self.encrypt_button.setStyleSheet("font-size: 13px;")
    #     self.encrypt_button.setGeometry(260, 230 + (spacing * 5),180,55)
    #     #self.encrypt_button.clicked.connect(self.encrypt_pressed)
    #     self.encrypt_button.setDisabled(True)
        
    #     self.decrypt_button = QPushButton('Decrypt', self)
    #     self.decrypt_button.setStyleSheet("font-size: 13px;")
    #     self.decrypt_button.setGeometry(60, 230 + (spacing * 5),180,55)
    #     self.decrypt_button.clicked.connect(lambda: self.alert("no",0))
    #     # self.decrypt_button.setDisabled(True)
        
    #     self.prog_bar = QProgressBar(self)
    #     self.prog_bar.setGeometry(60, 285 + (spacing * 6), 380, 55)
        
    #     mx = 380 + (spacing * 6)
    #     self.setFixedSize(QSize(700, mx))

    # def alert(self, message,severity):
    #         print(message)
    #         if severity == 0:
    #             color = "red"
    #         elif severity == 1:
    #             color = "#ffbf00"
    #         elif severity == 2:
    #             color = "green"
    #         else:
    #             color = "red"

    #         x = self.alert_label.x()
    #         y = self.alert_label.y()
    #         if x == 0 and y == -30:
    #             self.alert_label.setText(message)
    #             self.alert_label.setStyleSheet(f"background-color: {color};"
    #                                             "font-size: 16px;")
    #             self.anim = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
    #             self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
    #             self.anim.setEndValue(QPoint(0, 0))
    #             self.anim.setDuration(1500)
    #             self.anim_2 = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
    #             self.anim_2.setEndValue(QPoint(0, -30))
    #             self.anim_2.setDuration(2000)
    #             self.delay = QPauseAnimation(5000)
    #             self.anim_group = QSequentialAnimationGroup()
    #             self.anim_group.addAnimation(self.anim)
    #             self.anim_group.addAnimation(self.delay)
    #             self.anim_group.addAnimation(self.anim_2)
                
    #             self.anim_group.start()
    #         else:
    #             self.return_ = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
    #             self.return_.setEndValue(QPoint(0, -20))
    #             self.return_.setDuration(1000)
    #             self.return_.start()



app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()

