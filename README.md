﻿## Dashboard Analisis Kualitas Udara Beijing

Dashboard ini dikembangkan menggunakan **Streamlit** untuk menganalisis kualitas udara (PM2.5, PM10, SO2, NO2, CO, O3) dari 12 stasiun di Beijing pada periode 2013-2017.

## Pertanyaan Bisnis
- Stasiun mana yang memiliki rata-rata PM2.5 tertinggi pada periode 2013-2017, dan bagaimana perbandingan antar stasiun?
- Bagaimana pola musiman PM2.5 pada periode 2013-2017 (rata-rata bulanan)?
- Bagaimana perbandingan rata-rata polutan lain (PM10, NO2, O3) antar stasiun pada periode 2013-2017?

## Fitur Dashboard
- **Summary**: Ringkasan metrik utama berdasarkan filter yang dipilih.
- **Pola Bulanan (Semua Stasiun)**: Tren bulanan gabungan untuk metrik terpilih.
- **Pola Bulanan per Stasiun**: Tren bulanan per stasiun.
- **Perbandingan Stasiun**: Rata-rata polutan per stasiun.
- **Heatmap Metrik Terpilih (Interaktif)**: Perbandingan nilai rata-rata metrik terpilih per stasiun.
- **Analisis Lanjutan**: Distribusi kategori PM2.5 per musim (jika PM2.5 dipilih) dan boxplot metrik terpilih per stasiun.
- **Filter Interaktif**: Pilih stasiun, rentang tanggal, dan **lebih dari satu** metrik polutan.
- **Tab Terpisah**: Setiap fitur ditampilkan di tab terpisah agar navigasi lebih jelas.

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
