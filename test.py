import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
import sqlite3

print("Importing config - DONE!")

# Check database connection
c = sqlite3.connect(database_path)
if c:
    print("Database connection successful.")
else:
    print("Error: Unable to connect to the database.")
    exit()

# Drop table if force_new_database is enabled in config
cursor = c.cursor()
if force_new_database:
    cursor.execute('''DROP TABLE ORDERS;''')
    print("Forcing new database is enabled. Dropped table ORDERS. To disable it, navigate to config.py")
else:
    print("Force new database is disabled.")

# Create ORDERS table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS `ORDERS` (
  `ID` INTEGER PRIMARY KEY,
  `TGID` int(15) ,
  `MarketplaceType` varchar(15) ,
  `MarketplaceOption` varchar(10) ,
  `PackageType` varchar(5) ,
  `PackageOption` varchar(15),
  `OtherMarketplaceOption` varchar(100)
);''')
print("Table found/generated successfully!")
c.close()

bot = telebot.TeleBot("5873919687:AAEWzqvi3jg_Pvj26tYRaL5lV39bwVe9EG8")

# Main handler
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

# Order handler
@bot.message_handler(commands=['order'])
def send_welcome(message):
    print("Handling users order (" + str(message.chat.id)+")")
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_a = telebot.types.InlineKeyboardButton(text="Яндекс Маркет", callback_data="YM")
    button_b = telebot.types.InlineKeyboardButton(text="Wildberries", callback_data="WB")
    button_c = telebot.types.InlineKeyboardButton(text="Ozon", callback_data="OZ")
    keyboard.add(button_a, button_b, button_c)
    bot.send_message(message.chat.id, "Выберите ваш маркетплейс:", reply_markup=keyboard)

    c = sqlite3.connect(database_path)
    cursor = c.cursor()
    cursor.execute("INSERT INTO ORDERS (TGID) VALUES(?)", ([message.chat.id]))
    c.commit()
    c.close()

@bot.callback_query_handler(func=lambda call: True)
def handle_group_selection(call):
    print("Responding to user (" + str(call.message.chat.id) + ") choice. Chosen: " + str(call.data))

    if call.data == "YM":
        keyboard = telebot.types.InlineKeyboardMarkup()
        for option_value, option_text in storage_options["YM"].items():
            button = telebot.types.InlineKeyboardButton(text=option_text, callback_data=f"{option_value}")
            keyboard.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите склад:")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)  
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET MarketplaceType = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ((str(call.data)),call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()
    elif call.data == "WB":
        keyboard = telebot.types.InlineKeyboardMarkup()
        for option_value, option_text in storage_options["WB"].items():
            button = telebot.types.InlineKeyboardButton(text=option_text, callback_data=f"{option_value}")
            keyboard.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите склад:")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET MarketplaceType = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ((str(call.data)),call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()
    elif call.data == "OZ":
        keyboard = telebot.types.InlineKeyboardMarkup()
        for option_value, option_text in storage_options["OZ"].items():
            button = telebot.types.InlineKeyboardButton(text=option_text, callback_data=f"{option_value}")
            keyboard.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите склад:")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET MarketplaceType = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ((str(call.data)),call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()

    elif call.data.startswith(("WB:","OZ:","YM:")) and "other" in call.data:
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Для других складов другие цены, узнать их можно в поддержке.(@AlenaKoroleva088) \nПожалуйста, напишите название склада:")
        bot.register_next_step_handler(msg, register_other_storage)
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET MarketplaceOption = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ("other",call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()

    elif call.data.startswith(("WB:","OZ:","YM:")):
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_a2 = telebot.types.InlineKeyboardButton(text="Коробки", callback_data="BOX")
        button_b2 = telebot.types.InlineKeyboardButton(text="Паллеты", callback_data="PAL")
        keyboard.add(button_a2, button_b2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип упаковки:")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET MarketplaceOption = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ((str(call.data)[-1]),call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()

    elif call.data == "BOX":
        keyboard = telebot.types.InlineKeyboardMarkup()
        for option_value, option_text in package_options["BOX"].items():
            button = telebot.types.InlineKeyboardButton(text=option_text, callback_data=f"{option_value}")
            keyboard.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите опцию упаковки:")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET PackageType = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ((str(call.data)),call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()
    elif call.data == "PAL":
        keyboard = telebot.types.InlineKeyboardMarkup()
        for option_value, option_text in package_options["PAL"].items():
            button = telebot.types.InlineKeyboardButton(text=option_text, callback_data=f"{option_value}")
            keyboard.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите опцию упаковки:")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET PackageType = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ((str(call.data)),call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()

    elif call.data.startswith(("BOX:","PAL:")):
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_a3 = telebot.types.InlineKeyboardButton(text="Подтвердить", callback_data="CONFIRM")
        button_b3 = telebot.types.InlineKeyboardButton(text="Отменить", callback_data="DECLINE")
        keyboard.add(button_a3, button_b3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Подтвердить заказ?")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET PackageOption = (?) WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", ((str(call.data))[-1],call.message.chat.id,call.message.chat.id))
        c.commit()
        c.close()

    elif call.data == "CONFIRM":
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("SELECT * FROM ORDERS WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", (call.message.chat.id,call.message.chat.id))
        records = cursor.fetchall()
        for row in records:
            if row[3] == "other":
                message =bot.send_message(call.message.chat.id, text=("Ваш заказ создан!"+"\nМаркетплейс: "+storage_names[row[2]]+"\nСклад: "+str(row[6])+"\nТип упаковки: "+package_names[row[4]]+"\nОпция упаковки: "+package_options[row[4]][(row[4]+":"+row[5])]))            
            else:
                message =bot.send_message(call.message.chat.id, text=("Ваш заказ создан!"+"\nМаркетплейс: "+storage_names[row[2]]+"\nСклад: "+storage_options[row[2]][(row[2]+":"+row[3])]+"\nТип упаковки: "+package_names[row[4]]+"\nОпция упаковки: "+package_options[row[4]][(row[4]+":"+row[5])]))
        keyboard = telebot.types.InlineKeyboardMarkup()
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        bot.forward_message(chat_id=operator, from_chat_id=message.chat.id, message_id= message.id)
        bot.send_message(call.message.chat.id, text=("Ваш заказ отправлен оператору!"))
        c.close()

    elif call.data == "DECLINE":
        c = sqlite3.connect(database_path)
        cursor = c.cursor()
        cursor.execute("UPDATE ORDERS SET (MarketplaceType, MarketplaceOption, PackageType, PackageOption) = (?,?,?,?)  WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", (None,None,None,None,call.message.chat.id,call.message.chat.id))
        c.commit()
        bot.send_message(call.message.chat.id, text=("Ваш заказ отменён! Данные о нём успешно удалены."))
        c.close()       

def register_other_storage(message):
    chatid = message.chat.id
    c = sqlite3.connect(database_path)
    cursor = c.cursor()
    cursor.execute("UPDATE ORDERS SET  OtherMarketplaceOption = (?)  WHERE TGID = (?) AND ID = (SELECT MAX(ID) FROM ORDERS WHERE TGID = (?))", (message.text, chatid,chatid))
    c.commit()
    c.close()  
    msg = bot.send_message(chatid, text=("Принято!"))
    chatid = msg.chat.id
    m_id = msg.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_a2 = telebot.types.InlineKeyboardButton(text="Коробки", callback_data="BOX")
    button_b2 = telebot.types.InlineKeyboardButton(text="Паллеты", callback_data="PAL")
    keyboard.add(button_a2, button_b2)
    bot.edit_message_text(chat_id=chatid, message_id=m_id, text="Выберите тип упаковки:")
    bot.edit_message_reply_markup(chat_id=chatid, message_id=m_id, reply_markup=keyboard)




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