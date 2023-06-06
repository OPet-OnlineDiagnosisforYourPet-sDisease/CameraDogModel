# Menggunakan base image Python
FROM python:3.8

# Mengatur working directory di dalam container
WORKDIR /app

# Menyalin dependencies ke dalam container
COPY requirements.txt .

# Menginstal dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin aplikasi Flask ke dalam container
COPY . .

# Menjalankan aplikasi Flask ketika container dijalankan
CMD ["python", "app.py"]
