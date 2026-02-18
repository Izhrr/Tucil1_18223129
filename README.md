# Queens LinkedIn Solver

## A. Penjelasan Singkat Program
Program ini adalah solusi untuk masalah penempatan N-Queens dengan tambahan constraint warna (Queens LinkedIn). Setiap queen harus diletakkan pada papan NxN sehingga:
- Tidak ada dua queen yang saling menyerang (tidak satu baris, kolom, atau kotak bersebelahan).
- Setiap queen harus berada pada warna (huruf) yang berbeda.
- Input papan diambil dari file `.txt` di folder `input`, dan solusi dapat disimpan dalam bentuk `.txt` dan `.jpg` di folder `test`.

Program dilengkapi dengan GUI berbasis Tkinter untuk memudahkan pemilihan input, visualisasi proses, dan penyimpanan solusi.

---

## B. Requirement Program & Instalasi

- **Python 3.7+**  
- Library eksternal:
  - `pyautogui`
  - `pillow`

Instalasi library:
```bash
pip install -r requirements.txt
```

---

## C. Cara Kompilasi

Tidak perlu kompilasi khusus. Pastikan semua dependensi sudah terpasang.

---

## D. Cara Menjalankan & Menggunakan Program

1. **Jalankan program utama:**
   ```bash
   python src/main.py
   ```
2. **Penggunaan GUI:**
   - Pilih file input dari dropdown (otomatis membaca file `.txt` di folder `input`).
   - Klik **Load Input** untuk memuat papan.
   - Klik **Start Solving** untuk memulai pencarian solusi.
   - Setelah solusi ditemukan, klik **Save Solution** untuk menyimpan hasil ke folder `test` dalam format `.txt` dan `.jpg`.

---

## E. Author / Identitas Pembuat

- Nama: Izhar Alif Akbar
- NIM: 18223129
- Tugas Kecil 1 IF2211 Strategi Algoritma 2026

---

## F. Menambah Input

Untuk menambah kasus baru:
1. Buat file `.txt` baru di folder `input`.
2. Format file: Setiap baris berisi deretan huruf kapital (A-Z) sebanyak N kolom, dan jumlah baris juga N (papan NxN).
   ```
   ABCDEFGHIJ
   ABCDEFGHIJ
   ...
   ```
3. File akan otomatis muncul di dropdown GUI saat program dijalankan.

---
