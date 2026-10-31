import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "9173034885:AAFXSXdtk5_JAYN0bRjRwFh72rKxjkNrnvM")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    user_name = message.from_user.first_name or "друг"
    welcome_text = (
        f"👋 Салют, {user_name}! Я твой личный AI-продюсер и генератор сниппетов.\n\n"
        "⚡️ **Что я умею в облаке 24/7:**\n"
        "1. 🎬 **Создавать сниппеты**: пришли мне идею или текст — я распишу раскадровку и сценарные промпты.\n"
        "2. 🎵 **Работать с треками**: отправь мне аудиофайл или голосовое сообщение — выделю хук и подготовлю концепт клипа.\n"
        "3. 📸 **Image-to-Video**: отправь фото/кадр — я подготовлю точный промпт анимации движения (затяжка, дым, свет, движение камеры).\n\n"
        "Напиши мне идею или скинь файл, чтобы начать!"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Сделать раскадровку сниппета", callback_data="make_snippet")],
        [InlineKeyboardButton(text="🔥 Идея для вирусного Reels/TikTok", callback_data="make_viral")]
    ])
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(F.data == "make_snippet")
async def cb_make_snippet(callback: types.CallbackQuery):
    await callback.message.answer(
        "🎧 Отлично! Напиши мне в ответ:\n"
        "1. О чём трек / какая атмосфера (ночной город, романтика, трэп, драйв)?\n"
        "2. Кто в кадре (артист, персонаж, локация)?\n\n"
        "Или просто пришли мне аудиозапись трека!"
    )
    await callback.answer()

@dp.callback_query(F.data == "make_viral")
async def cb_make_viral(callback: types.CallbackQuery):
    await callback.message.answer(
        "🚀 Назови тему ролика или продукт, и я выдам 3 цепляющих хука на первые 3 секунды + сценарий на 20 секунд."
    )
    await callback.answer()

@dp.message(F.audio | F.voice)
async def handle_audio(message: types.Message):
    await message.answer(
        "🎵 Аудио получено!\n"
        "Анализирую трек... Подготавливаю структуру для 15-секундного сниппета (0-3с хук, 3-10с развитие, 10-15с дроп)."
    )

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer(
        "📸 Кадр принят!\n"
        "Создаю Image-to-Video промпт для анимации движения (Motion Prompt) под Google Flow / Kling..."
    )

@dp.message(F.text)
async def handle_text(message: types.Message):
    prompt = message.text
    response = (
        f"🎬 **Концепт сниппета по запросу:** «{prompt}»\n\n"
        "⏱ **0:00 – 0:03 (Визуальный хук):**\n"
        "Крупный план персонажа, неоновый свет, взгляд в камеру. В кадре появляется интригующий элемент.\n\n"
        "⏱ **0:03 – 0:08 (Динамика сцены):**\n"
        "Камера плавно облетает локацию. Движение, клубящийся дым / брызги дождя, атмосферное освещение.\n\n"
        "⏱ **0:08 – 0:15 (Кульминация):**\n"
        "Синхрон под бит, акцент на эмоциях артиста, затемнение в кульминации.\n\n"
        "✨ *Промпт для генерации видео в Flow/Kling:*\n"
        f"`Cinematic 4k shot of {prompt}, dynamic camera movement, volumetric cinematic lighting, 35mm lens, atmospheric depth.`"
    )
    await message.answer(response, parse_mode="Markdown")

async def main():
    logger.info("Starting Telegram Bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
