import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

QUOTES = [
    "Четыре колеса движут тело. Два колеса движут душу.",
    "Жизнь коротка — езди быстро.",
    "Мотоцикл — это образ жизни.",
    "Ветер в лицо кричит: ты живёшь!",
    "Настоящая свобода — полный бак и открытая дорога.",
    "Два колеса, бесконечные возможности.",
    "Когда жизнь усложняется — я еду.",
    "Не бывает плохих дней на мотоцикле.",
    "Горизонт — это приглашение.",
    "Рождён ездить, вынужден работать.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏍️ Привет! Напиши /quote")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🏍️ {random.choice(QUOTES)}")

def main():
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quote", quote))
    app.run_polling()

if __name__ == "__main__":
    main()
