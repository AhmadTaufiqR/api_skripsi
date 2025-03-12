import numpy as np
import joblib
from fastapi import HTTPException

# Load model yang sudah dilatih (pastikan path benar)
model = joblib.load("model/naive_bayes_model.pkl")

def get_predict(height: float, age: int, gender: int) -> dict:
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
        # Hitung rasio tinggi/umur
        ratio = height / age

        # Buat array input sesuai fitur yang digunakan saat training
        X_new = np.array([[height, age, gender, ratio]])

        # Lakukan prediksi
        prediction_result = model.predict(X_new)

        return {
            "status": "Berhasil Mendeteksi Status Stunting",
            "result": prediction_result[0]  # Pastikan hasil prediksi dikembalikan dengan benar
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")
