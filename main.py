import os
import json
import random
import logging
import threading
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

START_TIME = datetime.now(timezone.utc)

QUOTES = [
    "Четыре колеса движут тело. Два колеса движут душу.",
    "Жизнь коротка — езди быстро и оставляй красивый след.",
    "Ты не перестаёшь ездить, когда стареешь. Ты стареешь, когда перестаёшь ездить.",
    "Дело не в пункте назначения. Дело в пути — и в наклоне.",
    "Езди столько, сколько хочешь — далеко или близко. Но езди.",
    "Мотоцикл на дороге стоит двух в гараже.",
    "Нет ничего лучше хорошей поездки, кроме ещё одной хорошей поездки.",
    "Ночные мошки на вкус такие же, как дневные, но свобода — всегда одна.",
    "Иногда лучшая терапия — это долгая поездка без цели.",
    "У психиатра никогда не паркуется мотоцикл.",
    "Мотоцикл — это не просто машина. Это образ жизни.",
    "Дорога не заканчивается — она продолжается для тех, кто едет.",
    "На мотоцикле не возьмёшь много вещей. Но зато почувствуешь всё.",
    "Каждый километр вдвойне приятен после зимы.",
    "Ветер в лицо не шепчет. Он кричит: ты живёшь!",
    "Держи блестящую сторону сверху, а резину — снизу.",
    "Дождь, солнце или шторм — дороге нет дела до твоих отговорок.",
    "Крути ручку. Оставь сомнения позади.",
    "Скорость — это не всё. Но это великолепное всё.",
    "Хороший мотоциклист имеет равновесие, суждение и хорошую резину.",
    "Рождён ездить, вынужден работать.",
    "Дорога впереди всегда длиннее дороги позади.",
    "Мотоциклы — это не транспорт. Это трансформация.",
    "Жизнь лучше, когда едешь.",
    "Счастье не купишь, но мотоцикл — можно. Это одно и то же.",
    "Прямые дороги для быстрых байков. Повороты для быстрых гонщиков.",
    "Езди так, будто угнал — но владей так, будто сам построил.",
    "Не бывает плохих дней на мотоцикле.",
    "Когда жизнь усложняется — я еду.",
    "Два колеса, бесконечные возможности.",
    "Двигатель — сердце машины. Мотоциклист — её душа.",
    "Настоящая свобода — полный бак и открытая дорога.",
    "Смелость — это не отсутствие страха. Это сжать руль и всё равно наклониться.",
    "Езди далеко. Езди часто. Езди жёстко.",
    "Мотоцикл честен — он отвечает именно так, как ты с ним обращаешься.",
    "Километры, которые ты проезжаешь — это километры, которыми ты живёшь.",
    "Заправь машину. Освободи разум.",
    "Каждый великий мотоциклист когда-то был нервным новичком. Продолжай.",
    "Горизонт — это не конец. Это приглашение.",
    "Скорость — награда для тех, кто осмеливается двигаться вперёд.",
]


def format_uptime(delta_seconds: int) -> str:
    days = delta_seconds // 86400
    hours = (delta_seconds % 86400) // 3600
    minutes = (delta_seconds % 3600) // 60
    seconds = delta_seconds % 60
    parts = []
    if days:
        parts.append(f"{days} дн.")
    if hours:
        parts.append(f"{hours} ч.")
    if minutes:
        parts.append(f"{minutes} мин.")
    parts.append(f"{seconds} сек.")
    return " ".join(parts)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        uptime_seconds = int((datetime.now(timezone.utc) - START_TIME).total_seconds())
        if self.path in ("/health", "/healthz", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            body = json.dumps({
                "status": "ok",
                "bot": "Moto Quotes Bot",
                "uptime_seconds": uptime_seconds,
                "uptime": format_uptime(uptime_seconds),
                "started_at": START_TIME.isoformat(),
            }, ensure_ascii=False)
            self.wfile.write(body.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def run_health_server(port: int) -> None:
    HTTPServer.allow_reuse_address = True
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info("Health server running on port %d", port)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"🏍️ Добро пожаловать, {user}!\n\n"
        "Я — твоя ежедневная доза мотоциклетной мотивации.\n\n"
        "Используй /quote, чтобы получить цитату, или /help — чтобы увидеть все команды.\n\n"
        "Езди безопасно и почаще! 🤘"
    )


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    selected = random.choice(QUOTES)
    await update.message.reply_text(f"🏍️ *{selected}*", parse_mode="Markdown")


async def uptime_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    delta = int((datetime.now(timezone.utc) - START_TIME).total_seconds())
    started = START_TIME.strftime("%d.%m.%Y %H:%M UTC")
    await update.message.reply_text(
        f"⏱️ *Время работы бота*\n\n"
        f"Запущен: {started}\n"
        f"Аптайм: {format_uptime(delta)}",
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🏍️ *Moto Quotes Bot — Команды*\n\n"
        "/quote — Получить случайную мотивационную цитату\n"
        "/uptime — Показать время работы бота\n"
        "/start — Приветственное сообщение\n"
        "/help — Показать это сообщение\n\n"
        "_Держи резину снизу! 🤘_",
        parse_mode="Markdown"
    )


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand("quote", "Получить мотивационную цитату"),
        BotCommand("uptime", "Время работы бота"),
        BotCommand("help", "Показать доступные команды"),
        BotCommand("start", "Приветственное сообщение"),
    ])


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set.")

    health_port = int(os.environ.get("PORT", 8000))
    health_thread = threading.Thread(
        target=run_health_server,
        args=(health_port,),
        daemon=True
    )
    health_thread.start()

    app = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("uptime", uptime_command))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("Moto Quotes Bot запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
