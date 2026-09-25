import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait, PeerIdInvalid
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 1. Kendi Hesabın (Userbot Bilgileri) - Mesajları bu hesap atacak
API_ID = 34285857
API_HASH = "cbdd983527af284d64655b5592fdb515"

# 2. Verdiğin Telegram Bot Token (Butonları ve komutları yöneten bot)
BOT_TOKEN = "8824951755:AAEkxb25LsXQvLUkIzwNspklWI2oKhIKhpI"

# Sadece bu ID'ye sahip kişi botu yönetebilir (Senin ID'n)
ADMIN_ID = 8169536869

# Pyrogram Userbot İstemcisini Başlatıyoruz
userbot = Client("jesuss", api_id=API_ID, api_hash=API_HASH)

# Gönderdiğin Kanal ve Grup Listesi
groups = [
    "dusesfinans",
    "illegalpiyasa",
    "pubghesap757",
    "lionillegal",
    "kinseimedyaticaret",
    "sohbetstrixz",
    "baskanticaret",
    "ppislempazari",
    "alimsatimmerkezii",
    "serenityalimsatim",
    "grupticaret",
    "freyaticaret",
    "TicaretGrubuuu",
    "liliht_ticaret",
    "aylatic",
    "ladyileticarett",
    "RossoTicaret",
    "farukmedyaa0",
    "illegal_ticaretx",
    "illegallerklubuu",
    "Bononzasohbet",
    "BANKAHESABIII",
    "aslantcrt11",
    "trticaret",
    "venomillegal",
    "KARAPARATCARET",
    "illegaltradecity",
    "ticaretguvenilir",
    "Apollonticaret",
    "illegalforshell",
    "zkamamam",
    "deltasohbetticaret",
    "canticaret",
    "SAGHEJBE",
    "ticaretdunyas1",
    "illegallegall1",
    "gmailmerkezi0",
    "illegallersehri",
    "illegalizmhack",
    "ppranfc",
    "paparaalmsatmmerkezi",
    "guzmankingg",
    "ticar4t",
    "ioralsat",
    "globaltticaret",
    "baron67732",
    "R3xeus_ticaret",
    "gangticaret",
    "lasvomedya",
    "illegalhubpapara",
    "finansticaretgrubu",
    "tezgahticarett",
    "darksocial1",
    "neastronhesap",
    "Elitticaret",
    "illegalyollar",
    "paparahesapal",
    "trodexticaret",
    "illegalyollardan",
    "illegalsticaret",
    "captan_jack1",
    "reklamyaps",
    "zentaticaret",
    "sosyoticaret",
    "ticarethub",
    "AlqiSatqiElanllar",
    "maksipppp",
    "illegal_ticarett",
    "bedavahesapdiyariichat",
    "firariticaret",
    "illegalbizim",
    "RuhsuzlarTicaret",
    "illegalticaret7",
    "illegalticaret43",
    "Toptan_Perakende_Wholesale",
    "illegallerklubutr",
    "ticaretkarapara",
    "betbakiyeticaret",
    "mailorderposislem",
    "bankahesapticaret",
    "GeneralllBusiness",
    "Coinlist_Uph3427",
    "zombieticaret",
    "lacasaderio",
    "gelbirader31",
    "illegalticarethome",
    "illegalfinanstr",
    "trcoinkazanma",
    "BURHANALIM",
    "cattpattt",
    "demirticaretmerkezi",
    "illegalhometrtr",
    "ticaret00pp",
    "illegaller",
    "parakazanmaverefkasma",
    "paparaaalim",
    "ppalvesat",
    "smbsmwbwwmwbbwn",
    "referansvebilgi",
    "sharelinktrxusdt",
    "tocareto",
    "vigorfinans",
    "reklamvereferanss",
    "Parakazan41",
    "barezconfing",
    "romeoticaret7",
    "refkasmax",
    "girdapss",
    "sanalpos3d",
    "binancetrkiralama",
    "ReklamOnliene",
    "askoticaret",
    "rafiklarticaretodasi",
    "parakazanmaref",
    "illegalerklubu",
    "parakazanmareferanskassma",
    "parakazanma1903",
    "TRlinkyardimlasmagrub",
    "sanalalimsatimticaret",
    "no1ticaret2",
    "cindyticaret",
    "Royalbey",
    "illegalislerrr",
    "ayhankoct",
    "guvenilirpaparakiralama",
    "stormanx011",
    "internettenkaza",
    "hesapackazan_sohbet",
    "ankaticaret",
    "groupberk",
    "ticaretne",
    "BtcBitcoinAirdrop",
    "MailOrderCcCeel",
    "CosmosReferans",
    "ppozanalimsatim",
    "sedaticaret",
    "ataturkticaretmerkezi",
    "kesintisizticaret",
    "ekremabiticaretmekani",
    "Tomasorgu",
    "AksinoxTicaret",
    "karmachatgroup",
    "romeoticaret5",
    "illegalpapara",
    "canticaret2",
    "parakazanmavelink",
    "kervansaraypapara",
    "referansreklam1",
    "paparaticaretx",
    "referanskasmagrubbu",
    "gencgirisimciler1",
    "barcelonaysticaret",
    "internettenparakazanmagercekk",
    "thelostxteam",
    "romeoticaret2",
    "fakenoalsaty",
    "haneticaret",
    "ReferansReklamYardimlasma",
    "kyrfinanss",
    "goldileticaret",
    "wwwtheirregularscom",
    "referans0",
    "ticarethanem",
    "adorableticaret",
    "ticaretofisi",
    "satiliktiktokhesaplar",
    "prticaret",
    "parakazanmareferansgrubu",
    "gruponline1234",
    "altncocuklar",
    "parakazanmagrub",
    "cerkesinmekan",
    "dexterppgrup",
    "romeoticaret4",
    "tahaaslan11",
    "GhostRiderpp2",
    "timsah_Ticaret",
    "XTicaret",
    "referansreklam",
    "legendticaretr",
    "katanereklam",
    "ticaretsohbetorg",
    "KLASTICARET",
    "ReklamveTanitimGrubu",
    "ticaret_mekani",
    "referansairdroptr",
    "guvenlicoinlist",
    "illegaltradeq",
    "zerooticaret",
    "referanskasmatrx",
    "alsatticarettt",
    "newtonticaret",
    "konnusanlar",
    "BedelTicarets",
    "pPTSKhGK1IMzMTg8",
    "Parakazanmayardimlasmaa",
    "powerxchat",
    "efootbal_takas",
    "illegallerklubu3",
    "paparamefetepephayhay",
    "CexyTRADE",
    "guvenilirsitelerduyuru",
    "REFERANSLI",
    "NightTicaretdunyasii",
    "Ravnon",
    "zweiprocess",
    "instagramtiktokalimsatim",
    "fakenoalimm",
    "illegalizmworld",
    "ticaretintemeli",
    "TicaretYeni",
    "ticaretdunya",
    "PonziTanitimlari",
    "TurkeySohbetgel",
    "canticaret4",
    "g0vexticaret",
    "darkwebunderGroundn",
    "cezaevigiriş",
    "forexsikayetcomtr",
    "deltan1dolandirici",
    "avukatvar",
    "yargipaketi",
    "rrLpByWaJg1NTA0",
    "cezavebosanmaavukatlari",
    "SucDuyurusu",
    "sahibindenarabailanlari",
    "cezaduyuru",
    "kislasizvecezasizbedelli",
    "bitaydava",
    "dolandirici_siteler",
    "dolandiricipaylasim",
    "uckagit",
    "bakubetresmi",
    "rtxailesi",
    "karadagdakiturkler",
    "avukatasor",
    "avukat_yardim_hukuk_fakultesi",
    "infazVeCeza",
    "BDDKmagdurları",
    "ticaretforumofficial",
    "shawtysaha",
    "ankara2",
    "Turkiyeakademi",
    "AlmanyaGoc",
    "mntforex",
    "bulgaristanli",
    "trkangalalimsatim",
    "aracalimsatim1",
    "elektroniksigaraistanbull",
    "Bahissikayetlerii",
    "sikayetkanali",
    "forexvipuk",
    "ForexislemForexSikayett",
    "SegemSorulari",
    "Bankahesapkiralamavs",
    "otoemlakajans",
    "AofAtaAuzefISG",
    "Coinmuhendisi",
    "metinmagdur",
    "detaymaxinett",
    "capricegold",
    "ankaragucusohbet",
    "guneymarmara",
    "eskisehiralsat",
    "emadder",
    "poliscevirmeist",
    "elektriklibisikletciler",
    "uzmancavusalimlari",
    "turkiyesiberkaletoplulugu",
    "TGdestek",
    "GeyiKKafe",
    "Sahinlerticaret",
    "casinoxgroup",
    "NarcozTicaret",
    "jokerillegalticaret",
    "HESAP_ALIM_SATIMGTQWCcKbeRxkZDg0",
    "esenyurtalsat",
    "ticaretmerkeziofficall",
    "fpticaretmerkezi",
    "ticaret_merkezi",
    "oIbQS4pKt0c4YTg0",
    "piccoBG01",
    "Yesariep",
    "illegalmarketx",
    "derinweborg",
    "paycowticaret",
    "kriptotayfa",
    "globalairdropchat",
    "referanslinkim",
    "gelirevrenicekilis",
    "fchatuk",
    "meksikasahaa",
    "TECHAGIIT",
    "yonlendirmexx",
    "ticaretcanavari",
    "alsatticarettz",
    "illegalticck",
    "TcGenelKurmay112",
    "mellyrefkef",
    "kraliceninheyeti",
    "globalsahacireferans",
    "wearecleanns",
    "CriminalResmi",
    "TicaretHanesi",
    "Roxiwebcc",
    "FransaTrading",
    "gameResmi",
    "changeticaret",
    "eliteprrime",
    "hesapkiralamax",
    "referansbanksohbet",
    "ticaretteler",
    "cmspa2",
    "ryzetrading",
    "CHEIFTICARET",
    "VeloraSohbet0",
    "papazvip",
    "vazolturke",
    "cantuborgtrade",
    "tereaturky",
    "leaxnew1",
    "ryzenx18",
    "dreamprojectof2026",
    "dmittrryy1755",
    "CCCHATtg",
    "TCK158F11",
    "privbiziz",
    "mahsunticaret",
    "DAYITICARET",
    "ticarethan1",
    "LARSPANEL",
    "doganmadia",
    "illegalsupport",
    "trccchat1",
    "xgangpp",
    "darkwebticaret",
    "illegelticaret",
    "illegalsss",
    "HesapYrRush",
    "illegalgrup_001",
    "illegalizmx",
    "illegalistx",
    "companyforty",
    "pekerticaret",
    "ofispapara",
    "nirvanaticarettt",
    "ccharlichaplin",
    "illegaldunyam",
    "rusticaretmekani2",
    "yildirimclub",
    "rowdytrade",
    "kuzeyt35",
    "fulmonticaret73",
    "keellee0",
    "illegalteamw",
    "atatv44israil",
    "hesapkiralasat",
    "kiralamamerkeziofis",
    "paparalam",
    "ticarethanee",
    "rusticaretmekani",
    "athenaticaret",
    "amgailesi10",
    "illegalltrade",
    "rusticaretmekani3",
    "illegal_ticaretim2",
    "forhome3d",
    "fishygrinds",
    "zourmarket",
    "fireworksfsg",
    "sfsbabyshare",
    "TalhaMarket",
    "trilldailymega",
    "Marshall_SMM",
    "lookingforsellers",
    "dan35kmega",
    "sfsmarketbuysell",
    "banditsmarket2",
    "medyaticaret",
    "AlmanyaVizeveDenklik",
    "Alfticaretgurup",
    "diyarbakirikincielarac",
    "unlulermotors",
    "sahibindenaraclar",
    "beratxalimsatim",
    "ikinciel01chat",
    "ilanlar_burada",
    "Kotekli2el",
    "MOTORRSIKLETALIMSATIMYEDEKPARCA",
    "Ticaretlerburda",
    "hakimlik_savcilik",
    "yargidanisysk",
    "hakimsavcilik",
    "hakimliksavciliksinavlari",
    "tevkiltrgenel",
    "TevkilveHukukiDayanisma",
    "TCK215",
    "gucluavukatgucluyargi",
    "hukukiyardim",
    "hoyg1",
    "yargitaydanistay",
    "arabuluculukvehukuk",
    "adalet_birligi",
    "Renshaneshopproofs14",
    "skainnnnMarket",
    "skainvouches",
    "skyboostingsrvc",
    "skyyyvouch",
    "thaliabooster",
    "thaliasvouche",
    "felinessroom",
    "natashaorg_market",
    "zeivouch",
    "ziamarket",
    "peachygamess",
    "NekoMart",
    "marketmarketxx",
    "anonymousphi",
    "SMmarketlounge",
    "BHIEMARKET",
    "demonmarkett",
    "serpentmarkett",
    "ticaretteyiz",
    "illegallalbay",
    "illegallllplatform",
    "GlobalForumTR",
    "ireliaTicaret",
    "kurtlarsf",
    "ticaretportali34",
    "viptrxsharelinksusdt",
    "EmmiTicaret",
    "HubTicaret",
    "AhbapTicaret",
    "trswapticaretgrubu",
    "ElitSohbettt",
    "ticaretgrubusc",
    "dijitalticaretgrubu",
    "ticaretarayis",
    "ticarett09",
    "Ticarettsohbet",
]

