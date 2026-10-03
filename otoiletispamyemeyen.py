import asyncio
from datetime import datetime
import logging
import os
import random
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

# 🛠️ Loglama Ayarı
logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8',
)
logger = logging.getLogger(__name__)

# Bilgiler
API_ID = 34285857
API_HASH = "cbdd983527af284d64655b5592fdb515"
SESSION_NAME = "jesuss"
BOT_TOKEN = "8824951755:AAEkxb25LsXQvLUkIzwNspklWI2oKhIKhpI"
ADMIN_IDS = [8169536869, 8274327683]

userbot = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

groups = []
blacklist = []
is_running = False

# 🔒 SPAM KORUMASI: Gecikme artırıldı (11 saniye) ve grup paket boyutu (50'şerli) belirlendi
GROUP_DELAY = 11
BATCH_SIZE = 50
BATCH_PAUSE = 60  # Her 50 grupta bir 60 saniye dinlenme
LOOP_INTERVAL = 35 * 60

START_HOUR = 8
END_HOUR = 1

waiting_for_custom_time = {}
waiting_for_custom_delay = {}
waiting_for_new_text = {}
waiting_for_blacklist = {}
waiting_for_photo = {}

MESSAGE_TEXT = """🔤🔤🔤🔤 🔤🔤🔤🔤🔤
𝗬𝗘𝗠𝗘𝗞𝗦𝗘𝗣𝗘𝗧𝗜‌,𝗛𝗘𝗣𝗘𝗦𝗜‌𝗕𝗨𝗥𝗔𝗗𝗔 𝗡𝟭𝟭 𝗕𝗔𝗞𝗜‌𝗬𝗘 𝗬𝗨‌𝗞𝗟𝗘𝗠𝗘
𝟯.𝟬𝟬𝟬 𝗧𝗟 - 𝟱𝟬0 𝗧𝗟 
𝟱.𝟬𝟬𝟬 𝗧𝗟 - 𝟴𝟬0 𝗧𝗟 
𝟳.𝟬𝟬𝟬 𝗧𝗟 - 𝟭.𝟮𝟬𝟬 𝗧𝗟

𝗕𝗔𝗛𝗜‌𝗦 𝗦𝗜‌𝗧𝗘𝗟𝗘𝗥𝗜‌𝗡𝗘 𝗩𝗘 𝗞𝗥𝗜‌‌𝗣𝗧𝗢 𝗛𝗘𝗦𝗔𝗣𝗟𝗔𝗥𝗜𝗡𝗔 𝗕𝗔𝗞𝗜‌𝗬𝗘 𝗬𝗨‌𝗞𝗟𝗘𝗡𝗜‌𝗥 

𝟯.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 600 ₺ 
𝟲.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 900 ₺ 
𝟴.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 1.500 ₺ 
𝟭𝟬.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 2.700 ₺ 
𝟮0.000 𝗯𝗮𝗸𝗶𝘆𝗲 - 3.200 ₺ 
𝟯0.000 𝗯𝗮𝗸𝗶𝘆𝗲 - 4.000 ₺

𝗜‌‌𝗣𝗛𝗢𝗡𝗘 𝗨‌𝗥𝗨‌𝗡𝗟𝗘𝗥𝗜‌ 𝗨𝗬𝗚𝗨𝗡𝗔 𝗚𝗘𝗖‌𝗜‌𝗟𝗜‌𝗥

𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟭 - 5.000 ₺ 
𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟮- 10.000 (𝘁𝘂‌𝗸𝗲𝗻𝗱𝗶 ) 
𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟯 - 15.000 ₺
𝗜‌𝗣𝗛𝗢𝗡𝗘𝟭𝟰- 25.000 (𝘁𝘂‌𝗸𝗲𝗻𝗱𝗶 ) 
𝗜‌𝗣𝗛𝗢𝗡𝗘 𝟭𝟱 - 35.000 ₺

DİĞER TÜM İŞLEMLER “

𝗣𝗨𝗕𝗚 𝗠𝗢𝗕𝗜‌𝗟 𝗨𝗖 𝗬𝗨‌𝗞𝗟𝗘𝗡𝗜‌𝗥

𝗧𝗘𝗞 𝗨𝗬𝗚𝗨𝗟𝗔𝗠𝗔𝗗𝗔 𝗕𝗨‌𝗧𝗨‌𝗡 𝗛𝗔𝗖𝗞 𝗔𝗥𝗔𝗖‌𝗟𝗔𝗥𝗜 𝗩𝗘 𝗘𝗚‌𝗜‌𝗧𝗜‌𝗠 𝗦𝗘𝗧𝗜‌ 

𝗜‌‌𝗡𝗙𝗟𝗨 𝗖𝗖 𝗕𝗨𝗟𝗨𝗡𝗨𝗥 𝗧𝗥 - 𝗬𝗗

📱 📱 WhatsApp & Telegram Fake No Sağlanır

𝗜‌𝗟𝗘𝗧𝗜‌𝗦‌𝗜‌𝗠 : @keinmedyaaa 💠"""

