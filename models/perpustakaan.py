from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .db import Database
from .anggota import Anggota
from .buku import Buku, BukuReferensi
from datetime import datetime

console = Console()

class Perpustakaan:
    def __init__(this):
        this.__daftar_anggota = []
        this.__daftar_buku = []
        this.__daftar_peminjaman = {}
        this.db = Database()
        
    # 🔹 Bagian Anggota
    def tambah_anggota(this, id_anggota, nama, alamat, show_message=False):
        anggota_baru = Anggota(id_anggota, nama, alamat)
        anggota_baru.save()
        if show_message:
            console.print(f"[bold green]✔ Anggota '{nama}' berhasil ditambahkan![/bold green]")
        return anggota_baru

    def get_anggota_by_id(this, id_anggota):
        sql = "SELECT * FROM anggota WHERE id_anggota = %s"
        row = this.db.fetch_one(sql, (id_anggota,))
        
        if row:
            return Anggota(row["id_anggota"], row["nama"], row["alamat"])
        return None


    def load_anggota(this):
        rows = this.db.fetch_all("SELECT * FROM anggota")
        for row in rows:
            anggota = Anggota(row["id_anggota"], row["nama"], row["alamat"])
            this.__daftar_anggota.append(anggota)

    # 🔹 Bagian Buku
    def tambah_buku(this, buku, show_message=False):
        this.__daftar_buku.append(buku)
        if show_message:
            console.print(f"[cyan]📘 Buku '{buku.judul}' berhasil ditambahkan ke koleksi.[/cyan]")

    def get_buku_by_id(this, id_buku):
        sql = "SELECT * FROM buku WHERE id_buku = %s"
        row = this.db.fetch_one(sql, (id_buku,))

        if row:
            # kembalikan objek Buku
            return Buku(
                row["id_buku"],
                row["judul"],
                row["pengarang"],
                row["tahun_terbit"],
                row["tersedia"]
            )
        return None

    # 🔹 Bagian Peminjaman
    def pinjam_buku(this, anggota, buku):
        if not buku.is_tersedia():
            return False, "Buku sedang dipinjam orang lain."

        # tandai buku sebagai dipinjam di memori
        buku.set_tersedia(False)
        this.__daftar_peminjaman[buku.id_buku] = anggota.id_anggota
        anggota.tambah_pinjaman(buku)

        # update status buku di database
        sql_update_buku = "UPDATE buku SET tersedia = %s WHERE id_buku = %s"
        sukses = this.db.execute(sql_update_buku, (False, buku.id_buku))
        if not sukses:
            return False, "Gagal memperbarui status buku di database."

        # simpan data peminjaman ke tabel peminjaman
        tanggal_pinjam = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_insert_peminjaman = """
            INSERT INTO peminjaman (id_anggota, id_buku, tanggal_pinjam)
            VALUES (%s, %s, %s)
        """
        sukses = this.db.execute(sql_insert_peminjaman, (anggota.id_anggota, buku.id_buku, tanggal_pinjam))
        if not sukses:
            return False, "Gagal menyimpan data peminjaman ke database."

        return True, f"Buku '{buku.judul}' berhasil dipinjam oleh {anggota.nama}."

    def kembalikan_buku(this, anggota, buku, hari_terlambat=0):
        if buku not in anggota.get_pinjaman():
            console.print(f"[bold red]❌ Buku '{buku.judul}' tidak ditemukan di daftar pinjaman anggota.[/bold red]")
            return False, "Buku tidak ditemukan di daftar pinjaman anggota."

        # Hapus dari daftar pinjaman anggota
        anggota.hapus_pinjaman(buku)
        
        # Tandai buku sebagai tersedia
        buku.set_tersedia(True)
        
        # Update status buku di database
        sql = "UPDATE buku SET tersedia = %s WHERE id_buku = %s"
        sukses_update = this.db.execute(sql, (1, buku.id_buku))
        if not sukses_update:
            console.print(f"[bold red]❌ Gagal memperbarui status buku di database.[/bold red]")
            return False, "Gagal memperbarui status buku di database."

        # Hitung denda jika ada
        denda = buku.hitung_denda(hari_terlambat)

        # Hapus dari daftar peminjaman internal
        if buku.id_buku in this.__daftar_peminjaman:
            del this.__daftar_peminjaman[buku.id_buku]

        # Tampilkan info pengembalian
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
        sql = "SELECT id_buku, judul, pengarang, tahun_terbit, tersedia FROM buku"
        rows = this.db.fetch_all(sql)

        if not rows:
            console.print("[bold yellow]⚠ Belum ada buku di database.[/bold yellow]")
            return []

        # convert DB → object Buku
        list_buku = []
        for row in rows:
            buku = Buku(
                id_buku=row["id_buku"],
                judul=row["judul"],
                pengarang=row["pengarang"],
                tahun_terbit=row["tahun_terbit"]
            )
            # set status tersedia
            buku.set_tersedia(bool(row["tersedia"]))
            list_buku.append(buku)

        # tampilkan tabel Rich
        table = Table(title="📚 Daftar Buku di Perpustakaan", header_style="bold magenta")
        table.add_column("ID", justify="center", style="bold cyan")
        table.add_column("Judul", style="white")
        table.add_column("Penulis", style="white")
        table.add_column("Tahun", justify="center", style="yellow")
        table.add_column("Status", justify="center", style="bold")

        for buku in list_buku:
            status = "[green]Tersedia[/green]" if buku.is_tersedia() else "[red]Dipinjam[/red]"
            table.add_row(
                str(buku.id_buku),
                buku.judul,
                buku.pengarang,
                str(buku.tahun_terbit),
                status
            )

        console.print(table)
        return list_buku
