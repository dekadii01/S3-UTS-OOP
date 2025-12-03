from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()

class MainView:
    @staticmethod
    def tampilkan_menu():
        print("\n--- Menu Perpustakaan ---")
        print("1. Pinjam Buku")
        print("2. Kembalikan Buku")
        print("3. Tampilkan Semua Buku")
        print("4. Tampilkan Buku yang Dipinjam")  
        print("5. Keluar")

    @staticmethod
    def input_nim():
        return input("Masukkan NIM: ")

    @staticmethod
    def input_data(prompt):
        return input(prompt)

    @staticmethod
    def tampilkan_pesan(pesan):
        console.print(pesan)

    @staticmethod
    def tampilkan_list(data_list):
        for item in data_list:
            print(item)