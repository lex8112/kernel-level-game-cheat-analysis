<div align="center">
  <img src="assets/istinye-logo.png" width="350" alt="İstinye Üniversitesi Logo">
</div>

# Kernel-Level Game Reversing & Analysis 🔬

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Analysis Mode](https://img.shields.io/badge/Analysis-Kernel%20Ring%200-red)
![Linting](https://img.shields.io/badge/Linting-Flake8-blue)

Bu depo, modern bir oyunun Kernel (Ring-0) seviyesinde nasıl çalıştığını, bellek yönetimini ve ağ (TCP) trafiğini analiz eden **uygulamalı tersine mühendislik** projesini içermektedir.

## 🎬 Demo (Live Execution & Analysis)

Projenin tüm adımlarını, canlı bellek (memory) manipülasyonunu ve araçların kullanımını içeren **3-5 dakikalık kapsamlı teknik analiz videosu** repoya yüklenmiştir.
Ayrıca youtube linki: "https://youtu.be/sIuC5Arvtq4"

*`demo/` klasöründeki dosyaya tıklayabilirsiniz.)*


## 🛠️ Kullanılan Profesyonel Araçlar (Toolchain)

Bu projede kod hacminden ziyade **teknik derinliğe** ve **canlı çalıştırmaya** odaklanılmıştır. Analiz aşağıdaki endüstri standardı araçlarla yapılmıştır:

1. **WinDbg:** İşletim sistemi çekirdeği (Kernel) seviyesinde bellek dökümü (memory dump) ve debugging işlemleri.
2. **Process Hacker:** Süreç (process) ağaçlarının, bellek sayfalarının (memory pages) ve handle'ların dinamik analizi.
3. **YDArk:** Anti-rootkit ve kernel seviyesi kanca (hook) tespit mekanizmalarının bypass analizi.
4. **Procmon (Process Monitor):** Dosya sistemi (File System) ve Kayıt Defteri (Registry) aktivitelerinin anlık izlenmesi.
5. **TCPview:** Oyunun sunucularla kurduğu soket bağlantılarının ve ağ trafiği tünellerinin tespiti.

## 📂 Repo Yapısı ve Mühendislik Disiplini

* `scripts/`: Procmon CSV loglarını ve bellek adreslerini analiz eden otomasyon araçları (TODO ve Linting standartlarına uygun).
* `yara/`: Oyunun anti-debug mekanizmalarını tespit eden YARA kuralları.
* `.github/workflows/`: Kod kalitesini (Linting) sürekli denetleyen CI/CD pipeline.
* `Dockerfile`: Analiz araçlarının izolasyonunu sağlayan rootless (yetkisiz) konteyner mimarisi.
