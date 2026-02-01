from database import init_db, get_connection
from models import Barang

# Struktur Data
list_barang = []          # Array 1D
stack_transaksi = []      # Stack
queue_pembelian = []      # Queue


def load_barang():
    list_barang.clear()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama, stok, harga FROM barang")
    for row in cursor.fetchall():
        list_barang.append(Barang(row[0], row[1], row[2]))
    conn.close()


def tambah_barang():
    nama = input("Nama barang: ")
    stok = int(input("Stok: "))
    harga = int(input("Harga: "))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO barang (nama, stok, harga) VALUES (?, ?, ?)",
                   (nama, stok, harga))
    conn.commit()
    conn.close()

    print("Barang berhasil ditambahkan!")


def lihat_barang():
    load_barang()
    print("\nDAFTAR BARANG")
    for i, b in enumerate(list_barang, start=1):
        print(f"{i}. {b.nama} | Stok: {b.stok} | Harga: {b.harga}")


def cari_barang():
    keyword = input("Masukkan nama barang: ")
    load_barang()
    for b in list_barang:
        if b.nama.lower() == keyword.lower():
            print(f"Ditemukan: {b.nama} | Stok: {b.stok} | Harga: {b.harga}")
            return
    print("Barang tidak ditemukan")


def beli_barang():
    nama = input("Nama barang: ")
    jumlah = int(input("Jumlah beli: "))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stok FROM barang WHERE nama=?", (nama,))
    data = cursor.fetchone()

    if data and data[0] >= jumlah:
        cursor.execute("UPDATE barang SET stok = stok - ? WHERE nama=?", (jumlah, nama))
        cursor.execute("INSERT INTO transaksi (nama_barang, jumlah) VALUES (?, ?)",
                       (nama, jumlah))
        conn.commit()

        stack_transaksi.append((nama, jumlah))
        queue_pembelian.append((nama, jumlah))

        print("Transaksi berhasil!")
    else:
        print("Stok tidak cukup atau barang tidak ada")

    conn.close()


def lihat_riwayat():
    print("\nRIWAYAT TRANSAKSI (STACK)")
    while stack_transaksi:
        print(stack_transaksi.pop())


def proses_antrian():
    print("\nPROSES ANTRIAN (QUEUE)")
    while queue_pembelian:
        print(queue_pembelian.pop(0))


def cek_stok_menipis():
    load_barang()
    print("\nSTOK MENIPIS (< 5)")
    for b in list_barang:
        if b.stok < 5:
            print(f"{b.nama} | Sisa: {b.stok}")


def menu():
    init_db()
    while True:
        print("""
===== TOKOKU INVENTORY MANAGER =====
NOTE: Pilih opsi dengan memasukkan angka sesuai menu
1. Tambah Barang
2. Lihat Barang
3. Cari Barang
4. Beli Barang
5. Riwayat Transaksi
6. Proses Antrian
7. Cek Stok Menipis
0. Keluar
""")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_barang()
        elif pilihan == "2":
            lihat_barang()
        elif pilihan == "3":
            cari_barang()
        elif pilihan == "4":
            beli_barang()
        elif pilihan == "5":
            lihat_riwayat()
        elif pilihan == "6":
            proses_antrian()
        elif pilihan == "7":
            cek_stok_menipis()
        elif pilihan == "0":
            break
        else:
            print("Menu tidak valid")


menu()
