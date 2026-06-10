import telebot
from telebot import types
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

users = {}


@bot.message_handler(commands=['start'])
def start(message):
    users[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "🤖 Калькулятор Sarab\n\nВведите цену товара в юанях:"
    )


@bot.message_handler(func=lambda m: True)
def process(message):
    chat_id = message.chat.id

    if chat_id not in users:
        users[chat_id] = {}

    try:
        if "yuan" not in users[chat_id]:
            users[chat_id]["yuan"] = float(message.text)
            bot.send_message(chat_id, "⚖️ Введите вес товара (кг):")
            return

        if "weight" not in users[chat_id]:
            users[chat_id]["weight"] = float(message.text)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("🚚 Авто", "✈️ Авиа")

            bot.send_message(
                chat_id,
                "Выберите тип доставки:",
                reply_markup=markup
            )
            return

        yuan = users[chat_id]["yuan"]
        weight = users[chat_id]["weight"]

        product_price = yuan * 1800

        if message.text == "🚚 Авто":
            delivery = weight * 71390
        elif message.text == "✈️ Авиа":
            delivery = weight * 108900
        else:
            return
        total1 = product_price + delivery
        avr = total1 / 100 * 20
        total = product_price + delivery + avr
         
        bot.send_message(
            chat_id,
            f"""📦 Результат расчёта

💴 Цена товара: {product_price:,.0f} сум
🚚 Доставка: {delivery:,.0f} сум
💰 Цена услуги: {avr:,.0f} сум

✅ Итого: {total:,.0f} сум"""
        )

        users[chat_id] = {}

    except ValueError:
        bot.send_message(chat_id, "❌ Введите число.")


print("Бот запущен...")
bot.infinity_polling()
