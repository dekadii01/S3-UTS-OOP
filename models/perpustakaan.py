from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .anggota import Anggota
from .buku import Buku, BukuReferensi

console = Console()

class Perpustakaan:
    def __init__(this):
        this.__daftar_anggota = []
        this.__daftar_buku = []
        this.__daftar_peminjaman = {}

    # ======================
    # 🔹 Bagian Anggota
    # ======================
    def tambah_anggota(this, id_anggota, nama, alamat, show_message=False):
        anggota_baru = Anggota(id_anggota, nama, alamat)
        this.__daftar_anggota.append(anggota_baru)
        if show_message:
            console.print(f"[bold green]✔ Anggota '{nama}' berhasil ditambahkan![/bold green]")
        return anggota_baru

    def get_anggota_by_id(this, id_anggota):
        for anggota in this.__daftar_anggota:
            if anggota.id_anggota == id_anggota:
                return anggota
        return None

    # ======================
    # 🔹 Bagian Buku
    # ======================
    def tambah_buku(this, buku, show_message=False):
        this.__daftar_buku.append(buku)
        if show_message:
            console.print(f"[cyan]📘 Buku '{buku.judul}' berhasil ditambahkan ke koleksi.[/cyan]")

    def get_buku_by_id(this, id_buku):
        for buku in this.__daftar_buku:
            if buku.id_buku == id_buku:
                return buku
        return None

    # ======================
    # 🔹 Bagian Peminjaman
    # ======================
    def pinjam_buku(this, anggota, buku, hari_pinjam=7):
        if not buku.is_tersedia():
            console.print(f"[bold red]❌ Buku '{buku.judul}' sedang dipinjam orang lain.[/bold red]")
            return False, "Buku sedang dipinjam orang lain."

        buku.set_tersedia(False)
        anggota.tambah_pinjaman(buku)
        this.__daftar_peminjaman[buku] = {
            "anggota": anggota,
            "hari_pinjam": hari_pinjam,
            "hari_terlambat": 0
        }

        console.print(Panel.fit(
            f"📖 Buku [bold cyan]'{buku.judul}'[/bold cyan] berhasil dipinjam oleh [bold yellow]{anggota.nama}[/bold yellow].\n"
            f"Batas waktu: {hari_pinjam} hari.",
            title="Peminjaman Berhasil",
            style="bold green"
        ))
        return True, f""

    def kembalikan_buku(this, anggota, buku, hari_terlambat=0):
        if buku not in anggota.get_pinjaman():
            console.print(f"[bold red]❌ Buku '{buku.judul}' tidak ditemukan di daftar pinjaman anggota.[/bold red]")
            return False, "Buku tidak ditemukan di daftar pinjaman anggota."

        anggota.hapus_pinjaman(buku)
        buku.set_tersedia(True)
        denda = buku.hitung_denda(hari_terlambat)
        del this.__daftar_peminjaman[buku]

        warna_panel = "bold red" if denda > 0 else "bold green"
        console.print(Panel.fit(
            f"📗 Buku [bold cyan]'{buku.judul}'[/bold cyan] dikembalikan oleh [bold yellow]{anggota.nama}[/bold yellow].\n"
            f"Denda keterlambatan: [bold]{'Rp' + str(denda) if denda > 0 else 'Tidak ada'}[/bold]",
            title="Pengembalian Buku",
            style=warna_panel
        ))

        return True, f"Buku '{buku.judul}' dikembalikan. Denda: Rp{denda}"

    # tampilkan semua buku
    def tampilkan_semua_buku(this):
        if not this.__daftar_buku:
            console.print("[bold yellow]⚠ Belum ada buku di perpustakaan.[/bold yellow]")
            return

        table = Table(title="📚 Daftar Buku di Perpustakaan", header_style="bold magenta")
        table.add_column("ID", justify="center", style="bold cyan")
        table.add_column("Judul", style="white")
        table.add_column("Penulis", style="white")
        table.add_column("Tahun", justify="center", style="yellow")
        table.add_column("Status", justify="center", style="bold")

        for buku in this.__daftar_buku:
            status = "[green]Tersedia[/green]" if buku.is_tersedia() else "[red]Dipinjam[/red]"
            table.add_row(str(buku.id_buku), buku.judul, buku.pengarang, str(buku.tahun_terbit), status)

        console.print(table)
        buku = this.__daftar_buku
        return buku
