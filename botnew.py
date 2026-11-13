import telebot
from telebot import types
import requests
import json
import sqlite3
import os
import re
import html
from io import BytesIO
from gtts import gTTS
from threading import Thread
from flask import Flask

# ==================== 🌐 24/7 KEEP ALIVE SERVER ====================
app = Flask('')

@app.route('/')
def home():
    return "⚡ Sandesh Ultra-VIP AI & Lookup Bot is Running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

keep_alive()

# ==================== ⚙️ CONFIGURATION ====================
BOT_TOKEN = "8852300357:AAHHfKP6qsbdJcNXhZP0UWIqTWrAWgSA2n4"
GEMINI_API_KEY = "AQ.Ab8RN6LDB1oSEQrrOQX7YpnMyhNoLfJ7sIBJx8kI2QRn_hY81A"
ADMIN_ID = 1752541652

DEVELOPER_NAME = "SANDESH SINGH"
DEVELOPER_TAG = "@SANDESH870"
ADMIN_PROFILE_URL = "https://t.me/SANDESH870"

user_chat_history = {}  # हर यूज़र की पिछली बातचीत याद रखने के लिए
ai_disabled_users = set()  # जो यूज़र AI ऑफ करना चाहें

# 🖼️ Ultra-HD 3D Neon & Cyberpunk Banner Images
WELCOME_3D_PHOTO = "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=1000&q=90"
RESULT_3D_PHOTO = "https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?auto=format&fit=crop&w=1000&q=90"
LOCK_3D_PHOTO = "https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&w=1000&q=90"

# 📢 3 Channels List
CHANNELS = [
    {
        "name": "🔥 JOIN CHANNEL 1 ↗",
        "url": "https://t.me/Dracula_injector_selller",
        "id": -1002649665421
    },
    {
        "name": "⚡ JOIN CHANNEL 2 ↗",
        "url": "https://t.me/+NJstT20iTmozYjc1",
        "id": -1003280242572
    },
    {
        "name": "💎 JOIN CHANNEL 3 ↗",
        "url": "https://t.me/SANDESH_VIP_MOD02",
        "id": -1002589313551
    }
]

# ✨ ULTRA PREMIUM CUSTOM EMOJI IDS
PREMIUM_EMOJIS = {
    "user": ("5368324170671202286", "👤"),
    "lock": ("5440621591387980068", "🔐"),
    "join": ("5372981976804366741", "📢"),
    "verify": ("5206607081334906820", "✅"),
    "crown": ("5217822164362739968", "👑"),
    "bolt": ("5456140674028019486", "⚡"),
    "search": ("5188311512791393083", "🔍"),
    "fire": ("5424972470023104089", "🔥"),
    "star": ("5334882760735598374", "🌟"),
    "mic": ("5350452584119279096", "🎙️"),
    "rocket": ("5445284980978621387", "🚀"),
    "shield": ("5397782960512444700", "🛡️")
}

def em(key, use_premium=True):
    eid, fallback = PREMIUM_EMOJIS.get(key, ("", "✨"))
    if use_premium and eid:
        return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'
    return fallback

# 👑 हर मैसेज के नीचे हमेशा दिखने वाला एडमिन फ़ुटर
def admin_footer(use_premium=True):
    return (
        f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{em('crown', use_premium)} <b>ADMIN :</b> <a href='{ADMIN_PROFILE_URL}'><b>{DEVELOPER_NAME}</b></a> ({DEVELOPER_TAG})"
    )

