from PyQt6 import QtWidgets, QtCore
import pyodbc

class UI_ThemGiangVien(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thêm Giảng Viên Mới")
        self.setFixedSize(400, 450)
        
        layout = QtWidgets.QVBoxLayout()
        
        # Nhập liệu
        self.txtHoTen = QtWidgets.QLineEdit()
        self.txtHoTen.setPlaceholderText("Họ và tên giảng viên")
        
        self.txtSDT = QtWidgets.QLineEdit()
        self.txtSDT.setPlaceholderText("Số điện thoại")
        
        self.txtEmail = QtWidgets.QLineEdit()
        self.txtEmail.setPlaceholderText("Email (Dùng làm tài khoản)")
        
        self.txtMatKhau = QtWidgets.QLineEdit()
        self.txtMatKhau.setPlaceholderText("Mật khẩu")
        self.txtMatKhau.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        self.btnLuu = QtWidgets.QPushButton("Lưu giảng viên")
        self.btnLuu.clicked.connect(self.save_to_db)
        
        layout.addWidget(QtWidgets.QLabel("Họ tên:"))
        layout.addWidget(self.txtHoTen)
        layout.addWidget(QtWidgets.QLabel("Số điện thoại:"))
        layout.addWidget(self.txtSDT)
        layout.addWidget(QtWidgets.QLabel("Email:"))
        layout.addWidget(self.txtEmail)
        layout.addWidget(QtWidgets.QLabel("Mật khẩu:"))
        layout.addWidget(self.txtMatKhau)
        layout.addWidget(self.btnLuu)
        
        self.setLayout(layout)

    def save_to_db(self):
        email = self.txtEmail.text().strip()
        hoten = self.txtHoTen.text().strip()
        matkhau = self.txtMatKhau.text().strip()

        # 1. Kiểm tra để trống
        if not email or not hoten or not matkhau:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # 2. Kiểm tra định dạng @gmail.com
        if not email.endswith("@gmail.com"):
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Email không hợp lệ! Vui lòng nhập đúng định dạng @gmail.com")
            return

        try:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-CGVDUCU;DATABASE=quanlysinhvien;Trusted_Connection=yes;')
            cursor = conn.cursor()

            # 3. Kiểm tra trùng email trong database
            cursor.execute("SELECT COUNT(*) FROM taikhoan WHERE email = ?", (email,))
            count = cursor.fetchone()[0]
            if count > 0:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Email này đã tồn tại trong hệ thống!")
                cursor.close()
                conn.close()
                return

            # 4. Tiếp tục thực hiện INSERT nếu dữ liệu hợp lệ
            cursor.execute("SELECT ISNULL(MAX(mataikhoan), 0) + 1 FROM taikhoan")
            new_id = cursor.fetchone()[0]
            
            # Insert tài khoản
            sql_tk = "INSERT INTO taikhoan (mataikhoan, email, matkhau, maquyen) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_tk, (new_id, email, matkhau, "GV"))
            
            # Insert giảng viên
            magv = "GV" + str(new_id)
            sql_gv = "INSERT INTO giangvien (magiangvien, hoten, sodienthoai, mataikhoan) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_gv, (magv, hoten, self.txtSDT.text().strip(), new_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            QtWidgets.QMessageBox.information(self, "Thành công", "Đã thêm giảng viên thành công!")
            self.close()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi Database", f"Chi tiết: {str(e)}")