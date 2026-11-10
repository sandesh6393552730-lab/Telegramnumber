import telebot
from telebot import types
import requests
import json
import sqlite3
import os
from threading import Thread
from flask import Flask

# ==================== 🌐 24/7 KEEP ALIVE SERVER ====================
app = Flask('')

@app.route('/')
def home():
    return "⚡ Sandesh Multi-Service Bot is Running 24/7!"

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
ADMIN_ID = 1752541652

DEVELOPER_NAME = "Sandesh Singh"
DEVELOPER_TAG = "@SANDESH870"

# 🖼️ Banner Images
WELCOME_PHOTO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
SNAKE_PHOTO_URL = "https://images.unsplash.com/photo-1531386151447-fd76ad50012f?auto=format&fit=crop&w=800&q=80"

# 📢 Channels List
CHANNELS = [
    {
        "name": "Join 1 ↗",
        "url": "https://t.me/Dracula_injector_selller",
        "id": -1002649665421
    },
    {
        "name": "Join 2 ↗",
        "url": "https://t.me/+NJstT20iTmozYjc1",
        "id": -1003280242572
    },
    {
        "name": "Join 3 ↗",
        "url": "https://t.me/SANDESH_VIP_MOD02",
        "id": -1002589313551
    }
]

# 🔗 All 18 API Endpoints Mapped with Commands & Examples
API_CONFIG = {
    "rc": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=rc&query={query}",
        "name": "Vehicle RC",
        "example": "WB26AW3880"
    },
    "rc2": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=rc2&query={query}",
        "name": "RC v2",
        "example": "WB26AW3880"
    },
    "smcv1": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=smcv1&query={query}",
        "name": "SMC v1",
        "example": "WB26AW3880"
    },
    "vehiclenum": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=vehiclenum&query={query}",
        "name": "Vehicle Num",
        "example": "WB26AW3880"
    },
    "v2n": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=v2n&query={query}",
        "name": "V2N",
        "example": "WB26AW3880"
    },
    "number": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=number&query={query}",
        "name": "Number Info",
        "example": "9093614290"
    },
    "numberv2": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=numberv2&query={query}",
        "name": "Number v2",
        "example": "9093614290"
    },
    "numtoupi": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=numtoupi&query={query}",
        "name": "Num to UPI",
        "example": "6296362230"
    },
    "pan": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=pan&query={query}",
        "name": "PAN Info",
        "example": "CFXPV5799D"
    },
    "pan2": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=pan2&query={query}",
        "name": "PAN v2",
        "example": "CFXPV5799D"
    },
    "hp": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=hp&query={query}",
        "name": "HP Info",
        "example": "7074578844"
    },
    "family": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=family&query={query}",
        "name": "Family Info",
        "example": "[12-Digit Number]"
    },
    "ration": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=ration&query={query}",
        "name": "Ration Info",
        "example": "[12-Digit Number]"
    },
    "lpg": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=lpg&query={query}",
        "name": "LPG Info",
        "example": "1234567890"
    },
    "ip": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=ip&query={query}",
        "name": "IP Info",
        "example": "122.183.39.132"
    },
    "vehiclechallan": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=vehiclechallan&query={query}",
        "name": "Vehicle Challan",
        "example": "HR26EV0001"
    },
    "tgid": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=tgid&query={query}",
        "name": "Telegram ID Info",
        "example": "8269316828"
    },
    "tgusername": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=tgusername&query={query}",
        "name": "Telegram Username",
        "example": "@XZ1OR"
    },
    "aadhar": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=aadhar&query={query}",
        "name": "Aadhaar Info",
        "example": "[12-Digit Number]"
    },
    "all": {
        "url": "https://admin.gbssystems.com/public/gateway/apiv1/api.php?key=9NXZC&cmd=all&query={query}",
        "name": "All Info",
        "example": "9093614290"
    }
}

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

