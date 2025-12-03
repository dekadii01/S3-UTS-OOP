# main.py
from rich.console import Console
from rich.theme import Theme

from models.perpustakaan import Perpustakaan
from views.main_view import MainView
from controllers.controller import Controller

# Rich theme
custom_theme = Theme({
    "info": "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
})
console = Console(theme=custom_theme)

# Inisialisasi
perpus = Perpustakaan()
perpus.load_anggota()

view = MainView()
controller = Controller(perpus, view)

# Tampilkan header awal
view.tampilkan_header_awal()

# Login
controller.login_atau_exit()

# Loop menu utama
while True:
    view.tampilkan_menu_utama()
    pilihan = view.input_pilihan_menu()

    if pilihan == "1":
        view.tampilkan_panel("📖 Menu Pinjam Buku")
        controller.pinjam_buku()

    elif pilihan == "2":
        view.tampilkan_panel("🔁 Menu Kembalikan Buku")
        controller.kembalikan_buku()

    elif pilihan == "3":
        view.tampilkan_panel("📚 Daftar Buku yang Tersedia")
        controller.tampilkan_buku()

    elif pilihan == "4":
        view.tampilkan_panel("📕 Buku yang Sedang Dipinjam")
        controller.tampilkan_buku_dipinjam()

    elif pilihan == "5":
        view.tampilkan_panel("👋 Terima kasih telah menggunakan sistem perpustakaan!")
        break