user_states = {}
is_running = False

# Gönderilecek reklam metni
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
𝟯𝟬.𝟬𝟬𝟬 𝗯𝗮𝗸𝗶𝘆𝗲 - 4.000 ₺

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

GROUP_DELAY = 5
LOOP_INTERVAL = 35 * 60


# Bot Paneli Klavyesi
def get_main_keyboard():
  status_text = "🟢 Döngü Aktif (Durdur)" if is_running else "🚀 Döngüyü Başlat"
  return InlineKeyboardMarkup([
      [InlineKeyboardButton(status_text, callback_data="toggle_loop")],
      [InlineKeyboardButton("🚀 Tek Seferlik At (/at)", callback_data="btn_at")],
      [
          InlineKeyboardButton("➕ Kanal Ekle", callback_data="btn_ekle_prompt"),
          InlineKeyboardButton("🗑️ Kanal Sil", callback_data="btn_sil_prompt"),
      ],
      [InlineKeyboardButton("📋 Ekli Kanalları Göster", callback_data="btn_liste")],
      [InlineKeyboardButton("❌ Paneli Kapat", callback_data="btn_kapat")],
  ])


# Tek Seferlik Gönderim (Hata Korumalı)
async def send_single_batch(context: ContextTypes.DEFAULT_TYPE, chat_id):
  if not groups:
    await context.bot.send_message(
        chat_id=chat_id, text="❌ **Liste boş!** Önce kanal eklemelisin."
    )
    return

  await context.bot.send_message(
      chat_id=chat_id, text="🚀 **Tek seferlik reklam gönderimi başlatıldı...**"
  )

  success_count = 0
  fail_count = 0
  total = len(groups)

  for group in groups:
    try:
      await userbot.send_message(group, MESSAGE_TEXT)
      success_count += 1
      await asyncio.sleep(GROUP_DELAY)
    except PeerIdInvalid:
      fail_count += 1
      print(f"[ÖLÜ KANAL ATLANDI] Geçersiz Peer ID: @{group}")
    except FloodWait as e:
      print(f"[FLOOD] {e.value} saniye bekleniyor...")
      await asyncio.sleep(e.value)
    except Exception as e:
      fail_count += 1
      print(f"[HATA] Kanal: @{group} | Sebep: {e}")

  report = (
      "📊 **Tek Seferlik Gönderim Tamamlandı!**\n\n"
      f"✅ Başarılı: {success_count}\n"
      f"❌ Ölü/Hatalı Kanal: {fail_count}\n"
      f"📋 Toplam Kanal: {total}"
  )
  await context.bot.send_message(chat_id=chat_id, text=report)


