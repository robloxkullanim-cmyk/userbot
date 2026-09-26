import asyncio
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import FloodWait
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 1. Kendi Hesabın (Userbot Bilgileri)
API_ID = 34285857
API_HASH = "cbdd983527af284d64655b5592fdb515"

# 2. Telegram Bot Token'ın
BOT_TOKEN = "8824951755:AAEkxb25LsXQvLUkIzwNspklWI2oKhIKhpI"

# Admin ID'leri (Sen ve arkadaşın)
ADMIN_IDS = [8169536869, 8274327683]

# Pyrogram Userbot İstemcisi
userbot = Client("jesuss", api_id=API_ID, api_hash=API_HASH)

# Listeler
groups = []
blacklist = []  # Mesaj gitmeyecek yasaklı grup ID'leri

is_running = False
GROUP_DELAY = 5  
LOOP_INTERVAL = 35 * 60  # Varsayılan döngü süresi (saniye)

# Güvenli Çalışma Saatleri (Örn: Sabah 08:00 - Gece 01:00 arası)
START_HOUR = 8
END_HOUR = 1

# Kullanıcı giriş durumlarını takip sözlükleri
waiting_for_custom_time = {}
waiting_for_custom_delay = {}
waiting_for_new_text = {}
waiting_for_blacklist = {}

# Gönderilecek reklam metni (Varsayılan)
MESSAGE_TEXT = """🔤🔤🔤🔤 🔤🔤🔤🔤🔤
𝗬𝗘𝗠𝗘𝗞𝗦𝗘𝗣𝗘𝗧𝗜‌,𝗛𝗘𝗣𝗘𝗦𝗜‌𝗕𝗨𝗥𝗔𝗗𝗔 𝗡𝟭𝟭 𝗕𝗔𝗞𝗜‌𝗬𝗘 𝗬𝗨‌𝗞𝗟𝗘𝗠𝗘
𝟯.𝟬𝟬𝟬 𝗧𝗟 - 𝟱𝟬0 𝗧𝗟 
𝟱.𝟬𝟬𝟬 𝗧𝗟 - 𝟴𝟬0 𝗧𝗟 
𝟳.𝟬𝟬𝟬 𝗧𝗟 - 𝟭.𝟮𝟬𝟬 𝗧𝗟

𝗕𝗔𝗛𝗜‌𝗦 𝗦𝗜‌𝗧𝗘𝗟𝗘𝗥𝗜‌𝗡𝗘 𝗩𝗘 𝗞𝗥𝗜‌𝗣𝗧𝗢 𝗛𝗘𝗦𝗔𝗣𝗟𝗔𝗥𝗜𝗡𝗔 𝗕𝗔𝗞𝗜‌𝗬𝗘 𝗬𝗨‌𝗞𝗟𝗘𝗡𝗜‌𝗥 

𝟯.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 600 ₺ 
𝟲.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 900 ₺ 
𝟴.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 1.500 ₺ 
𝟭𝟬.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 2.700 ₺ 
𝟮𝟬.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 3.200 ₺ 
𝟯0.000 𝗯𝗮𝗸𝗶𝘆𝗲 - 4.000 ₺

𝗜‌𝗣𝗛𝗢𝗡𝗘 𝗨‌𝗥𝗨‌𝗡𝗟𝗘𝗥𝗜‌ 𝗨𝗬𝗚𝗨𝗡𝗔 𝗚𝗘𝗖‌𝗜‌𝗟𝗜‌𝗥

𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟭 - 5.000 ₺ 
𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟮- 10.000 (𝘁𝘂‌𝗸𝗲𝗻𝗱𝗶 ) 
𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟯 - 15.000 ₺
𝗜‌𝗣𝗛𝗢𝗡𝗘𝟭𝟰- 25.000 (𝘁𝘂‌𝗸𝗲𝗻𝗱𝗶 ) 
𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟱 - 35.000 ₺

DİĞER TÜM İŞLEMLER “

𝗣𝗨𝗕𝗚 𝗠𝗢𝗕𝗜‌𝗟 𝗨𝗖 𝗬𝗨‌𝗞𝗟𝗘𝗡𝗜‌𝗥

𝗧𝗘𝗞 𝗨𝗬𝗚𝗨𝗟𝗔𝗠𝗔𝗗𝗔 𝗕𝗨‌𝗧𝗨‌𝗡 𝗛𝗔𝗖𝗞 𝗔𝗥𝗔𝗖‌𝗟𝗔𝗥𝗜 𝗩𝗘 𝗘𝗚‌𝗜‌𝗧𝗜‌𝗠 𝗦𝗘𝗧𝗜‌ 

𝗜‌𝗡𝗙𝗟𝗨 𝗖𝗖 𝗕𝗨𝗟𝗨𝗡𝗨𝗥 𝗧𝗥 - 𝗬𝗗

📱 📱 WhatsApp & Telegram Fake No Sağlanır

𝗜‌𝗟𝗘𝗧𝗜‌𝗦‌𝗜‌𝗠 : @keinmedyaaa 💠"""

