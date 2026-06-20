from PyQt6 import QtGui, QtWidgets, QtCore
from pathlib import Path
import sys
import os
import NhanDien
import QuanLyDiemDanh
import ThongKe
import qdarkstyle
import ThemBuoiHoc
import ThemGiangVien
import ThemSinhVien

# Tự động import thêm các module bổ trợ nếu có trong dự án
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
    def back_to_home(self, MainWindow):
        """Hàm xử lý an toàn khi nhấn nút Trở về"""
        try:
            # 1. TẮT CAMERA HOẶC TIMER NẾU ĐANG CHẠY TRƯỚC KHI ĐỔI GIAO DIỆN
            # (Bạn cần thay 'stop_camera', 'timer' bằng tên biến/hàm thực tế trong file NhanDien.py của bạn)
            if hasattr(self.ui, 'stop_camera'):
                self.ui.stop_camera()
            elif hasattr(self.ui, 'cap'):  # Nếu dùng OpenCV (cv2.VideoCapture)
                self.ui.cap.release()
            elif hasattr(self.ui, 'timer'): # Nếu dùng QTimer để update frame
                self.ui.timer.stop()
                
            # Cố gắng dừng các chức năng ngầm ở các form khác (Thống kê, Quản lý...)
            if hasattr(self.ui, 'release_resources'):
                self.ui.release_resources()

            # 2. Xóa giao diện hiện tại đi một cách an toàn để giải phóng RAM
            if MainWindow.centralWidget() is not None:
                MainWindow.centralWidget().deleteLater()
                
        except Exception as e:
            print("Lỗi khi dọn dẹp giao diện cũ:", e)
            
        # 3. Mở lại trang chủ
        self.mainUi(MainWindow, "home")

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
        """Khởi tạo Menu chính hệ thống tích hợp phân quyền động"""
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 10) 
        
        # 1. TOP BAR (Giữ nguyên)
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_layout.addStretch() 
        
        self.btnMinimizeHome = QtWidgets.QPushButton("—")
        self.btnMinimizeHome.setFixedSize(45, 30)
        self.btnMinimizeHome.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; font-size: 12px; color: #888888; }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); color: white; }
        """)
        self.btnMinimizeHome.clicked.connect(MainWindow.showMinimized)
        top_bar_layout.addWidget(self.btnMinimizeHome)
        
        self.btnCloseHome = QtWidgets.QPushButton("✕")
        self.btnCloseHome.setFixedSize(45, 30)
        self.btnCloseHome.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; font-size: 13px; font-weight: bold; color: #888888; }
            QPushButton:hover { background-color: #e81123; color: white; }
        """)
        self.btnCloseHome.clicked.connect(lambda: sys.exit(0))
        top_bar_layout.addWidget(self.btnCloseHome)
        
        layout.addLayout(top_bar_layout)
        
        # 2. TIÊU ĐỀ
        title = QtWidgets.QLabel("Face ID Attendance System")
        title_font = QtGui.QFont("Arial", 28, QtGui.QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("margin: 20px 0px 20px 0px;")
        layout.addWidget(title)
        
        # 3. KHỞI TẠO TẤT CẢ CÁC NÚT (Nhưng chưa thêm vào layout)
        btn_font = QtGui.QFont("Arial", 12, QtGui.QFont.Weight.Bold)
        btn_size = (240, 100)
        
        # Định nghĩa danh sách các nút
        buttons_info = [
            ("btnNhanDien", "📸 Nhận Diện Khuôn Mặt", lambda: self.NhanDien_UI(MainWindow)),
            ("btnDiemDanh", "📋 Quản Lý Điểm Danh", lambda: self.QuanLyDiemDanh_UI(MainWindow)),
            ("btnThongKe", "📊 Thống Kê Hệ Thống", lambda: self.ThongKe_UI(MainWindow)),
            ("btnUserMgmt", "👥 Quản Lý Người Dùng\n(Thêm, Xóa, Sửa)", lambda: self.QuanLyNguoiDung_UI(MainWindow)),
            ("btnFaceData", "⚙️ Face Data Train", lambda: self.DuLieuKhuonMat_UI(MainWindow)),
            ("btnSchedule", "📅 Schedule & Shifts", lambda: self.QuanLyLichTrinh_UI(MainWindow)),
            ("btnCamera", "📹 Camera Streams", lambda: self.QuanLyCamera_UI(MainWindow)),
            ("btnThemSV", "👤 Thêm Sinh Viên Mới", lambda: self.ThemSinhVien_UI(MainWindow)),
            ("btnThemGiangVien", "➕ Thêm Giảng Viên", lambda: self.QuanLyNguoiDung_UI(MainWindow)),
            ("btnThemBuoiHoc", "📚 Thêm Buổi Học Mới", lambda: self.ThemBuoiHoc_UI(MainWindow))
            
        ]
        
        # Tạo instance cho các nút
        for attr_name, text, func in buttons_info:
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumSize(*btn_size)
            btn.setFont(btn_font)
            btn.clicked.connect(func)
            setattr(self, attr_name, btn) # Gán vào self.btnNhanDien, self.btnDiemDanh...

        # 4. GRID LAYOUT - CHỈ THÊM CÁC NÚT PHÙ HỢP
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setContentsMargins(30, 0, 30, 0)
        grid_layout.setSpacing(20)

        current_permission = str(self.maquyen).strip()
        
        # Logic chọn nút dựa vào quyền
        if current_permission == 'Admin':
            # Danh sách nút cho Admin
            allowed_buttons = [
                self.btnThemGiangVien, 
                self.btnThemSV, 
                self.btnThemBuoiHoc
            ]
        else:
            # Danh sách nút cho User
            allowed_buttons = [self.btnNhanDien, self.btnDiemDanh, self.btnThongKe]
            
        # Thêm nút vào grid
        for i, btn in enumerate(allowed_buttons):
            row = i // 3
            col = i % 3
            grid_layout.addWidget(btn, row, col)
        
        layout.addLayout(grid_layout)
        layout.addStretch()
        
        central_widget.setLayout(layout)
        MainWindow.setCentralWidget(central_widget)
        
        self.ChangeStyleDarkMode()
        # Không cần gọi checkFunctionInPermission ở đây để ẩn/hiện nút nữa, 
        # vì chúng ta đã chủ động chọn nút rồi.        
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

    def ThemSinhVien_UI(self, MainWindow):
        try:
            self.dialog_sv = ThemSinhVien.UI_ThemSinhVien()
            self.dialog_sv.exec()
        except Exception as e:
            print("Lỗi khi mở form thêm sinh viên:", e)
            
    def showMinimized(self):
        if hasattr(self, 'MainWindow'):
            self.MainWindow.showMinimized()

    # ========================================================
    # 📑 HÀM KHỞI TẠO CÁC PHÂN HỆ ADMIN (Cần Import File Giao Diện Tương Ứng)
    # ========================================================
    def QuanLyNguoiDung_UI(self, MainWindow):
        try:
            self.dialog_gv = ThemGiangVien.UI_ThemGiangVien()
            self.dialog_gv.exec()
        except Exception as e:
            print("Lỗi khi mở form thêm giảng viên:", e)
    def DuLieuKhuonMat_UI(self, MainWindow):
        """Tính năng: Chụp ảnh webcam, Upload ảnh, Kích hoạt Train Model"""
        QtWidgets.QMessageBox.information(MainWindow, "Thông báo", "Đang mở phân hệ: Quản lý & Huấn luyện dữ liệu khuôn mặt")

    def QuanLyLichTrinh_UI(self, MainWindow):
        """Tính năng: Tạo ca làm việc, cấu hình thời gian đi muộn"""
        QtWidgets.QMessageBox.information(MainWindow, "Thông báo", "Đang mở phân hệ: Cấu hình Lịch học / Ca làm việc")

    def QuanLyCamera_UI(self, MainWindow):
        """Tính năng: Cấu hình luồng IP Camera / Webcam"""
        QtWidgets.QMessageBox.information(MainWindow, "Thông báo", "Đang mở phân hệ: Cấu hình luồng Camera")

    # ========================================================
    # CÁC UI CÓ SẴN CỦA BẠN
    # ========================================================
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
        if hasattr(self.ui, 'btnBack'): self.ui.btnBack.clicked.connect(lambda: self.back_to_home(MainWindow))
        
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
        if hasattr(self.ui, 'btnBack'): self.ui.btnBack.clicked.connect(lambda: self.back_to_home(MainWindow))
        self.ChangeStyleDarkMode()
        if hasattr(self.ui, 'btnDark'): self.ui.btnDark.clicked.connect(self.ChangeDarkMode_UI)
        MainWindow.show()

    def QuanLyDiemDanh_UI(self, MainWindow):
        self.ui = QuanLyDiemDanh.UI_QuanLyDiemDanh()
        self.MainWindow = MainWindow
        self.ui.setupUi(MainWindow)
        if hasattr(self.ui, 'btnMinimize'): self.ui.btnMinimize.clicked.connect(self.showMinimized)
        if hasattr(self.ui, 'btnClose'): self.ui.btnClose.clicked.connect(lambda: sys.exit(self.app.exit()))
        if hasattr(self.ui, 'btnBack'): self.ui.btnBack.clicked.connect(lambda: self.back_to_home(MainWindow))
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


    def ThemBuoiHoc_UI(self, MainWindow):
        try:
            self.dialog_them_buoi = ThemBuoiHoc.UI_ThemBuoiHoc()
            self.dialog_them_buoi.exec()
        except Exception as e:
         print("Lỗi khi mở form:", e)

    def checkFunctionInPermission(self, maquyen):
        """Xử lý ẩn/hiện các nút tính năng dựa vào mã quyền của tài khoản đăng nhập"""
        if maquyen == 'Q001':
            # Ẩn nút nhận diện khuôn mặt đối với ADMIN
            if hasattr(self, 'btnNhanDien'): self.btnNhanDien.hide()
            
            # Đảm bảo hiển thị đầy đủ các nút quản lý cho ADMIN
            if hasattr(self, 'btnUserMgmt'): self.btnUserMgmt.show()
            if hasattr(self, 'btnFaceData'): self.btnFaceData.show()
            if hasattr(self, 'btnSchedule'): self.btnSchedule.show()
            if hasattr(self, 'btnCamera'): self.btnCamera.show()
            if hasattr(self, 'btnThemSV'): self.btnThemSV.show()
            if hasattr(self, 'btnThemBuoiHoc'): self.btnThemBuoiHoc.show()
        else:
            # Nếu không phải Admin, ẩn hoàn toàn các tính năng quản trị cấp cao này đi và hiện Nhận Diện
            if hasattr(self, 'btnNhanDien'): self.btnNhanDien.show()
            if hasattr(self, 'btnUserMgmt'): self.btnUserMgmt.hide()
            if hasattr(self, 'btnFaceData'): self.btnFaceData.hide()
            if hasattr(self, 'btnSchedule'): self.btnSchedule.hide()
            if hasattr(self, 'btnCamera'): self.btnCamera.hide()

        # Giữ lại logic kiểm tra phân quyền từ database cũ của bạn dưới đây:
        if Quyen_ChucNangBUS is None:
            return
        try:
            qcn = Quyen_ChucNangBUS()
            listcn = qcn.getListChucNangTheoQuyen(maquyen) 
            if not hasattr(self, 'ui'):
                return
            if any(cn in listcn for cn in ['CN001', 'CN002', 'CN003', 'CN004']):
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
    
    # Giả lập đăng nhập với quyền Admin ('Q001') -> Nút Nhận diện ẩn, các nút Quản lý & Thống kê lên hàng đầu.
    ui = mainGUI('admin@gmail.com', '12345678', 'Q001')
    ui.mainUi(MainWindow, "home")
    MainWindow.show()
    sys.exit(app.exec())