PHOTO_PATH = None


# 🔒 SPAM KORUMASI: Spintax / Metin Varyasyonu
def get_spintax_text():
  """Gönderim sırasında metni hafifçe çeşitlendirerek Telegram spam filtrelerini atlatır."""
  greetings = ["", "", "Selamlar.", "İyi günler.", "Merhaba dostlar."]
  dots = [".", "..", "...", " ✨"]

  chosen_greeting = random.choice(greetings)
  chosen_dot = random.choice(dots)

  varied_text = MESSAGE_TEXT
  if chosen_greeting:
    varied_text = f"{chosen_greeting}\n\n" + varied_text
  return varied_text + chosen_dot


def get_main_keyboard():
  status_text = "🟢 Döngü Aktif (Durdur)" if is_running else "🚀 Döngüyü Başlat"
  return InlineKeyboardMarkup([
      [InlineKeyboardButton(status_text, callback_data="toggle_loop")],
      [InlineKeyboardButton("🚀 Tek Seferlik Canlı At (/at)", callback_data="btn_at")],
      [InlineKeyboardButton("🧪 Bana Test Mesajı At", callback_data="btn_test")],
      [InlineKeyboardButton("✏️ Reklam Metnini Değiştir", callback_data="btn_change_text")],
      [InlineKeyboardButton("🖼️ Fotoğraf Ekle/Kaldır", callback_data="btn_set_photo")],
      [InlineKeyboardButton("⏱️ Süreyi Belirle (Dk)", callback_data="btn_custom_time")],
      [InlineKeyboardButton("⚡ Gecikmeyi Belirle (Sn)", callback_data="btn_custom_delay")],
      [InlineKeyboardButton("🚫 Kara Listeye Ekle", callback_data="btn_add_blacklist")],
      [InlineKeyboardButton("📋 Durum & Bilgi", callback_data="btn_liste")],
      [InlineKeyboardButton("❌ Paneli Kapat", callback_data="btn_kapat")],
  ])


async def fetch_folder_groups(client):
  global groups
  groups.clear()
  async for dialog in client.get_dialogs(limit=300):
    if "group" in str(dialog.chat.type).lower():
      if dialog.chat.id not in blacklist:
        groups.append(dialog.chat.id)


def is_working_hour():
  h = datetime.now().hour
  if START_HOUR < END_HOUR:
    return START_HOUR <= h < END_HOUR
  return h >= START_HOUR or h < END_HOUR


async def send_advertisement(chat_id):
  current_text = get_spintax_text()
  if PHOTO_PATH and os.path.exists(PHOTO_PATH):
    await userbot.send_photo(chat_id, photo=PHOTO_PATH, caption=current_text)
  else:
    await userbot.send_message(chat_id, current_text)