def get_main_keyboard():
  status_text = "🟢 Döngü Aktif (Durdur)" if is_running else "🚀 Döngüyü Başlat"
  return InlineKeyboardMarkup([
      [InlineKeyboardButton(status_text, callback_data="toggle_loop")],
      [InlineKeyboardButton("🚀 Tek Seferlik At (/at)", callback_data="btn_at")],
      [InlineKeyboardButton("🧪 Bana Test Mesajı At", callback_data="btn_test")],
      [InlineKeyboardButton("✏️ Reklam Metnini Değiştir", callback_data="btn_change_text")],
      [InlineKeyboardButton("⏱️ Döngü Süresini Belirle (Dk)", callback_data="btn_custom_time")],
      [InlineKeyboardButton("⚡ Grup Gecikmesini Belirle (Sn)", callback_data="btn_custom_delay")],
      [InlineKeyboardButton("🚫 Kara Listeye Grup Ekle", callback_data="btn_add_blacklist")],
      [InlineKeyboardButton("📋 Ekli Gruplar & Kara Liste", callback_data="btn_liste")],
      [InlineKeyboardButton("⚙️ Bot Ayarları / Durum", callback_data="btn_ayar")],
      [InlineKeyboardButton("❌ Paneli Kapat", callback_data="btn_kapat")],
  ])

# 🔄 Garanti ve Hızlı Grup Çekme Fonksiyonu
async def fetch_folder_groups(client):
  global groups
  groups.clear()
  print("🔄 Sohbetler taranıyor...")
  
  async for dialog in client.get_dialogs(limit=300):
    chat_type = str(dialog.chat.type)
    if "group" in chat_type.lower():
      if dialog.chat.id not in blacklist:
        groups.append(dialog.chat.id)
      
  print(f"✨ Toplam {len(groups)} geçerli grup yüklendi!")

# 🕒 Saat kontrolü (Gece botu durdurmak için)
def is_working_hour():
  current_hour = datetime.now().hour
  if START_HOUR < END_HOUR:
    return START_HOUR <= current_hour < END_HOUR
  else:  # Gece yarısını aşan saatler için (Örn: 08:00 - 01:00 arası)
    return current_hour >= START_HOUR or current_hour < END_HOUR

