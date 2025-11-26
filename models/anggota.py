from .db import Database

class Anggota:
    def __init__(this, id_anggota, nama, alamat):
        this.id_anggota = id_anggota
        this.nama = nama
        this.alamat = alamat
        this.__pinjaman = []  # list buku yang dipinjam (Encapsulation)
        this.db = Database()

    def save(this):
        sql = "INSERT INTO anggota (id_anggota, nama, alamat) VALUES (%s, %s, %s)"
        this.db.cursor.execute(sql, (this.id_anggota, this.nama, this.alamat))
        this.db.commit()

    def tampilkan_info(this):
        return f"ID Anggota: {this.id_anggota}, Nama: {this.nama}, Alamat: {this.alamat}"

    def tambah_pinjaman(this, buku):
        this.__pinjaman.append(buku)

    def hapus_pinjaman(this, buku):
        if buku in this.__pinjaman:
            this.__pinjaman.remove(buku)

    def get_anggota(this):
        sql = "SELECT * FROM anggota"
        rows = this.db.fetch_all(sql)
        

    def get_pinjaman(this):
        return this.__pinjaman