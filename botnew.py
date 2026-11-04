import telebot
from telebot import types
import requests
import json
import sqlite3
import os
import re
from threading import Thread
from flask import Flask

# ==================== 🌐 24/7 KEEP ALIVE SERVER ====================
app = Flask('')

@app.route('/')
def home():
    return "⚡ Sandesh Number Info Bot is Alive & Running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

keep_alive()

# ==================== ⚙️ CONFIGURATION ====================
BOT_TOKEN = os.environ.get("8852300357:AAHHfKP6qsbdJcNXhZP0UWIqTWrAWgSA2n4", "")

# API URLs: examples are shown in Admin > API Settings. Keep URLs blank until configured.
NUMBER_API_URL = "https://nitin-developer-api-paid.nitinshab43.workers.dev/api?action=num&number={number}&key=JAANI"
UPI_API_URL = "https://nitin-developer-api-paid.nitinshab43.workers.dev/api?action=upiinfo&upi={upi}&key=JAANI"
AADHAAR_API_URL = "https://nitin-developer-api-paid.nitinshab43.workers.dev/api?action=aadhar&aadhar={aadhar}&key=JAANI"
VEHICLE_API_URL = ""
PINCODE_API_URL = ""
IFSC_API_URL = ""
COUNTRY_API_URL = ""

# Admin Telegram Numeric User ID
ADMIN_ID = 1752541652

# Official Channel Link (यूजर के जॉइन करने के लिए)
CHANNEL_LINK = "https://t.me/Dracula_injector_selller"

# यहाँ अपने चैनल की Numeric ID डालें (जैसे -100xxxxxxxxxx)
# अगर अभी ID नहीं पता, तो इसे ऐसे ही रहने दें
CHANNEL_ID = -1002649665421  # <-- अपनी असली चैनल ID से बदलें

# Developer Details
DEVELOPER_NAME = "Sandesh Singh"
DEVELOPER_TAG = "@SANDESH870"

if not BOT_TOKEN:
    raise RuntimeError("Set the new Telegram bot token in the BOT_TOKEN environment variable.")
bot = telebot.TeleBot(BOT_TOKEN)

# Register the Telegram command menu
try:
    bot.set_my_commands([
        types.BotCommand("start", "Start the bot"),
        types.BotCommand("help", "Show help"),
        types.BotCommand("number", "Number search"),
        types.BotCommand("upi", "UPI ID format check"),
        types.BotCommand("aadhaar", "Official Aadhaar verification info"),
        types.BotCommand("country", "Country information"),
        types.BotCommand("admin", "Admin panel"),
        types.BotCommand("broadcast", "Send broadcast"),
    ])
except Exception as command_error:
    print(f"Could not register Telegram commands: {command_error}")

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
    cursor.execute(
        "INSERT OR REPLACE INTO bot_settings (setting, value) VALUES ('maintenance', ?)",
        ("1" if enabled else "0",)
    )
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
def is_user_joined(user_id):
    # Admin / Owner Bypass
    if user_id == ADMIN_ID:
        return True
    if not CHANNEL_ID:
        return True
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['creator', 'administrator', 'member', 'restricted']:
            return True
        return False
    except Exception as e:
        print(f"Force Join Check Error for User {user_id}: {e}")
        return False

def force_join_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel = types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
    btn_verify = types.InlineKeyboardButton("🔄 Check / Refresh", callback_data="check_join")
    markup.add(btn_channel, btn_verify)
    return markup

# ==================== 🔘 INLINE KEYBOARDS ====================
def user_main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("👨‍💻 Developer", callback_data="dev_info")
    b2 = types.InlineKeyboardButton("📢 Updates Channel", url=CHANNEL_LINK)
    b3 = types.InlineKeyboardButton("ℹ️ Help / How to use", callback_data="help_info")
    markup.add(b1, b2)
    markup.add(b3)
    markup.add(
        types.InlineKeyboardButton("🏦 IFSC Info", callback_data="api_ifsc"),
        types.InlineKeyboardButton("🌍 Country Info", callback_data="api_country")
    )
    markup.add(types.InlineKeyboardButton("📮 Pincode Info", callback_data="api_pincode"))
    return markup

