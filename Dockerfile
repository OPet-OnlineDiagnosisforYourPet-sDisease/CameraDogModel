# Gunakan base image Python yang sesuai dengan versi Python yang Anda gunakan
FROM python:3.9

# Set working directory di dalam kontainer
WORKDIR /app

# Salin file requirements.txt ke dalam kontainer
COPY requirements.txt .

# Install dependensi yang diperlukan
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh konten aplikasi ke dalam kontainer
COPY . .

# Expose port yang digunakan oleh aplikasi (sesuaikan dengan port yang digunakan dalam aplikasi Anda)
EXPOSE 8080

# Jalankan perintah untuk menjalankan aplikasi ketika kontainer berjalan
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
