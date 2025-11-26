class Buku:
    def __init__(this, id_buku, judul, pengarang, tahun_terbit, tersedia=True):
        this.id_buku = id_buku
        this.judul = judul
        this.pengarang = pengarang
        this.tahun_terbit = tahun_terbit
        this.__tersedia = tersedia  # true = tersedia, false = dipinjam

    # Tampilkan info buku
    def tampilkan_info(this):
        status = "Tersedia" if this.__tersedia else "Dipinjam"
        return f"ID Buku: {this.id_buku}, Judul: {this.judul}, Pengarang: {this.pengarang}, Tahun Terbit: {this.tahun_terbit}, Status: {status}"

    # Getter & Setter
    def is_tersedia(this):
        return this.__tersedia

    def set_tersedia(this, value: bool):
        this.__tersedia = value

    # Hitung denda
    def hitung_denda(this, hari_terlambat):
        denda_per_hari = 2000 
        return hari_terlambat * denda_per_hari


class BukuReferensi(Buku):
    def hitung_denda(this, hari_terlambat):
        denda_per_hari = 5000
        return hari_terlambat * denda_per_hari
