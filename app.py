import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QDialog, QMessageBox
import pandas as pd

class CartItem:
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga

class ShoppingCart:
    def __init__(self):
        self.cart = []

    def tambahBarang(self, barang):
        self.cart.append(barang)

    def hapusBarang(self, namaBarang):
        for barang in self.cart:
            if barang.nama == namaBarang:
                self.cart.remove(barang)
                return True
        return False

    def tampilBarang(self):
        return '\n'.join([f'{barang.nama} {barang.harga}' for barang in self.cart])

    def totalBarang(self):
        total_harga = sum([barang.harga for barang in self.cart])
        return total_harga

class MenuDialog(QDialog):
    def __init__(self, shoopingcart):
        super().__init__()

        self.shoopingcart = shoopingcart

        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.nama_barang_input = QLineEdit()
        self.harga_barang_input = QLineEdit()
        layout.addRow('Nama Barang:', self.nama_barang_input)
        layout.addRow('Harga Barang:', self.harga_barang_input)

        self.tambah_button = QPushButton('Tambah Barang')
        self.tambah_button.clicked.connect(self.tambahBarang)
        layout.addWidget(self.tambah_button)

        self.hapus_button = QPushButton('Hapus Barang')
        self.hapus_button.clicked.connect(self.hapusBarang)
        layout.addWidget(self.hapus_button)

        self.tampilkan_button = QPushButton('Tampilkan Barang')
        self.tampilkan_button.clicked.connect(self.tampilkanBarang)
        layout.addWidget(self.tampilkan_button)

        self.lihat_total_button = QPushButton('Lihat Total Belanja')
        self.lihat_total_button.clicked.connect(self.lihatTotal)
        layout.addWidget(self.lihat_total_button)

        # Tambahkan tombol "Simpan Struk Belanja"
        self.simpan_struk_button = QPushButton('Simpan Struk Belanja')
        self.simpan_struk_button.clicked.connect(self.simpanStrukBelanja)
        layout.addWidget(self.simpan_struk_button)

        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def tambahBarang(self):
        try:
            nama = self.nama_barang_input.text()
            harga = float(self.harga_barang_input.text())
            barang = CartItem(nama, harga)
            self.shoopingcart.tambahBarang(barang)
            QMessageBox.information(self, 'Tambah Barang', f'Barang {nama} berhasil ditambahkan')
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Harga hanya bisa diinputkan angka, coba lagi ya.')

    def hapusBarang(self):
        nama = self.nama_barang_input.text()
        if self.shoopingcart.hapusBarang(nama):
            QMessageBox.information(self, 'Hapus Barang', f'{nama} telah berhasil dihapus')
        else:
            QMessageBox.warning(self, 'Error', f'{nama} belum ada di keranjang')

    def tampilkanBarang(self):
        QMessageBox.information(self, 'Tampilkan Barang', self.shoopingcart.tampilBarang())

    def lihatTotal(self):
        harga_total = self.shoopingcart.totalBarang()
        QMessageBox.information(self, 'Total Belanja', f'Total Barang di Keranjang anda {harga_total} Rp')

    def simpanStrukBelanja(self):
        # Simpan data ke Excel saat tombol "Simpan Struk Belanja" ditekan
        self.simpanDataKeExcel()
        QMessageBox.information(self, 'Simpan Struk Belanja', 'Struk Belanja berhasil disimpan')

    # Fungsi untuk menyimpan data ke dalam file Excel
    def simpanDataKeExcel(self):
        try:
            data = {'Nama': [barang.nama for barang in self.shoopingcart.cart],
                    'Harga': [barang.harga for barang in self.shoopingcart.cart]}

            df = pd.DataFrame(data)
            df.to_excel('keranjang_belanja.xlsx', index=False)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Gagal menyimpan data ke Excel: {str(e)}')

class ShoppingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.shoopingcart = ShoppingCart()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Selamat Datang di Toko Makmur!')
        layout.addWidget(self.label)

        self.menu_button = QPushButton('Menu')
        self.menu_button.clicked.connect(self.showMenu)
        layout.addWidget(self.menu_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def showMenu(self):
        menu_dialog = MenuDialog(self.shoopingcart)
        menu_dialog.setWindowTitle('Menu Keranjang Belanja')
        menu_dialog.setGeometry(200, 200, 400, 300)
        menu_dialog.exec_()

def main():
    app = QApplication(sys.argv)
    main_app = ShoppingApp()
    main_app.setWindowTitle('Shopping Cart')
    main_app.setGeometry(100, 100, 400, 300)
    main_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
