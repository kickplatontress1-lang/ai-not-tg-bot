import telebot
from model import get_class

# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, отправь картинку и я узнаю, насколько эта картинка нейрослоп или нет")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, "Это не картинка")
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    result = get_class("keras_model.h5", "labels.txt", file_name)
    bot.send_message(message.chat.id, result)

# Запускаем бота
bot.polling()