# 🔗 All 20 API Endpoints Mapped
API_CONFIG = {
    "rc": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=rc&query={query}", "name": "🚗 Vehicle RC", "example": "WB26AW3880"},
    "rc2": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=rc2&query={query}", "name": "🚘 RC v2", "example": "WB26AW3880"},
    "smcv1": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=smcv1&query={query}", "name": "🚙 SMC v1", "example": "WB26AW3880"},
    "vehiclenum": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=vehiclenum&query={query}", "name": "🔢 Vehicle Num", "example": "WB26AW3880"},
    "v2n": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=v2n&query={query}", "name": "📲 V2N Lookup", "example": "WB26AW3880"},
    "number": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=number&query={query}", "name": "📱 Number Info", "example": "9093614290"},
    "numberv2": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=numberv2&query={query}", "name": "📞 Number v2", "example": "9093614290"},
    "numtoupi": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=numtoupi&query={query}", "name": "💳 Num to UPI", "example": "6296362230"},
    "pan": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=pan&query={query}", "name": "🪪 PAN Info", "example": "CFXPV5799D"},
    "pan2": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=pan2&query={query}", "name": "🆔 PAN v2", "example": "CFXPV5799D"},
    "hp": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=hp&query={query}", "name": "⛽ HP Gas Info", "example": "7074578844"},
    "family": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=family&query={query}", "name": "👨‍👩‍👧‍👦 Family Info", "example": "[12-Digit Number]"},
    "ration": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=ration&query={query}", "name": "🌾 Ration Info", "example": "[12-Digit Number]"},
    "lpg": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=lpg&query={query}", "name": "🔥 LPG Info", "example": "1234567890"},
    "ip": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=ip&query={query}", "name": "🌐 IP Info", "example": "122.183.39.132"},
    "vehiclechallan": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=vehiclechallan&query={query}", "name": "🚨 Vehicle Challan", "example": "HR26EV0001"},
    "tgid": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=tgid&query={query}", "name": "🤖 TG ID Info", "example": "8269316828"},
    "tgusername": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=tgusername&query={query}", "name": "👤 TG Username", "example": "username likhiye"},
    "aadhar": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=aadhar&query={query}", "name": "🆔 Aadhaar Info", "example": "[12-Digit Number]"},
    "all": {"url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=all&query={query}", "name": "⚡ All Info", "example": "9093614290"}
}

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}
voice_enabled_users = set()

# ==================== 🧠 GEMINI CONVERSATIONAL AI ENGINE ====================
def ask_sandesh_ai(user_id, user_name, user_query):
    history = user_chat_history.get(user_id, [])
    history_text = "\n".join(history[-6:])

    system_prompt = (
        f"तुम 'SANDESH VIP AI' हो, जिसे {DEVELOPER_NAME} ({DEVELOPER_TAG}) ने बनाया है। "
        f"तुम बिल्कुल एक स्मार्ट, दोस्ताना और समझदार AI असिस्टेंट की तरह बात करते हो। "
        f"यूज़र का नाम {user_name} है। यूज़र जिस भाषा (हिंदी, हिंग्लिश या इंग्लिश) में बात करे, उसी अंदाज़ में सटीक, साफ़ और मददगार जवाब दो। "
        f"जवाब बहुत लंबा न रखें (अधिकतम 150-200 शब्दों में रखें) ताकि टेलीग्राम पर पढ़ने में अच्छा लगे।\n\n"
        f"पिछली बातचीत:\n{history_text}\n"
        f"यूज़र ({user_name}): {user_query}\n"
        f"SANDESH VIP AI:"
    )

    try:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        payload = {
            "contents": [
                {
                    "parts": [{"text": system_prompt}]
                }
            ]
        }
        res = requests.post(api_url, headers=headers, json=payload, timeout=20)
        data = res.json()
        
        reply_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        history.append(f"User: {user_query}")
        history.append(f"AI: {reply_text}")
        user_chat_history[user_id] = history[-8:]
        
        return html.escape(reply_text)
    except Exception as e:
        print(f"[Gemini AI Error]: {e}")
        return "भाई अभी AI सर्वर पर थोड़ा लोड है, कृपया कुछ सेकंड बाद फिर से पूछें या नीचे दिए गए मेनू से कोई सर्विस चुनें!"

