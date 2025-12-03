from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()

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
            return True
        else:
            this.view.tampilkan_pesan("[bold red]NIM tidak ditemukan.[/bold red]")
            return False

    def login_atau_exit(this):
        berhasil = this.login()
        if not berhasil:
            this.view.tampilkan_pesan("[bold red]Login gagal. Program dihentikan.[/bold red]")
            exit()


    def tampilkan_buku_dipinjam(this):
        peminjam = this.user_logged_in.get_pinjaman()
        if not peminjam:
            console.print("[bold yellow]📭 Anda belum meminjam buku apapun.[/bold yellow]")
            return
        
        table = Table(title=f"📚 Buku yang Sedang Dipinjam oleh {this.user_logged_in.nama}", header_style="bold magenta")
        table.add_column("ID Buku", justify="center", style="bold cyan")
        table.add_column("Judul", style="white")
        table.add_column("Penulis", style="white")
        table.add_column("Tahun", justify="center", style="yellow")
        table.add_column("Status", justify="center", style="bold red")

        for buku in peminjam:
            table.add_row(
                str(buku.id_buku),
                buku.judul,
                buku.pengarang,
                str(buku.tahun_terbit),
                "[red]Dipinjam[/red]"
            )

        console.print(table)

    def pinjam_buku(this):
        buku_tersedia = [buku for buku in this.perpustakaan.tampilkan_semua_buku() if buku.is_tersedia()]

        if not buku_tersedia:
            this.view.tampilkan_pesan("Maaf, tidak ada buku yang tersedia saat ini.")
            return

        # Input ID buku
        id_buku = console.input("[bold green]Masukkan ID buku yang ingin dipinjam:[/bold green] ")

        buku = this.perpustakaan.get_buku_by_id(id_buku)
        if not buku:
            console.print("[bold red]❌ Buku tidak ditemukan.[/bold red]")
            return

        # tampilkan detail
        console.print(Panel.fit(
            f"[bold cyan]ID:[/bold cyan] {buku.id_buku}\n"
            f"[bold cyan]Judul:[/bold cyan] {buku.judul}\n"
            f"[bold cyan]Penulis:[/bold cyan] {buku.pengarang}\n"
            f"[bold cyan]Tahun Terbit:[/bold cyan] {buku.tahun_terbit}\n"
            f"[bold cyan]Status:[/bold cyan] {'Tersedia' if buku.is_tersedia() else 'Dipinjam'}",
            title="📘 Detail Buku",
            border_style="cyan"
        ))

        # konfirmasi pinjam
        konfirmasi = console.input("[bold yellow]Apakah Anda yakin ingin meminjam buku ini? (y/n): [/bold yellow]").lower()
        if konfirmasi != "y":
            console.print("[bold cyan]Peminjaman dibatalkan.[/bold cyan]")
            return

        # proses peminjaman
        sukses, pesan = this.perpustakaan.pinjam_buku(this.user_logged_in, buku)
        if sukses:
            console.print(f"[bold green]{pesan}[/bold green]")
        else:
            console.print(f"[bold red]❌ {pesan}[/bold red]")


    def kembalikan_buku(this):
        # Tampilkan daftar buku yang sedang dipinjam user
        sql = """
            SELECT 
                p.id_peminjaman,
                b.id_buku,
                b.judul,
                b.pengarang,
                b.tahun_terbit,
                p.tanggal_pinjam,
                p.tanggal_kembali,
                a.nama AS nama_peminjam
            FROM peminjaman p
            JOIN buku b ON p.id_buku = b.id_buku
            JOIN anggota a ON p.id_anggota = a.id_anggota
            WHERE p.id_anggota = %s AND p.tanggal_kembali IS NULL
            ORDER BY p.tanggal_pinjam DESC

        """
        daftar_pinjam = this.perpustakaan.db.fetch_all(sql, (this.user_logged_in.id_anggota))

        if not daftar_pinjam:
            console.print("[bold yellow]📭 Anda belum meminjam buku apapun.[/bold yellow]")
            return

        # Tampilkan tabel buku yang dipinjam
        table = Table(title=f"📚 Buku yang Sedang Dipinjam oleh {this.user_logged_in.nama}", header_style="bold magenta")
        table.add_column("ID Buku", justify="center", style="bold cyan")
        table.add_column("Judul", style="white")
        table.add_column("Penulis", style="white")
        table.add_column("Tahun", justify="center", style="yellow")
        table.add_column("Tanggal Pinjam", justify="center", style="green")

        for buku in daftar_pinjam:
            table.add_row(
                buku["id_buku"],
                buku["judul"],
                buku["pengarang"],
                str(buku["tahun_terbit"]),
                str(buku["tanggal_pinjam"])
            )

        console.print(table)

        id_buku = this.view.input_data("Masukkan ID buku yang dikembalikan: ").strip()

        if not id_buku:
            console.print("[bold red]❌ ID buku tidak boleh kosong![/bold red]")
            return

        # Ambil buku dari perpustakaan
        buku = this.perpustakaan.get_buku_by_id(id_buku)
        if not buku:
            console.print("[bold red]❌ Buku tidak ditemukan.[/bold red]")
            return

        # Input hari keterlambatan
        try:
            hari_terlambat = int(this.view.input_data("Hari terlambat: "))
        except ValueError:
            hari_terlambat = 0  # Jika user input salah, anggap 0 hari
            console.print("[bold yellow]Input hari terlambat tidak valid, dianggap 0 hari[/bold yellow]")

        # Proses pengembalian melalui model
        sukses, pesan = this.perpustakaan.kembalikan_buku(this.user_logged_in, buku, hari_terlambat)

        # Tampilkan pesan hasil pengembalian
        if sukses:
            console.print(f"[bold green]{pesan}[/bold green]")
        else:
            console.print(f"[bold red]❌ {pesan}[/bold red]")

    def tampilkan_buku(this):
        buku_list = this.perpustakaan.tampilkan_semua_buku()
