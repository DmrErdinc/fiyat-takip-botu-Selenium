
<h1 align="center">💸 Fiyat Takip Botu</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue?logo=python">
  <img src="https://img.shields.io/badge/selenium-active-brightgreen?logo=selenium">
  <img src="https://img.shields.io/badge/telegram-bot-orange?logo=telegram">
</p>

<p align="center">
  <b>Hepsiburada gibi sitelerde ürün fiyatlarını takip eden,<br>
  fiyat düşünce sana Telegram'dan mesaj atan tam otomatik fırsat botu!</b>
</p>

---

## 🚀 Özellikler

- 🔎 Kategori sayfasındaki tüm ürünleri tarar  
- 📉 Fiyat eşik değerin altına inince otomatik uyarı gönderir  
- 💬 Telegram üzerinden `/fiyatlar` komutuna cevap verir  
- 📊 Fiyat geçmişini `CSV` dosyasına loglar  
- 📈 Son 10 fiyat değişimini grafikle gösterir  
- 🧠 Aynı fiyatı tekrar tekrar bildirmez  

---

## 🖼️ Görsel Tanıtım

<p align="center">
  <img src="https://i.imgur.com/6lQnTRq.png" alt="Telegram Örneği" width="600">
  <br><i>Telegram üzerinden gelen uyarı mesajı ve grafik örneği</i>
</p>

---

## ⚙️ Kurulum

```bash
pip install selenium python-telegram-bot pandas matplotlib nest_asyncio
```

1. Tarayıcına uygun WebDriver indir ([ChromeDriver](https://sites.google.com/chromium.org/driver/))  
2. `chromedriver.exe` dosyasını proje klasörüne yerleştir  
3. `config.py` dosyasını aşağıdaki gibi doldur:

```python
TELEGRAM_TOKEN = "BOT_TOKENINIZ"
CHAT_ID = 123456789
URL = "https://www.hepsiburada.com/ara?q=bilgisayar&markalar=asus"
FIYAT_LIMITI = 20000
```

4. Botu başlat:

```bash
python fiyat_takip.py
```

---

## 🔧 Kullanım

| Komut       | Açıklama                                   |
|-------------|--------------------------------------------|
| `/fiyatlar` | Güncel tüm ürün fiyatlarını listeler       |
| Başlangıçta | Bot çalışır çalışmaz tüm fiyatları kontrol eder, ardından saatlik döngü başlatır |

---

## 📝 Dosya Yapısı

```bash
.
├── config.py
├── fiyat_takip.py
├── fiyat_log.csv          # Otomatik oluşur
├── fiyat_trend.png        # Grafik olarak gönderilir
└── chromedriver.exe       # WebDriver
```

---

## 👨‍💻 Geliştirici Notu

Bu proje Rojda’ya adanmış olabilir 😄  
İstersen `.exe` haline getirme, cron job’a bağlama veya farklı sitelere entegre etme desteği verilir.

---

## ⚠️ Uyarı

Bu bot sadece kişisel kullanım için tasarlanmıştır.  
Yoğun isteklerde e-ticaret siteleri tarafından engellenebilirsin. Fiyat kontrol aralıklarını abartma 😇

---

<p align="center">
  Made with ❤️ by <b>ChatGPT & Erdinç</b>
</p>