async def send_single_batch_background(context, chat_id):
  if not groups:
    await context.bot.send_message(chat_id=chat_id, text="❌ Grup bulunamadı!")
    return

  status_msg = await context.bot.send_message(chat_id=chat_id, text="🚀 Parçalı gönderim başlatıldı...")
  success, fail, total = 0, 0, len(groups)

  for i, gid in enumerate(groups, 1):
    if gid in blacklist:
      continue
    try:
      await send_advertisement(gid)
      success += 1
      
      # Anlık bilgi güncellemesi
      if i % 3 == 0 or i == total:
        await status_msg.edit_text(
            f"⏳ İlerleme: {i}/{total}\n✅ Başarılı: {success}\n❌ Hatalı: {fail}"
        )
      
      # 🔒 SPAM KORUMASI: Belirli gruplardan sonra (örn: 50 grup) mola verme
      if i % BATCH_SIZE == 0 and i < total:
        await status_msg.edit_text(f"☕ Güvenlik Molası: {i}/{total} grup atıldı. {BATCH_PAUSE} saniye dinleniliyor...")
        await asyncio.sleep(BATCH_PAUSE)
        await status_msg.edit_text(f"🚀 Gönderime devam ediliyor...")

      await asyncio.sleep(GROUP_DELAY)
    except FloodWait as e:
      logger.warning(f"FloodWait yakalandı: {e.value} saniye bekleniyor.")
      await asyncio.sleep(e.value + 5)
    except Exception:
      fail += 1

  await status_msg.edit_text(f"📊 Gönderim Tamamlandı!\n• Başarılı: {success}\n• Hatalı: {fail}")


async def background_loop(context, chat_id):
  global is_running, LOOP_INTERVAL
  while is_running:
    try:
      if not is_working_hour():
        await asyncio.sleep(300)
        continue
      if not groups:
        await fetch_folder_groups(userbot)

      for index, gid in enumerate(groups, 1):
        if not is_running:
          break
        if gid in blacklist:
          continue
        try:
          await send_advertisement(gid)
          
          # Döngü içinde de paket molası
          if index % BATCH_SIZE == 0:
            await asyncio.sleep(BATCH_PAUSE)

          await asyncio.sleep(GROUP_DELAY)
        except FloodWait as e:
          await asyncio.sleep(e.value + 5)
        except Exception:
          pass

      for _ in range(LOOP_INTERVAL):
        if not is_running:
          break
        await asyncio.sleep(1)
    except Exception:
      await asyncio.sleep(10)


async def start(update, context):
  if update.effective_user.id not in ADMIN_IDS:
    return
  await update.message.reply_text("🎛️ Kontrol Paneli (Güvenli Mod Aktif)", reply_markup=get_main_keyboard())


async def at_command(update, context):
  if update.effective_user.id not in ADMIN_IDS:
    return
  asyncio.create_task(send_single_batch_background(context, update.effective_chat.id))


async def button_handler(update, context):
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
      await query.message.edit_text("🚀 Döngü başlatıldı!", reply_markup=get_main_keyboard())
    else:
      is_running = False
      await query.message.edit_text("🛑 Döngü durduruldu.", reply_markup=get_main_keyboard())

  elif data == "btn_at":
    asyncio.create_task(send_single_batch_background(context, chat_id))
    await query.message.reply_text("⏳ Parçalı gönderim başlatıldı!")

  elif data == "btn_test":
    try:
      await send_advertisement(chat_id)
      await query.message.reply_text("✅ Test mesajı (Spintax varyasyonlu) gönderildi!")
    except Exception as e:
      await query.message.reply_text(f"❌ Hata: {e}")

  elif data == "btn_change_text":
    waiting_for_new_text[user_id] = True
    await query.message.reply_text("✏️ Yeni reklam metnini yazıp gönder:")

  elif data == "btn_set_photo":
    waiting_for_photo[user_id] = True
    await query.message.reply_text(
        "🖼️ Fotoğrafı gönder (Kaldırmak için 'sil' yaz):"
    )

  elif data == "btn_custom_time":
    waiting_for_custom_time[user_id] = True
    await query.message.reply_text("⏱️ Döngü süresini dakika olarak yaz:")

  elif data == "btn_custom_delay":
    waiting_for_custom_delay[user_id] = True
    await query.message.reply_text("⚡ Gecikmeyi saniye olarak yaz (Örn: 11):")

  elif data == "btn_add_blacklist":
    waiting_for_blacklist[user_id] = True
    await query.message.reply_text("🚫 Kara listeye eklenecek grup ID'sini yaz:")

  elif data == "btn_liste":
    await query.message.edit_text(
        f"📋 Güvenli Mod Bilgi\n\n• Aktif Grup: {len(groups)}\n• Kara Liste: {len(blacklist)}\n• Gecikme: {GROUP_DELAY} sn\n• Paket Boyutu: {BATCH_SIZE} grup",
        reply_markup=get_main_keyboard(),
    )

  elif data == "btn_kapat":
    await query.message.delete()


