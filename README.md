# Dashboard Analisis Kualitas Udara Beijing

Dashboard ini dikembangkan menggunakan **Streamlit** untuk menganalisis kualitas udara (PM2.5, PM10, SO2, NO2, CO, O3) dari 12 stasiun di Beijing pada periode 2013-2017.

## Fitur Dashboard
- **Summary**: Ringkasan metrik utama berdasarkan filter yang dipilih.
- **Perbandingan Stasiun**: Rata-rata polutan per stasiun.
- **Pola Bulanan**: Tren bulanan per stasiun.
- **Analisis Lanjutan**: Distribusi kategori PM2.5 per musim (khusus PM2.5).
- **Filter Interaktif**: Pilih stasiun, rentang tanggal, dan metrik polutan.

## Link Dashboard
https://dashboard-kualitas-udara-beijing.streamlit.app/

## Cara Menjalankan Dashboard
### 1 Clone Repository
```bash
git clone https://github.com/AlwanFauzi/idcamp-Proyek-Analisis-Data.git
cd idcamp-Proyek-Analisis-Data
```

### 2 Siapkan Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### 3 Jalankan Notebook (Untuk Menyiapkan Data)
Buka `Proyek_Analisis_Data.ipynb`, jalankan semua sel, dan pastikan file `dashboard/main_data.csv` terbentuk.

### 4 Jalankan Aplikasi Streamlit
```powershell
.\.venv\Scripts\streamlit run dashboard\dashboard.py
```

Aplikasi akan berjalan di `http://localhost:8501`.
