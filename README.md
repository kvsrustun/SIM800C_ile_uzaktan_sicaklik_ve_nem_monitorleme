# 🌐 SIM800C GSM/GPRS ile Uzaktan Sıcaklık ve Nem Monitörleme

<p align="center">
  <img src="https://img.shields.io/badge/Donanım-Deneyap%20Kart-007acc?style=for-the-badge&logo=espressif&logoColor=white" alt="Donanım" />
  <img src="https://img.shields.io/badge/GSM%20Modülü-SIM800C%20GPRS-e11d48?style=for-the-badge" alt="GSM" />
  <img src="https://img.shields.io/badge/Sensör-Sıcaklık%20%26%20Nem-059669?style=for-the-badge" alt="Sensör" />
  <img src="https://img.shields.io/badge/Backend-PHP-777BB4?style=for-the-badge&logo=php&logoColor=white" alt="PHP" />
  <img src="https://img.shields.io/badge/Dashboard-Python%20%26%20Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Lisans-MIT-brightgreen?style=for-the-badge" alt="Lisans" />
</p>

> **Wi-Fi veya sabit internet altyapısının bulunmadığı tarım, sera ve açık saha alanlarında;** Deneyap Kart ve **SIM800C GSM/GPRS** modülü üzerinden hücresel veriyle uzak sunucuya aktarılan telemetri verilerinin, **Python (Streamlit)** tabanlı interaktif web kokpitinde anlık grafikler ve anomali uyarılarıyla canlı izlenmesini sağlayan uçtan uca IoT izleme sistemi.

---

<a id="icindekiler"></a>
## 📑 İçindekiler

