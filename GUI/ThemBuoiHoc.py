from PyQt6 import QtWidgets, QtCore
import pyodbc
import datetime # Import thêm thư viện này để tạo mã tự động

class UI_ThemBuoiHoc(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thêm Buổi Học Mới")
        self.setFixedSize(400, 400) # Thu nhỏ lại vì đã bỏ ô nhập mã
        
        layout = QtWidgets.QVBoxLayout()
        
        # ĐÃ XÓA TRƯỜNG NHẬP MÃ BUỔI HỌC Ở ĐÂY
        
        # 1. Chọn Giảng viên (Hiển thị tên, ẩn mã)
        layout.addWidget(QtWidgets.QLabel("Chọn Giảng viên:"))
        self.cmbTenGV = QtWidgets.QComboBox()
        layout.addWidget(self.cmbTenGV)
        
        # 2. Ngày và Giờ
        layout.addWidget(QtWidgets.QLabel("Ngày học:"))
        self.dateNgay = QtWidgets.QDateEdit()
        self.dateNgay.setCalendarPopup(True)
        self.dateNgay.setDate(QtCore.QDate.currentDate())
        layout.addWidget(self.dateNgay)
        
        layout.addWidget(QtWidgets.QLabel("Giờ bắt đầu:"))
        self.timeBatDau = QtWidgets.QTimeEdit()
        layout.addWidget(self.timeBatDau)
        
        layout.addWidget(QtWidgets.QLabel("Giờ kết thúc:"))
        self.timeKetThuc = QtWidgets.QTimeEdit()
        layout.addWidget(self.timeKetThuc)
        
        self.btnLuu = QtWidgets.QPushButton("Lưu Buổi Học")
        self.btnLuu.clicked.connect(self.save_to_db)
        layout.addWidget(self.btnLuu)
        
        self.setLayout(layout)
        
        # Tải dữ liệu vào Combobox khi mở form
        self.load_data_to_combobox()

    def get_connection(self):
        return pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=quanlysinhvien;Trusted_Connection=yes;')

    def load_data_to_combobox(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Load giảng viên: Lấy mã và họ tên
            cursor.execute("SELECT magiangvien, hoten FROM giangvien") 
            for row in cursor.fetchall():
                ma_gv = str(row[0])
                ten_gv = str(row[1])
                self.cmbTenGV.addItem(ten_gv, userData=ma_gv)
                
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể tải danh sách dữ liệu: {e}")

    def save_to_db(self):
        # TỰ ĐỘNG TẠO MÃ BUỔI HỌC (Ví dụ kết quả: BH260620112626)
        # Sử dụng 2 số cuối của năm + tháng + ngày + giờ + phút + giây
        mabuoihoc = "BH" + datetime.datetime.now().strftime("%y%m%d%H%M%S")
        
        # Lấy mã giảng viên từ dữ liệu ngầm của Combobox
        magv = self.cmbTenGV.currentData() 
        
        if not magv:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Chưa có thông tin giảng viên!")
            return
            
        ngay = self.dateNgay.date().toString("yyyy-MM-dd")
        giobd = self.timeBatDau.time().toString("HH:mm")
        giokt = self.timeKetThuc.time().toString("HH:mm")

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Câu lệnh INSERT vẫn giữ đủ 5 cột vì mã buổi học đã được Python tự tạo
            query = """INSERT INTO buoihoc (mabuoihoc, giobatdau, gioketthuc, ngay, magiangvien) 
                       VALUES (?, ?, ?, ?, ?)"""
            
            cursor.execute(query, (mabuoihoc, giobd, giokt, ngay, magv))
            conn.commit()
            conn.close()
            
            QtWidgets.QMessageBox.information(self, "Thành công", f"Đã lưu buổi học!\nMã tự động: {mabuoihoc}")
            self.close()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi Database", f"Chi tiết: {str(e)}")