# ==================== 🎙️ VOICE ASSISTANT ENGINE ====================
def send_voice_summary(chat_id, text_to_speak, caption="🎙️ AI Voice Information Assistant"):
    try:
        clean_speech = re.sub(r'<[^>]+>', '', text_to_speak)[:450]
        tts = gTTS(text=clean_speech, lang='hi', slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_fp.name = "assistant_report.ogg"
        bot.send_voice(
            chat_id=chat_id,
            voice=audio_fp,
            caption=f"{caption}\n👑 <b>Admin:</b> {DEVELOPER_NAME} ({DEVELOPER_TAG})",
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"[Voice Assistant Error]: {e}")

def extract_summary_for_voice(service_name, query, raw_data):
    clean_service = re.sub(r'[^\w\s]', '', service_name).strip()
    if isinstance(raw_data, dict):
        important_keys = ['name', 'full_name', 'owner_name', 'operator', 'circle', 'address', 'state', 'status', 'rc_status', 'model', 'maker_model']
        spoken_parts = []
        def find_fields(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if any(ik in str(k).lower() for ik in important_keys) and v and not isinstance(v, (dict, list)):
                        spoken_parts.append(f"{k}: {v}")
                    elif isinstance(v, (dict, list)):
                        find_fields(v)
            elif isinstance(obj, list):
                for item in obj[:2]:
                    find_fields(item)
        find_fields(raw_data)
        if spoken_parts:
            details_text = ", ".join(spoken_parts[:4])
            return f"नमस्ते! {clean_service} की रिपोर्ट तैयार है। क्वेरी {query} के लिए मुख्य जानकारी यह है: {details_text}।"
    return f"नमस्ते! {clean_service} की रिपोर्ट तैयार है। आपकी क्वेरी {query} का पूरा डेटा स्क्रीन पर भेज दिया गया है।"

# 🛡️ स्मार्ट प्रीमियम सेंडर
def send_vip_photo(chat_id, photo_url, caption_builder, reply_to_id=None, markup=None):
    try:
        return bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=caption_builder(True),
            reply_to_message_id=reply_to_id,
            reply_markup=markup,
            parse_mode='HTML'
        )
    except Exception:
        return bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=caption_builder(False),
            reply_to_message_id=reply_to_id,
            reply_markup=markup,
            parse_mode='HTML'
        )

def send_vip_message(chat_id, text_builder, reply_to_id=None, markup=None):
    try:
        return bot.send_message(
            chat_id=chat_id,
            text=text_builder(True),
            reply_to_message_id=reply_to_id,
            reply_markup=markup,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception:
        return bot.send_message(
            chat_id=chat_id,
            text=text_builder(False),
            reply_to_message_id=reply_to_id,
            reply_markup=markup,
            parse_mode='HTML',
            disable_web_page_preview=True
        )

# ==================== 🗄️ DATABASE SETUP ====================
conn = sqlite3.connect("bot_users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, total_searches INTEGER DEFAULT 0)")
cursor.execute("INSERT OR IGNORE INTO stats (id, total_searches) VALUES (1, 0)")
cursor.execute("CREATE TABLE IF NOT EXISTS bot_settings (setting TEXT PRIMARY KEY, value TEXT NOT NULL)")
cursor.execute("INSERT OR IGNORE INTO bot_settings (setting, value) VALUES ('maintenance', '0')")
conn.commit()

def maintenance_enabled():
    cursor.execute("SELECT value FROM bot_settings WHERE setting = 'maintenance'")
    row = cursor.fetchone()
    return bool(row and row[0] == "1")

def set_maintenance(enabled):
    cursor.execute("INSERT OR REPLACE INTO bot_settings (setting, value) VALUES ('maintenance', ?)", ("1" if enabled else "0",))
    conn.commit()

def add_user(user_id, username, first_name):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                   (user_id, username or "None", first_name or "User"))
    cursor.execute("UPDATE users SET username = ?, first_name = ? WHERE user_id = ?",
                   (username or "None", first_name or "User", user_id))
    conn.commit()

def get_all_users():
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]

def increment_search():
    cursor.execute("UPDATE stats SET total_searches = total_searches + 1 WHERE id = 1")
    conn.commit()

