class Controller:
    def __init__(this, perpustakaan, view):
        this.perpustakaan = perpustakaan
        this.view = view
        this.user_logged_in = None  

    def login(this):
        nim = this.view.input_nim()
        anggota = this.perpustakaan.get_anggota_by_id(int(nim))
        if anggota:
            this.user_logged_in = anggota
            this.view.tampilkan_pesan(f"Selamat datang, {anggota.nama}!")
        else:
            this.view.tampilkan_pesan("NIM tidak ditemukan.")

    def tampilkan_buku_dipinjam(this):
        pinjaman = this.user_logged_in.get_pinjaman()
        if not pinjaman:
            this.view.tampilkan_pesan("Anda belum meminjam buku apapun.")
        else:
            this.view.tampilkan_pesan("Buku yang sedang Anda pinjam:")
            for buku in pinjaman:
                this.view.tampilkan_pesan(buku.tampilkan_info())

    def pinjam_buku(this):
        # Filter buku yang tersedia
        buku_tersedia = [b for b in this.perpustakaan.tampilkan_semua_buku()
        if this.perpustakaan.get_buku_by_id(int(b.split(",")[0].split(":")[1].strip())).is_tersedia()]

        if not buku_tersedia:
            this.view.tampilkan_pesan("Maaf, tidak ada buku yang tersedia saat ini.")
            return

        # Tampilkan daftar buku tersedia
        this.view.tampilkan_pesan("Daftar buku tersedia:")
        this.view.tampilkan_list(buku_tersedia)

        # Input ID buku
        id_buku = int(this.view.input_data("Masukkan ID buku yang ingin dipinjam: "))
        buku = this.perpustakaan.get_buku_by_id(id_buku)
        if not buku:
            this.view.tampilkan_pesan("Buku tidak ditemukan.")
            return

        # Konfirmasi
        this.view.tampilkan_pesan("\nDetail Buku:")
        this.view.tampilkan_pesan(buku.tampilkan_info())
        konfirmasi = this.view.input_data("Apakah Anda yakin ingin meminjam buku ini? (y/n): ").lower()

        if konfirmasi == "y":
            sukses, pesan = this.perpustakaan.pinjam_buku(this.user_logged_in, buku)
            this.view.tampilkan_pesan(pesan)
        else:
            this.view.tampilkan_pesan("Peminjaman dibatalkan.")

    def kembalikan_buku(this):
        id_buku = int(this.view.input_data("Masukkan ID buku yang dikembalikan: "))
        buku = this.perpustakaan.get_buku_by_id(id_buku)
        if buku:
            hari_terlambat = int(this.view.input_data("Hari terlambat: "))
            sukses, pesan = this.perpustakaan.kembalikan_buku(this.user_logged_in, buku, hari_terlambat)
            this.view.tampilkan_pesan(pesan)
        else:
            this.view.tampilkan_pesan("Buku tidak ditemukan.")

    def tampilkan_buku(this):
        buku_list = this.perpustakaan.tampilkan_semua_buku()
        this.view.tampilkan_list(buku_list)
