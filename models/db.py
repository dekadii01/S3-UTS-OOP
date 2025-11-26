import mysql.connector

class Database:
    def __init__(this):
        try:
            this.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_perpus_oop"
            )

            this.cursor = this.conn.cursor(dictionary=True)

        except mysql.connector.Error as e:
            print("[DATABASE ERROR]", e)
            this.conn = None
            this.cursor = None

    def execute(this, sql, params=None):
        """Menjalankan query INSERT, UPDATE, DELETE"""
        if this.cursor is None:
            print("❌ Tidak dapat execute, koneksi tidak tersedia")
            return False

        try:
            this.cursor.execute(sql, params)
            this.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("[QUERY ERROR]", e)
            return False

    def fetch_all(this, sql, params=None):
        """Mengambil banyak data (SELECT)"""
        if this.cursor is None:
            print("❌ Tidak dapat fetch_all, koneksi tidak tersedia")
            return []

        try:
            this.cursor.execute(sql, params)
            return this.cursor.fetchall()
        except mysql.connector.Error as e:
            print("[FETCH ERROR]", e)
            return []

    def fetch_one(this, sql, params=None):
        """Mengambil satu data (SELECT LIMIT 1)"""
        if this.cursor is None:
            print("❌ Tidak dapat fetch_one, koneksi tidak tersedia")
            return None

        try:
            this.cursor.execute(sql, params)
            return this.cursor.fetchone()
        except mysql.connector.Error as e:
            print("[FETCH ERROR]", e)
            return None

    def close(this):
        if this.cursor:
            this.cursor.close()
        if this.conn:
            this.conn.close()