def get_stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT total_searches FROM stats WHERE id = 1")
    total_searches = cursor.fetchone()[0]
    return total_users, total_searches

# ==================== 🛡️ STRICT FORCE JOIN CHECK ====================
def check_all_joined(user_id, force_check_admin=False):
    if user_id == ADMIN_ID and not force_check_admin:
        return True
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch["id"], user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"[Force-Join Check Warning] {ch['name']} ({ch['id']}): {e}")
            return False
    return True

def make_btn(text, callback_data=None, url=None, style=None):
    try:
        if url:
            return types.InlineKeyboardButton(text=text, url=url, style=style)
        return types.InlineKeyboardButton(text=text, callback_data=callback_data, style=style)
    except TypeError:
        if url:
            return types.InlineKeyboardButton(text=text, url=url)
        return types.InlineKeyboardButton(text=text, callback_data=callback_data)

def force_join_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = make_btn("JOIN 1 ↗", url=CHANNELS[0]["url"], style="primary")
    b2 = make_btn("JOIN 2 ↗", url=CHANNELS[1]["url"], style="primary")
    b3 = make_btn("JOIN 3 ↗", url=CHANNELS[2]["url"], style="primary")
    v_btn = make_btn("🛡️ VERIFY ACCESS", callback_data="verify_channels", style="success")
    c_btn = make_btn(f"👑 ADMIN ({DEVELOPER_TAG})", url=ADMIN_PROFILE_URL, style="primary")
    
    markup.add(b1, b2)
    markup.add(b3)
    markup.add(v_btn)
    markup.add(c_btn)
    return markup

def send_force_join_screen(chat_id, first_name, reply_to_id=None):
    def build_join_box(p):
        return (
            f"<blockquote>"
            f"╔══════════════════════╗\n"
            f"   {em('lock', p)} <b>ACCESS RESTRICTED</b> {em('lock', p)}\n"
            f"╚══════════════════════╝\n\n"
            f"{em('user', p)} <b>HELLO, {first_name}!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{em('fire', p)} <b>TO UNLOCK ALL 20 VIP LOOKUP TOOLS &amp; AI CHAT, JOIN ALL 3 CHANNELS BELOW:</b>\n\n"
            f"{em('join', p)} <b>1.</b> <a href='{CHANNELS[0]['url']}'><b>VIP CHANNEL 01</b></a>\n"
            f"{em('join', p)} <b>2.</b> <a href='{CHANNELS[1]['url']}'><b>VIP PRIVATE HUB 02</b></a>\n"
            f"{em('join', p)} <b>3.</b> <a href='{CHANNELS[2]['url']}'><b>VIP MODS &amp; TOOLS 03</b></a>\n\n"
            f"{em('bolt', p)} <b>AFTER JOINING ALL 3, TAP</b> <b>[VERIFY ACCESS]</b> {em('verify', p)}"
            f"{admin_footer(p)}"
            f"</blockquote>"
        )
    send_vip_photo(chat_id, LOCK_3D_PHOTO, build_join_box, reply_to_id=reply_to_id, markup=force_join_markup())

def user_main_markup(user_id=None):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    for key, val in API_CONFIG.items():
        buttons.append(make_btn(val["name"], callback_data=f"svc_{key}", style="primary"))
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])

    ai_status = "🤖 AI CHAT: ON" if (user_id not in ai_disabled_users) else "🤖 AI CHAT: OFF"
    voice_status = "🎙️ VOICE: ON" if (user_id in voice_enabled_users) else "🎙️ VOICE: OFF"
    
    b_ai = make_btn(ai_status, callback_data="toggle_ai", style="success")
    b_voice = make_btn(voice_status, callback_data="toggle_voice", style="success")
    b_contact = make_btn(f"💬 CONTACT ADMIN ({DEVELOPER_TAG})", url=ADMIN_PROFILE_URL, style="success")
    b_chan = make_btn("📢 OFFICIAL CHANNEL", url=CHANNELS[0]["url"], style="primary")
    
    markup.add(b_ai, b_voice)
    markup.add(b_contact)
    markup.add(b_chan)
    return markup