def admin_panel_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats")
    b2 = types.InlineKeyboardButton("📢 Broadcast Msg", callback_data="admin_broadcast")
    b3 = types.InlineKeyboardButton("👥 Export Users Count", callback_data="admin_users")
    b4 = types.InlineKeyboardButton("❌ Close Panel", callback_data="close_panel")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(
        types.InlineKeyboardButton(
            "🛠 Maintenance: " + ("ON" if maintenance_enabled() else "OFF"),
            callback_data="admin_toggle_maintenance"
        ),
        types.InlineKeyboardButton("🔗 API Settings", callback_data="admin_api_settings")
    )
    return markup

# ==================== 🚀 COMMAND HANDLERS ====================
@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/number - Number search\n"
        "/upi - Check UPI ID format only\n"
        "/aadhaar - Official Aadhaar verification information\n"
        "/country - Country information (API must be configured)\n"
        "/admin - Admin panel\n"
        "/broadcast - Admin broadcast"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=["upi"])
def upi_command(message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2:
        bot.reply_to(message, "Usage: /upi name@bank\nThis checks basic format only, not account ownership.")
        return
    upi_id = parts[1].strip()
    if re.fullmatch(r"[A-Za-z0-9._-]{2,256}@[A-Za-z0-9.-]{2,64}", upi_id):
        bot.reply_to(message, "UPI ID ka basic format sahi lag raha hai. Account ownership verify nahi hui hai.")
    else:
        bot.reply_to(message, "UPI ID format valid nahi lag raha. Example: /upi name@bank")

@bot.message_handler(commands=["aadhaar"])
def aadhaar_command(message):
    bot.reply_to(message, "Aadhaar ke liye UIDAI ya authorized provider ka consent-based verification flow use karein. Is bot mein Aadhaar personal-details lookup enabled nahi hai.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    add_user(user_id, username, first_name)

    if maintenance_enabled() and user_id != ADMIN_ID:
        bot.reply_to(message, "🛠 Bot maintenance mode mein hai. Kripya kuch der baad try karein.")
        return
    
    # Check Force Join
    if not is_user_joined(user_id):
        text = (
            "⚠️ **Access Denied!**\n\n"
            "👋 Namaste! Bot ka istemal karne ke liye aapko pehle hamare official channel ko join karna hoga.\n\n"
            "👉 Niche diye gaye button par click karke channel join karein aur fir **'Check / Refresh'** dabayein!"
        )
        bot.reply_to(message, text, parse_mode='Markdown', reply_markup=force_join_markup())
        return

    welcome_text = (
        f"✨ **Welcome to Sandesh Number Info** ✨\n\n"
        f"👋 Hello **{first_name}**!\n\n"
        f"🔍 *Yahan aap kisi bhi 10 ankon ke mobile number ki information search kar sakte hain.*\n\n"
        f"📱 **Istemal kaise karein:**\n"
        f"Bas mujhe koi bhi 10 digits ka mobile number send karein.\n\n"
        f"👑 **Owner & Developer:** [{DEVELOPER_NAME}]({CHANNEL_LINK})\n"
        f"💬 **Admin:** {DEVELOPER_TAG}\n"
        f"🛡️ **Status:** Active & Ready\n\n"
        f"⚠️ **Safety Notice:** Do not message anyone using another person’s username or impersonate anyone. This may be considered a scam. Do not make false scam accusations or threaten anyone with an FIR."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=user_main_markup())

@bot.message_handler(commands=["number"])
def number_command(message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2:
        bot.reply_to(message, "Usage: /number 10-digit-number")
        return
    bot.reply_to(message, "Please send only a number you are authorized to check.")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Aapke paas is command ko use karne ki permission nahi hai!")
        return
    bot.reply_to(message, "👑 **Welcome Admin Sandesh!**\n\nNiche diye gaye options se bot control karein:", parse_mode='Markdown', reply_markup=admin_panel_markup())

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    msg = bot.reply_to(message, "📢 **Broadcast Mode:**\n\nKripya wo message bhejein jo sabhi users ko send karna hai (Text, Photo, Forwarded message):\n(Cancel karne ke liye /cancel likhein)", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.text == "/cancel":
        bot.reply_to(message, "❌ Broadcast cancel kar diya gaya.")
        return
    
    users = get_all_users()
    total = len(users)
    success = 0
    failed = 0
    
    status_msg = bot.reply_to(message, f"⏳ Broadcast shuru ho raha hai... (Total Users: {total})")
    
    for uid in users:
        try:
            bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
            success += 1
        except Exception:
            failed += 1
            
    bot.edit_message_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"👥 Total Users: `{total}`\n"
        f"🟢 Delivered: `{success}`\n"
        f"🔴 Failed / Blocked: `{failed}`",
        chat_id=message.chat.id,
        message_id=status_msg.message_id,
        parse_mode='Markdown'
    )

# ==================== 🔘 CALLBACK QUERY HANDLER ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    
    if call.data == "check_join":
        if is_user_joined(user_id):
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.send_message(
                call.message.chat.id,
                "✅ **Verification Successful!**\n\nWelcome to Sandesh Number Info! Ab aap koi bhi 10 digit number bhej kar info search kar sakte hain. 🔍",
                parse_mode='Markdown',
                reply_markup=user_main_markup()
            )
        else:
            bot.answer_callback_query(call.id, "❌ Aapne abhi tak channel join nahi kiya hai! Pehle join karein.", show_alert=True)
            
    elif call.data == "dev_info":
        dev_text = (
            f"👨‍💻 **Developer Information:**\n\n"
            f"👤 **Name:** {DEVELOPER_NAME}\n"
            f"💬 **Telegram:** {DEVELOPER_TAG}\n"
            f"📢 **Channel:** [Click Here]({CHANNEL_LINK})\n"
            f"⚡ **Version:** 2.0 (Official Edition)"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, dev_text, parse_mode='Markdown')
        
    elif call.data == "help_info":
        help_text = (
            "ℹ️ **How to Use Sandesh Number Info:**\n\n"
            "1️⃣ Chat me seedha 10 digits ka mobile number type karke bhejein.\n"
            "2️⃣ Jaise hi number aayega, bot instantly info search karke dikha dega.\n"
            "3️⃣ Agar koi problem aati hai to channel me admin se contact karein."
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, help_text, parse_mode='Markdown')
        
    elif call.data == "admin_stats":
        if user_id != ADMIN_ID:
            bot.answer_callback_query(call.id, "Access Denied!")
            return
        total_users, total_searches = get_stats()
        stats_text = (
            f"📊 **Bot Current Statistics:**\n\n"
            f"👥 **Total Registered Users:** `{total_users}`\n"
            f"🔍 **Total Searches Made:** `{total_searches}`\n"
            f"🟢 **Server Status:** Online (24/7)"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, stats_text, parse_mode='Markdown')
        
    elif call.data == "admin_broadcast":
        if user_id != ADMIN_ID:
            bot.answer_callback_query(call.id, "Access Denied!")
            return
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "📢 **Broadcast Message Bhejein:**\n(Cancel karne ke liye /cancel likhein)")
        bot.register_next_step_handler(msg, process_broadcast)
        
    elif call.data == "admin_users":
        if user_id != ADMIN_ID:
            return
        total_users, _ = get_stats()
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"👥 Database me abhi total `{total_users}` active users hain.")
        
    elif call.data == "api_ifsc":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🏦 IFSC lookup\nSend: /ifsc SBIN0000001")

    elif call.data == "api_country":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🌍 Country lookup\nSend: /country India")

    elif call.data == "api_pincode":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📮 Pincode lookup\nExample: /pincode 411001")

    elif call.data == "admin_toggle_maintenance":
        if user_id != ADMIN_ID:
            bot.answer_callback_query(call.id, "Access Denied!", show_alert=True)
            return
        new_state = not maintenance_enabled()
        set_maintenance(new_state)
        bot.answer_callback_query(call.id, "Maintenance " + ("ON" if new_state else "OFF"))
        try:
            bot.edit_message_reply_markup(
                call.message.chat.id, call.message.message_id,
                reply_markup=admin_panel_markup()
            )
        except Exception:
            pass

    elif call.data == "admin_api_settings":
        if user_id != ADMIN_ID:
            bot.answer_callback_query(call.id, "Access Denied!", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        text = (
            "🔗 *API URL Settings*\n\n"
            "URL placeholders blank hain. Examples: \n"
            "• Number: 9876543210\n"
            "• UPI: name@bank\n"
            "• Aadhaar: XXXX-XXXX-XXXX (sirf apne/authorized records)\n"
            "• Vehicle: vehicle registration number\n"
            "• Pincode: 411001\n"
            "• IFSC: SBIN0000001\n"
            "• Country: India\n\n"
            "Private personal-data lookup APIs activate nahi kiye gaye hain."
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        for label, key in [
            ("📱 Number API URL", "number"), ("💳 UPI API URL", "upi"),
            ("🪪 Aadhaar API URL", "aadhaar"), ("🚗 Vehicle API URL", "vehicle"),
            ("📮 Pincode API URL", "pincode"), ("🏦 IFSC API URL", "ifsc"),
            ("🌍 Country API URL", "country")
        ]:
            markup.add(types.InlineKeyboardButton(label, callback_data="api_url_" + key))
        markup.add(types.InlineKeyboardButton("↩️ Back to Admin", callback_data="back_admin"))
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

    elif call.data.startswith("api_url_"):
        if user_id != ADMIN_ID:
            bot.answer_callback_query(call.id, "Access Denied!", show_alert=True)
            return
        key = call.data.replace("api_url_", "", 1)
        placeholders = {
            "number": 'NUMBER_API_URL = ""', "upi": 'UPI_API_URL = ""',
            "aadhaar": 'AADHAAR_API_URL = ""', "vehicle": 'VEHICLE_API_URL = ""',
            "pincode": 'PINCODE_API_URL = ""', "ifsc": 'IFSC_API_URL = ""',
            "country": 'COUNTRY_API_URL = ""'
        }
        if key not in placeholders:
            bot.answer_callback_query(call.id, "Unknown API", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Code mein yeh blank setting hai:\n`" + placeholders[key] + "`\n\nExample input: " + {"number":"9876543210", "upi":"name@bank", "aadhaar":"XXXX-XXXX-XXXX", "vehicle":"registration number", "pincode":"411001", "ifsc":"SBIN0000001", "country":"India"}[key], parse_mode="Markdown")

    elif call.data == "back_admin":
        if user_id != ADMIN_ID:
            bot.answer_callback_query(call.id, "Access Denied!", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "👑 *Admin Panel*", parse_mode="Markdown", reply_markup=admin_panel_markup())

    elif call.data == "close_panel":
        bot.delete_message(call.message.chat.id, call.message.message_id)



# ==================== API COMMAND EXAMPLES ====================
# Examples: /ifsc SBIN0000001 | /country India | /pincode 411001
# API URL placeholders are intentionally blank. Add only authorized endpoints.

def api_not_configured(message, api_name):
    bot.reply_to(message, f"⚙️ {api_name} URL abhi blank hai. Admin code mein URL configure karein.")

@bot.message_handler(commands=["ifsc"])
def ifsc_command(message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2:
        bot.reply_to(message, "Example: /ifsc SBIN0000001")
        return
    code = parts[1].strip().upper()
    if not re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", code):
        bot.reply_to(message, "Please enter a valid-format IFSC code. Example: /ifsc SBIN0000001")
        return
    api_not_configured(message, "IFSC API")

@bot.message_handler(commands=["country"])
def country_command(message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2:
        bot.reply_to(message, "Example: /country India")
        return
    if len(parts[1].strip()) > 80:
        bot.reply_to(message, "Country name is too long.")
        return
    api_not_configured(message, "Country API")

@bot.message_handler(commands=["pincode"])
def pincode_command(message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2 or not re.fullmatch(r"\d{6}", parts[1].strip()):
        bot.reply_to(message, "Example: /pincode 411001")
        return
    api_not_configured(message, "Pincode API")


# ==================== 🔍 NUMBER SEARCH & ADMIN LOGGER ====================
    if not message.text:
        return

    if message.text.strip().startswith("/"):
        return
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    first_name = message.from_user.first_name
    add_user(user_id, message.from_user.username, first_name)

    if maintenance_enabled() and user_id != ADMIN_ID:
        bot.reply_to(message, "🛠 Bot maintenance mode mein hai. Kripya kuch der baad try karein.")
        return
    
    # 1. Force Join Check
    if not is_user_joined(user_id):
        bot.reply_to(
            message,
            "⚠️ **Access Denied!**\n\nBot use karne ke liye pehle hamara channel join karein!",
            reply_markup=force_join_markup(),
            parse_mode='Markdown'
        )
        return

    number = message.text.strip()
    
    # Check if input is 10 digit number
    if number.isdigit() and len(number) == 10:
        increment_search()
        loading_msg = bot.reply_to(message, "🔍 **सर्च किया जा रहा है, कृपया प्रतीक्षा करें...** ⏳", parse_mode='Markdown')
        
        # 2. ADMIN KO INSTANT LOG BHEJNA
        if ADMIN_ID:
            log_text = (
                f"🚨 **New Number Search Alert!** 🚨\n\n"
                f"👤 **User:** [{first_name}](tg://user?id={user_id})\n"
                f"🆔 **User ID:** `{user_id}`\n"
                f"🔗 **Username:** {username}\n"
                f"📱 **Searched Number:** `{number}`\n"
                f"⏰ **Status:** Executed"
            )
            try:
                bot.send_message(ADMIN_ID, log_text, parse_mode='Markdown')
            except Exception as e:
                print(f"Admin log error: {e}")
        
        # Number API URL (intentionally blank until you add your authorized endpoint)
        if not NUMBER_API_URL:
            bot.edit_message_text(
                "⚙️ Number API URL abhi blank hai. Admin code mein NUMBER_API_URL configure karein.",
                chat_id=message.chat.id,
                message_id=loading_msg.message_id
            )
            return

        try:
            api_url = NUMBER_API_URL.format(number=number)
            response = requests.get(api_url, timeout=15)
            
            try:
                data = response.json()
                formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
            except Exception:
                formatted_data = response.text
            
            reply_text = (
                f"🎉 **रिजल्ट सफलतापूर्वक मिल गया!** ✅\n\n"
                f"📱 **Mobile:** `{number}`\n\n"
                f"```json\n{formatted_data}\n```\n"
                f"⚡ Powered by: {DEVELOPER_NAME}"
            )
            bot.edit_message_text(reply_text, chat_id=message.chat.id, message_id=loading_msg.message_id, parse_mode='Markdown')
            
        except Exception as e:
            bot.edit_message_text(f"❌ **एरर आया:** `{str(e)}`", chat_id=message.chat.id, message_id=loading_msg.message_id, parse_mode='Markdown')
    else:
        bot.reply_to(message, "⚠️ **कृपया सिर्फ 10 अंकों का वैध मोबाइल नंबर भेजें।**\nउदाहरण: `9876543210`", parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling(none_stop=True, skip_pending=True)