# 🚀 Canlı Sayaçlı Tek Seferlik Gönderim
async def send_single_batch_background(context: ContextTypes.DEFAULT_TYPE, chat_id):
  if not groups:
    await context.bot.send_message(chat_id=chat_id, text="❌ **Grup bulunamadı!**")
    return

  status_msg = await context.bot.send_message(chat_id=chat_id, text="🚀 **Canlı gönderim başlatıldı...**")

  success_count = 0
  fail_count = 0
  total_groups = len(groups)
  
  for index, chat_id_item in enumerate(groups, 1):
    if chat_id_item in blacklist:
      continue
    try:
      await userbot.send_message(chat_id_item, MESSAGE_TEXT)
      success_count += 1
      
      # Her 5 grupta bir veya son grupta arayüzü güncelle
      if index % 5 == 0 or index == total_groups:
        await status_msg.edit_text(f"⏳ **Gönderim Yapılıyor...**\n📊 İlerleme: {index}/{total_groups} grup\n✅ Başarılı: {success_count}\n❌ Hatalı: {fail_count}")
        
      await asyncio.sleep(GROUP_DELAY)
    except FloodWait as e:
      await asyncio.sleep(e.value)
    except Exception:
      fail_count += 1

  await status_msg.edit_text(
      f"📊 **Toplu Gönderim Raporu Tamamlandı!**\n\n"
      f"• Hedeflenen Grup: {total_groups}\n"
      f"• Başarılı: {success_count}\n"
      f"• Hatalı/Engelli: {fail_count}"
  )

