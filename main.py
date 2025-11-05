from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.theme import Theme

from models.perpustakaan import Perpustakaan
from models.buku import Buku, BukuReferensi
from models.anggota import Anggota
from views.main_view import MainView
from controllers.controller import Controller

# Setup Rich console
custom_theme = Theme({
    "info": "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
})
console = Console(theme=custom_theme)

# Inisialisasi
perpus = Perpustakaan()
view = MainView()
controller = Controller(perpus, view)

# Tambah anggota contoh
perpus.tambah_anggota(2401010015, "Adi Pramana", "Badung")
perpus.tambah_anggota(2401010018, "Reza Satya", "Denpasar")

# Tambah buku contoh
perpus.tambah_buku(Buku(1, "Python Dasar", "Lois", 2024))
perpus.tambah_buku(Buku(2, "OOP Lanjutan", "Adi", 2025))
perpus.tambah_buku(BukuReferensi(3, "Kamus Bahasa", "Pustaka", 2020))
perpus.tambah_buku(Buku(4, "Algoritma & Struktur Data", "Reina", 2023))

# Tampilan awal
console.rule("[bold cyan]📚 SISTEM PERPUSTAKAAN 📚[/bold cyan]")
console.print(Panel("Selamat datang di [bold green]Perpustakaan Digital[/bold green]!\nSilakan login untuk melanjutkan.", style="cyan"))

controller.login()

# Loop menu utama
while True:
    console.rule("[bold yellow]MENU UTAMA[/bold yellow]")
    table = Table(title="Pilih Menu", show_header=False, header_style="bold magenta")
    table.add_column("Nomor", justify="center", style="bold cyan")
    table.add_column("Deskripsi", style="white")
    table.add_row("1", "Pinjam Buku")
    table.add_row("2", "Kembalikan Buku")
    table.add_row("3", "Tampilkan Daftar Buku")
    table.add_row("4", "Tampilkan Buku yang Dipinjam")
    table.add_row("5", "Keluar")

    console.print(table)

    pilihan = Prompt.ask("[bold yellow]Masukkan pilihan kamu[/bold yellow]", choices=["1", "2", "3", "4", "5"], default="1")

    if pilihan == "1":
        console.print(Panel("📖 [bold cyan]Menu Pinjam Buku[/bold cyan]", style="bold green"))
        controller.pinjam_buku()
    elif pilihan == "2":
        console.print(Panel("🔁 [bold cyan]Menu Kembalikan Buku[/bold cyan]", style="bold green"))
        controller.kembalikan_buku()
    elif pilihan == "3":
        console.print(Panel("📚 [bold cyan]Daftar Buku yang Tersedia[/bold cyan]", style="bold green"))
        controller.tampilkan_buku()
    elif pilihan == "4":
        console.print(Panel("📕 [bold cyan]Buku yang Sedang Dipinjam[/bold cyan]", style="bold green"))
        controller.tampilkan_buku_dipinjam()
    elif pilihan == "5":
        console.print(Panel("👋 Terima kasih telah menggunakan sistem perpustakaan!", style="bold yellow"))
        break
    else:
        console.print("[error]Pilihan tidak valid![/error]")