async def handle_inputs(update, context):
  global LOOP_INTERVAL, GROUP_DELAY, MESSAGE_TEXT, PHOTO_PATH
  user_id = update.effective_user.id
  if user_id not in ADMIN_IDS:
    return

  if user_id in waiting_for_photo and waiting_for_photo[user_id]:
    if update.message.photo:
      file = await context.bot.get_file(update.message.photo[-1].file_id)
      PHOTO_PATH = "reklam_foto.jpg"
      await file.download_to_drive(PHOTO_PATH)
      waiting_for_photo[user_id] = False
      await update.message.reply_text("✅ Fotoğraf kaydedildi!", reply_markup=get_main_keyboard())
      return
    elif update.message.text and update.message.text.lower() == "sil":
      PHOTO_PATH = None
      waiting_for_photo[user_id] = False
      await update.message.reply_text("🗑️️ Fotoğraf kaldırıldı.", reply_markup=get_main_keyboard())
      return

  text = update.message.text.strip() if update.message.text else ""

  if user_id in waiting_for_new_text and waiting_for_new_text[user_id]:
    MESSAGE_TEXT = update.message.text
    waiting_for_new_text[user_id] = False
    await update.message.reply_text("✅ Metin güncellendi!", reply_markup=get_main_keyboard())

  elif user_id in waiting_for_custom_time and waiting_for_custom_time[user_id]:
    if text.isdigit():
      LOOP_INTERVAL = int(text) * 60
      waiting_for_custom_time[user_id] = False
      await update.message.reply_text(f"✅ Süre {text} dk yapıldı!", reply_markup=get_main_keyboard())

  elif user_id in waiting_for_custom_delay and waiting_for_custom_delay[user_id]:
    if text.isdigit():
      GROUP_DELAY = int(text)
      waiting_for_custom_delay[user_id] = False
      await update.message.reply_text(f"✅ Gecikme {text} sn yapıldı!", reply_markup=get_main_keyboard())

  elif user_id in waiting_for_blacklist and waiting_for_blacklist[user_id]:
    try:
      b_id = int(text)
      if b_id not in blacklist:
        blacklist.append(b_id)
        if b_id in groups:
          groups.remove(b_id)
      waiting_for_blacklist[user_id] = False
      await update.message.reply_text("✅ Eklendi!", reply_markup=get_main_keyboard())
    except ValueError:
      await update.message.reply_text("❌ Geçersiz ID!")


async def main():
  await userbot.start()
  await fetch_folder_groups(userbot)

  application = ApplicationBuilder().token(BOT_TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("at", at_command))
  application.add_handler(CallbackQueryHandler(button_handler))
  application.add_handler(
      MessageHandler(filters.TEXT | filters.PHOTO & ~filters.COMMAND, handle_inputs)
  )

  await application.initialize()
  await application.start()
  await application.updater.start_polling()

  await asyncio.Event().wait()


if __name__ == "__main__":
  asyncio.run(main())
