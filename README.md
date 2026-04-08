<div align="center">
  <img src="assets/istinye-logo.png" width="350" alt="İstinye Üniversitesi Logo">
</div>

# Kernel-Level Game Reversing & Analysis 🔬

**Danışman:** Keyvan Arasteh Abbasabad

## İçindekiler
- [🎬 Demo](#-demo-live-execution--analysis)
- [📊 Interactive Timeline](#-interactive-investigation-timeline)
- [🏗️ Architecture](#️-technical-architecture)
- [🛠️ Kullanılan Profesyonel Araçlar](#️-kullanılan-profesyonel-araçlar-toolchain)
- [📂 Repo Yapısı](#-repo-yapısı-ve-mühendislik-disiplini)
- [🔍 Adım Adım Analiz Süreci](#-adım-adım-analiz-süreci-ve-bulgular-video-özeti)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Analysis Mode](https://img.shields.io/badge/Analysis-Kernel%20Ring%200-red)
![Linting](https://img.shields.io/badge/Linting-Flake8-blue)
![Language](https://img.shields.io/badge/Language-EN%20%7C%20TR-blue)

Bu depo, modern bir oyunun Kernel (Ring-0) seviyesinde nasıl çalıştığını, bellek yönetimini ve ağ (TCP) trafiğini analiz eden **uygulamalı tersine mühendislik** projesini içermektedir.

> **🌐 Bilingual Documentation:** The interactive timeline and architecture documents are available in both English and Turkish. / İnteraktif zaman çizelgesi ve mimari belgeler hem İngilizce hem Türkçe olarak mevcuttur.

> **⚠️ Önemli Not:** Bu proje genel amaçlı bir araç değildir. Belirli bir senaryo (dosyasız Ring-0 oyun hilesi) üzerinde gerçekleştirilen uygulamalı adli analiz çalışmasıdır. `scripts/` klasöründeki kodlar bu analiz senaryosu için yazılmıştır. Projeyi genel amaçlı bir forensik araç setine dönüştürmek isterseniz, yol haritasını [`TODO.md`](TODO.md) dosyasından takip edebilirsiniz. **Katkılarınızdan çok memnuniyet duyarız!** 🤝

## 🎬 Demo (Live Execution & Analysis)

Projenin tüm adımlarını, canlı bellek (memory) manipülasyonunu ve araçların kullanımını içeren **10 dakikalık kapsamlı teknik analiz videosu** repoya yüklenmiştir.

▶ **YouTube:** [https://youtu.be/sIuC5Arvtq4](https://youtu.be/sIuC5Arvtq4)

📁 *`demo/` klasöründeki video dosyasına da tıklayabilirsiniz.*

## 📊 Interactive Investigation Timeline

Adli analiz sürecinin **5 aşamasını** görselleştiren interaktif HTML zaman çizelgesi:

- 🎬 **Video Oynatma:** Her bölüm için ▶ butonuyla ilgili zaman damgasından video izleme
- 📸 **14 Ekran Görüntüsü:** ProcMon, Process Hacker, YDArk, WinDbg gibi araçlardan alınmış forensik kanıt çerçeveleri
- 🌙/☀️ **Karanlık/Aydınlık Mod:** LocalStorage ile kalıcı tema geçişi
- 🌐 **EN/TR Dil Desteği:** Tek tıkla İngilizce-Türkçe geçiş

📄 **[Timeline'ı Görüntüle → `docs/timeline.html`](docs/timeline.html)**

## 🏗️ Technical Architecture

Dosyasız Ring-0 enjeksiyon saldırısının **6 aşamalı teknik mimarisi:**

1. **User-Mode Loader** — Polimorfik adla indirilen başlatıcı
2. **Vulnerable Driver Exploitation** — İmzalı 3. parti sürücünün istismarı
3. **Non-Paged Pool Injection** — Çekirdek belleğine kod enjeksiyonu
4. **Fake System Thread** — `nt!PsCreateSystemThread` ile sahte sistem iş parçacığı
5. **DWM.exe Hijacking** — Masaüstü pencere yöneticisine UI enjeksiyonu
6. **Handle Stripping** — Bellek incelemesinin engellenmesi

📄 **[Architecture Belgesini Oku → `docs/architecture.md`](docs/architecture.md)**

## 🛠️ Kullanılan Profesyonel Araçlar (Toolchain)

Bu projede kod hacminden ziyade **teknik derinliğe** ve **canlı çalıştırmaya** odaklanılmıştır. Analiz aşağıdaki endüstri standardı araçlarla yapılmıştır:

| Araç | Kullanım Amacı | Sonuç |
|------|---------------|-------|
| **ProcMon** | Dosya sistemi ve Registry izleme — "Drop & Load" tuzağı | ❌ Disk aktivitesi bulunamadı |
| **Process Hacker** | Süreç ağaçları ve servis taraması | ❌ Şüpheli process yok |
| **YDArk** | Kernel hook ve rootkit tespiti | ❌ Kanca bulunamadı |
| **TCPView** | Ağ trafiği ve C2 bağlantı taraması | ❌ Şüpheli trafik yok |
| **WinDbg** | Post-mortem crash dump analizi | ✅ **Anonim kernel kodu tespit edildi** |
| **Event Viewer** | Sistem günlüğü inceleme | ✅ BSOD düzgün yakalandı |

## 📂 Repo Yapısı ve Mühendislik Disiplini

```
├── demo/                     # 10 dakikalık analiz videosu
├── docs/
│   ├── timeline.html         # İnteraktif forensik zaman çizelgesi (EN/TR)
│   ├── architecture.md       # Teknik mimari analiz belgesi
│   ├── sub.vtt              # Video altyazı transkripti
│   └── frames/              # 14 video çerçevesi ekran görüntüsü
├── scripts/
│   ├── memory_scanner.py     # Windows API bellek okuyucu (ReadProcessMemory)
│   ├── procmon_analyzer.py   # ProcMon CSV log ayrıştırıcı
│   └── injection_poc.cpp     # VirtualAllocEx + CreateRemoteThread PoC
├── yara/
│   └── anti_debug_detect.yar # Anti-debug API ve araç sürücüsü tespit kuralı
├── .github/workflows/        # CI/CD linting pipeline
├── Dockerfile                # Rootless konteyner izolasyonu
├── TODO.md                   # Yol haritası & katkıda bulunma rehberi
└── README.md
```

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

---

## 🤝 Katkıda Bulunma (Contributing)

Bu projeyi geliştirmek veya genel amaçlı bir araç setine dönüştürmek istiyorsanız:

1. 📋 **[TODO.md](TODO.md)** dosyasındaki yol haritasını inceleyin
2. Repoyu fork edin
3. Yeni branch: `git checkout -b feature/your-feature`
4. Commit: `git commit -m 'feat: Add some feature'`
5. Push: `git push origin feature/your-feature`
6. Pull Request açın

> Mevcut bilingual (TR/EN) yorum geleneğini koruyun. Yeni YARA kuralları, analiz scriptleri ve dokümantasyon katkıları özellikle değerlidir.

---

*İstinye Üniversitesi — Tersine Mühendislik Dersi — Danışman: Keyvan Arasteh*
