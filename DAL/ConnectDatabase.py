import os
import re
import pyodbc  # Thay thế sqlite3 bằng pyodbc

class CursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        query = self._rewrite_query(query, params)
        if params is None:
            return self.cursor.execute(query)
        
        # Đảm bảo params truyền vào pyodbc phải là dạng tuple/list
        if params is not None and not isinstance(params, (tuple, list)):
            params = (params,)
            
        return self.cursor.execute(query, params)

    def executemany(self, query, params_seq):
        query = self._rewrite_query(query, params_seq)
        return self.cursor.executemany(query, params_seq)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size=10):
        return self.cursor.fetchmany(size)

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        return self.cursor.close()

    def __iter__(self):
        return iter(self.cursor)

    def __getattr__(self, name):
        return getattr(self.cursor, name)

    def _rewrite_query(self, query, params):
        if params is None:
            return query
        # SQL Server sử dụng dấu '?' làm tham số giống SQLite, 
        # hàm này giữ lại phòng trường hợp code cũ của bạn dùng '%s'
        return query.replace('%s', '?')


class ConnectionWrapper:
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return CursorWrapper(self.conn.cursor())

    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()

    def __getattr__(self, name):
        return getattr(self.conn, name)


class ConnectDatabase:
    def __init__(self):
        # Thông tin cấu hình lấy từ ảnh SSMS của bạn
        self.server = 'localhost'
        self.database = 'quanlysinhvien'
        self.username = 'sa'
        self.password = '123456'

    def Connect(self):
        try:
            # Chuỗi kết nối cấu hình chuẩn theo ảnh cấu hình của bạn:
            # - Sử dụng Driver mã nguồn SQL Server công nghiệp
            # - Encrypt=yes & TrustServerCertificate=yes tương ứng mục Encryption: Mandatory trong ảnh
            conn_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
            )
            
            conn = pyodbc.connect(conn_string)
            return ConnectionWrapper(conn)
            
        except pyodbc.Error as e:
            # Nếu máy bạn cài bản Driver đời mới hơn (bản 18), thử tự động fallback sang Driver 18
            try:
                conn_string_v18 = conn_string.replace("ODBC Driver 17", "ODBC Driver 18")
                conn = pyodbc.connect(conn_string_v18)
                return ConnectionWrapper(conn)
            except Exception:
                print('Lỗi kết nối SQL Server!', e)
                return None
        except Exception as ex:
            print('Lỗi hệ thống khi kết nối!', ex)
            return None
        # Dán đoạn này vào CUỐI CÙNG file kết nối database của bạn
if __name__ == "__main__":
    print("=== ĐANG TIẾN HÀNH KIỂM TRA KẾT NỐI SQL SERVER ===")
    
    # Khởi tạo đối tượng kết nối
    db = ConnectDatabase()
    connection = db.Connect()
    
    if connection is not None:
        print("\n🎉 THÀNH CÔNG: Python đã kết nối tới SQL Server thành công!")
        
        # Chạy thử 1 lệnh truy vấn hệ thống để lấy phiên bản SQL Server
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()
            print("\n[Thông tin hệ thống]:")
            print(version[0])
            cursor.close()
        except Exception as e:
            print("⚠️ Kết nối được nhưng lệnh truy vấn thử nghiệm bị lỗi:", e)
            
        finally:
            connection.close()
            print("\n=== ĐÃ ĐÓNG KẾT NỐI AN TOÀN ===")
    else:
        print("\n❌ THẤT BẠI: Không thể kết nối tới SQL Server.")
        print("Vui lòng kiểm tra lại trạng thái Service của SQL Server hoặc tài khoản sa.")