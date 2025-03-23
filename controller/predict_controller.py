import numpy as np
import pandas as pd
import joblib
from fastapi import HTTPException

# Load model yang sudah dilatih (pastikan path benar)
model = joblib.load("model/naive_bayes_model1.pkl")


# Baca file Excel WHO untuk masing-masing kelompok usia
file_path_girl_0_to_2 = 'LHFA_WHO/lhfa_girl_birth_to_2_years.xlsx'
file_path_girl_2_to_5 = 'LHFA_WHO/lhfa_girl_2_to_5_years.xlsx'
file_path_boy_0_to_2 = 'LHFA_WHO/lhfa_boys_birth_to_2_years.xlsx'
file_path_boy_2_to_5 = 'LHFA_WHO/lhfa_boys_2_to_5_years.xlsx'

# Load tabel referensi WHO
antropometri_girl_0_to_2 = pd.read_excel(file_path_girl_0_to_2)
antropometri_girl_2_to_5 = pd.read_excel(file_path_girl_2_to_5)
antropometri_boy_0_to_2 = pd.read_excel(file_path_boy_0_to_2)
antropometri_boy_2_to_5 = pd.read_excel(file_path_boy_2_to_5)

# Fungsi untuk menghitung Z-Score
def calculate_zscore(row):
    """
    Menghitung Z-Score berdasarkan data referensi WHO.
    """
    # Pilih tabel referensi berdasarkan jenis kelamin dan usia
    if row['Age'] < 24:  # Usia < 2 tahun
        antropometri_table = antropometri_girl_0_to_2 if row['Gender'] == 'female' else antropometri_boy_0_to_2
    else:  # Usia 2–5 tahun
        antropometri_table = antropometri_girl_2_to_5 if row['Gender'] == 'female' else antropometri_boy_2_to_5

    # Cari baris yang sesuai berdasarkan usia
    reference = antropometri_table[antropometri_table['Month'] == row['Age']]
    if reference.empty:
        return None  # Jika tidak ada data referensi

    # Ambil nilai referensi
       # Ambil nilai referensi
    try:
        M = reference['M'].values[0]  # Median
        S = reference['SD'].values[0]  # Standar deviasi
    except KeyError as e:
        raise KeyError(f"Kolom referensi tidak ditemukan: {e}")
    X = row['Body Length']

    # Hitung Z-Score
    Z = (X - M) / S
    return float(Z)

# Fungsi untuk menentukan status stunting berdasarkan Z-Score
# def determine_stunting_status(z_score):
#     if z_score is None:
#         return "Unknown"
#     elif z_score > -2:
#         return "NO"
#     else:
#         return "YES"

def get_predict(height: float, age: int, gender: int, breastFeeding: int) -> dict:
    """
    Melakukan prediksi status stunting berdasarkan tinggi, umur, dan jenis kelamin.

    Parameters:
    - height (int): Tinggi badan dalam cm
    - age (int): Umur dalam bulan
    - gender (int): Jenis kelamin (0 = Perempuan, 1 = Laki-laki)

    Returns:
    - dict: Hasil prediksi dalam format JSON
    """
    try:
        if height <= 0 or age <= 0 or gender not in [0, 1] or breastFeeding not in [0, 1]:
            raise ValueError("Input tidak valid. Pastikan height > 0, age > 0, gender ∈ {0, 1}, dan breastFeeding ∈ {0, 1}.")
        
        # Konversi gender ke string untuk kompatibilitas dengan calculate_zscore
        gender_str = 'female' if gender == 0 else 'male'
        
        print(gender_str)

        # Buat dictionary untuk input ke calculate_zscore
        row = {
            'Age': age,
            'Body Length': height,
            'Gender': gender_str
        }
        
        z_score = calculate_zscore(row)
        print(f"ini adalah {z_score}")
        
        # Jika Z-Score tidak dapat dihitung, kembalikan status "Unknown"
        if z_score is None:
            return {"status": "Unknown", "z_score": None}
        
        # Buat array input sesuai fitur yang digunakan saat training
        X_new = np.array([[breastFeeding, z_score]])

        # Lakukan prediksi
        prediction_result = model.predict(X_new)[0]


        return {
            "status": "Berhasil Mendeteksi Status Stunting",
            "result": prediction_result[0]  # Pastikan hasil prediksi dikembalikan dengan benar
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")
    
