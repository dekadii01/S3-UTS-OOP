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
        else:
            this.view.tampilkan_pesan("NIM tidak ditemukan.")
            return

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
        id_buku = int(this.view.input_data("Masukkan ID buku yang dikembalikan: "))
        buku = this.perpustakaan.get_buku_by_id(id_buku)
        if buku:
            hari_terlambat = int(this.view.input_data("Hari terlambat: "))
            sukses, pesan = this.perpustakaan.kembalikan_buku(this.user_logged_in, buku, hari_terlambat)
            # this.view.tampilkan_pesan(pesan)
        else:
            this.view.tampilkan_pesan("Buku tidak ditemukan.")

    def tampilkan_buku(this):
        buku_list = this.perpustakaan.tampilkan_semua_buku()
        # this.view.tampilkan_list(buku_list)
