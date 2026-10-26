import os
import threading
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  markup = telebot.types.InlineKeyboardMarkup()
  btn1 = telebot.types.InlineKeyboardButton("قناة التليجرام", url="https://t.me")
  btn2 = telebot.types.InlineKeyboardButton("مساعدة", callback_data="help")
  markup.add(btn1, btn2)
  bot.reply_to(
      message,
      "أهلاً بك عيني! البوت اشتغل بنجاح 🚀\nاختر من الأزرار أدناه:",
      reply_markup=markup,
  )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  if call.data == "help":
    bot.answer_callback_query(call.id, "تم النقر بنجاح!")
    bot.send_message(call.message.chat.id, "هذا بوت تجريبي يعمل بنجاح تامة.")


if __name__ == "__main__":

  def run_bot():
    bot.infinity_polling()

  t = threading.Thread(target=run_bot)
  t.daemon = True
  t.start()

  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
  