def admin_panel_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("📊 STATS", callback_data="admin_stats")
    b2 = types.InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast")
    status_text = "🔴 MAINT: ON" if maintenance_enabled() else "🟢 MAINT: OFF"
    b3 = types.InlineKeyboardButton(status_text, callback_data="admin_toggle_maint")
    b4 = types.InlineKeyboardButton("🔒 TEST JOIN UI", callback_data="admin_test_join")
    b5 = types.InlineKeyboardButton("❌ CLOSE", callback_data="close_panel")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5)
    return markup

# ==================== 🚀 COMMAND HANDLERS ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = (message.from_user.first_name or "USER").upper()
    add_user(user_id, message.from_user.username, first_name)

    if maintenance_enabled() and user_id != ADMIN_ID:
        send_vip_message(
            message.chat.id,
            lambda p: (
                f"<blockquote>"
                f"{em('lock', p)} <b>BOT UNDER MAINTENANCE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"PLEASE TRY AGAIN LATER."
                f"{admin_footer(p)}"
                f"</blockquote>"
            ),
            reply_to_id=message.message_id
        )
        return

    if not check_all_joined(user_id):
        send_force_join_screen(message.chat.id, first_name, reply_to_id=message.message_id)
        return

    user_states.pop(user_id, None)
    def build_welcome_caption(p):
        return (
            f"<blockquote>"
            f"╔══════════════════════╗\n"
            f"   {em('rocket', p)} <b>VIP INTELLIGENCE &amp; AI HUB</b> {em('rocket', p)}\n"
            f"╚══════════════════════╝\n\n"
            f"{em('star', p)} <b>WELCOME, <a href='tg://user?id={user_id}'>{first_name}</a>!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{em('bolt', p)} <b>20+ ULTRA-FAST LOOKUP APIS UNLOCKED</b>\n"
            f"🤖 <b>SMART AI CHAT :</b> DIRECT MESSAGE KAREIN BAAT KARNE KE LIYE\n"
            f"{em('mic', p)} <b>AI VOICE ASSISTANT :</b> ENABLE FOR AUDIO REPORTS\n"
            f"{em('verify', p)} <b>STATUS :</b> <b>ONLINE &amp; READY</b>"
            f"{admin_footer(p)}"
            f"</blockquote>"
        )
    send_vip_photo(message.chat.id, WELCOME_3D_PHOTO, build_welcome_caption, reply_to_id=message.message_id, markup=user_main_markup(user_id))

@bot.message_handler(commands=['clear'])
def clear_ai_memory(message):
    user_chat_history.pop(message.from_user.id, None)
    bot.reply_to(message, "🧹 <b>AI Chat Memory Cleared!</b> अब आप नई बातचीत शुरू कर सकते हैं।", parse_mode='HTML')

