import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from .TaiKhoan import TaiKhoan
from .ConnectDatabase import ConnectDatabase
import re

class TaiKhoanDAL:

    @staticmethod
    def iter_row(cursor, size=10):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    @staticmethod
    def get():
        res_list = []
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM taikhoan")            
            for row in TaiKhoanDAL.iter_row(cursor, 10):
                res_list.append(row)
        except Exception as e:
            print("Lỗi lấy danh sách tài khoản:", e)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
        return res_list

    @staticmethod
    def generateID():
        ma = ""
        stt = ""
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            # ĐÃ SỬA: Chuyển từ LIMIT 1 (MySQL) sang TOP 1 (SQL Server)
            query = "SELECT TOP 1 mataikhoan FROM taikhoan ORDER BY mataikhoan DESC"
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                stt = "0"
            else:
                stt = str(row[0])
        except Exception as e:
            print("Lỗi tăng id:", e)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            
        stt_num = int(re.sub("[^0-9]", "", stt)) + 1
        ma = "TK{0:03}".format(stt_num)
        return ma

    @staticmethod
    def add(tk: TaiKhoan):
        # ĐÃ SỬA: Chuyển từ %s sang ?
        query = "INSERT INTO taikhoan (mataikhoan, email, matkhau, maquyen) VALUES (?, ?, ?, ?)"
        data = (tk._mataikhoan, tk._email, tk._matkhau, tk._maquyen)   
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            cursor.execute(query, data)         
            conn.commit()
            return True
        except Exception as ex:
            print("Lỗi thêm tài khoản:", ex)
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def update(tk: TaiKhoan):
        # ĐÃ SỬA: Chuyển từ %s sang ?
        query = """ UPDATE taikhoan
                    SET email = ?,
                        maquyen = ?
                    WHERE mataikhoan = ? """
        data = (tk._email, tk._maquyen, tk._mataikhoan)
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return True
        except Exception as ex:
            print("Lỗi cập nhật tài khoản:", ex)
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def delete(id):
        # ĐÃ SỬA: Dùng Parameterized Query để an toàn và đồng bộ SQL Server
        query = "DELETE FROM taikhoan WHERE mataikhoan = ?"
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return True
        except Exception as ex:
            print("Lỗi xóa tài khoản:", ex)
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def find(key, value):
        res_list = []
        if key not in ['mataikhoan', 'email', 'maquyen']:
            key = 'email'
        query = "SELECT * FROM taikhoan WHERE {} LIKE ?".format(key)
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            cursor.execute(query, (f"%{value}%",))
            for row in TaiKhoanDAL.iter_row(cursor, 10):
                res_list.append(row)            
        except Exception as ex:
            print("Lỗi tìm kiếm tài khoản:", ex)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
        return res_list

    @staticmethod
    def checkLogin(email, password):
        db = ConnectDatabase()
        conn = db.Connect()
        if conn is None:
            return False
            
        cursor = None
        try:
            cursor = conn.cursor()
            query = "SELECT mataikhoan, email, maquyen FROM taikhoan WHERE email = ? AND matkhau = ?"
            cursor.execute(query, (email, password))
            row = cursor.fetchone()
            if row:
                return [row[0], row[1], row[2]]
            return False
        except Exception as e:
            print("Lỗi đăng nhập:", e)
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def changePassword(email, mkmoi):
        # ĐÃ SỬA: Chuyển từ %s sang ?
        query = """ UPDATE taikhoan
                    SET matkhau = ?
                    WHERE email = ? """
        data = (mkmoi, email)
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return True
        except Exception as ex:
            print("Lỗi đổi mật khẩu:", ex)
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def checkNotTaiKhoanAmin(mataikhoan):
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            query = "SELECT * FROM taikhoan WHERE mataikhoan = ? AND maquyen = 'Q001'"
            cursor.execute(query, (mataikhoan,))
            row = cursor.fetchone()
            if row is None:
                return True
        except Exception as ex:
            print(ex)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
        return False

    @staticmethod
    def checkEmailTonTai(email):
        cursor = None
        conn = None
        try:
            connDb = ConnectDatabase()
            conn = connDb.Connect()
            cursor = conn.cursor()
            query = "SELECT * FROM taikhoan WHERE email = ?"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row is None:
                return True
        except Exception as ex:
            print(ex)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
        return False