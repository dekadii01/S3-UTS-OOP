class MainView:
    @staticmethod
    def tampilkan_menu():
        print("\n--- Menu Perpustakaan ---")
        print("1. Pinjam Buku")
        print("2. Kembalikan Buku")
        print("3. Tampilkan Semua Buku")
        print("4. Tampilkan Buku yang Dipinjam")  # Menu baru
        print("5. Keluar")

    @staticmethod
    def input_nim():
        return input("Masukkan NIM: ")

    @staticmethod
    def input_data(prompt):
        return input(prompt)

    @staticmethod
    def tampilkan_pesan(pesan):
        print(pesan)

    @staticmethod
    def tampilkan_list(data_list):
        for item in data_list:
            print(item)