# ==================== 🗄️ DATABASE SETUP ====================
conn = sqlite3.connect("bot_users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY,
    total_searches INTEGER DEFAULT 0
)
""")
cursor.execute("INSERT OR IGNORE INTO stats (id, total_searches) VALUES (1, 0)")
cursor.execute("""
CREATE TABLE IF NOT EXISTS bot_settings (
    setting TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
""")
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

# ==================== 🛡️ FORCE JOIN CHECK ====================
def check_all_joined(user_id):
    if user_id == ADMIN_ID:
        return True

    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch["id"], user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"[Join Check Alert] {ch['name']} ({ch['id']}): {e}")
            continue

    return True

def force_join_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=ch["name"], url=ch["url"]) for ch in CHANNELS]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton(text="✅ VERIFY", callback_data="verify_channels"))
    return markup

def user_main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Dynamic buttons loop for all services in API_CONFIG
    buttons = []
    for key, val in API_CONFIG.items():
        buttons.append(types.InlineKeyboardButton(val["name"], callback_data=f"svc_{key}"))
    
    # Add buttons in pairs of 2
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])

    # Extra info buttons
    b_dev = types.InlineKeyboardButton("👨‍💻 Developer", callback_data="dev_info")
    b_chan = types.InlineKeyboardButton("📢 Channel", url=CHANNELS[0]["url"])
    markup.add(b_dev, b_chan)
    return markup

def admin_panel_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("📊 Stats", callback_data="admin_stats")
    b2 = types.InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
    status_text = "🔴 Maint: ON" if maintenance_enabled() else "🟢 Maint: OFF"
    b3 = types.InlineKeyboardButton(status_text, callback_data="admin_toggle_maint")
    b4 = types.InlineKeyboardButton("❌ Close", callback_data="close_panel")
    markup.add(b1, b2)
    markup.add(b3, b4)
    return markup

# ==================== 🚀 COMMAND HANDLERS ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "User"
    add_user(user_id, message.from_user.username, first_name)

    if maintenance_enabled() and user_id != ADMIN_ID:
        bot.reply_to(message, "🛠 **Bot Maintenance Mode me hai!**\nKripya thodi der baad prayas karein.", parse_mode='Markdown')
        return

    if not check_all_joined(user_id):
        caption_text = (
            f"Hey 👋 **{first_name.upper()}**\n\n"
            f"🔥 **Join all the channels to use the bot** 🔥"
        )
        bot.send_photo(
            chat_id=message.chat.id,
            photo=WELCOME_PHOTO_URL,
            caption=caption_text,
            reply_markup=force_join_markup(),
            parse_mode='Markdown'
        )
        return

    user_states.pop(user_id, None)
    welcome_caption = (
        f"✨ **Welcome {first_name}!** ✨\n\n"
        f"Niche diye gaye options me se apni service chunein:\n\n"
        f"👨‍💻 **Developer:** [{DEVELOPER_NAME}]({CHANNELS[0]['url']})\n"
        f"💬 **Admin:** {DEVELOPER_TAG}\n"
        f"⚡ **Status:** Active & Ready"
    )
    bot.send_photo(
        chat_id=message.chat.id,
        photo=WELCOME_PHOTO_URL,
        caption=welcome_caption,
        reply_markup=user_main_markup(),
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.reply_to(message, "👑 **Admin Control Panel**", parse_mode='Markdown', reply_markup=admin_panel_markup())

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    msg = bot.reply_to(message, "📢 **Broadcast Message bhejein:**\n(Cancel karne ke liye /cancel likhein)")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.text == "/cancel":
        bot.reply_to(message, "❌ Broadcast cancel kar diya gaya.")
        return
    users = get_all_users()
    total = len(users)
    success, failed = 0, 0
    status_msg = bot.reply_to(message, f"⏳ Broadcast shuru ho raha hai... (Total: {total})")
    for uid in users:
        try:
            bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
            success += 1
        except Exception:
            failed += 1
    bot.edit_message_text(
        f"✅ **Broadcast Done!**\n\n👥 Total: `{total}`\n🟢 Delivered: `{success}`\n🔴 Failed: `{failed}`",
        chat_id=message.chat.id,
        message_id=status_msg.message_id,
        parse_mode='Markdown'
    )

# ==================== 🔘 CALLBACK HANDLERS ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id

    if call.data == "verify_channels":
        if check_all_joined(user_id):
            bot.answer_callback_query(call.id, "✅ Verification Successful!")
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.send_message(
                call.message.chat.id,
                f"🎉 **Welcome {call.from_user.first_name}!**\nVerification safal raha. Niche diye gaye menu se service chunein:",
                reply_markup=user_main_markup()
            )
        else:
            bot.answer_callback_query(call.id, "❌ Aapne abhi tak sabhi channels join nahi kiye hain!", show_alert=True)

    elif call.data.startswith("svc_"):
        service_key = call.data.replace("svc_", "")
        if service_key in API_CONFIG:
            user_states[user_id] = f"waiting_{service_key}"
            bot.answer_callback_query(call.id)
            svc_info = API_CONFIG[service_key]
            bot.send_message(
                call.message.chat.id,
                f"🔍 **{svc_info['name']}**\n\nKripya query ya input bhejein.\n🔹 **Udaharan:** `{svc_info['example']}`",
                parse_mode='Markdown'
            )

    elif call.data == "dev_info":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"👨‍💻 **Developer:** {DEVELOPER_NAME}\n💬 **Telegram:** {DEVELOPER_TAG}", parse_mode='Markdown')

    elif call.data == "admin_stats":
        if user_id != ADMIN_ID:
            return
        u_count, s_count = get_stats()
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"📊 **Stats:**\n👥 Users: `{u_count}`\n🔍 Searches: `{s_count}`", parse_mode='Markdown')

    elif call.data == "admin_toggle_maint":
        if user_id != ADMIN_ID:
            return
        set_maintenance(not maintenance_enabled())
        bot.answer_callback_query(call.id, "Maintenance status changed!")
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_panel_markup())
        except Exception:
            pass

    elif call.data == "close_panel":
        bot.delete_message(call.message.chat.id, call.message.message_id)

# ==================== 📨 TEXT & API EXECUTION HANDLER ====================
@bot.message_handler(func=lambda message: True)
def handle_text_inputs(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "User"
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    add_user(user_id, message.from_user.username, first_name)

    if maintenance_enabled() and user_id != ADMIN_ID:
        bot.reply_to(message, "🛠 **Bot Maintenance Mode me hai!**", parse_mode='Markdown')
        return

    if not check_all_joined(user_id):
        caption_text = (
            f"Hey 👋 **{first_name.upper()}**\n\n"
            f"🔥 **Join all the channels to use the bot** 🔥"
        )
        bot.send_photo(
            chat_id=message.chat.id,
            photo=WELCOME_PHOTO_URL,
            caption=caption_text,
            reply_markup=force_join_markup(),
            parse_mode='Markdown'
        )
        return

    text_input = message.text.strip()
    state = user_states.get(user_id)

    if not state:
        bot.reply_to(message, "ℹ️ Kripya menu se pehle koi service chunein:", reply_markup=user_main_markup())
        return

    service_key = state.replace("waiting_", "")
    user_states.pop(user_id, None)
    increment_search()

    svc_data = API_CONFIG.get(service_key, {})
    service_name = svc_data.get("name", service_key)

    loading_msg = bot.reply_to(message, f"🔍 **Searching {service_name} Details...** ⏳", parse_mode='Markdown')

    # 👑 ADMIN REAL-TIME ALERT
    if ADMIN_ID:
        admin_alert = (
            f"🚨 **New {service_name} Query Alert!** 🚨\n\n"
            f"👤 **Searched By:** [{first_name}](tg://user?id={user_id})\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"🔗 **Username:** {username}\n"
            f"🛠️ **Service:** `{service_name}`\n"
            f"🔎 **Input:** `{text_input}`\n"
            f"⏰ **Status:** Executed"
        )
        try:
            bot.send_message(ADMIN_ID, admin_alert, parse_mode='Markdown')
        except Exception:
            pass

    # API Request Execution
    target_api = svc_data.get("url", "")
    if not target_api:
        bot.edit_message_text(
            f"⚙️ **{service_name} API URL** configure nahi hai.",
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            parse_mode='Markdown'
        )
        return

    try:
        url = target_api.format(query=text_input)
        response = requests.get(url, timeout=15)
        try:
            data = response.json()
            result_display = json.dumps(data, indent=2, ensure_ascii=False)
        except Exception:
            result_display = response.text

        caption_text = (
            f"🐍 **{service_name.upper()} SEARCH COMPLETED** 🐍\n\n"
            f"👤 **Queried By:** {first_name}\n"
            f"🔎 **Input:** `{text_input}`\n\n"
            f"📋 **Data:**\n```json\n{result_display[:850]}\n```\n\n"
            f"⚡ Powered by: {DEVELOPER_NAME}"
        )

        bot.send_photo(chat_id=message.chat.id, photo=SNAKE_PHOTO_URL, caption=caption_text, parse_mode='Markdown')
        bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error aaya: `{str(e)}`", chat_id=message.chat.id, message_id=loading_msg.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling(none_stop=True, skip_pending=True)
