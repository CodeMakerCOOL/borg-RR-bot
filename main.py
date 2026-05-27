import telebot
import json
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# In the JSON file keys are strings; always use string chat IDs
userdict = {}
DATA_FILE = os.path.join(os.path.dirname(__file__), "user_data.json")

# Load user data from a JSON file if it exists
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        userdict = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    userdict = {}


def save_user_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(userdict, f, indent=2)
    except Exception as e:
        print(f"Failed to save user data: {e}")


def ensure_user_entry(chat_id):
    uid = str(chat_id)
    if uid not in userdict:
        userdict[uid] = {"balance": 0, "account_link": None}
    return uid


@bot.message_handler(commands=['start'])
def start(msg):
    uid = ensure_user_entry(msg.chat.id)
    bot.send_message(msg.chat.id, "Hello i am Dorg, i will help you to use Borg's services such as investing RR stocks and RR business, to start please type /help.")
    save_user_data()


@bot.message_handler(commands=['help'])
def help(msg):
    bot.send_message(msg.chat.id, "Commands:"
    "\n/start - Start the bot,"
    "\n/help - Get some help," 
    "\n/register <account-link> - Register your RR account," 
    "\n/deposit <amount> - Deposits B$ to registered account," 
    "\n/withdraw <amount> - Withdraws B$ from your account and sends it as RR money to your RR account," 
    "\n/balance - Shows how much B$ you have in your account.")


@bot.message_handler(commands=['register'])
def register(msg):
    parts = msg.text.split(' ', 1)
    account_link = parts[1].strip() if len(parts) > 1 else None

    if not account_link:
        bot.send_message(msg.chat.id, "Please provide an account link. Usage: /register <account-link>")
        return
    if userdict.get(str(msg.chat.id), {}).get("account_link") is not None:
        bot.send_message(msg.chat.id, "You have already registered an account link. To update it, please contact support.")
        return
    if not account_link.startswith("https://rivalregions.com") and not account_link.startswith("https://rivalka.ru"):
        bot.send_message(msg.chat.id, "Invalid account link. It should start with 'https://rivalregions.com' or 'https://rivalka.ru'. Please try again.")
        return

    uid = ensure_user_entry(msg.chat.id)
    userdict[uid]["account_link"] = account_link
    bot.send_message(msg.chat.id, f"Account link '{account_link}' registered successfully!")
    save_user_data()


@bot.message_handler(commands=['deposit'])
def deposit(msg):
    parts = msg.text.split(' ', 1)
    amount = parts[1].strip() if len(parts) > 1 else None

    if amount and amount.isdigit() and userdict.get(str(msg.chat.id), {}).get("account_link") is not None:
        uid = ensure_user_entry(msg.chat.id)
        userdict[uid]["balance"] = userdict.get(uid, {}).get("balance", 0) + int(amount)
        bot.send_message(msg.chat.id, f"Deposited {amount} B$ to your account successfully!")
        save_user_data()
    elif userdict.get(str(msg.chat.id), {}).get("account_link") is None:
        bot.send_message(msg.chat.id, "You need to register an account link before depositing. Use /register <account-link> to register.")
    else:
        bot.send_message(msg.chat.id, "Please provide a valid amount. Usage: /deposit <amount>")


@bot.message_handler(commands=['withdraw'])
def withdraw(msg):
    parts = msg.text.split(' ', 1)
    amount = parts[1].strip() if len(parts) > 1 else None

    if amount and amount.isdigit() and userdict.get(str(msg.chat.id), {}).get("account_link") is not None:
        uid = ensure_user_entry(msg.chat.id)
        amt = int(amount)
        current = userdict.get(uid, {}).get("balance", 0)
        if amt > current:
            bot.send_message(msg.chat.id, "Insufficient balance.")
            return
        userdict[uid]["balance"] = current - amt
        bot.send_message(msg.chat.id, f"Withdrew {amount} B$ from your account and sent it as RR money successfully!")
        save_user_data()
    elif userdict.get(str(msg.chat.id), {}).get("account_link") is None:
        bot.send_message(msg.chat.id, "You need to register an account link before withdrawing. Use /register <account-link> to register.")
    else:
        bot.send_message(msg.chat.id, "Please provide a valid amount. Usage: /withdraw <amount>")


@bot.message_handler(commands=['balance'])
def balance(msg):
    if userdict.get(str(msg.chat.id), {}).get("account_link") is None:
        bot.send_message(msg.chat.id, "You need to register an account link before checking balance. Use /register <account-link> to register.")
        return
    uid = str(msg.chat.id)
    bal = userdict.get(uid, {}).get("balance", 0)
    bot.send_message(msg.chat.id, f"Your current balance is: {bal} B$")


while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        save_user_data()
        break
    except Exception as e:
        print(f"Error: {e}")
        # keep running after transient errors
        continue
quit()