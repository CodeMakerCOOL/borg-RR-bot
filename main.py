import telebot
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
user_dict = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "Hello i am Dorg, i will help you to use Borg's services such as investing RR stocks and RR business, to start please type /help.")

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
    
    if account_link:
        # Here you would add code to register the account link with the user's Telegram ID
        bot.send_message(msg.chat.id, f"Account link '{account_link}' registered successfully!")
    else:
        bot.send_message(msg.chat.id, "Please provide an account link. Usage: /register <account-link>")

@bot.message_handler(commands=['deposit'])
def deposit(msg):
    # Extract the amount from the message
    amount = msg.text.split(' ', 1)[1] if len(msg.text.split(' ', 1)) > 1 else None
    
    if amount and amount.isdigit():
        # Here you would add code to deposit the specified amount to the user's account
        bot.send_message(msg.chat.id, f"Deposited {amount} B$ to your account successfully!")
        user_dict[msg.chat.id] = user_dict.get(msg.chat.id, 0) + int(amount)  # Update the user's balance in the dictionary
    else:
        bot.send_message(msg.chat.id, "Please provide a valid amount. Usage: /deposit <amount>")

@bot.message_handler(commands=['withdraw'])
def withdraw(msg):
    # Extract the amount from the message
    amount = msg.text.split(' ', 1)[1] if len(msg.text.split(' ', 1)) > 1 else None
    
    if amount and amount.isdigit():
        # Here you would add code to withdraw the specified amount from the user's account and send it as RR money
        bot.send_message(msg.chat.id, f"Withdrew {amount} B$ from your account and sent it as RR money successfully!")
        user_dict[msg.chat.id] = user_dict.get(msg.chat.id, 0) - int(amount)  # Update the user's balance in the dictionary
    else:
        bot.send_message(msg.chat.id, "Please provide a valid amount. Usage: /withdraw <amount>")

@bot.message_handler(commands=['balance'])
def balance(msg):
    # Here you would add code to retrieve the user's account balance
    balance = user_dict.get(msg.chat.id, 0)
    bot.send_message(msg.chat.id, f"Your current balance is: {balance} B$")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        break