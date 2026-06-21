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
    "Дорога впереди всегда длиннее дороги позади.",
    "Скорость — награда для тех, кто осмеливается двигаться вперёд.",
    "Каждый километр вдвойне приятен после зимы.",
    "Мотоциклы — это не транспорт. Это трансформация.",
    "Держи блестящую сторону сверху, а резину — снизу.",
    "Дело не в пункте назначения. Дело в пути.",
    "Ты не перестаёшь ездить, когда стареешь. Ты стареешь, когда перестаёшь ездить.",
    "Лучшее лекарство от любых проблем — открытая трасса.",
    "Мотоцикл учит главному: падать не страшно, страшно не встать.",
    "На мотоцикле ты не стоишь в пробке — ты наблюдаешь за ней сверху.",
    "Дорога — это не место назначения, это состояние души.",
    "Каждый поворот — это выбор. Делай его осознанно.",
    "Дорога уравнивает всех. На ней ты просто байкер.",
    "Мотоцикл — единственная машина, которая едет душой.",
    "Не спрашивай зачем байк. Спроси — каково без него.",
]

FACTS = [
    "Первый в мире мотоцикл был построен в 1885 году Готлибом Даймлером.",
    "Самый дорогой мотоцикл в истории был продан за более чем $1 млн.",
    "Слово 'мотоцикл' происходит от французского 'motocyclette'.",
    "В Индии производится больше мотоциклов, чем в любой другой стране мира.",
    "Самый быстрый серийный мотоцикл может разгоняться свыше 400 км/ч.",
    "Harley-Davidson был основан в 1903 году в маленьком сарае.",
    "Мотоциклетные шлемы стали обязательными в большинстве стран только в 1970-х.",
    "Самая длинная мотоциклетная поездка в истории превысила 700 000 км.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"🏍️ Привет, {name}!\n\n"
        "Я твой мото-напарник.\n\n"
        "/quote — мото цитата\n"
        "/fact — интересный факт\n"
        "/help — все команды\n\n"
        "Езди безопасно! 🤘"
    )

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🏍️ {random.choice(QUOTES)}")

async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💡 {random.choice(FACTS)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏍️ Команды:\n\n"
        "/quote — случайная мото цитата\n"
        "/fact — интересный факт о мотоциклах\n"
        "/start — приветствие\n"
        "/help — это сообщение"
    )

def main():
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("fact", fact))
    app.add_handler(CommandHandler("help", help_command))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
