import telebot
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "Hello i am Dorg, i will help you to use Borg's services such as investing RR stocks and RR business, to start please type /help.")

@bot.message_handler(commands=['help'])
def help(msg):
    bot.send_message(msg.chat.id, "Commands\n/start - Start the bot\n/help - Get some help\n/register <account-link> - Register your RR account\n/deposit <amount> - Deposits B$ to registered account\n/withdraw <amount> - Withdraws B$ from your account and sends it as RR money to your RR account\n/balance - Shows how much B$ you have in your account")