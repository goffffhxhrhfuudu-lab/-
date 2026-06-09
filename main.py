import os
import random
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

QUOTES = [
    "Четыре колеса движут тело. Два колеса движут душу.",
    "Жизнь коротка — езди быстро и оставляй красивый след.",
    "Ты не перестаёшь ездить, когда стареешь. Ты стареешь, когда перестаёшь ездить.",
    "Дело не в пункте назначения. Дело в пути — и в наклоне.",
    "Мотоцикл — это не просто машина. Это образ жизни.",
    "Ветер в лицо не шепчет. Он кричит: ты живёшь!",
    "Настоящая свобода — полный бак и открытая дорога.",
    "Два колеса, бесконечные возможности.",
    "Когда жизнь усложняется — я еду.",
    "Держи блестящую сторону сверху, а резину — снизу.",
    "Не бывает плохих дней на мотоцикле.",
    "Горизонт — это не конец. Это приглашение.",
    "Мотоциклы — это не транспорт. Это трансформация.",
    "Каждый километр вдвойне приятен после зимы.",
    "Рождён ездить, вынужден работать.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"🏍️ Добро пожаловать, {user}!\n\n"
        "Я — твоя ежедневная доза мотоциклетной мотивации.\n\n"
        "/quote — получить цитату\n"
        "/help — все команды\n\n"
        "Езди безопасно! 🤘"
    )

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected = random.choice(QUOTES)
    await update.message.reply_text(f"🏍️ {selected}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏍️ Команды:\n\n"
        "/quote — случайная цитата\n"
        "/start — приветствие\n"
        "/help — это сообщение\n\n"
        "Держи резину снизу! 🤘"
    )

async def post_init(application: Application):
    await application.bot.set_my_commands([
        BotCommand("quote", "Мотивационная цитата"),
        BotCommand("help", "Список команд"),
        BotCommand("start", "Приветствие"),
    ])

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не установлен")

    app = Application.builder().token(token).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("help", help_command))

    print("🏍️ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
