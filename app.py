from flask import Flask, render_template, request, redirect, url_for, flash, session
import time
import json
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'kunci_rahasia_sim_2026')

# Simulasi Database Akun di Memory
users_db = {"admin": "admin123"}

# FILE PATH UNTUK FILE I/O
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_MAHASISWA = os.path.join(BASE_DIR, "data_mahasiswa.json")

# --- DATA INTERNAL TEKNIK INFORMATIKA ---
MATA_KULIAH = [
    {"kode": "IF101", "nama": "Algoritma dan Pemrograman", "sks": 3, "semester": 3},
    {"kode": "IF102", "nama": "Sistem Informasi", "sks": 3, "semester": 3},
    {"kode": "IF103", "nama": "Matematika Diskrit", "sks": 3, "semester": 3},
    {"kode": "IF104", "nama": "Kalkulus", "sks": 3, "semester": 3},
    {"kode": "IF105", "nama": "Struktur Data", "sks": 3, "semester": 3},
    {"kode": "IF106", "nama": "Sistem Berkas", "sks": 2, "semester": 3},
    {"kode": "IF107", "nama": "Sistem Operasi", "sks": 3, "semester": 3},
    {"kode": "IF108", "nama": "Pemrograman Orientasi Objek", "sks": 3, "semester": 3},
    {"kode": "IF109", "nama": "Basis Data", "sks": 3, "semester": 3},
    {"kode": "IF110", "nama": "Jaringan Komputer", "sks": 3, "semester": 3},
    {"kode": "IF111", "nama": "Komputer Grafik", "sks": 3, "semester": 3},
    {"kode": "IF112", "nama": "Fisika Dasar", "sks": 3, "semester": 3},
    {"kode": "IF113", "nama": "Komunikasi Data", "sks": 3, "semester": 3},
    {"kode": "IF114", "nama": "Pengantar Aplikasi Komputer", "sks": 3, "semester": 3},
    {"kode": "IF115", "nama": "Statistika dan Probabilitas", "sks": 3, "semester": 3},
    {"kode": "IF116", "nama": "Graph Terapan", "sks": 2, "semester": 3}
]

DOSEN = [
    {"nama": "Prof. Haikal Maulana Rayhan, M.Kom.", "lulusan": "Ilmu Komputer", "matkul": "Sistem Informasi"},
    {"nama": "Eka Sri Rahayu S.Kom., M.Kom.", "lulusan": "Teknik Informatika", "matkul": "Algoritma dan Pemrograman"},
    {"nama": "Siti Aminah, M.T.", "lulusan": "Sistem Informasi", "matkul": "Matematika Diskrit"},
    {"nama": "Irwan Kurniawan, Ph.D", "lulusan": "Teknik Informatika", "matkul": "Kalkulus"},
    {"nama": "Rina Wijaya, M.Cs.", "lulusan": "Ilmu Komputer", "matkul": "Struktur Data"},
    {"nama": "Agus Setiawan, M.Kom.", "lulusan": "Teknik Informatika", "matkul": "Sistem Berkas"},
    {"nama": "Dewi Lestari, M.T.", "lulusan": "Teknik Informatika", "matkul": "Sistem Operasi"},
    {"nama": "Eko Prasetyo, M.Kom.", "lulusan": "Ilmu Komputer", "matkul": "Pemrograman Orientasi Objek"},
    {"nama": "Fahmi Idris, M.T.", "lulusan": "Sistem Informasi", "matkul": "Basis Data"},
    {"nama": "Gita Permata, M.Sc.", "lulusan": "Teknik Elektro", "matkul": "Jaringan Komputer"},
    {"nama": "Nabila Azzahra Pratama, S.Kom.", "lulusan": "Sistem Informasi", "matkul": "Graph Terapan"},
    {"nama": "Dinda Maharani Saputri, S.Kom.", "lulusan": "Ilmu Komputer", "matkul": "Statistika dan Probabilitas"},
    {"nama": "Nadira Khairunnisa Putri, S.Kom.", "lulusan": "Teknologi Informasi", "matkul": "Komputer Grafik"},
    {"nama": "Salsabila Nur Aini, S.Kom.", "lulusan": "Teknik Informatika", "matkul": "Komunikasi Data"},
    {"nama": "Muhammad Rizky Pratama, S.Kom.", "lulusan": "Teknik Informatika", "matkul": "Pengantar Aplikasi Komputer"},
    {"nama": "Dimas Saputra Wijaya, S.Kom.", "lulusan": "Ilmu Komputer", "matkul": "Fisika Dasar"}
]

