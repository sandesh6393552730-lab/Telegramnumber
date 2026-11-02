import telebot
from telebot import types
import requests
import json
import sqlite3
import os
from threading import Thread
from flask import Flask

# ==================== 🌐 24/7 KEEP ALIVE SERVER (FOR RENDER / KOYEB) ====================
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
BOT_TOKEN = "8852300357:AAHHfKP6qsbdJcNXhZP0UWIqTWrAWgSA2n4"

# Admin Telegram Numeric User ID
ADMIN_ID = 1752541652

# Official Channel Details
CHANNEL_USERNAME = "@Dracula_injector_selller"
CHANNEL_LINK = "https://t.me/Dracula_injector_selller"

# Developer Details
DEVELOPER_NAME = "Sandesh Singh"
DEVELOPER_TAG = "@SANDESH870"

bot = telebot.TeleBot(BOT_TOKEN)

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
    if not CHANNEL_USERNAME:
        return True
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception:
        return True

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
    return markup

def admin_panel_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats")
    b2 = types.InlineKeyboardButton("📢 Broadcast Msg", callback_data="admin_broadcast")
    b3 = types.InlineKeyboardButton("👥 Export Users Count", callback_data="admin_users")
    b4 = types.InlineKeyboardButton("❌ Close Panel", callback_data="close_panel")
    markup.add(b1, b2)
    markup.add(b3, b4)
    return markup

# ==================== 🚀 COMMAND HANDLERS ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    add_user(user_id, username, first_name)
    
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
        f"🛡️ **Status:** Active & Ready"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=user_main_markup())

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
            bot.delete_message(call.message.chat.id, call.message.message_id)
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
            f"📢 **Channel:** {CHANNEL_USERNAME}\n"
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
        
    elif call.data == "close_panel":
        bot.delete_message(call.message.chat.id, call.message.message_id)

# ==================== 🔍 NUMBER SEARCH & ADMIN LOGGER ====================
@bot.message_handler(func=lambda message: True)
def get_number_info(message):
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    first_name = message.from_user.first_name
    add_user(user_id, message.from_user.username, first_name)
    
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
        
        # 2. ADMIN KO INSTANT LOG BHEJNA (User Details + Searched Number)
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
        
        # API URL (Already set with key and number)
        api_url = f"https://admin.gbssystems.com/public/api/v1/api.php?key=8AF6N&cmd=number&query={number}"
        
        try:
            response = requests.get(api_url, timeout=15)
            
            # API JSON ya Text handling
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
