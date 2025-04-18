from selenium import webdriver
from selenium.webdriver.common.by import By
import time, re, os, threading
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import telegram
from config import TELEGRAM_TOKEN, CHAT_ID, URL, FIYAT_LIMITI

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

import asyncio
import nest_asyncio
nest_asyncio.apply()

bildirilenler = {}
bot = telegram.Bot(token=TELEGRAM_TOKEN)
LOG_DOSYASI = "fiyat_log.csv"

def fiyat_metni_sayi_cevir(metin):
    try:
        return float(re.sub(r"[^\d,]", "", metin).replace(",", "."))
    except:
        return None

def loga_yaz(urun_adi, fiyat):
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([[zaman, urun_adi, fiyat]], columns=["Zaman", "Urun", "Fiyat"])
    df.to_csv(LOG_DOSYASI, mode='a', index=False, header=not os.path.exists(LOG_DOSYASI))

def grafik_olustur(urun_adi):
    df = pd.read_csv(LOG_DOSYASI)
    df = df[df["Urun"] == urun_adi][-10:]
    if df.empty:
        return None
    plt.figure()
    plt.plot(df["Zaman"], df["Fiyat"], marker="o")
    plt.title(urun_adi)
    plt.xticks(rotation=45)
    plt.ylabel("TL")
    plt.tight_layout()
    grafik_dosya = "fiyat_trend.png"
    plt.savefig(grafik_dosya)
    plt.close()
    return grafik_dosya

def fiyatlari_kontrol_et_bir_kez():
    print("🔍 İlk fiyat kontrolü yapılıyor...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(5)

    urunler = driver.find_elements(By.CLASS_NAME, "product-card")
    for urun in urunler:
        try:
            ad = urun.find_element(By.CLASS_NAME, "product-title").text
            fiyat = urun.find_element(By.CLASS_NAME, "price").text
            fiyat_sayi = fiyat_metni_sayi_cevir(fiyat)
            if fiyat_sayi:
                loga_yaz(ad, fiyat_sayi)
                if fiyat_sayi <= FIYAT_LIMITI and bildirilenler.get(ad) != fiyat_sayi:
                    mesaj = f"💥 {ad}\n💸 {fiyat_sayi} TL altında!"
                    bot.send_message(chat_id=CHAT_ID, text=mesaj)
                    grafik = grafik_olustur(ad)
                    if grafik:
                        bot.send_photo(chat_id=CHAT_ID, photo=open(grafik, 'rb'))
                    bildirilenler[ad] = fiyat_sayi
        except Exception as e:
            print("Hata:", e)

    driver.quit()
    print("✅ İlk kontrol tamamlandı.")

def fiyat_kontrol_surekli():
    while True:
        print("🔁 Saatlik fiyat kontrolü başladı...")
        fiyatlari_kontrol_et_bir_kez()
        print("⏳ 1 saat bekleniyor...\n")
        time.sleep(3600)

# Telegram komutu: /fiyatlar
async def komut_fiyatlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(LOG_DOSYASI):
        await update.message.reply_text("Henüz veri yok!")
        return
    df = pd.read_csv(LOG_DOSYASI)
    son_veriler = df.sort_values("Zaman").groupby("Urun").last().reset_index()
    mesaj = "\n".join([f"{row['Urun']} → {row['Fiyat']} TL" for _, row in son_veriler.iterrows()])
    await update.message.reply_text(mesaj)

async def main():
    # 1️⃣ Önce bir defa fiyatları kontrol et
    fiyatlari_kontrol_et_bir_kez()

    # 2️⃣ Telegram mesajı at
    try:
        await bot.send_message(chat_id=CHAT_ID, text="🤖 Patron! İlk fiyat kontrolü yapıldı, bot çalışmaya başladı.")
    except Exception as e:
        print("Telegram mesajı gönderilemedi:", e)

    # 3️⃣ Telegram bot ayarla
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("fiyatlar", komut_fiyatlar))

    # 4️⃣ Sürekli fiyat kontrolünü başlat
    kontrol_thread = threading.Thread(target=fiyat_kontrol_surekli)
    kontrol_thread.start()

    # 5️⃣ Telegram komutları dinleniyor
    print("💬 Telegram komutları dinleniyor...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
