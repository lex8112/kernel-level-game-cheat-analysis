<div align="center">
  <img src="assets/istinye-logo.png" width="350" alt="İstinye Üniversitesi Logo">
</div>

# Kernel-Level Game Reversing & Analysis 🔬

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Analysis Mode](https://img.shields.io/badge/Analysis-Kernel%20Ring%200-red)
![Linting](https://img.shields.io/badge/Linting-Flake8-blue)

Bu depo, modern bir oyunun Kernel (Ring-0) seviyesinde nasıl çalıştığını, bellek yönetimini ve ağ (TCP) trafiğini analiz eden **uygulamalı tersine mühendislik** projesini içermektedir.

## 🎬 Demo (Live Execution & Analysis)

Projenin tüm adımlarını, canlı bellek (memory) manipülasyonunu ve araçların kullanımını içeren **10 dakikalık kapsamlı teknik analiz videosu** repoya yüklenmiştir.
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

* ## 🔍 Adım Adım Analiz Süreci ve Bulgular (Video Özeti)

[cite_start]Bu projede, güvenlik açığı bulunan meşru sürücüleri (vulnerable drivers) istismar ederek Kernel (Ring-0) seviyesine inen gelişmiş bir hile/malware yazılımı analiz edilmiştir[cite: 14, 17]. [cite_start]Yazılımın, işletim sistemini manipüle ederek doğrudan çekirdeğe komutlar gönderdiği tespit edilmiştir[cite: 18]. Analiz adımları ve bulgular aşağıda özetlenmiştir:

* **Aşama 1: Davranışsal Analiz ve BSOD Tetiklenmesi**
  [cite_start]Zararlı yazılım (.exe) her çalıştırıldığında polimorfik olarak adını değiştirmekte [cite: 28] [cite_start]ve Görev Yöneticisi (Task Manager) aracılığıyla sonlandırılamamaktadır[cite: 31]. [cite_start]Sistem yeniden başlatılmaya veya süreç zorla kapatılmaya çalışıldığında, sistem koruma mekanizmaları tetiklenerek kernel seviyesinde Mavi Ekran (BSOD) hatası vermektedir[cite: 32].

* **Aşama 2: ProcMon ile Dinamik "Drop & Load" Taraması**
  [cite_start]Bu tür yazılımların genellikle diske imzasız/zararlı bir `.sys` dosyası bırakıp hemen sildiği "Drop and Load" tekniğini yakalamak için Sysinternals Process Monitor (Procmon) kullanılmıştır[cite: 40]. [cite_start]Sıkı dosya yazma (WriteFile) filtreleri uygulanmasına rağmen diskte hiçbir sürücü izine rastlanmamıştır[cite: 42, 45]. [cite_start]Bu durum, zararlının tamamen bellekte (memory-based/fileless) çalıştığını göstermektedir[cite: 46].

* **Aşama 3: Process Hacker ile Süreç (Process) Hijacking Tespiti**
  [cite_start]Process Hacker üzerinden şüpheli, debug edilen (mor) veya yetkisi yükseltilmiş (turuncu) süreçler analiz edilmiştir[cite: 48, 51]. [cite_start]Doğrudan şüpheli bir süreç bulunamamasına rağmen, "Find Window" aracıyla yapılan incelemede hilenin kendisini Windows'un Masaüstü Pencere Yöneticisi olan `dwm.exe` içerisine gizlediği (Process Hijacking) tespit edilmiştir[cite: 57, 58, 60].

* **Aşama 4: YDArk ve TCPView ile Derin Tarama**
  [cite_start]YDArk kullanılarak kernel modundaki System Callbacks, Notify Routines ve kancalar (hooks) incelenmiş; imzasız veya modül ismi eksik olan sürücüler aranmıştır[cite: 67, 68, 72]. [cite_start]Ayrıca TCPView ile olası bir uzak sunucu (C2) bağlantısı veya payload indirme işlemi için ağ trafiği dinlenmiştir[cite: 76, 77]. [cite_start]Yazılımın kendini Kernel içinde çok iyi kamufle etmesi nedeniyle bu aşamalarda standart anomaliler saptanamamıştır[cite: 75, 81].

* **Aşama 5: WinDbg ile Post-Mortem Crash (Memory Dump) Analizi**
  [cite_start]Zararlının canlı yakalanamaması üzerine, sistem kasıtlı olarak mavi ekrana (BSOD) düşürülmüş ve RAM'in anlık görüntüsünü içeren `memory.dmp` dosyası elde edilmiştir[cite: 82, 83]. [cite_start]WinDbg üzerinden yapılan analizde "1e" Bugcheck kodu (Kernel modunda yetkisiz bellek erişimi) tespit edilmiştir[cite: 91, 92]. 

* **Sonuç ve Kernel-Ring 0 Tehdit Modeli:**
  [cite_start]`BUGCHECK_P2` parametresi ile çökmenin yaşandığı bellek adresi bulunmuş ancak bu adrese bağlı hiçbir sürücü modülüne rastlanmamıştır[cite: 93, 95, 96]. [cite_start]Hilenin veri okuma/yazma esnasında multi-threading "Lock" (Kilitleme) mekanizması kullandığı; zorla kapatıldığında boşluğa düşen bu kilitli bellek adreslerinin sistemin çökmesine neden olduğu anlaşılmıştır[cite: 100, 102, 103]. [cite_start]Zararlının diske dosya bırakmak yerine doğrudan Windows süreç yöneticisi (`nt!ps`) üzerinden kendi sahte "Sistem İş parçacıklarını (System Thread)" yaratarak bir "hayalet" gibi çalıştığı kanıtlanmıştır[cite: 106, 108]. [cite_start]Bu durum, geleneksel antivirüslerin (sadece diski tarayan) etkisiz kaldığını ve Ring-0 seviyesinde koruma gerektiğini (Vanguard vb.) doğrulamaktadır[cite: 109, 115, 118].
