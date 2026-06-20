from PyQt6 import QtWidgets, QtCore, QtGui
import pyodbc
import cv2
import os

class UI_ThemSinhVien(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thêm Sinh Viên & Thu Thập Khuôn Mặt")
        self.setFixedSize(900, 550)
        
        # Biến xử lý camera
        self.cap = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Bố cục chính chia làm 2 phần (Trái: Form, Phải: Camera)
        main_layout = QtWidgets.QHBoxLayout()
        
        # ================= LÊN LAYOUT BÊN TRÁI (FORM NHẬP LIỆU) =================
        form_layout = QtWidgets.QFormLayout()
        
        self.txtMaSV = QtWidgets.QLineEdit()
        form_layout.addRow("Mã Sinh Viên:", self.txtMaSV)
        
        self.txtHoTen = QtWidgets.QLineEdit()
        form_layout.addRow("Họ Tên:", self.txtHoTen)
        
        self.txtCMND = QtWidgets.QLineEdit()
        form_layout.addRow("CMND/CCCD:", self.txtCMND)
        
        self.cmbGioiTinh = QtWidgets.QComboBox()
        self.cmbGioiTinh.addItems(["Nam", "Nữ", "Khác"])
        form_layout.addRow("Giới Tính:", self.cmbGioiTinh)
        
        self.dateNgaySinh = QtWidgets.QDateEdit()
        self.dateNgaySinh.setCalendarPopup(True)
        self.dateNgaySinh.setDisplayFormat("yyyy-MM-dd")
        self.dateNgaySinh.setDate(QtCore.QDate.currentDate())
        form_layout.addRow("Ngày Sinh:", self.dateNgaySinh)
        
        self.txtEmail = QtWidgets.QLineEdit()
        form_layout.addRow("Email:", self.txtEmail)
        
        self.txtSDT = QtWidgets.QLineEdit()
        form_layout.addRow("Số Điện Thoại:", self.txtSDT)
        
        self.txtKhoaHoc = QtWidgets.QLineEdit()
        form_layout.addRow("Khóa Học:", self.txtKhoaHoc)
        
        self.btnLuu = QtWidgets.QPushButton("💾 Lưu Thông Tin Sinh Viên")
        self.btnLuu.clicked.connect(self.save_to_db)
        self.btnLuu.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        form_layout.addRow(self.btnLuu)
        
        # ================= LÊN LAYOUT BÊN PHẢI (CAMERA) =================
        camera_layout = QtWidgets.QVBoxLayout()
        
        self.lblCamera = QtWidgets.QLabel("Camera Feed")
        self.lblCamera.setFixedSize(400, 300)
        self.lblCamera.setStyleSheet("border: 2px solid gray; background-color: black;")
        self.lblCamera.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        camera_layout.addWidget(self.lblCamera)
        
        self.btnMoCamera = QtWidgets.QPushButton("📷 Mở Camera")
        self.btnMoCamera.clicked.connect(self.start_camera)
        camera_layout.addWidget(self.btnMoCamera)
        
        self.btnThuThap = QtWidgets.QPushButton("🎯 Bắt Đầu Thu Thập Khuôn Mặt (50 Ảnh)")
        self.btnThuThap.clicked.connect(self.start_capture)
        self.btnThuThap.setEnabled(False) # Chỉ mở khi camera đã bật
        camera_layout.addWidget(self.btnThuThap)
        
        self.lblStatus = QtWidgets.QLabel("Trạng thái: Chưa thu thập dữ liệu")
        self.lblStatus.setStyleSheet("color: #ff9800; font-weight: bold;")
        camera_layout.addWidget(self.lblStatus)
        
        # Ghép 2 phần vào main_layout
        main_layout.addLayout(form_layout, 1)
        main_layout.addLayout(camera_layout, 1)
        
        self.setLayout(main_layout)
        
        # Biến đếm ảnh
        self.is_capturing = False
        self.count = 0
        self.dataset_dir = ""

    def get_connection(self):
        return pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=quanlysinhvien;Trusted_Connection=yes;')

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.timer.start(30) # Cập nhật frame mỗi 30ms
            self.btnMoCamera.setText("🛑 Tắt Camera")
            self.btnThuThap.setEnabled(True)
        else:
            self.stop_camera()

    def stop_camera(self):
        if self.cap is not None:
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.lblCamera.clear()
            self.lblCamera.setText("Camera Feed")
            self.btnMoCamera.setText("📷 Mở Camera")
            self.btnThuThap.setEnabled(False)

    def start_capture(self):
        masv = self.txtMaSV.text().strip()
        if not masv:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Mã Sinh Viên trước khi thu thập khuôn mặt!")
            return
            
        # Tạo thư mục chứa dữ liệu ảnh theo mã sinh viên
        self.dataset_dir = f"dataset/{masv}"
        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)
            
        self.is_capturing = True
        self.count = 0
        self.lblStatus.setText("Đang tiến hành chụp ảnh... Vui lòng nhìn thẳng vào camera.")
        self.btnThuThap.setEnabled(False)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret: return
        
        # Xử lý cắt khuôn mặt nếu đang trong chế độ thu thập
        if self.is_capturing:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                self.count += 1
                
                # Lưu ảnh khuôn mặt (chỉ cắt phần mặt để train cho nhẹ)
                face_img = gray[y:y+h, x:x+w]
                cv2.imwrite(f"{self.dataset_dir}/user.{self.count}.jpg", face_img)
                
                self.lblStatus.setText(f"Đang chụp ảnh... {self.count}/50")
                
                # Dừng sau khi chụp đủ 50 tấm
                if self.count >= 50:
                    self.is_capturing = False
                    self.lblStatus.setText(f"Hoàn tất thu thập 50 ảnh tại: {self.dataset_dir}")
                    self.btnThuThap.setEnabled(True)
                    break

        # Hiển thị lên giao diện PyQt
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qt_img).scaled(self.lblCamera.width(), self.lblCamera.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.lblCamera.setPixmap(pixmap)

    def save_to_db(self):
        masv = self.txtMaSV.text().strip()
        hoten = self.txtHoTen.text().strip()
        cmnd = self.txtCMND.text().strip()
        gioitinh = self.cmbGioiTinh.currentText()
        ngaysinh = self.dateNgaySinh.date().toString("yyyy-MM-dd")
        email = self.txtEmail.text().strip()
        sdt = self.txtSDT.text().strip()
        khoahoc = self.txtKhoaHoc.text().strip()
        
        if not masv or not hoten:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Mã SV và Họ tên không được để trống!")
            return
            
        # Đường dẫn thư mục chứa ảnh (nếu chưa chụp sẽ để trống)
        hinhanh_path = self.dataset_dir if self.dataset_dir else ""

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """INSERT INTO sinhvien (masinhvien, hoten, cmnd, gioitinh, ngaysinh, email, sodienthoai, khoahoc, hinhanh) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            
            cursor.execute(query, (masv, hoten, cmnd, gioitinh, ngaysinh, email, sdt, khoahoc, hinhanh_path))
            conn.commit()
            conn.close()
            
            QtWidgets.QMessageBox.information(self, "Thành công", "Đã lưu sinh viên và dữ liệu khuôn mặt thành công!")
            self.stop_camera()
            self.close()
            
        except pyodbc.IntegrityError:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Mã sinh viên đã tồn tại trong hệ thống!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi Database", f"Chi tiết: {str(e)}")

    def closeEvent(self, event):
        """Đảm bảo tắt camera an toàn khi đóng form bằng nút X"""
        self.stop_camera()
        event.accept()