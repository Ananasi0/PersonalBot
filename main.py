import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

bot = telebot.TeleBot("5873919687:AAEWzqvi3jg_Pvj26tYRaL5lV39bwVe9EG8")

@bot.message_handler(commands=['start'])
def send_main_menu(message):
    print("Sending main menu to " + str(message.chat.id))
    bot.send_message(message.chat.id, "Приветствуем!\nПри помощи бота вы можете получить прайс-лист (/price), оформить заказ (/order) или обратиться в поддержку (/support).\nДля этого нажмите или напишите нужную команду.")

@bot.message_handler(commands=['price'])
def send_main_menu(message):
    print("Sending price list to " + str(message.chat.id))
    bot.send_message(message.chat.id, price_list)

@bot.message_handler(commands=['support'])
def send_main_menu(message):
    print("Sending support contacts to " + str(message.chat.id))
    bot.send_message(message.chat.id, support_contacts)

@bot.message_handler(commands=['stop'])
def send_main_menu(message):
    if message.chat.id in admins:
        print("Stopping the bot! Command sent by:" + str(message.chat.id))
        bot.send_message(message.chat.id, "Экстренное выключение!")
    else:
        print(str(message.chat.id) + "tried stopping the bot. Access denied.")
        bot.send_message(message.chat.id, "У вас нет доступа!")

import os
import sys
import time

def main():
    # Your bot's main logic goes here
    while True:
        try:
            # Run your bot
            bot.polling()
        except Exception as e:
            # Log the exception or take any necessary actions
            print(f"Error: {e}")
            
            # Restart the bot after a delay
            # Delay in seconds before restarting
            print(f"Restarting in {delay} seconds...")
            time.sleep(delay)
            os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == '__main__':
    main()