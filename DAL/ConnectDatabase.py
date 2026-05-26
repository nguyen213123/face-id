import os
import re
import sqlite3

class CursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        query = self._rewrite_query(query, params)
        if params is None:
            return self.cursor.execute(query)
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
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'quanlysinhvien.db'))
        self.schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db_schema.sql'))

    def Connect(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            conn.execute('PRAGMA foreign_keys = ON')
            self._ensure_schema(conn)
            return ConnectionWrapper(conn)
        except Exception as ex:
            print('Error connect!', ex)
            return None

    def _ensure_schema(self, conn):
        if not os.path.exists(self.schema_path):
            return

        with open(self.schema_path, 'r', encoding='utf-8') as f:
            script = f.read()

        script = self._normalize_schema(script)
        try:
            conn.executescript(script)
        except Exception as ex:
            print('Schema initialization error:', ex)

    def _normalize_schema(self, script):
        script = re.sub(r"(?mi)CREATE DATABASE .*?;", "", script)
        script = re.sub(r"(?mi)USE .*?;", "", script)
        script = re.sub(r"(?mi)INSERT IGNORE INTO", "INSERT OR IGNORE INTO", script)
        script = re.sub(r"(?mi)UNIQUE KEY\s+`?\w+`?\s*\(([^)]+)\)", r"UNIQUE (\1)", script)
        script = re.sub(r"(?mi)ENGINE=\w+\s*DEFAULT CHARSET=[^;]+;", ";", script)
        script = re.sub(r"(?mi)CHARACTER SET\s*=\s*\w+\s*COLLATE\s*=\s*\w+", "", script)
        return script