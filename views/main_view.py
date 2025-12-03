# views/main_view.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

class MainView:

    # ==========================
    # Tampilan awal
    # ==========================
    def tampilkan_header_awal(self):
        console.rule("[bold cyan]📚 SISTEM PERPUSTAKAAN 📚[/bold cyan]")
        console.print(Panel(
            "Selamat datang di [bold green]Perpustakaan Digital[/bold green]!\nSilakan login untuk melanjutkan.",
            style="cyan"
        ))

    # ==========================
    # Menu utama
    # ==========================
    def tampilkan_menu_utama(self):
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

    def input_pilihan_menu(self):
        return Prompt.ask(
            "[bold yellow]Masukkan pilihan kamu[/bold yellow]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )

    # ==========================
    # Panel judul menu
    # ==========================
    def tampilkan_panel(self, judul):
        console.print(Panel(f"[bold cyan]{judul}[/bold cyan]", style="bold green"))

    # ==========================
    # Input form
    # ==========================
    def input_nim(self):
        return Prompt.ask("[bold cyan]Masukkan NIM[/bold cyan]")

    def input_data(self, pesan):
        return Prompt.ask(pesan)

    # ==========================
    # Pesan umum
    # ==========================
    def tampilkan_pesan(self, pesan):
        console.print(pesan)

    # ==========================
    # List Data
    # ==========================
    def tampilkan_list(self, data):
        if not data:
            console.print("[yellow]Tidak ada data.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Judul")
        table.add_column("Pengarang")
        table.add_column("Tahun")

        for b in data:
            table.add_row(str(b.id), b.judul, b.pengarang, str(b.tahun))

        console.print(table)
