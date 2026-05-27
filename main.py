import telebot
import json
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
userdict = {}

# Load user data from a JSON file if it exists
try:
    with open(os.path.join(os.path.dirname(__file__), "user_data.json"), "r") as f:
        userdict = json.load(f)
except FileNotFoundError:
    pass

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "Hello i am Dorg, i will help you to use Borg's services such as investing RR stocks and RR business, to start please type /help.")
    userdict[msg.chat.id] = {"balance": 0, "account_link": None}  # Initialize user data in the dictionary

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
    # Extract the account link from the message
    account_link = msg.text.split(' ', 1)[1] if len(msg.text.split(' ', 1)) > 1 else None
    
    if account_link and userdict.get(msg.chat.id, {}).get("account_link") is None:
        # Here you would add code to register the account link with the user's Telegram ID
        bot.send_message(msg.chat.id, f"Account link '{account_link}' registered successfully!")
        userdict[msg.chat.id]["account_link"] = account_link  # Update the user's account
    else:
        bot.send_message(msg.chat.id, "Please provide an account link. Usage: /register <account-link>")

@bot.message_handler(commands=['deposit'])
def deposit(msg):
    # Extract the amount from the message
    amount = msg.text.split(' ', 1)[1] if len(msg.text.split(' ', 1)) > 1 else None
    
    if amount and amount.isdigit():
        # Here you would add code to deposit the specified amount to the user's account
        bot.send_message(msg.chat.id, f"Deposited {amount} B$ to your account successfully!")
        userdict[msg.chat.id]["balance"] = userdict.get(msg.chat.id, {}).get("balance", 0) + int(amount)  # Update the user's balance in the dictionary
    else:
        bot.send_message(msg.chat.id, "Please provide a valid amount. Usage: /deposit <amount>")

@bot.message_handler(commands=['withdraw'])
def withdraw(msg):
    # Extract the amount from the message
    amount = msg.text.split(' ', 1)[1] if len(msg.text.split(' ', 1)) > 1 else None
    
    if amount and amount.isdigit():
        # Here you would add code to withdraw the specified amount from the user's account and send it as RR money
        bot.send_message(msg.chat.id, f"Withdrew {amount} B$ from your account and sent it as RR money successfully!")
        userdict[msg.chat.id]["balance"] = userdict.get(msg.chat.id, {}).get("balance", 0) - int(amount)  # Update the user's balance in the dictionary
    else:
        bot.send_message(msg.chat.id, "Please provide a valid amount. Usage: /withdraw <amount>")

@bot.message_handler(commands=['balance'])
def balance(msg):
    # Here you would add code to retrieve the user's account balance
    balance = userdict.get(msg.chat.id, {}).get("balance", 0)
    bot.send_message(msg.chat.id, f"Your current balance is: {balance} B$")

# Save user data to a JSON file periodically
def save_user_data():
    with open(os.path.join(os.path.dirname(__file__), "user_data.json"), "w") as f:
        json.dump(userdict, f)

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        save_user_data()
        break
quit()