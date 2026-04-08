# TODO — Roadmap & Contribution Guide

> **Bu proje bir araç değildir.** Belirli bir senaryo (dosyasız Ring-0 oyun hilesi) üzerinden yapılan uygulamalı tersine mühendislik analizidir. Ancak bu projeyi genel amaçlı bir araç setine dönüştürmek isterseniz, aşağıdaki yol haritasını takip edebilirsiniz. **Katkılarınızdan memnuniyet duyarız!**

---

## 🔬 Memory Forensics Enhancements

- [ ] **Volatility 3 Integration**: Crash dump (`.dmp`) dosyalarının otomatik analizi
  - `windows.pslist` — Aktif süreç listesi
  - `windows.malfind` — Enjekte edilmiş bellek bölgelerinin tespiti
  - `windows.driverirp` — Şüpheli IRP handler'larının analizi
  - `windows.callbacks` — Kernel callback tablosu dökümü
- [ ] **Non-Paged Pool Scanner**: İmzasız/kayıtsız bellek havuzu tahsislerini tespit eden modül
- [ ] **Orphaned Thread Detector**: `nt!PsCreateSystemThread` ile oluşturulmuş modülsüz sistem thread'lerini bulan araç
- [ ] **Memory Diff Tool**: Hile öncesi/sonrası bellek anlık görüntülerini karşılaştırma

## 🛡️ YARA Rules Expansion

- [ ] **Fileless malware detection**: Non-Paged Pool'da çalışan imzasız kod kalıpları
- [ ] **DWM.exe injection signatures**: dwm.exe'ye enjekte edilmiş şüpheli bellek bölgeleri
- [ ] **Handle stripping patterns**: `ObRegisterCallbacks` ile handle haklarının kaldırılması
- [ ] **Spin lock anomaly detection**: Kernel seviyesinde yüksek IRQL'li spin lock kullanım kalıpları
- [ ] **Packed/encrypted section entropy**: PE dosyasındaki yüksek entropili bölümlerin tespiti
- [ ] **Anti-debug evasion matris**: Daha kapsamlı API çağrı kombinasyonları (NtSetInformationThread, NtClose w/ invalid handle, INT 2D)

## 🔎 ProcMon Analyzer Improvements

- [ ] **Multiprocessing desteği**: 1GB+ CSV dosyaları için paralel işlem
- [ ] **JSON export**: Elasticsearch/Splunk entegrasyonu için yapılandırılmış çıktı
- [ ] **Real-time mode**: ProcMon canlı veri akışını okuma (ETW Consumer)
- [ ] **Timeline correlation**: ProcMon olaylarını video zaman damgalarıyla eşleştirme
- [ ] **Suspicious pattern alerting**: Bilinen kötü amaçlı kalıplar için otomatik uyarı sistemi

## 🧠 WinDbg Automation

- [ ] **Automated crash analysis script**: `.dmp` dosyasını alıp otomatik rapor üreten WinDbg script
  ```
  !analyze -v
  !process 0 0
  !thread
  !pool
  lm (module listing)
  ```
- [ ] **BugCheck code database**: Yaygın BSOD kodlarını açıklamalarıyla eşleştiren veritabanı
- [ ] **Stack trace visualizer**: WinDbg çıktısını görsel call graph'a dönüştürme
- [ ] **Anonymous memory region mapper**: Modül ile eşleşmeyen bellek bölgelerini haritalama

## 🌐 Network Forensics

- [ ] **Wireshark/tshark integration**: PCAP dosyaları üzerinden otomatik C2 bağlantı analizi
- [ ] **DNS sinkhole detection**: Şüpheli domain çözümlemelerinin tespiti
- [ ] **Encrypted traffic analysis**: TLS fingerprinting (JA3/JA4) ile bilinen kötü amaçlı istemci tespiti
- [ ] **TCPView export parser**: TCPView verilerini yapılandırılmış formata dönüştürme

## 🏗️ Architecture & Documentation

- [ ] **Mermaid diyagramları**: `architecture.md`'deki ASCII diyagramlarını interaktif Mermaid diyagramlarına dönüştürme
- [ ] **Attack tree modeli**: MITRE ATT&CK framework'ü ile eşleştirilmiş saldırı ağacı
- [ ] **Video bölüm indeksi**: Zaman damgalı arama yapılabilir altyazı veritabanı
- [ ] **Defense playbook**: Her saldırı aşaması için savunma stratejileri ve IOC'ler

## 🐳 Infrastructure

- [ ] **Docker Compose**: Tüm analiz araçlarını (Volatility, YARA, Python scripts) içeren tek komutla çalışan ortam
- [ ] **CI/CD pipeline enhancements**:
  - YARA kural doğrulama (syntax check)
  - Python lint (flake8 + mypy)
  - C++ static analysis (cppcheck)
  - Markdown lint
- [ ] **GitHub Actions**: PR açıldığında otomatik YARA kural testi
- [ ] **Dependabot**: Python bağımlılıklarının güvenlik güncellemeleri

## 🎓 Educational Content

- [ ] **Lab ortamı kurulumu**: Analiz için güvenli sanal makine yapılandırma rehberi
- [ ] **Adım adım workshop**: Her araç için etkileşimli alıştırmalar
- [ ] **Quiz sistemi**: Forensik bulguları test eden çoktan seçmeli sorular
- [ ] **Glossary / Sözlük**: Kernel forensics terimleri (İngilizce-Türkçe)

## 📊 Reporting & Visualization

- [ ] **HTML rapor oluşturucu**: Tüm bulguları tek sayfalık interaktif rapora dönüştürme
- [ ] **PDF export**: Akademik sunum için formatlanmış PDF rapor
- [ ] **IOC export**: STIX/TAXII formatında tehdit göstergeleri

---

## 🤝 Contributing / Katkıda Bulunma

Bu projeye katkıda bulunmak istiyorsanız:

1. Repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/your-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add some feature'`)
4. Branch'inizi push edin (`git push origin feature/your-feature`)
5. Pull Request açın

> **Not:** Lütfen mevcut kod stilini ve Türkçe/İngilizce bilingual yorum geleneğini koruyun.

---

*İstinye Üniversitesi — Tersine Mühendislik Dersi — Danışman: Keyvan Arasteh*
