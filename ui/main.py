from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
import os
import os
import sys
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
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



app = QApplication(sys.argv)
with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
        

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encryption Tool")

        self.proceed_folder = False
        self.proceed_passphrase = False

        spacing = 25
        
        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(0, -30, 500, 30)
        self.alert_label.setStyleSheet("")
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        self.select = QPushButton("Select Folder",self)
        self.select.setGeometry(140, 40, 220, 55)
        #self.select.clicked.connect(self.select_folder)
        
        self.select_label = QLabel("No Folder Selected Yet", self)
        self.select_label.setGeometry(10, 95 + spacing, 480, 45)
        self.select_label.setStyleSheet("font-size: 3vw;")
        self.select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.passcode_label = QLabel("Enter Passphrase For Encryption:", self)
        self.passcode_label.setGeometry(140, 140 + (spacing * 2) , 220, 30)
        self.passcode_label.setStyleSheet("font-size: 15px;")
        self.passcode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.passcode = QLineEdit("",self)
        self.passcode.setGeometry(140, 170 + (spacing * 3), 220, 30)
        self.passcode.setMaxLength(20)
        self.passcode.setEchoMode(QLineEdit.EchoMode.Password)
        #self.passcode.textChanged.connect(self.line_edited)
        
        self.button = QPushButton('', self)
        self.button.setGeometry(330, 170 + (spacing * 3), 30, 30)
        #self.button.clicked.connect(self.show_pass)
        self.button.setIcon(QtGui.QIcon('eye.png'))
        self.button.setIconSize(QtCore.QSize(20,30))
        self.button.setCheckable(True)
        
        self.slider_label = QLabel("Level Of Encryption:", self)
        self.slider_label.setGeometry(60, 198 + (spacing * 4), 160, 30)
        self.slider_label.setStyleSheet("font-size: 15px;")
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.slider_num = QLabel("1", self)
        self.slider_num.setGeometry(410, 198 + (spacing * 4), 20, 30)
        self.slider_num.setStyleSheet("font-size: 15px;")
        self.slider_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.slider.setGeometry(240, 200 + (spacing * 4), 160, 30)
        #self.slider.valueChanged[int].connect(self.slider_update) 
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
    
        self.encrypt_button = QPushButton('Encrypt', self)
        self.encrypt_button.setStyleSheet("font-size: 13px;")
        self.encrypt_button.setGeometry(260, 230 + (spacing * 5),180,55)
        #self.encrypt_button.clicked.connect(self.encrypt_pressed)
        self.encrypt_button.setDisabled(True)
        
        self.decrypt_button = QPushButton('Decrypt', self)
        self.decrypt_button.setStyleSheet("font-size: 13px;")
        self.decrypt_button.setGeometry(60, 230 + (spacing * 5),180,55)
        #self.decrypt_button.clicked.connect(self.decrypt_pressed)
        self.decrypt_button.setDisabled(True)
        
        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(60, 285 + (spacing * 6), 380, 55)
        
        mx = 380 + (spacing * 6)
        self.setFixedSize(QSize(500, mx))




app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()