# Arka Plan Döngüsü (Hata Korumalı)
async def background_loop(context: ContextTypes.DEFAULT_TYPE, chat_id):
  global is_running
  while is_running:
    if not groups:
      await asyncio.sleep(60)
      continue

    success_count = 0
    fail_count = 0
    total = len(groups)

    for group in groups:
      if not is_running:
        break
      try:
        await userbot.send_message(group, MESSAGE_TEXT)
        success_count += 1
        await asyncio.sleep(GROUP_DELAY)
      except PeerIdInvalid:
        fail_count += 1
        print(f"[ÖLÜ KANAL ATLANDI] Geçersiz Peer ID: @{group}")
      except FloodWait as e:
        print(f"[FLOOD] {e.value} saniye bekleniyor...")
        await asyncio.sleep(e.value)
      except Exception as e:
        fail_count += 1
        print(f"[HATA] Kanal: @{group} | Sebep: {e}")

    if not is_running:
      break

    report = (
        "📊 **Reklam Turu Tamamlandı!**\n\n"
        f"✅ Başarılı: {success_count}\n"
        f"❌ Ölü/Hatalı: {fail_count}\n"
        f"📋 Toplam: {total}\n\n"
        f"⏳ *Sonraki tur {LOOP_INTERVAL // 60} dakika sonra başlayacak.*"
    )
    try:
      await context.bot.send_message(chat_id=chat_id, text=report)
    except:
      pass

    for _ in range(LOOP_INTERVAL):
      if not is_running:
        break
      await asyncio.sleep(1)


