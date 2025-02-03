import os
import logging
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import TOKEN, URL

DEEPSEEK_API_URL = URL

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я бот на базе DeepSeek. Напиши вопрос или сообщение."
    )

def help_command(update, context):
    help_msg = """
*Как пользоваться:*
- Отправьте любое сообщение (текст).
- Я передам его DeepSeek, и бот ответит, что она сгенерирует.
"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.ParseMode.MARKDOWN,
        text=help_msg
    )

def echo_text(update, context):
    user_text = update.message.text
    try:
        # Шлём запрос к нашему DeepSeek API
        resp = requests.post(DEEPSEEK_API_URL, data={"prompt": user_text})
        if resp.status_code == 200:
            data = resp.json()
            deepseek_answer = data.get("response", "")
            context.bot.send_message(chat_id=update.effective_chat.id, text=deepseek_answer)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ошибка при запросе к DeepSeek API."
            )
    except Exception as e:
        logging.error(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Произошла ошибка при запросе к DeepSeek API."
        )

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Извините, я не знаю такой команды.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
