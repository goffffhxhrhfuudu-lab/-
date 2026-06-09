import os
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

QUOTES = [
    "Четыре колеса движут тело. Два колеса движут душу.",
    "Жизнь коротка — езди быстро и оставляй красивый след.",
    "Мотоцикл — это не просто машина. Это образ жизни.",
    "Ветер в лицо не шепчет. Он кричит: ты живёшь!",
    "Настоящая свобода — полный бак и открытая дорога.",
    "Два колеса, бесконечные возможности.",
    "Когда жизнь усложняется — я еду.",
    "Не бывает плохих дней на мотоцикле.",
    "Горизонт — это не конец. Это приглашение.",
    "Рождён ездить, вынужден работать.",
    "Держи блестящую сторону сверху, а резину — снизу.",
    "Дорога впереди всегда длиннее дороги позади.",
    "Скорость — награда для тех, кто осмеливается двигаться вперёд.",
    "Каждый километр вдвойне приятен после зимы.",
    "Мотоциклы — это не транспорт. Это трансформация.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"🏍️ Привет, {name}!\n\n"
        "Я твой мото-напарник.\n\n"
        "/quote — случайная цитата\n"
        "/help — все команды\n\n"
        "Езди безопасно! 🤘"
    )

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🏍️ {random.choice(QUOTES)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏍️ Команды:\n\n"
        "/quote — цитата\n"
        "/start — приветствие\n"
        "/help — это сообщение"
    )

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("help", help_command))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
