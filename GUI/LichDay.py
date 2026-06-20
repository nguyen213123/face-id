import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui

# Đảm bảo import đúng đường dẫn
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from DAL.ConnectDatabase import ConnectDatabase

class UI_LichDay(QtWidgets.QDialog):
    def __init__(self, email_gv):
        super().__init__()
        print(f"DEBUG: Email nhận được từ form Login là: '{email_gv}'")
        self.email_gv = email_gv
        self.db = ConnectDatabase()
        self.setWindowTitle("Lịch Dạy & Quản Lý Sinh Viên")
        self.setFixedSize(900, 600)
        self.magiangvien = self.get_magiangvien_by_email()
        print(f"DEBUG: Mã giảng viên lấy được từ DB là: {self.magiangvien}")
        
        self.setup_ui()
        self.load_lich_day()

    def get_magiangvien_by_email(self):
        conn = self.db.Connect()
        try:
            cursor = conn.cursor()
            # Thay đổi câu lệnh truy vấn để so sánh với mataikhoan thay vì email
            cursor.execute("""
                SELECT g.magiangvien FROM giangvien g
                JOIN taikhoan t ON g.mataikhoan = t.mataikhoan
                WHERE t.mataikhoan = ?
            """, (self.email_gv,)) # Đảm bảo self.email_gv đang chứa giá trị '1'
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()
            
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        
        # Danh sách buổi học
        self.tableLich = QtWidgets.QTableWidget()
        self.tableLich.setColumnCount(4)
        self.tableLich.setHorizontalHeaderLabels(["Mã Buổi", "Ngày", "Giờ BĐ", "Giờ KT"])
        self.tableLich.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableLich.clicked.connect(self.load_sinhvien_trong_lop)
        layout.addWidget(QtWidgets.QLabel("Danh sách buổi dạy của bạn:"))
        layout.addWidget(self.tableLich)

        # Khu vực thêm sinh viên
        add_layout = QtWidgets.QHBoxLayout()
        self.txtMaSV = QtWidgets.QLineEdit()
        self.txtMaSV.setPlaceholderText("Nhập Mã SV cần thêm...")
        btnThem = QtWidgets.QPushButton("Thêm vào lớp")
        btnThem.clicked.connect(self.add_student_to_class)
        add_layout.addWidget(self.txtMaSV)
        add_layout.addWidget(btnThem)
        layout.addLayout(add_layout)

        # Danh sách SV trong lớp
        self.tableSV = QtWidgets.QTableWidget()
        self.tableSV.setColumnCount(2)
        self.tableSV.setHorizontalHeaderLabels(["Mã SV", "Họ Tên"])
        layout.addWidget(QtWidgets.QLabel("Sinh viên trong lớp:"))
        layout.addWidget(self.tableSV)
        
        self.setLayout(layout)

    def load_lich_day(self):
        self.tableLich.setRowCount(0)
        if not self.magiangvien: return
        conn = self.db.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT mabuoihoc, ngay, giobatdau, gioketthuc FROM buoihoc WHERE magiangvien = ?", (self.magiangvien,))
        for row_idx, row in enumerate(cursor.fetchall()):
            self.tableLich.insertRow(row_idx)
            for col_idx, data in enumerate(row):
                self.tableLich.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()

    def load_sinhvien_trong_lop(self):
        row = self.tableLich.currentRow()
        mabuoihoc = self.tableLich.item(row, 0).text()
        self.tableSV.setRowCount(0)
        conn = self.db.Connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.masinhvien, s.hoten FROM sinhvien s
            JOIN ChiTietBuoiHoc ct ON s.masinhvien = ct.masinhvien
            WHERE ct.mabuoihoc = ?
        """, (mabuoihoc,))
        for row_idx, row in enumerate(cursor.fetchall()):
            self.tableSV.insertRow(row_idx)
            self.tableSV.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableSV.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(row[1]))
        conn.close()

    def add_student_to_class(self):
        row = self.tableLich.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một buổi học!")
            return
        mabuoihoc = self.tableLich.item(row, 0).text()
        masv = self.txtMaSV.text().strip()
        
        if not masv: return
        
        conn = self.db.Connect()
        try:
            cursor = conn.cursor()
            # Kiểm tra xem SV có tồn tại không
            cursor.execute("SELECT masinhvien FROM sinhvien WHERE masinhvien = ?", (masv,))
            if not cursor.fetchone():
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Không tìm thấy sinh viên!")
                return
            
            # Thêm vào bảng trung gian
            cursor.execute("INSERT INTO ChiTietBuoiHoc (mabuoihoc, masinhvien) VALUES (?, ?)", (mabuoihoc, masv))
            conn.commit()
            QtWidgets.QMessageBox.information(self, "Thành công", "Đã thêm sinh viên!")
            self.load_sinhvien_trong_lop()
            self.txtMaSV.clear()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Sinh viên đã có trong lớp hoặc có lỗi xảy ra.")
        finally:
            conn.close()