@bot.message_handler(commands=['testjoin'])
def test_join_preview(message):
    first_name = (message.from_user.first_name or "USER").upper()
    send_force_join_screen(message.chat.id, first_name, reply_to_id=message.message_id)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(
            message,
            f"<blockquote>❌ <b>ACCESS DENIED!</b>\nYour Telegram ID: <code>{message.from_user.id}</code>{admin_footer(False)}</blockquote>",
            parse_mode='HTML'
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=(
            f"<blockquote>"
            f"╔══════════════════════╗\n"
            f"   👑 <b>ADMIN CONTROL PANEL</b>\n"
            f"╚══════════════════════╝\n\n"
            f"⚡ <b>MANAGE BOT SETTINGS &amp; BROADCASTS BELOW:</b>"
            f"{admin_footer(False)}"
            f"</blockquote>"
        ),
        reply_to_message_id=message.message_id,
        reply_markup=admin_panel_markup(),
        parse_mode='HTML',
        disable_web_page_preview=True
    )

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    msg = bot.reply_to(message, f"<blockquote>📢 <b>SEND BROADCAST MESSAGE:</b>\n(Type /cancel to abort){admin_footer(False)}</blockquote>", parse_mode='HTML', disable_web_page_preview=True)
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.text == "/cancel":
        bot.reply_to(message, "❌ Broadcast cancelled.")
        return
    users = get_all_users()
    total = len(users)
    if total == 0:
        bot.reply_to(message, "⚠️ No users found in database.")
        return
    success, failed = 0, 0
    status_msg = bot.reply_to(message, f"⏳ Broadcasting to {total} users...")
    for uid in users:
        try:
            bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
            success += 1
        except Exception:
            failed += 1
    bot.edit_message_text(
        f"<blockquote>✅ <b>BROADCAST COMPLETED</b>\n━━━━━━━━━━━━━━━━━━━━━━\n👥 Total: <code>{total}</code>\n🟢 Sent: <code>{success}</code>\n🔴 Failed: <code>{failed}</code>{admin_footer(False)}</blockquote>",
        chat_id=message.chat.id,
        message_id=status_msg.message_id,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

# ==================== 🔘 CALLBACK HANDLERS ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    first_name = (call.from_user.first_name or "USER").upper()

    if call.data == "verify_channels":
        if check_all_joined(user_id):
            bot.answer_callback_query(call.id, "✅ VERIFICATION SUCCESSFUL! ACCESS GRANTED.")
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            def build_verified_box(p):
                return (
                    f"<blockquote>"
                    f"╔══════════════════════╗\n"
                    f"   {em('verify', p)} <b>VERIFICATION PASSED</b> {em('verify', p)}\n"
                    f"╚══════════════════════╝\n\n"
                    f"{em('star', p)} <b>WELCOME TO VIP PANEL, <a href='tg://user?id={user_id}'>{first_name}</a>!</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{em('bolt', p)} <b>CHOOSE ANY SERVICE OR ASK AI ANYTHING:</b>"
                    f"{admin_footer(p)}"
                    f"</blockquote>"
                )
            send_vip_photo(call.message.chat.id, WELCOME_3D_PHOTO, build_verified_box, markup=user_main_markup(user_id))
        else:
            bot.answer_callback_query(call.id, "❌ ACCESS DENIED! PEHLE TEENO CHANNELS JOIN KAREIN!", show_alert=True)

    elif call.data == "admin_test_join":
        bot.answer_callback_query(call.id, "Showing Force-Join Preview...")
        send_force_join_screen(call.message.chat.id, first_name)

    elif call.data == "toggle_ai":
        if user_id in ai_disabled_users:
            ai_disabled_users.remove(user_id)
            bot.answer_callback_query(call.id, "🤖 AI Chat Mode ON! Ab aap bot se kuch bhi pooch sakte hain.")
        else:
            ai_disabled_users.add(user_id)
            bot.answer_callback_query(call.id, "💤 AI Chat Mode OFF kar diya gaya.")
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=user_main_markup(user_id))
        except Exception:
            pass

    elif call.data == "toggle_voice":
        if user_id in voice_enabled_users:
            voice_enabled_users.remove(user_id)
            bot.answer_callback_query(call.id, "🔇 Voice Assistant OFF kar diya gaya.")
        else:
            voice_enabled_users.add(user_id)
            bot.answer_callback_query(call.id, "🎙️ Voice Assistant ON! Ab har report aur AI jawab audio mein bhi milega.")
            send_voice_summary(
                call.message.chat.id,
                f"नमस्ते {first_name}! आपका वॉयस असिस्टेंट सक्रिय हो गया है।",
                caption="🎙️ <b>Voice Information Assistant Active</b>"
            )
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=user_main_markup(user_id))
        except Exception:
            pass

    elif call.data == "admin_broadcast":
        if user_id != ADMIN_ID:
            return
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, f"<blockquote>📢 <b>SEND BROADCAST MESSAGE:</b>\n(Type /cancel to stop){admin_footer(False)}</blockquote>", parse_mode='HTML', disable_web_page_preview=True)
        bot.register_next_step_handler(msg, process_broadcast)

    elif call.data.startswith("svc_"):
        if not check_all_joined(user_id):
            bot.answer_callback_query(call.id, "❌ Pehle teeno channels join karein!", show_alert=True)
            send_force_join_screen(call.message.chat.id, first_name)
            return

        service_key = call.data.replace("svc_", "")
        if service_key in API_CONFIG:
            user_states[user_id] = f"waiting_{service_key}"
            bot.answer_callback_query(call.id)
            svc_info = API_CONFIG[service_key]
            send_vip_message(
                call.message.chat.id,
                lambda p: (
                    f"<blockquote>"
                    f"╔══════════════════════╗\n"
                    f"   {em('search', p)} <b>{svc_info['name'].upper()}</b>\n"
                    f"╚══════════════════════╝\n\n"
                    f"{em('bolt', p)} <b>ENTER YOUR QUERY BELOW:</b>\n"
                    f"🔹 <b>EXAMPLE :</b> <code>{svc_info['example']}</code>"
                    f"{admin_footer(p)}"
                    f"</blockquote>"
                )
            )
            if user_id in voice_enabled_users:
                clean_name = re.sub(r'[^\w\s]', '', svc_info['name']).strip()
                send_voice_summary(
                    call.message.chat.id,
                    f"कृपया {clean_name} के लिए अपना नंबर या आईडी दर्ज करें।",
                    caption=f"🎙️ Voice Prompt: {clean_name}"
                )

    elif call.data == "admin_stats":
        if user_id != ADMIN_ID:
            return
        u_count, s_count = get_stats()
        bot.answer_callback_query(call.id)
        send_vip_message(
            call.message.chat.id,
            lambda p: f"<blockquote>{em('bolt', p)} <b>BOT LIVE STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n👥 <b>TOTAL USERS :</b> <code>{u_count}</code>\n🔍 <b>TOTAL SEARCHES :</b> <code>{s_count}</code>{admin_footer(p)}</blockquote>"
        )

    elif call.data == "admin_toggle_maint":
        if user_id != ADMIN_ID:
            return
        set_maintenance(not maintenance_enabled())
        bot.answer_callback_query(call.id, "Maintenance status updated!")
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_panel_markup())
        except Exception:
            pass

    elif call.data == "close_panel":
        bot.delete_message(call.message.chat.id, call.message.message_id)