1. [Proje Özeti ve Temel Özellikler](#proje-ozeti)
2. [Canlı Web Kokpiti ve Ekran Görüntüleri](#ekran-goruntuleri)
3. [Uçtan Uca Sistem Mimarisi](#sistem-mimarisi)
4. [Kullanılan Donanımlar ve Pin Bağlantıları](#donanim-ve-baglantilar)
5. [Yazılım Mimarisi (Gömülü, PHP API, Streamlit)](#yazilim-mimarisi)
6. [Kurulum ve Çalıştırma Rehberi](#kurulum-ve-calistirma)
7. [Karşılaşılabilecek Sorunlar ve Çözümleri](#sorunlar-ve-cozumleri)
8. [Geliştirici](#gelistirici)
9. [Lisans](#lisans)

---

<a id="proje-ozeti"></a>
## 🎯 1. Proje Özeti ve Temel Özellikler

Bu proje, internet kablosu veya Wi-Fi erişimi olmayan izole bölgelerde çevresel parametrelerin uzaktan güvenle takip edilmesi için tasarlanmıştır:

- **Hücresel Ağ Üzerinden İletişim:** SIM800C modülü ve SIM kart üzerinden GPRS mobil internet (Vodafone / Turkcell / TT) kullanılarak HTTP GET istekleriyle veriler buluta taşınır.
- **Sürekli Loglama & Doğrulama (PHP):** Uzak sunucudaki `kevser.php` uç noktası verileri doğrular, zaman damgası ekler ve güvenli dosya kilitleme (`LOCK_EX`) ile kaydeder.
- **İnteraktif Web Kokpiti (Streamlit):** Kullanıcı dostu arayüz ile veriler canlı olarak çekilir, Regex ve Pandas ile filtrelenir.
- **Zaman Serisi Grafikleri (Altair):** Sıcaklık ve nem değerleri milisaniyelik zaman ekseninde etkileşimli eğrilerle çizilir.
- **Eşik Değeri Uyarı Bildirimi:** Sıcaklık tehlikeli seviyeleri aştığında (Örn: > 70 °C) kullanıcıya anlık sarı uyarı kutusuyla bildirilir.
- **CSV Olarak İndirme:** Seçilen tarih aralığındaki tüm kayıtlar tek tıkla Excel/CSV formatında dışa aktarılabilir.

---

<a id="ekran-goruntuleri"></a>
## 📸 2. Canlı Web Kokpiti ve Ekran Görüntüleri

> 💡 **Arayüz Tanıtımı:** Streamlit ile geliştirilmiş karanlık mod (dark theme) analitik panelinden canlı ekran görüntüleri:

### 📋 1. Filtrelenmiş Veri Tablosu, Tarih Filtresi & Yüksek Sıcaklık Uyarısı
<p align="center">
  <!-- Resmi sürükle-bırak yaptığında GitHub'ın vereceği linki buradaki src kısmına yapıştırabilirsin -->
<img width="1884" height="843" alt="Ekran görüntüsü 2025-10-10 101302" src="https://github.com/user-attachments/assets/ed7986d8-a835-4e48-a4e9-b68b7d652bcf" />
  <br/><em>Tarih aralığı seçici, kritik sıcaklık uyarı bildirimi ve filtrelenmiş telemetri tablosu</em>
</p>

### 📈 2. Zaman Serisi Sıcaklık ve Nem Grafikleri
<div align="center">
  <table>
    <tr>
      <td width="50%" align="center" valign="top">
        <b>🌡️ Sıcaklık - Zaman Eğrisi</b><br/><br/>
<img width="1893" height="624" alt="Ekran görüntüsü 2025-10-10 101313" src="https://github.com/user-attachments/assets/408993b1-72da-460f-9bcc-1fa5440ad710" />
        <br/><br/><em>Anlık sıcaklık değişimleri ve pik noktaları (Altair)</em>
      </td>
      <td width="50%" align="center" valign="top">
        <b>💧 Nem - Zaman Eğrisi</b><br/><br/>
<img width="1869" height="584" alt="Ekran görüntüsü 2025-10-10 101323" src="https://github.com/user-attachments/assets/5d0deee4-d7c6-44e9-b811-817abf4c1d24" />        <br/><br/><em>Ortam bağıl nem yüzdesi (%) zaman serisi takibi</em>
      </td>
    </tr>
  </table>
</div>

---

<a id="sistem-mimarisi"></a>
## 🔄 3. Uçtan Uca Sistem Mimarisi

```text
 [ Deneyap Sensör ]
        │ (I2C)
        ▼
 [ Deneyap Kart ] ──(UART AT Komutları)──► [ SIM800C GSM Modülü ]
                                                    │
                                                    ▼ (GPRS / 2G Mobil Veri)
                                           [ Bulut Sunucu (HTTP GET) ]
                                                    │
                                                    ▼
                                            [ kevser.php API ]
                                                    │ (Yazma & Kilitleme)
                                                    ▼
                                            [ kevser.txt Log ]
                                                    │ (HTTP İstek & Regex)
                                                    ▼
                                       [ Python Streamlit Kokpiti ]
                                         (Tablo, Grafikler, CSV İndir)
```

---

<a id="donanim-ve-baglantilar"></a>
## 🧰 4. Kullanılan Donanımlar ve Pin Bağlantıları

| Bileşen | Model / Açıklama | Görev |
| :--- | :--- | :--- |
| **Ana İşlemci** | Deneyap Kart | Sensör okuma ve AT komutları yönetimi |
| **GSM Modülü** | SIM800C GSM/GPRS Modülü | Mobil ağa bağlanarak buluta HTTP GET gönderme |
| **Sensör** | Deneyap Sıcaklık ve Nem Ölçer | Ortamın sıcaklık (°C) ve bağıl nem (%) ölçümü |
| **SIM Kart** | Standart 2G Destekli Mobil Hat | GPRS internet veri paketi |

### Pin Haritası
```text
+-----------------------------------+              +-----------------------------+
|          Deneyap Kart             |              |        Modül / Sensör       |
|                                   |              |                             |
|  D8 (SoftwareSerial RX)           |<------------>| SIM800C TX Pini             |
|  D14 (SoftwareSerial TX)          |------------->| SIM800C RX Pini             |
|  I2C Hatları (SDA / SCL)          |<------------>| Sıcaklık ve Nem Sensörü     |
|  5V (VCC) / 3.3V                  |------------->| Sensör ve SIM800C Beslemesi |
|  GND                              |<------------>| Ortak GND Toprak Hattı      |
+-----------------------------------+              +-----------------------------+
```

> ⚠️ **Önemli Güç İpucu:** SIM800C modülü şebekeye bağlanırken ve veri aktarırken anlık **2 Amper'e varan pik akım** çekebilir. Kararlı çalışması için modülün yeterli akım verebilen bir güç kaynağı ile beslenmesi önerilir.

---

<a id="yazilim-mimarisi"></a>
## 💻 5. Yazılım Mimarisi

- **Gömülü Yazılım (`SIM800C_ile_uzaktan_sicaklik_ve_nem_monitorleme.ino`):**
  - Sensörden I2C üzerinden sıcaklık ve nem okunur.
  - `AT+SAPBR` komutlarıyla APN yapılandırılır ve GPRS oturumu başlatılır.
  - `AT+HTTPINIT` ve `AT+HTTPACTION=0` komutlarıyla PHP endpoint'ine GET isteği fırlatılır.
- **Backend API (`kevser.php`):**
  - Gelen GET parametreleri regex ile filtrelenir ve doğrulanır.
  - Zaman damgası eklenerek `kevser.txt` dosyasına eklenir (`FILE_APPEND | LOCK_EX`).
- **Ön Yüz Kokpiti (`app1.py`):**
  - Streamlit web çatısı üzerinde çalışır.
  - Pandas ile veri çerçevesine dönüştürülür, Altair kütüphanesi ile interaktif çizgi grafiklerine dönüştürülür.

---

<a id="kurulum-ve-calistirma"></a>
## 🚀 6. Kurulum ve Çalıştırma Rehberi

### 1. Arduino / Deneyap Kodunu Yükleme
1. Arduino IDE ile `SIM800C_ile_uzaktan_sicaklik_ve_nem_monitorleme.ino` dosyasını açın.
2. Kullandığınız operatöre göre APN bilgisini düzenleyin:
   ```cpp
   sendAT("AT+SAPBR=3,1,\"APN\",\"vodafone\"", 1000); // veya "internet", "turkcell"
   ```
3. Kodu Deneyap Kart'a yükleyin ve Seri Monitör'den GPRS bağlantı onayını (`+SAPBR: 1,1`) gözlemleyin.

### 2. Streamlit Web Dashboard'unu Başlatma
```bash
# Gerekli kütüphaneleri yükleyin
pip install streamlit pandas requests altair

# Dashboard'u başlatın
streamlit run app1.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresi açılacaktır.

---

<a id="sorunlar-ve-cozumleri"></a>
## ⚠️ 7. Karşılaşılabilecek Sorunlar ve Çözümleri

### 1. "+SAPBR: 1,3" veya GPRS Bağlantı Hatası
- **Neden:** SIM kartta PIN kodu aktif olabilir veya APN ayarı operatörle uyuşmuyordur.
- **Çözüm:** SIM kartı telefona takıp PIN kodu sorgusunu kaldırın. Kullandığınız hatta göre APN adını (`internet`, `vodafone`, `mgbs`) kontrol edin.

### 2. Modül Reset Atıyor / Şebekeden Düşüyor
- **Neden:** SIM800C veri gönderirken anlık yüksek akım çeker.
- **Çözüm:** Modül besleme hattına paralel bir 1000µF elektrolitik kondansatör bağlayın veya harici 5V 2A adaptör kullanın.

---

<a id="gelistirici"></a>
## 👩‍💻 8. Geliştirici

**Kevser ÜSTÜN**  
🎓 Giresun Üniversitesi — Bilgisayar Mühendisliği  
🔗 [GitHub Profilim](https://github.com/kvsrustun)

---

<a id="lisans"></a>
## 📄 9. Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında açık kaynak olarak paylaşılmıştır.

