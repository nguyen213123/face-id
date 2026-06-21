import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui

# Đảm bảo import đúng đường dẫn
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from DAL.ConnectDatabase import ConnectDatabase

class UI_QuanLyDiemDanh(object):
    def __init__(self, email_gv=None):
        self.email_gv = email_gv
        self.db = ConnectDatabase()
        self.magiangvien = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        # Tiêu đề
        self.lblTitle = QtWidgets.QLabel("QUẢN LÝ ĐIỂM DANH SINH VIÊN")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.lblTitle)

        # Chọn buổi học
        self.topLayout = QtWidgets.QHBoxLayout()
        self.lblBuoiHoc = QtWidgets.QLabel("Chọn buổi học của bạn:")
        self.cboBuoiHoc = QtWidgets.QComboBox()
        self.cboBuoiHoc.setMinimumWidth(300)
        self.cboBuoiHoc.currentIndexChanged.connect(self.load_sinhvien_diemdanh)
        
        self.topLayout.addWidget(self.lblBuoiHoc)
        self.topLayout.addWidget(self.cboBuoiHoc)
        self.topLayout.addStretch()
        self.mainLayout.addLayout(self.topLayout)

        # ================= Thêm Khu Vực Thống Kê =================
        self.statsLayout = QtWidgets.QHBoxLayout()
        
        font_stat = QtGui.QFont()
        font_stat.setPointSize(11)
        font_stat.setBold(True)

        self.lblTongSV = QtWidgets.QLabel("Tổng số SV: 0")
        self.lblTongSV.setFont(font_stat)
        self.lblTongSV.setStyleSheet("color: #0078D7;") # Màu xanh dương

        self.lblCoMat = QtWidgets.QLabel("Đã điểm danh (Có mặt/Muộn): 0")
        self.lblCoMat.setFont(font_stat)
        self.lblCoMat.setStyleSheet("color: #107C10;") # Màu xanh lá

        self.lblVang = QtWidgets.QLabel("Vắng mặt: 0")
        self.lblVang.setFont(font_stat)
        self.lblVang.setStyleSheet("color: #D83B01;") # Màu cam/đỏ

        self.lblChuaDD = QtWidgets.QLabel("Chưa điểm danh: 0")
        self.lblChuaDD.setFont(font_stat)
        self.lblChuaDD.setStyleSheet("color: #888888;") # Màu xám

        self.statsLayout.addWidget(self.lblTongSV)
        self.statsLayout.addWidget(self.lblCoMat)
        self.statsLayout.addWidget(self.lblVang)
        self.statsLayout.addWidget(self.lblChuaDD)
        self.statsLayout.addStretch()
        
        self.mainLayout.addLayout(self.statsLayout)
        # =========================================================

        # Bảng danh sách sinh viên
        self.tableDiemDanh = QtWidgets.QTableWidget()
        self.tableDiemDanh.setColumnCount(4)
        self.tableDiemDanh.setHorizontalHeaderLabels(["Mã SV", "Họ Tên", "Trạng Thái", "Ghi Chú"])
        self.tableDiemDanh.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.mainLayout.addWidget(self.tableDiemDanh)

        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.btnLuu = QtWidgets.QPushButton("Lưu Điểm Danh")
        self.btnLuu.setMinimumHeight(35)
        self.btnLuu.setStyleSheet("background-color: #0078D7; color: white; font-weight: bold;")
        self.btnLuu.clicked.connect(self.luu_diem_danh)
        
        self.btnBack = QtWidgets.QPushButton("Trở Về")
        self.btnBack.setMinimumHeight(35)
        
        self.btnMinimize = QtWidgets.QPushButton("Thu Nhỏ")
        self.btnMinimize.setMinimumHeight(35)
        
        # Tạo nút X (Thoát)
        self.btnX = QtWidgets.QPushButton("X")
        self.btnX.setMinimumHeight(35)
        self.btnX.setFixedWidth(50)
        self.btnX.setStyleSheet("background-color: #e81123; color: white; font-weight: bold; border-radius: 5px;")

        self.bottomLayout.addWidget(self.btnLuu)
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.btnMinimize)
        self.bottomLayout.addWidget(self.btnX) # Đã thay btnClose bằng btnX
        self.bottomLayout.addWidget(self.btnBack)
        
        self.mainLayout.addLayout(self.bottomLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        # Load dữ liệu ban đầu
        self.get_magiangvien()
        self.load_cbo_buoihoc()

    def get_magiangvien(self):
        if not self.email_gv: return
        conn = self.db.Connect()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT g.magiangvien FROM giangvien g
                JOIN taikhoan t ON g.mataikhoan = t.mataikhoan
                WHERE t.mataikhoan = ? OR t.email = ?
            """, (self.email_gv, self.email_gv))
            row = cursor.fetchone()
            if row: self.magiangvien = row[0]
        finally:
            conn.close()

    def load_cbo_buoihoc(self):
        self.cboBuoiHoc.blockSignals(True) # Chặn signal để tránh lỗi khi đang clear
        self.cboBuoiHoc.clear()
        conn = self.db.Connect()
        try:
            cursor = conn.cursor()
            if self.magiangvien:
                cursor.execute("SELECT mabuoihoc, ngay, giobatdau FROM buoihoc WHERE magiangvien = ?", (self.magiangvien,))
            else:
                cursor.execute("SELECT mabuoihoc, ngay, giobatdau FROM buoihoc")
            
            for row in cursor.fetchall():
                display_text = f"Mã: {str(row[0])} - Ngày: {str(row[1])} ({str(row[2])})"
                self.cboBuoiHoc.addItem(display_text, str(row[0]))
        finally:
            conn.close()
            self.cboBuoiHoc.blockSignals(False)
            self.load_sinhvien_diemdanh() # Tự động load danh sách cho buổi học đầu tiên

    def load_sinhvien_diemdanh(self):
        self.tableDiemDanh.setRowCount(0)
        mabuoihoc = self.cboBuoiHoc.currentData()
        if not mabuoihoc: 
            self.cap_nhat_thong_ke()
            return

        conn = self.db.Connect()
        try:
            cursor = conn.cursor()
            # Dùng LEFT JOIN với bảng DiemDanh để xem sinh viên nào đã được điểm danh trước đó chưa
            # LƯU Ý: Giả sử bảng của bạn tên là 'DiemDanh', nếu tên khác bạn hãy đổi lại nhé
            cursor.execute("""
                SELECT s.masinhvien, s.hoten, d.trangthai, d.ghichu 
                FROM sinhvien s
                JOIN ChiTietBuoiHoc ct ON s.masinhvien = ct.masinhvien
                LEFT JOIN DiemDanh d ON ct.mabuoihoc = d.mabuoihoc AND ct.masinhvien = d.masinhvien
                WHERE ct.mabuoihoc = ?
            """, (mabuoihoc,))
            
            for row_idx, row in enumerate(cursor.fetchall()):
                self.tableDiemDanh.insertRow(row_idx)
                
                # Mã SV & Họ tên
                self.tableDiemDanh.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                self.tableDiemDanh.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                
                # Cột Trạng thái
                cboTrangThai = QtWidgets.QComboBox()
                cboTrangThai.addItems(["Chưa điểm danh", "Có mặt", "Vắng", "Đi muộn"])
                
                # Lấy trạng thái từ DB, nếu None thì gán là "Chưa điểm danh"
                trangthai_db = row[2] if row[2] else "Chưa điểm danh"
                cboTrangThai.setCurrentText(trangthai_db)
                
                # Kết nối sự kiện để khi GV đổi trạng thái -> Số liệu thống kê tự nhảy
                cboTrangThai.currentTextChanged.connect(self.cap_nhat_thong_ke)
                self.tableDiemDanh.setCellWidget(row_idx, 2, cboTrangThai)
                
                # Ghi chú
                ghichu_db = row[3] if row[3] else ""
                self.tableDiemDanh.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(ghichu_db))
                
        except Exception as e:
            print("Lỗi load danh sách sinh viên:", e)
        finally:
            conn.close()
            # Cập nhật con số thống kê ngay sau khi load xong
            self.cap_nhat_thong_ke()

    def cap_nhat_thong_ke(self):
        """Hàm duyệt qua toàn bộ bảng để đếm trạng thái Real-time"""
        tong_sv = self.tableDiemDanh.rowCount()
        co_mat = 0
        vang = 0
        chua_dd = 0

        for row in range(tong_sv):
            cbo = self.tableDiemDanh.cellWidget(row, 2)
            if cbo:
                txt = cbo.currentText()
                if txt in ["Có mặt", "Đi muộn"]:
                    co_mat += 1
                elif txt == "Vắng":
                    vang += 1
                else:
                    chua_dd += 1

        # Hiển thị lên giao diện
        self.lblTongSV.setText(f"Tổng số SV: {tong_sv}")
        self.lblCoMat.setText(f"Đã điểm danh (Có mặt/Muộn): {co_mat}")
        self.lblVang.setText(f"Vắng mặt: {vang}")
        self.lblChuaDD.setText(f"Chưa điểm danh: {chua_dd}")

    def luu_diem_danh(self):
        mabuoihoc = self.cboBuoiHoc.currentData()
        if not mabuoihoc: return
        
        conn = self.db.Connect()
        try:
            cursor = conn.cursor()
            for row in range(self.tableDiemDanh.rowCount()):
                masv = self.tableDiemDanh.item(row, 0).text()
                trangthai = self.tableDiemDanh.cellWidget(row, 2).currentText()
                item_ghichu = self.tableDiemDanh.item(row, 3)
                ghichu = item_ghichu.text() if item_ghichu else ""

                # Thực thi lưu vào database. 
                # Chú ý: Cấu trúc dưới đây dùng MERGE hoặc xóa đi insert lại tùy DB. 
                # Đây là mẫu Delete rồi Insert cho đơn giản và tránh trùng lặp:
                cursor.execute("DELETE FROM DiemDanh WHERE mabuoihoc = ? AND masinhvien = ?", (mabuoihoc, masv))
                cursor.execute("""
                    INSERT INTO DiemDanh (mabuoihoc, masinhvien, trangthai, ghichu) 
                    VALUES (?, ?, ?, ?)
                """, (mabuoihoc, masv, trangthai, ghichu))
            
            conn.commit()
            QtWidgets.QMessageBox.information(None, "Thành công", "Lưu điểm danh thành công!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Lỗi", f"Có lỗi khi lưu vào Database: {str(e)}\n(Hãy kiểm tra lại bảng DiemDanh)")
        finally:
            conn.close()