# ==================== 📨 TEXT, AI CHAT & API EXECUTION HANDLER ====================
@bot.message_handler(func=lambda message: True)
def handle_text_inputs(message):
    user_id = message.from_user.id
    first_name = (message.from_user.first_name or "USER").upper()
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    add_user(user_id, message.from_user.username, first_name)

    if maintenance_enabled() and user_id != ADMIN_ID:
        send_vip_message(
            message.chat.id,
            lambda p: f"<blockquote>{em('lock', p)} <b>BOT MAINTENANCE MODE</b>{admin_footer(p)}</blockquote>",
            reply_to_id=message.message_id
        )
        return

    if not check_all_joined(user_id):
        send_force_join_screen(message.chat.id, first_name, reply_to_id=message.message_id)
        return

    text_input = message.text.strip()
    state = user_states.get(user_id)

    # 🤖 अगर कोई सर्विस बटन नहीं दबाया है तो SMART AI ASSISTANT बात करेगा
    if not state:
        if user_id not in ai_disabled_users:
            bot.send_chat_action(message.chat.id, 'typing')
            ai_reply = ask_sandesh_ai(user_id, first_name, text_input)
            send_vip_message(
                message.chat.id,
                lambda p: (
                    f"<blockquote>"
                    f"{em('rocket', p)} <b>SANDESH VIP AI</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{ai_reply}"
                    f"{admin_footer(p)}"
                    f"</blockquote>"
                ),
                reply_to_id=message.message_id,
                markup=user_main_markup(user_id)
            )
            if user_id in voice_enabled_users:
                send_voice_summary(message.chat.id, ai_reply, caption="🎙️ <b>AI Voice Reply</b>")
        else:
            send_vip_message(
                message.chat.id,
                lambda p: f"<blockquote>{em('bolt', p)} <b>PLEASE SELECT A SERVICE FROM MENU BELOW (OR TURN ON AI CHAT):</b>{admin_footer(p)}</blockquote>",
                reply_to_id=message.message_id,
                markup=user_main_markup(user_id)
            )
        return

    # 🔍 अगर किसी API सर्विस का इनपुट आया है
    service_key = state.replace("waiting_", "")
    user_states.pop(user_id, None)
    increment_search()

    svc_data = API_CONFIG.get(service_key, {})
    service_name = svc_data.get("name", service_key)

    loading_msg = send_vip_message(
        message.chat.id,
        lambda p: f"<blockquote>{em('search', p)} <b>FETCHING {service_name.upper()} DETAILS...</b> ⏳{admin_footer(p)}</blockquote>",
        reply_to_id=message.message_id
    )

    # 👑 ADMIN REAL-TIME ALERT (Clickable Profile Link ke saath)
    if ADMIN_ID:
        try:
            bot.send_message(
                ADMIN_ID,
                (
                    f"<blockquote>"
                    f"🚨 <b>NEW {service_name.upper()} QUERY</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 <b>USER :</b> <a href='tg://user?id={user_id}'><b>{first_name}</b></a>\n"
                    f"🆔 <b>USER ID :</b> <code>{user_id}</code>\n"
                    f"🔗 <b>USERNAME :</b> {username}\n"
                    f"🔎 <b>INPUT :</b> <code>{text_input}</code>"
                    f"{admin_footer(False)}"
                    f"</blockquote>"
                ),
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        except Exception:
            pass

    target_api = svc_data.get("url", "")
    if not target_api:
        bot.edit_message_text(
            f"<blockquote>⚙️ <b>{service_name} API URL</b> not configured.{admin_footer(False)}</blockquote>",
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        return

    try:
        url = target_api.format(query=text_input)
        response = requests.get(url, timeout=15)
        parsed_json = None
        try:
            parsed_json = response.json()
            result_display = json.dumps(parsed_json, indent=2, ensure_ascii=False)
        except Exception:
            result_display = response.text

        def build_result_caption(p):
            return (
                f"<blockquote>"
                f"╔══════════════════════╗\n"
                f"   {em('verify', p)} <b>{service_name.upper()} REPORT</b>\n"
                f"╚══════════════════════╝\n\n"
                f"{em('user', p)} <b>QUERIED BY :</b> <a href='tg://user?id={user_id}'><b>{first_name}</b></a>\n"
                f"{em('search', p)} <b>INPUT :</b> <code>{text_input}</code>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"<pre>{html.escape(result_display[:800])}</pre>"
                f"{admin_footer(p)}"
                f"</blockquote>"
            )

        send_vip_photo(message.chat.id, RESULT_3D_PHOTO, build_result_caption, reply_to_id=message.message_id, markup=user_main_markup(user_id))
        
        if user_id in voice_enabled_users:
            spoken_report = extract_summary_for_voice(service_name, text_input, parsed_json)
            send_voice_summary(message.chat.id, spoken_report, caption=f"🎙️ <b>Voice Assistant Report:</b> {service_name}")

        try:
            bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)
        except Exception:
            pass

    except Exception as e:
        bot.edit_message_text(
            f"<blockquote>❌ <b>ERROR :</b> <code>{html.escape(str(e))}</code>{admin_footer(False)}</blockquote>",
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            parse_mode='HTML',
            disable_web_page_preview=True
        )

if __name__ == "__main__":
    print("Ultra-VIP 3D AI & Lookup Bot is starting...")
    bot.infinity_polling(none_stop=True, skip_pending=True)