# Bot Komutları ve Güvenlik Kontrolü
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.effective_user.id != ADMIN_ID:
    return  # Başkası yazarsa yoksay
  await update.message.reply_text(
      "🎛️ **Reklam Botu Yönetim Paneli**\n\nAşağıdaki butonları kullanarak"
      " yönetebilirsin:",
      reply_markup=get_main_keyboard(),
  )


async def at_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.effective_user.id != ADMIN_ID:
    return
  await send_single_batch(context, update.effective_chat.id)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global is_running
  query = update.callback_query

  # Sadece admin tıklayabilsin
  if query.from_user.id != ADMIN_ID:
    await query.answer("❌ Bu botu yönetmeye yetkin yok!", show_alert=True)
    return

  await query.answer()
  data = query.data
  chat_id = query.message.chat_id

  if data == "toggle_loop":
    if not is_running:
      if not groups:
        await query.answer(
            "⚠️ Önce listeye en az bir kanal eklemelisin!", show_alert=True
        )
        return
      is_running = True
      asyncio.create_task(background_loop(context, chat_id))
      await query.message.edit_text(
          "🚀 **Otomatik reklam döngüsü çalışıyor!**",
          reply_markup=get_main_keyboard(),
      )
    else:
      is_running = False
      await query.message.edit_text(
          "🛑 **Reklam döngüsü durduruldu.**", reply_markup=get_main_keyboard()
      )

  elif data == "btn_at":
    await send_single_batch(context, chat_id)

  elif data == "btn_liste":
    if not groups:
      txt = "📁 **Liste şu an boş.**"
    else:
      txt = (
          "📋 **Ekli Kanallar (Toplam:"
          f" {len(groups)}):**\n\n"
          + "\n".join([f"- @{g}" for g in groups[:30]])
          + ("\n\n...ve dahası" if len(groups) > 30 else "")
      )
    await query.message.edit_text(txt, reply_markup=get_main_keyboard())

  elif data == "btn_ekle_prompt":
    user_states[query.from_user.id] = "waiting_for_add"
    await query.message.edit_text(
        "✍️ Lütfen eklemek istediğin kanalın kullanıcı adını gönder (Örnek:"
        " `kanaladi`):\n\n*(İptal için /start yazabilirsin)*"
    )

  elif data == "btn_sil_prompt":
    if not groups:
      await query.answer("⚠️ Zaten liste boş!", show_alert=True)
      return
    user_states[query.from_user.id] = "waiting_for_remove"
    await query.message.edit_text(
        "🗑️ Lütfen silmek istediğin kanalın kullanıcı adını gönder:\n\n*(İptal"
        " için /start yazabilirsin)*"
    )

  elif data == "btn_kapat":
    await query.message.delete()


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.message.from_user.id
  if user_id != ADMIN_ID:
    return

  if user_id in user_states:
    state = user_states[user_id]
    target = update.message.text.replace("@", "").strip()

    if state == "waiting_for_add":
      if target in groups:
        await update.message.reply_text(f"⚠️ `@{target}` zaten listede var!")
      else:
        groups.append(target)
        await update.message.reply_text(
            f"✅ `@{target}` eklendi!\nToplam kanal: {len(groups)}"
        )
      del user_states[user_id]
      await update.message.reply_text(
          "🎛️ Paneli açmak için `/start` yazabilirsin."
      )

    elif state == "waiting_for_remove":
      if target in groups:
        groups.remove(target)
        await update.message.reply_text(
            f"🗑️ `@{target}` silindi!\nKalan kanal: {len(groups)}"
        )
      else:
        await update.message.reply_text(f"❌ `@{target}` listede bulunamadı.")
      del user_states[user_id]
      await update.message.reply_text(
          "🎛️ Paneli açmak için `/start` yazabilirsin."
      )


async def main():
  # Userbot'u başlat
  await userbot.start()
  print("Userbot Hesap Oturumu Açıldı...")

  # Telegram Botunu Başlat
  application = ApplicationBuilder().token(BOT_TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("at", at_command))
  application.add_handler(CallbackQueryHandler(button_handler))
  application.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
  )

  print("Yönetim Botu Aktif Edildi...")
  await application.initialize()
  await application.start()
  await application.updater.start_polling()

  # Programın kapanmaması için sonsuz döngü
  await asyncio.Event().wait()


if __name__ == "__main__":
  asyncio.run(main())
