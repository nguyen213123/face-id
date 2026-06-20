# Form implementation generated from reading ui file 'ui/Login.ui'
# Refactored: Removed Left Panel, Centered Compact Login Form

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QMessageBox
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from BUS.TaiKhoanBUS import TaiKhoanBUS
import main

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        MainWindow.setObjectName("MainWindow")
        # Thu nhỏ kích thước cửa sổ vừa vặn với Form đăng nhập
        MainWindow.resize(400, 540)
        
        # Bảng mã Style Sheet toàn cục - Phong cách Tối giản Hiện đại (Modern Dark)
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A1E;
            }
            QWidget#centralwidget {
                background-color: #1A1A1E;
            }
            QLabel {
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #121214;
                border: 1px solid #29292E;
                border-radius: 6px;
                padding: 8px 12px;
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
                background-color: #1F1F23;
            }
            QPushButton#btnDangNhap {
                background-color: #3b82f6;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
                border: none;
            }
            QPushButton#btnDangNhap:hover {
                background-color: #2563eb;
            }
            QPushButton#btnDangNhap:pressed {
                background-color: #1d4ed8;
            }
            
            /* Style cho nút Minimize và Close dạng chữ */
            QPushButton#btnClose, QPushButton#btnMinimize {
                border: none;
                background: transparent;
                color: #A1A1AA;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btnMinimize:hover {
                background-color: #29292e;
                color: #FFFFFF;
            }
            QPushButton#btnClose:hover {
                background-color: #ef4444;
                color: #FFFFFF;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # --- THANH TIÊU ĐỀ (TITLE BAR) ---
        self.titleBar = QtWidgets.QWidget(parent=self.centralwidget)
        self.titleBar.setGeometry(QtCore.QRect(0, 0, 400, 40))
        self.titleBar.setStyleSheet("background-color: #121214;")
        
        self.label_15 = QtWidgets.QLabel(parent=self.titleBar)
        self.label_15.setGeometry(QtCore.QRect(15, 10, 250, 20))
        self.label_15.setStyleSheet("font-size: 12px; color: #71717A; font-weight: 500;")
        
        # Nút thu nhỏ cửa sổ ("—") dịch theo chiều rộng mới
        self.btnMinimize = QtWidgets.QPushButton(parent=self.titleBar)
        self.btnMinimize.setObjectName("btnMinimize")
        self.btnMinimize.setGeometry(QtCore.QRect(320, 0, 40, 40))
        self.btnMinimize.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnMinimize.setText("—")
        
        # Nút đóng cửa sổ ("✕") nằm sát góc phải 400px
        self.btnClose = QtWidgets.QPushButton(parent=self.titleBar)
        self.btnClose.setObjectName("btnClose")
        self.btnClose.setGeometry(QtCore.QRect(360, 0, 40, 40))
        self.btnClose.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnClose.setText("✕")

        # --- KHU VỰC FORM ĐĂNG NHẬP (CĂN GIỮA TOÀN BỘ CHIỀU RỘNG 400PX) ---
        self.loginCard = QtWidgets.QWidget(parent=self.centralwidget)
        self.loginCard.setGeometry(QtCore.QRect(0, 40, 400, 500))
        
        # Tiêu đề Đăng nhập
        self.label = QtWidgets.QLabel(parent=self.loginCard)
        self.label.setGeometry(QtCore.QRect(50, 50, 300, 40))
        self.label.setStyleSheet("font-size: 26px; font-weight: bold; color: #FFFFFF;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) # Căn chữ giữa form
        
        # Label Email
        self.label_2 = QtWidgets.QLabel(parent=self.loginCard)
        self.label_2.setGeometry(QtCore.QRect(50, 140, 300, 20))
        self.label_2.setStyleSheet("font-size: 11px; color: #A1A1AA; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;")
        
        # Input Email
        self.txtEmail = QtWidgets.QLineEdit(parent=self.loginCard)
        self.txtEmail.setGeometry(QtCore.QRect(50, 170, 300, 40))
        self.txtEmail.setObjectName("txtEmail")
        
        # Label Password
        self.label_3 = QtWidgets.QLabel(parent=self.loginCard)
        self.label_3.setGeometry(QtCore.QRect(50, 230, 300, 20))
        self.label_3.setStyleSheet("font-size: 11px; color: #A1A1AA; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;")
        
        # Input Password
        self.txtPassword = QtWidgets.QLineEdit(parent=self.loginCard)
        self.txtPassword.setGeometry(QtCore.QRect(50, 260, 300, 40))
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtPassword.setObjectName("txtPassword")
        
        # Nút Đăng nhập
        self.btnDangNhap = QtWidgets.QPushButton(parent=self.loginCard)
        self.btnDangNhap.setGeometry(QtCore.QRect(50, 350, 300, 44))
        self.btnDangNhap.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnDangNhap.setObjectName("btnDangNhap")

        # --- KẾT NỐI LOGIC & SỰ KIỆN ---
        self.btnDangNhap.clicked.connect(lambda: self.login_func(MainWindow))
        self.btnMinimize.clicked.connect(lambda: MainWindow.showMinimized())
        self.btnClose.clicked.connect(QCoreApplication.instance().quit)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_15.setText(_translate("MainWindow", "Phần mềm điểm danh sinh viên"))
        self.label.setText(_translate("MainWindow", "Đăng Nhập"))
        self.label_2.setText(_translate("MainWindow", "Email"))
        self.label_3.setText(_translate("MainWindow", "Mật khẩu"))
        self.btnDangNhap.setText(_translate("MainWindow", "ĐĂNG NHẬP"))

    def login_func(self, MainWindow):
        username = self.txtEmail.text()
        password = self.txtPassword.text()
        tk = TaiKhoanBUS()
        resultLogin = tk.checkLogin(username, password)
        if resultLogin != False:        
            self.window = QtWidgets.QMainWindow()
            self.window.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            self.ui = main.mainGUI(resultLogin[0], resultLogin[1], resultLogin[2])                        
            self.ui.mainUi(self.window, "home")
            MainWindow.hide()
            self.window.show()
        else:
            QMessageBox.information(self.centralwidget, "Thông báo", "Login thất bại")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())