# Reverse Engineering Sandbox (Rootless)
FROM python:3.10-slim

# Güvenlik için yetkisiz kullanıcı oluşturma
RUN groupadd -r analyst && useradd -r -g analyst -m analyst

WORKDIR /sandbox

# Gerekli kütüphanelerin kurulumu (Simülasyon)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=analyst:analyst . .

USER analyst

# 2. Adımda yazdığımız scripti tetikleyici olarak ayarlıyoruz
ENTRYPOINT ["python", "./scripts/memory_scanner.py"]
