from PyQt6 import QtGui, QtWidgets, QtCore
from pathlib import Path
import sys
import os
import NhanDien
import QuanLyDiemDanh
import ThongKe
import qdarkstyle

# Tự động import thêm các module bổ trợ nếu có trong dự án của bạn
try:
    import QuanLyTaiKhoan
except ImportError:
    pass

try:
    import Login
except ImportError:
    pass

try:
    from BUS.Quyen_ChucNangBUS import Quyen_ChucNangBUS
except ImportError:
    try:
        from Quyen_ChucNangBUS import Quyen_ChucNangBUS
    except ImportError:
        Quyen_ChucNangBUS = None


class mainGUI:
    def __init__(self, email='admin@gmail.com', matkhau='', maquyen='Q001'):
        self.email = email
        self.matkhau = matkhau
        self.maquyen = maquyen
        self.DarkMode = True
        
        # Lấy instance ứng dụng đang chạy từ Login.py để đồng bộ giao diện
        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)

    def mainUi(self, MainWindow, page="home"):
        self.MainWindow = MainWindow
        if page == "home":
            self.create_main_menu(MainWindow)
        MainWindow.show()

    def create_main_menu(self, MainWindow):
        """Khởi tạo Menu chính hệ thống tích hợp phân quyền và nút đóng/thu nhỏ giống Login"""
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 10) # Tối ưu khoảng cách viền
        
        # ========================================================
        # 👑 THANH ĐIỀU KHIỂN TOP BAR (NÚT THU NHỎ VÀ NÚT X THOÁT)
        # ========================================================
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_layout.addStretch() # Đẩy cụm nút về góc phải ngoài cùng
        
        # 1. Nút ẩn/thu nhỏ cửa sổ (—)
        self.btnMinimizeHome = QtWidgets.QPushButton("—")
        self.btnMinimizeHome.setFixedSize(45, 30)
        self.btnMinimizeHome.setStyleSheet("""
            QPushButton { 
                background-color: transparent; 
                border: none; 
                font-size: 12px; 
                color: #888888;
            }
            QPushButton:hover { 
                background-color: rgba(255, 255, 255, 0.1); 
                color: white;
            }
        """)
        self.btnMinimizeHome.clicked.connect(MainWindow.showMinimized)
        top_bar_layout.addWidget(self.btnMinimizeHome)
        
        # 2. Nút đóng/thoát ứng dụng (✕)
        self.btnCloseHome = QtWidgets.QPushButton("✕")
        self.btnCloseHome.setFixedSize(45, 30)
        self.btnCloseHome.setStyleSheet("""
            QPushButton { 
                background-color: transparent; 
                border: none; 
                font-size: 13px; 
                font-weight: bold;
                color: #888888;
            }
            QPushButton:hover { 
                background-color: #e81123; 
                color: white; 
            }
        """)
        self.btnCloseHome.clicked.connect(lambda: sys.exit(0))
        top_bar_layout.addWidget(self.btnCloseHome)
        
        # Thêm thanh top bar này vào đầu layout chính
        layout.addLayout(top_bar_layout)
        # ========================================================
        
        # Tiêu đề ứng dụng
        title = QtWidgets.QLabel("Face ID Attendance System")
        title_font = QtGui.QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("margin: 20px 0px 30px 0px;")
        layout.addWidget(title)
        
        # Khu vực các nút bấm tính năng
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setContentsMargins(20, 0, 20, 0)
        buttons_layout.setSpacing(20)
        
        self.btnNhanDien = QtWidgets.QPushButton("📸 Face Recognition")
        self.btnNhanDien.setMinimumSize(250, 120)
        self.btnNhanDien.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold))
        self.btnNhanDien.clicked.connect(lambda: self.NhanDien_UI(MainWindow))
        buttons_layout.addWidget(self.btnNhanDien)
        
        self.btnDiemDanh = QtWidgets.QPushButton("📋 Attendance")
        self.btnDiemDanh.setMinimumSize(250, 120)
        self.btnDiemDanh.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold))
        self.btnDiemDanh.clicked.connect(lambda: self.QuanLyDiemDanh_UI(MainWindow))
        buttons_layout.addWidget(self.btnDiemDanh)
        
        self.btnThongKe = QtWidgets.QPushButton("📊 Statistics")
        self.btnThongKe.setMinimumSize(250, 120)
        self.btnThongKe.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold))
        self.btnThongKe.clicked.connect(lambda: self.ThongKe_UI(MainWindow))
        buttons_layout.addWidget(self.btnThongKe)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        central_widget.setLayout(layout)
        MainWindow.setCentralWidget(central_widget)
        
        # Áp dụng theme và thực hiện kiểm tra phân quyền tài khoản
        self.ChangeStyleDarkMode()
        self.checkFunctionInPermission(self.maquyen)
        
    def ChangeStyleDarkMode(self):
        try:
            if self.DarkMode:
                self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
            else:
                self.app.setStyleSheet("")
        except Exception as e:
            print("Không thể tải stylesheet DarkMode:", e)

    def ChangeDarkMode_UI(self):
        self.DarkMode = not self.DarkMode
        self.ChangeStyleDarkMode()

    def showMinimized(self):
        if hasattr(self, 'MainWindow'):
            self.MainWindow.showMinimized()

    def ThongKe_UI(self, MainWindow):
        self.ui = ThongKe.UI_ThongKe()
        self.MainWindow = MainWindow
        self.ui.setupUi(MainWindow)

        def ChangeTextDarkThongKe():
            if hasattr(self.ui, 'lbSoSV'): self.ui.lbSoSV.setStyleSheet('color:black;font-weight:bold;background-color:transparent;')
            if hasattr(self.ui, 'lbSoLanVang'): self.ui.lbSoLanVang.setStyleSheet('color:black;font-weight:bold;background-color:transparent;')
            if hasattr(self.ui, 'lbSoBanDiemDanh'): self.ui.lbSoBanDiemDanh.setStyleSheet('color:black;font-weight:bold;background-color:transparent')
            if hasattr(self.ui, 'lbSoLanDiMuon'): self.ui.lbSoLanDiMuon.setStyleSheet('color:black;font-weight:bold;background-color:transparent;')
        
        if hasattr(self.ui, 'btnMinimize'): self.ui.btnMinimize.clicked.connect(self.showMinimized)
        if hasattr(self.ui, 'btnClose'): self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
        if hasattr(self.ui, 'btnBack'): self.ui.btnBack.clicked.connect(lambda: self.mainUi(MainWindow, "home"))
        
        self.ChangeStyleDarkMode()
        ChangeTextDarkThongKe()
        if hasattr(self.ui, 'btnDark'):
            self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
            self.ui.btnDark.clicked.connect(ChangeTextDarkThongKe)
        MainWindow.show()

    def NhanDien_UI(self, MainWindow):
        self.ui = NhanDien.UI_NhanDien()
        self.MainWindow = MainWindow
        self.ui.setupUi(MainWindow)
        if hasattr(self.ui, 'btnMinimize'): self.ui.btnMinimize.clicked.connect(self.showMinimized)
        if hasattr(self.ui, 'btnClose'): self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
        if hasattr(self.ui, 'btnBack'): self.ui.btnBack.clicked.connect(lambda: self.mainUi(MainWindow, "home"))
        self.ChangeStyleDarkMode()
        if hasattr(self.ui, 'btnDark'): self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
        MainWindow.show()

    def QuanLyDiemDanh_UI(self, MainWindow):
        self.ui = QuanLyDiemDanh.UI_QuanLyDiemDanh()
        self.MainWindow = MainWindow
        self.ui.setupUi(MainWindow)
        if hasattr(self.ui, 'btnMinimize'): self.ui.btnMinimize.clicked.connect(self.showMinimized)
        if hasattr(self.ui, 'btnClose'): self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
        if hasattr(self.ui, 'btnBack'): self.ui.btnBack.clicked.connect(lambda: self.mainUi(MainWindow, "home"))
        self.ChangeStyleDarkMode()
        if hasattr(self.ui, 'btnDark'): self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
        MainWindow.show()

    def TaiKhoan_UI(self, MainWindow):
        if 'QuanLyTaiKhoan' in sys.modules:
            self.ui = QuanLyTaiKhoan.UI_QuanLyTaiKhoan()
            self.MainWindow = MainWindow
            self.ui.setupUi(MainWindow)
            if hasattr(self.ui, 'btnMinimize'): self.ui.btnMinimize.clicked.connect(self.showMinimized)
            if hasattr(self.ui, 'btnClose'): self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
            if hasattr(self.ui, 'btnBack'): self.ui.btnBack.clicked.connect(lambda: self.mainUi(MainWindow, "home"))
            self.ChangeStyleDarkMode()
            if hasattr(self.ui, 'btnDark'): self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
            MainWindow.show()    

    def logout(self, MainWindow):
        self.MainWindow = MainWindow
        self.window = QtWidgets.QMainWindow()
        if 'Login' in sys.modules:
            self.ui = Login.Ui_MainWindow()
            self.ui.setupUi(self.window)
            self.DarkMode = True
            try:
                self.app.setStyleSheet(Path(r"qss\py_md_style.qss").read_text(encoding='utf-8'))                      
            except:
                pass
            MainWindow.hide()
            self.window.show()

    def checkFunctionInPermission(self, maquyen):
        if Quyen_ChucNangBUS is None:
            return
        try:
            qcn = Quyen_ChucNangBUS()
            listcn = qcn.getListChucNangTheoQuyen(maquyen) 
            if not hasattr(self, 'ui'):
                return
            if ('CN001' or 'CN002' or 'CN003' or 'CN004') in listcn:
                if 'CN001' not in listcn and hasattr(self.ui, 'btnQLSV'): self.ui.btnQLSV.hide()
                if 'CN002' not in listcn and hasattr(self.ui, 'btnDiemDanh'): self.ui.btnDiemDanh.hide()                
                if 'CN003' not in listcn and hasattr(self.ui, 'btnGiangVien'): self.ui.btnGiangVien.hide() 
                if 'CN004' not in listcn and hasattr(self.ui, 'btnBuoiHoc'): self.ui.btnBuoiHoc.hide()
            else:
                if hasattr(self.ui, 'btnQuanLy'): self.ui.btnQuanLy.hide()
            if 'CN005' not in listcn and hasattr(self.ui, 'btnNhanDien'): self.ui.btnNhanDien.hide()
            if 'CN006' not in listcn and hasattr(self.ui, 'btnThongKe'): self.ui.btnThongKe.hide()
            if 'CN007' not in listcn and hasattr(self.ui, 'btnTaiKhoan'): self.ui.btnTaiKhoan.hide()
            if 'CN008' not in listcn and hasattr(self.ui, 'btnMatKhau'): self.ui.btnMatKhau.hide()
        except Exception as e:
            print("Lỗi khi xử lý phân quyền giao diện:", e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    ui = mainGUI('admin@gmail.com', '12345678', 'Q001')
    ui.mainUi(MainWindow, "home")
    MainWindow.show()
    sys.exit(app.exec())