MAHASISWA_INITIAL = [
    {"nim": 241011450240, "nama": "Haikal Anugrah Ramadhan", "prodi": "Teknik Informatika"},
    {"nim": 241011452511, "nama": "Arkan Mahendra Putra", "prodi": "Teknik Informatika"},
    {"nim": 241011459076, "nama": "Aisha Humaira Zahra", "prodi": "Teknik Informatika"},
    {"nim": 241011454025, "nama": "Elvano Akbar Pratama", "prodi": "Teknik Informatika"},
    {"nim": 241011453698, "nama": "Aria Celestine", "prodi": "Teknik Informatika"},
    {"nim": 241011450357, "nama": "Chloe Anindya", "prodi": "Teknik Informatika"},
    {"nim": 241011451024, "nama": "Axel Mahardika Putra", "prodi": "Teknik Informatika"},
    {"nim": 241011456975, "nama": "Alessa Nayla", "prodi": "Teknik Informatika"},
    {"nim": 241011453252, "nama": "Nathan Akbar Saputra", "prodi": "Teknik Informatika"},
    {"nim": 241011453963, "nama": "Alya Safira Putri", "prodi": "Teknik Informatika"},
    {"nim": 241011452045, "nama": "Yusuf Alfarel Akbar", "prodi": "Teknik Informatika"},
    {"nim": 241011451248, "nama": "Elina Grace", "prodi": "Teknik Informatika"},
    {"nim": 241011450560, "nama": "Arshaka Wijaya", "prodi": "Teknik Informatika"},
    {"nim": 241011457984, "nama": "Olivia Kirana", "prodi": "Teknik Informatika"},
    {"nim": 241011452566, "nama": "Alina Safira Putri", "prodi": "Teknik Informatika"},
    {"nim": 241011454982, "nama": "Syifa Nabila Putri", "prodi": "Teknik Informatika"},
    {"nim": 241011457234, "nama": "Luna Valerie", "prodi": "Teknik Informatika"},
    {"nim": 241011452241, "nama": "Yuna Aveline", "prodi": "Teknik Informatika"},
    {"nim": 241011452150, "nama": "Nathaniel Pratama", "prodi": "Teknik Informatika"},
    {"nim": 241011454157, "nama": "Bianca Azzahra", "prodi": "Teknik Informatika"}
]

# --- IMPLEMENTASI KONSEP OOP, VALIDASI REGEX, DAN TRY-CATCH ---
class Person:
    """Base class untuk mendemonstrasikan konsep Pewarisan (Inheritance)"""
    def __init__(self, nama):
        self._nama = nama  # Protected attribute

class Mahasiswa(Person):
    """Derived class dengan Enkapsulasi penuh"""
    def __init__(self, nim, nama, prodi):
        super().__init__(nama)
        
        # Validasi Input Menggunakan Regular Expression (Regex)
        if not re.match(r"^\d{8,15}$", str(nim)):
            raise ValueError("Format NIM tidak valid! Harus berupa angka 8-15 digit.")
        if not re.match(r"^[a-zA-Z\s\.]{3,50}$", nama):
            raise ValueError("Format Nama tidak valid! Harus alfabet 3-50 karakter.")
            
        self.__nim = int(nim)      # Private attribute (Enkapsulasi)
        self.__prodi = prodi       # Private attribute

    # Getter methods (Polimorfisme struktural via interface objek dict)
    def to_dict(self):
        return {"nim": self.__nim, "nama": self._nama, "prodi": self.__prodi}

# --- IMPLEMENTASI FILE I/O ---
def muat_data_mahasiswa():
    if not os.path.exists(FILE_MAHASISWA):
        simpan_data_mahasiswa(MAHASISWA_INITIAL)
        return MAHASISWA_INITIAL
    try:
        with open(FILE_MAHASISWA, 'r') as f:
            return json.load(f)
    except Exception:
        return MAHASISWA_INITIAL

def simpan_data_mahasiswa(data):
    with open(FILE_MAHASISWA, 'w') as f:
        json.dump(data, f, indent=4)

# --- ALGORITMA SORTING (Bubble & Insertion Sort) ---
def bubble_sort_by_nim(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j]['nim'] > arr[j+1]['nim']:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort_by_nama(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j]['nama'].lower() > key['nama'].lower():
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_db and users_db[username] == password:
            session['user'] = username
            flash("show_welcome_toast", "welcome")
            return redirect(url_for('dashboard'))
        else:
            flash("Username atau Password Salah!", "error")
            
    return render_template('login.html', form_type="login")