# 🔄 Arka Plan Döngüsü (Saat ve Kara Liste Kontrollü)
async def background_loop(context: ContextTypes.DEFAULT_TYPE, chat_id):
  global is_running, LOOP_INTERVAL
  while is_running:
    if not is_working_hour():
      await asyncio.sleep(300)
      continue

    if not groups:
      await asyncio.sleep(60)
      continue

    # Her döngü başında listeyi otomatik tazele
    await fetch_folder_groups(userbot)

    for chat_id_item in groups:
      if not is_running:
        break
      if chat_id_item in blacklist:
        continue
      try:
        await userbot.send_message(chat_id_item, MESSAGE_TEXT)
        await asyncio.sleep(GROUP_DELAY)
      except FloodWait as e:
        await asyncio.sleep(e.value)
      except Exception:
        pass

    for _ in range(LOOP_INTERVAL):
      if not is_running:
        break
      await asyncio.sleep(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.effective_user.id not in ADMIN_IDS:
    return
  await update.message.reply_text("🎛️ **Ultimate Reklam Botu Paneli**", reply_markup=get_main_keyboard())

async def at_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.effective_user.id not in ADMIN_IDS:
    return
  asyncio.create_task(send_single_batch_background(context, update.effective_chat.id))
  await update.message.reply_text("⏳ İşlem arka plana atıldı!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global is_running, LOOP_INTERVAL, GROUP_DELAY
  query = update.callback_query
  if query.from_user.id not in ADMIN_IDS:
    await query.answer("Yetkin yok!", show_alert=True)
    return

  await query.answer()
  data = query.data
  chat_id = query.message.chat_id
  user_id = query.from_user.id

  if data == "toggle_loop":
    if not is_running:
      is_running = True
      asyncio.create_task(background_loop(context, chat_id))
      await query.message.edit_text("🚀 **Döngü arka planda başlatıldı!**", reply_markup=get_main_keyboard())
    else:
      is_running = False
      await query.message.edit_text("🛑 **Döngü durduruldu.**", reply_markup=get_main_keyboard())

  elif data == "btn_at":
    asyncio.create_task(send_single_batch_background(context, chat_id))
    await query.message.reply_text("⏳ Tek seferlik canlı gönderim başlatıldı!")

  elif data == "btn_test":
    try:
      await userbot.send_message(chat_id, f"🧪 **TEST MESAJIDIR**\n\n{MESSAGE_TEXT}")
      await query.message.reply_text("✅ Test mesajı başarıyla hesabına gönderildi!")
    except Exception as e:
      await query.message.reply_text(f"❌ Test mesajı atılamadı: {e}")

  elif data == "btn_change_text":
    waiting_for_new_text[user_id] = True
    await query.message.reply_text("✏️ **Lütfen yeni reklam metnini gönder:**")

  elif data == "btn_custom_time":
    waiting_for_custom_time[user_id] = True
    await query.message.reply_text("⏱️ **Döngü süresini kaç dakika yapmak istediğini rakam olarak yaz:**")

  elif data == "btn_custom_delay":
    waiting_for_custom_delay[user_id] = True
    await query.message.reply_text("⚡ **Grup arası bekleme saniyesini yaz:**")

  elif data == "btn_add_blacklist":
    waiting_for_blacklist[user_id] = True
    await query.message.reply_text("🚫 **Kara listeye eklemek istediğin grubun ID'sini yaz (Örn: -100123456789):**")

  elif data == "btn_liste":
    await query.message.edit_text(
        f"📋 **Sistem Bilgileri**\n\n"
        f"• Aktif Grup Sayısı: {len(groups)}\n"
        f"• Kara Listedeki Grup Sayısı: {len(blacklist)}",
        reply_markup=get_main_keyboard()
    )

  elif data == "btn_ayar":
    status_str = "Çalışıyor 🟢" if is_running else "Durduruldu 🔴"
    working_status = "Aktif (Uygun Saat)" if is_working_hour() else "Beklemede (Saat Dışı)"
    info_text = (
        f"⚙️ **Gelişmiş Bot Durumu**\n\n"
        f"• Döngü Durumu: {status_str}\n"
        f"• Zaman Dilimi Kontrolü: {working_status}\n"
        f"• Hedef Grup Sayısı: {len(groups)}\n"
        f"• Kara Liste Sayısı: {len(blacklist)}\n"
        f"• Gecikme: {GROUP_DELAY} Saniye\n"
        f"• Döngü Aralığı: {LOOP_INTERVAL // 60} Dakika"
    )
    await query.message.edit_text(info_text, reply_markup=get_main_keyboard())

  elif data == "btn_kapat":
    await query.message.delete()

# Kullanıcıdan gelen metin/sayı girdilerini işleme
async def handle_message_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global LOOP_INTERVAL, GROUP_DELAY, MESSAGE_TEXT
  user_id = update.effective_user.id
  if user_id not in ADMIN_IDS:
    return

  text = update.message.text.strip()

  if user_id in waiting_for_new_text and waiting_for_new_text[user_id]:
    MESSAGE_TEXT = update.message.text
    waiting_for_new_text[user_id] = False
    await update.message.reply_text("✅ **Reklam metni güncellendi!**", reply_markup=get_main_keyboard())

  elif user_id in waiting_for_custom_time and waiting_for_custom_time[user_id]:
    if text.isdigit():
      mins = int(text)
      LOOP_INTERVAL = mins * 60
      waiting_for_custom_time[user_id] = False
      await update.message.reply_text(f"✅ **Süre {mins} dakika yapıldı!**", reply_markup=get_main_keyboard())
    else:
      await update.message.reply_text("❌ Lütfen geçerli bir sayı yaz.")

  elif user_id in waiting_for_custom_delay and waiting_for_custom_delay[user_id]:
    if text.isdigit():
      secs = int(text)
      GROUP_DELAY = secs
      waiting_for_custom_delay[user_id] = False
      await update.message.reply_text(f"✅ **Gecikme {secs} saniye yapıldı!**", reply_markup=get_main_keyboard())
    else:
      await update.message.reply_text("❌ Lütfen geçerli bir sayı yaz.")

  elif user_id in waiting_for_blacklist and waiting_for_blacklist[user_id]:
    try:
      b_id = int(text)
      if b_id not in blacklist:
        blacklist.append(b_id)
        if b_id in groups:
          groups.remove(b_id)
      waiting_for_blacklist[user_id] = False
      await update.message.reply_text(f"✅ **Grup başarıyla kara listeye eklendi!**", reply_markup=get_main_keyboard())
    except ValueError:
      await update.message.reply_text("❌ Geçersiz ID formatı! Sadece sayısal grup ID'si yaz.")

async def main():
  await userbot.start()
  print("Userbot Oturumu Açıldı...")
  await fetch_folder_groups(userbot)

  application = ApplicationBuilder().token(BOT_TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("at", at_command))
  application.add_handler(CallbackQueryHandler(button_handler))
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_input))

  await application.initialize()
  await application.start()
  await application.updater.start_polling()
  print("Ultimate Bot Aktif Edildi...")

  await asyncio.Event().wait()

if __name__ == "__main__":
  asyncio.run(main())
