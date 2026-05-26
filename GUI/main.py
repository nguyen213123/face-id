from PyQt6 import QtGui, QtWidgets, QtCore
from pathlib import Path
import sys
import os
import NhanDien
import QuanLyDiemDanh
import ThongKe
import qdarkstyle


def get_project_root():
    """Get the root directory of the project"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_qss_path(qss_name):
    """Get absolute path for QSS stylesheet"""
    return os.path.join(get_project_root(), "qss", qss_name)


class SimpleAttendanceApp:
    """Simple Face ID Attendance Application"""
    
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle("Face ID Attendance System")
        self.main_window.setGeometry(100, 100, 1000, 700)
        self.dark_mode = True
        self.create_main_menu()
        
    def create_main_menu(self):
        """Create main menu with 3 buttons"""
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        # Title
        title = QtWidgets.QLabel("Face ID Attendance System")
        title_font = QtGui.QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("margin: 30px; color: #333;")
        layout.addWidget(title)
        
        # Spacer
        layout.addSpacing(30)
        
        # Buttons layout
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        # Face Recognition Button
        btn_face = QtWidgets.QPushButton("📸 Face Recognition")
        btn_face.setMinimumSize(250, 120)
        btn_face.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold))
        btn_face.clicked.connect(self.open_face_recognition)
        buttons_layout.addWidget(btn_face)
        
        # Attendance Button
        btn_attendance = QtWidgets.QPushButton("📋 Attendance")
        btn_attendance.setMinimumSize(250, 120)
        btn_attendance.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold))
        btn_attendance.clicked.connect(self.open_attendance)
        buttons_layout.addWidget(btn_attendance)
        
        # Statistics Button
        btn_stats = QtWidgets.QPushButton("📊 Statistics")
        btn_stats.setMinimumSize(250, 120)
        btn_stats.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold))
        btn_stats.clicked.connect(self.open_statistics)
        buttons_layout.addWidget(btn_stats)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        central_widget.setLayout(layout)
        self.main_window.setCentralWidget(central_widget)
        self.apply_stylesheet()
        
    def open_face_recognition(self):
        """Open Face Recognition UI"""
        try:
            self.ui = NhanDien.UI_NhanDien()
            self.ui.setupUi(self.main_window)
            self.apply_stylesheet()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Error", f"Failed to load Face Recognition: {e}")
        
    def open_attendance(self):
        """Open Attendance Management UI"""
        try:
            self.ui = QuanLyDiemDanh.UI_QuanLyDiemDanh()
            self.ui.setupUi(self.main_window)
            self.apply_stylesheet()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Error", f"Failed to load Attendance: {e}")
        
    def open_statistics(self):
        """Open Statistics UI"""
        try:
            self.ui = ThongKe.UI_ThongKe()
            self.ui.setupUi(self.main_window)
            self.apply_stylesheet()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Error", f"Failed to load Statistics: {e}")
        
    def apply_stylesheet(self):
        """Apply stylesheet"""
        try:
            qss_path = get_qss_path("py_md_style.qss")
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Warning: Could not load stylesheet: {e}")
    
    def run(self):
        """Run the application"""
        self.main_window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = SimpleAttendanceApp()
    app.run()


        

    def ThongKe_UI(self,MainWindow):
        self.ui = ThongKe.UI_ThongKe()
        self.MainWindow = MainWindow
        self.ui.setupUi(MainWindow)

        def ChangeTextDarkThongKe():
            self.ui.lbSoSV.setStyleSheet(
                'color:black;font-weight:bold;background-color:transparent; ')
            self.ui.lbSoLanVang.setStyleSheet(
                'color:black;font-weight:bold;background-color:transparent;')
            self.ui.lbSoBanDiemDanh.setStyleSheet(
                'color:black;font-weight:bold;background-color:transparent')
            self.ui.lbSoLanDiMuon.setStyleSheet(
                'color:black;font-weight:bold;background-color:transparent;')
        # Chọn minimize
        self.ui.btnMinimize.clicked.connect(self.showMinimized)
        # Chọn close
        self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
        # Chọn trở về
        self.ui.btnBack.clicked.connect(lambda: self.mainUi(MainWindow,"home"))
        # Dark-Light Mode
        self.ChangeStyleDarkMode()
        ChangeTextDarkThongKe()
        self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
        self.ui.btnDark.clicked.connect(ChangeTextDarkThongKe)
        MainWindow.show()


    def NhanDien_UI(self, MainWindow):
        self.ui = NhanDien.UI_NhanDien()
        self.MainWindow = MainWindow
        self.ui.setupUi(MainWindow)
        # Chọn minimize
        self.ui.btnMinimize.clicked.connect(self.showMinimized)
        # Chọn close
        self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
        # Chọn trở về
        self.ui.btnBack.clicked.connect(lambda: self.mainUi(MainWindow,"home"))
        # Dark-Light Mode
        self.ChangeStyleDarkMode()
        self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
        MainWindow.show()
    def TaiKhoan_UI(self, MainWindow):
        self.ui = QuanLyTaiKhoan.UI_QuanLyTaiKhoan()
        self.MainWindow = MainWindow
        self.ui.setupUi(MainWindow)
        # Chọn minimize
        self.ui.btnMinimize.clicked.connect(self.showMinimized)
        # Chọn close
        self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
        # Chọn trở về
        self.ui.btnBack.clicked.connect(lambda: self.mainUi(MainWindow,"home"))
        # Dark-Light Mode
        self.ChangeStyleDarkMode()
        self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
        MainWindow.show()    
    def logout(self, MainWindow):
        
        # QtWidgets.QApplication.closeAllWindows()
        self.MainWindow = MainWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Login.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.DarkMode = True
        self.app.setStyleSheet(Path(
            r"qss\py_md_style.qss").read_text())                     
        MainWindow.hide()
        self.window.show()

    def checkFunctionInPermission(self, maquyen):
        qcn = Quyen_ChucNangBUS()
        listcn = qcn.getListChucNangTheoQuyen(maquyen) 
        if ('CN001' or 'CN002' or 'CN003' or 'CN004') in listcn:
            if 'CN001' not in listcn:
                self.ui.btnQLSV.hide()
            if 'CN002' not in listcn:
                self.ui.btnDiemDanh.hide()                
            if 'CN003' not in listcn:
                self.ui.btnGiangVien.hide() 
            if 'CN004' not in listcn:
                self.ui.btnBuoiHoc.hide()
                           
        else:
            self.ui.btnQuanLy.hide()
        if 'CN005' not in listcn:
            self.ui.btnNhanDien.hide()
        if 'CN006' not in listcn:
            self.ui.btnThongKe.hide()
        if 'CN007' not in listcn:
            self.ui.btnTaiKhoan.hide()
        if 'CN008' not in listcn:
            self.ui.btnMatKhau.hide()
        



    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    ui = mainGUI('admin@gmail.com','12345678','Q001')
    ui.mainUi(MainWindow, "home")
    MainWindow.show()
    sys.exit(app.exec())