@app.route('/registrasi', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if username in users_db:
            flash("Username sudah terdaftar!", "error")
        elif password != confirm_password:
            flash("Password dan Ulangi Password tidak cocok!", "error")
        elif not username or not password:
            flash("Semua kolom input wajib diisi!", "error")
        else:
            users_db[username] = password
            flash("Registrasi Berhasil! Silakan Masuk.", "success")
            return redirect(url_for('login'))

    return render_template('login.html', form_type="registrasi")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    mhs_list = muat_data_mahasiswa()
    return render_template('dashboard.html', page="dashboard", mhs_count=len(mhs_list), dsn_count=len(DOSEN), mk_count=len(MATA_KULIAH))

@app.route('/mahasiswa')
def mahasiswa_page():
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    # 1. Ambil seluruh data mahasiswa dari database JSON
    mhs_list = muat_data_mahasiswa()
    
    # 2. Urutkan secara default berdasarkan nama menggunakan Insertion Sort
    mhs_list = insertion_sort_by_nama(mhs_list)

    # 3. Kirimkan data bersih ke template (pencarian dihitung real-time di browser)
    return render_template(
        'dashboard.html', 
        page="mahasiswa", 
        data_list=mhs_list, 
        search_query="", 
        waktu_cari="0", 
        kompleksitas="Sequential Search Complexity: O(n)"
    )
    
# --- TAMBAH DATA MAHASISWA WITH OOP VALIDATION ---
@app.route('/mahasiswa/tambah', methods=['POST'])
def mahasiswa_tambah():
    if 'user' not in session: return redirect(url_for('login'))
    nim = request.form.get('nim')
    nama = request.form.get('nama')
    prodi = request.form.get('prodi', 'Teknik Informatika')
    
    try:
        # Pemanfaatan OOP & Exception Handling Try-Catch
        mhs_baru = Mahasiswa(nim, nama, prodi)
        mhs_dict = mhs_baru.to_dict()
        
        current_data = muat_data_mahasiswa()
        if any(m['nim'] == mhs_dict['nim'] for m in current_data):
            flash("NIM tersebut sudah terdaftar!", "error")
        else:
            current_data.append(mhs_dict)
            simpan_data_mahasiswa(current_data)
            flash("Data mahasiswa berhasil ditambahkan!", "success")
    except ValueError as e:
        flash(str(e), "error")
        
    return redirect(url_for('mahasiswa_page'))

# --- EDIT DATA MAHASISWA ---
@app.route('/mahasiswa/edit', methods=['POST'])
def mahasiswa_edit():
    if 'user' not in session: return redirect(url_for('login'))
    nim = request.form.get('nim')
    nama = request.form.get('nama')
    prodi = request.form.get('prodi')
    
    try:
        # Validasi Regex via Objek
        mhs_validasi = Mahasiswa(nim, nama, prodi)
        updated_dict = mhs_validasi.to_dict()
        
        current_data = muat_data_mahasiswa()
        for m in current_data:
            if m['nim'] == updated_dict['nim']:
                m['nama'] = updated_dict['nama']
                m['prodi'] = updated_dict['prodi']
                break
        simpan_data_mahasiswa(current_data)
        flash("Data mahasiswa berhasil diperbarui!", "success")
    except ValueError as e:
        flash(str(e), "error")
        
    return redirect(url_for('mahasiswa_page'))

# --- HAPUS DATA MAHASISWA ---
@app.route('/mahasiswa/hapus/<int:nim>')
def mahasiswa_hapus(nim):
    if 'user' not in session: return redirect(url_for('login'))
    current_data = muat_data_mahasiswa()
    filtered_data = [m for m in current_data if m['nim'] != nim]
    simpan_data_mahasiswa(filtered_data)
    flash("Data mahasiswa berhasil dihapus!", "success")
    return redirect(url_for('mahasiswa_page'))

@app.route('/dosen')
def dosen_page():
    if 'user' not in session: return redirect(url_for('login'))
    query = request.args.get('search', '').strip()
    dosen_list = DOSEN
    if query:
        dosen_list = [d for d in DOSEN if query.lower() in d['nama'].lower()]
    return render_template('dashboard.html', page="dosen", data_list=dosen_list, search_query=query)

@app.route('/matkul')
def matkul_page():
    if 'user' not in session: return redirect(url_for('login'))
    query = request.args.get('search', '').strip()
    matkul_list = MATA_KULIAH
    if query:
        matkul_list = [mk for mk in MATA_KULIAH if query.lower() in mk['nama'].lower()]
    return render_template('dashboard.html', page="matkul", data_list=matkul_list, search_query=query)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)
