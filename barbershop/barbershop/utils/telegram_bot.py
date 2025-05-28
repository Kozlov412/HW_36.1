import os
import logging
import telegram
import asyncio
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токена бота и ID администратора из переменных окружения
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

async def send_telegram_message(message, chat_id=None, parse_mode="Markdown"):
    """
    Отправляет сообщение через Telegram бота.
    
    Args:
        message (str): Текст сообщения
        chat_id (str, optional): ID чата для отправки. По умолчанию используется ADMIN_CHAT_ID
        parse_mode (str, optional): Режим форматирования. По умолчанию "Markdown"
    """
    if not chat_id:
        chat_id = ADMIN_CHAT_ID
        
    if not BOT_TOKEN or not chat_id:
        logger.error("Не заданы переменные окружения TELEGRAM_BOT_TOKEN или TELEGRAM_ADMIN_CHAT_ID")
        return
    
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
        logger.info(f'Сообщение успешно отправлено в чат {chat_id}')
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения в Telegram: {e}")

def send_message(message, chat_id=None, parse_mode="Markdown"):
    """
    Синхронная обертка для отправки сообщения в Telegram
    """
    try:
        asyncio.run(send_telegram_message(message, chat_id, parse_mode))
    except Exception as e:
        logger.error(f"Ошибка при запуске асинхронной отправки: {e}")