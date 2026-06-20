import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui

# =========================================================
# XỬ LÝ ĐƯỜNG DẪN ĐỂ IMPORT DATABASE TỪ THƯ MỤC DAL
# =========================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from DAL.ConnectDatabase import ConnectDatabase 

class UI_QuanLyChung(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Hệ Thống Toàn Diện")
        self.setFixedSize(1100, 650)
        
        self.db = ConnectDatabase()
        
        main_layout = QtWidgets.QVBoxLayout()
        
        lblTitle = QtWidgets.QLabel("HỆ THỐNG QUẢN LÝ DỮ LIỆU")
        lblTitle.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
        lblTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lblTitle.setStyleSheet("margin-bottom: 10px;")
        main_layout.addWidget(lblTitle)
        
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setFont(QtGui.QFont("Arial", 11))
        
        self.tab_sv = QtWidgets.QWidget()
        self.tab_gv = QtWidgets.QWidget()
        self.tab_bh = QtWidgets.QWidget()
        
        self.setup_tab_sinhvien()
        self.setup_tab_giangvien()
        self.setup_tab_buoihoc()
        
        self.tabs.addTab(self.tab_sv, "👨‍🎓 Quản Lý Sinh Viên")
        self.tabs.addTab(self.tab_gv, "👨‍🏫 Quản Lý Giảng Viên")
        self.tabs.addTab(self.tab_bh, "📚 Quản Lý Buổi Học")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    # =========================================================
    # TAB 1: QUẢN LÝ SINH VIÊN
    # =========================================================
    def setup_tab_sinhvien(self):
        layout = QtWidgets.QVBoxLayout()
        
        toolbar = QtWidgets.QHBoxLayout()
        btnTaiLai = QtWidgets.QPushButton("🔄 Tải lại danh sách")
        btnTaiLai.clicked.connect(self.load_data_sinhvien)
        
        # Nút Sửa
        btnSua = QtWidgets.QPushButton("✏️ Sửa Sinh Viên")
        btnSua.clicked.connect(self.edit_sinhvien)
        btnSua.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        # Nút Xóa
        btnXoa = QtWidgets.QPushButton("❌ Xóa Sinh Viên")
        btnXoa.clicked.connect(self.delete_sinhvien)
        btnXoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        toolbar.addWidget(btnTaiLai)
        toolbar.addWidget(btnSua)
        toolbar.addWidget(btnXoa)
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        self.tableSV = QtWidgets.QTableWidget()
        self.tableSV.setColumnCount(8)
        self.tableSV.setHorizontalHeaderLabels([
            "Mã SV", "Họ Tên", "CMND/CCCD", "Giới Tính", "Ngày Sinh", "Email", "SĐT", "Khóa Học"
        ])
        self.tableSV.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableSV.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers) # Chặn sửa trực tiếp trên bảng
        self.tableSV.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tableSV)
        
        self.tab_sv.setLayout(layout)
        self.load_data_sinhvien()

    def load_data_sinhvien(self):
        self.tableSV.setRowCount(0)
        conn = self.db.Connect()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT masinhvien, hoten, cmnd, gioitinh, ngaysinh, email, sodienthoai, khoahoc FROM sinhvien")
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.tableSV.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.tableSV.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(data if data is not None else "")))
        except Exception as e:
            print("Lỗi tải sinh viên:", e)
        finally:
            conn.close()

    def edit_sinhvien(self):
        row = self.tableSV.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một sinh viên để sửa!")
            return
            
        masv = self.tableSV.item(row, 0).text()
        hoten = self.tableSV.item(row, 1).text()
        
        # TODO: Chỗ này bạn sẽ gọi form SuaSinhVien của bạn lên và truyền `masv` sang
        QtWidgets.QMessageBox.information(self, "Thông báo", f"Bạn đang chọn sửa sinh viên:\n- Mã: {masv}\n- Tên: {hoten}\n\n(Hãy thay dòng này bằng code mở Form Sửa của bạn)")
        # Ví dụ: 
        # dialog = SuaSinhVien.UI_SuaSinhVien(masv)
        # dialog.exec()
        # self.load_data_sinhvien()

    def delete_sinhvien(self):
        row = self.tableSV.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một sinh viên để xóa!")
            return
            
        masv = self.tableSV.item(row, 0).text()
        hoten = self.tableSV.item(row, 1).text()
        
        reply = QtWidgets.QMessageBox.question(
            self, 'Xác nhận', f'Bạn có chắc muốn xóa sinh viên: {hoten} ({masv})?',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = self.db.Connect()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sinhvien WHERE masinhvien = ?", (masv,))
                conn.commit()
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã xóa sinh viên!")
                self.load_data_sinhvien()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể xóa.\nChi tiết: {e}")
            finally:
                if conn: conn.close()

    # =========================================================
    # TAB 2: QUẢN LÝ GIẢNG VIÊN
    # =========================================================
    def setup_tab_giangvien(self):
        layout = QtWidgets.QVBoxLayout()
        
        toolbar = QtWidgets.QHBoxLayout()
        btnTaiLai = QtWidgets.QPushButton("🔄 Tải lại danh sách")
        btnTaiLai.clicked.connect(self.load_data_giangvien)
        
        btnSua = QtWidgets.QPushButton("✏️ Sửa Giảng Viên")
        btnSua.clicked.connect(self.edit_giangvien)
        btnSua.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        btnXoa = QtWidgets.QPushButton("❌ Xóa Giảng Viên")
        btnXoa.clicked.connect(self.delete_giangvien)
        btnXoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        toolbar.addWidget(btnTaiLai)
        toolbar.addWidget(btnSua)
        toolbar.addWidget(btnXoa)
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        self.tableGV = QtWidgets.QTableWidget()
        self.tableGV.setColumnCount(4)
        self.tableGV.setHorizontalHeaderLabels(["Mã Giảng Viên", "Họ Tên", "Số Điện Thoại", "Mã Tài Khoản"])
        self.tableGV.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableGV.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableGV.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tableGV)
        
        self.tab_gv.setLayout(layout)
        self.load_data_giangvien()

    def load_data_giangvien(self):
        self.tableGV.setRowCount(0)
        conn = self.db.Connect()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT magiangvien, hoten, sodienthoai, mataikhoan FROM giangvien")
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.tableGV.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.tableGV.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(data if data is not None else "")))
        except Exception as e:
            print("Lỗi tải giảng viên:", e)
        finally:
            conn.close()

    def edit_giangvien(self):
        row = self.tableGV.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một giảng viên để sửa!")
            return
        magv = self.tableGV.item(row, 0).text()
        
        # TODO: Gọi form Sửa Giảng Viên
        QtWidgets.QMessageBox.information(self, "Thông báo", f"Bạn đang chọn sửa Giảng viên mã: {magv}")

    def delete_giangvien(self):
        row = self.tableGV.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một giảng viên để xóa!")
            return
            
        magv = self.tableGV.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, 'Xác nhận', f'Bạn có chắc muốn xóa giảng viên ({magv})?',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = self.db.Connect()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM giangvien WHERE magiangvien = ?", (magv,))
                conn.commit()
                self.load_data_giangvien()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể xóa giảng viên.\nChi tiết: {e}")
            finally:
                if conn: conn.close()

    # =========================================================
    # TAB 3: QUẢN LÝ BUỔI HỌC
    # =========================================================
    def setup_tab_buoihoc(self):
        layout = QtWidgets.QVBoxLayout()
        
        toolbar = QtWidgets.QHBoxLayout()
        btnTaiLai = QtWidgets.QPushButton("🔄 Tải lại danh sách")
        btnTaiLai.clicked.connect(self.load_data_buoihoc)
        
        btnSua = QtWidgets.QPushButton("✏️ Sửa Buổi Học")
        btnSua.clicked.connect(self.edit_buoihoc)
        btnSua.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        btnXoa = QtWidgets.QPushButton("❌ Xóa Buổi Học")
        btnXoa.clicked.connect(self.delete_buoihoc)
        btnXoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        toolbar.addWidget(btnTaiLai)
        toolbar.addWidget(btnSua)
        toolbar.addWidget(btnXoa)
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        self.tableBH = QtWidgets.QTableWidget()
        self.tableBH.setColumnCount(5)
        self.tableBH.setHorizontalHeaderLabels(["Mã Buổi Học", "Giờ Bắt Đầu", "Giờ Kết Thúc", "Ngày", "Mã Giảng Viên"])
        self.tableBH.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableBH.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableBH.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tableBH)
        
        self.tab_bh.setLayout(layout)
        self.load_data_buoihoc()

    def load_data_buoihoc(self):
        self.tableBH.setRowCount(0)
        conn = self.db.Connect()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT mabuoihoc, giobatdau, gioketthuc, ngay, magiangvien FROM buoihoc")
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.tableBH.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.tableBH.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(data if data is not None else "")))
        except Exception as e:
            print("Lỗi tải buổi học:", e)
        finally:
            conn.close()

    def edit_buoihoc(self):
        row = self.tableBH.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một buổi học để sửa!")
            return
        mabh = self.tableBH.item(row, 0).text()
        
        # TODO: Gọi form Sửa Buổi Học
        QtWidgets.QMessageBox.information(self, "Thông báo", f"Bạn đang chọn sửa Buổi học mã: {mabh}")

    def delete_buoihoc(self):
        row = self.tableBH.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một buổi học để xóa!")
            return
            
        mabh = self.tableBH.item(row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self, 'Xác nhận', f'Bạn có chắc muốn xóa buổi học ({mabh})?',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = self.db.Connect()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM buoihoc WHERE mabuoihoc = ?", (mabh,))
                conn.commit()
                self.load_data_buoihoc()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể xóa buổi học.\nChi tiết: {e}")
            finally:
                if conn: conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI_QuanLyChung()
    window.show()
    sys.exit(app.exec())