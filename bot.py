import asyncio
import logging
import os
import json
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, ReplyKeyboardMarkup, KeyboardButton,
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")
ADMIN_ID   = int(os.getenv("ADMIN_ID", "462231903"))
PORT       = int(os.getenv("PORT", "8080"))

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())
reply_map = {}

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="💳 Открыть QARA", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True, persistent=True
    )

def main_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Открыть QARA Wallet", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="📊 Курсы", callback_data="rates"),
         InlineKeyboardButton(text="ℹ️ О нас", callback_data="about")],
        [InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")],
    ])

def back_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="‹ Назад", callback_data="back_main")]
    ])

# ── HTTP endpoint для Mini App ──
async def handle_support(request: web.Request):
    try:
        data = await request.json()
        text      = data.get('text', '').strip()
        user_id   = data.get('user_id', 0)
        username  = data.get('username', '')
        full_name = data.get('full_name', 'Пользователь').strip()
        time_str  = data.get('time', '')

        if not text:
            return web.json_response({'ok': False, 'error': 'empty'}, status=400)

        uname = f"@{username}" if username else "—"
        sent = await bot.send_message(
            ADMIN_ID,
            f"💬 <b>Сообщение из Mini App</b>\n\n"
            f"👤 {full_name}\n🔗 {uname}\n🆔 <code>{user_id}</code>\n🕐 {time_str}\n\n"
            f"📝 {text}\n\n<i>Ответь на это сообщение чтобы написать пользователю</i>",
            parse_mode="HTML"
        )
        if user_id:
            reply_map[sent.message_id] = user_id

        return web.json_response({'ok': True})
    except Exception as e:
        logger.error(f"Support error: {e}")
        return web.json_response({'ok': False, 'error': str(e)}, status=500)

async def handle_health(request):
    return web.json_response({'status': 'ok'})

# ── Bot handlers ──
@dp.message(CommandStart())
async def cmd_start(message: Message):
    name = message.from_user.first_name or "друг"
    await message.answer(
        f"👋 Привет, <b>{name}</b>!\n\n"
        f"Добро пожаловать в <b>QARA</b> — твой крипто-кошелёк и виртуальная карта.\n\n"
        f"<b>Что умеет QARA:</b>\n"
        f"💰 Хранение BTC, ETH, USDT, SOL\n"
        f"💳 Виртуальная Visa карта\n"
        f"⚡ Мгновенный обмен крипты\n"
        f"🌍 Apple Pay & Google Pay\n"
        f"📊 Курсы в реальном времени\n\n"
        f"Нажми кнопку ниже 👇",
        parse_mode="HTML", reply_markup=main_keyboard()
    )
    await message.answer("Выбери действие:", reply_markup=main_inline())

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Команды:</b>\n/start /wallet /rates /card /referral /support /help",
        parse_mode="HTML", reply_markup=main_inline()
    )

@dp.message(Command("rates"))
async def cmd_rates(message: Message):
    await message.answer(
        "📊 <b>Курсы</b>\n\n₿ BTC $67,420 <code>+1.82%</code>\n◆ ETH $3,184 <code>+3.47%</code>\n"
        "₮ USDT $1.00 <code>+0.01%</code>\n◎ SOL $148.92 <code>-2.14%</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="📊 Открыть Markets", web_app=WebAppInfo(url=WEBAPP_URL))
        ]])
    )

@dp.message(Command("support"))
async def cmd_support(message: Message):
    await message.answer(
        "🆘 <b>Поддержка QARA</b>\n\nНапиши своё сообщение 👇",
        parse_mode="HTML"
    )

@dp.message(Command("referral"))
async def cmd_referral(message: Message):
    uid = message.from_user.id
    code = f"QARA{str(uid)[-4:]}"
    link = f"https://t.me/cruptoqara_bot?start=ref_{code}"
    await message.answer(
        f"🎁 <b>Реферальная программа</b>\n\nПолучай <b>$10 USDT</b> за каждого друга!\n\n"
        f"Код: <code>{code}</code>\nСсылка: <code>{link}</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Поделиться", url=f"https://t.me/share/url?url={link}")],
            [InlineKeyboardButton(text="💳 Открыть QARA", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
    )

@dp.callback_query(F.data == "rates")
async def cb_rates(call: CallbackQuery):
    await call.message.edit_text(
        "📊 <b>Курсы</b>\n\n₿ BTC $67,420 <code>+1.82%</code>\n◆ ETH $3,184 <code>+3.47%</code>\n"
        "₮ USDT $1.00 <code>+0.01%</code>\n◎ SOL $148.92 <code>-2.14%</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Markets", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton(text="‹ Назад", callback_data="back_main")]
        ])
    )
    await call.answer()

@dp.callback_query(F.data == "about")
async def cb_about(call: CallbackQuery):
    await call.message.edit_text(
        "ℹ️ <b>О QARA</b>\n\n• Крипто-кошелёк\n• Visa карта\n• Apple/Google Pay\n"
        "• 150+ стран\n\n<b>Юрисдикция:</b> Эстония\n<b>Партнёры:</b> Wallester, Sumsub",
        parse_mode="HTML", reply_markup=back_inline()
    )
    await call.answer()

@dp.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    await call.message.edit_text(
        "🆘 Напиши своё сообщение — ответим в течение 5 минут 👇",
        reply_markup=back_inline()
    )
    await call.answer()

@dp.callback_query(F.data == "back_main")
async def cb_back(call: CallbackQuery):
    await call.message.edit_text("Выбери действие:", reply_markup=main_inline())
    await call.answer()

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: Message):
    user = message.from_user
    if user.id == ADMIN_ID and message.reply_to_message:
        target = reply_map.get(message.reply_to_message.message_id)
        if target:
            try:
                await bot.send_message(target,
                    f"💬 <b>Ответ от поддержки QARA:</b>\n\n{message.text}", parse_mode="HTML")
                await message.answer("✅ Отправлено пользователю")
            except Exception as e:
                await message.answer(f"❌ Ошибка: {e}")
            return

    try:
        sent = await bot.send_message(ADMIN_ID,
            f"💬 <b>Сообщение из бота</b>\n\n👤 {user.full_name}\n🔗 @{user.username or '—'}\n"
            f"🆔 <code>{user.id}</code>\n\n📝 {message.text}\n\n"
            f"<i>Ответь на это сообщение чтобы написать пользователю</i>", parse_mode="HTML")
        reply_map[sent.message_id] = user.id
    except Exception as e:
        logger.error(f"Forward error: {e}")

    await message.answer("✅ Сообщение получено! Ответим в течение 5 минут.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="💳 Открыть QARA", web_app=WebAppInfo(url=WEBAPP_URL))
        ]])
    )

# ── Main ──
async def main():
    app = web.Application()
    app.router.add_post('/support', handle_support)
    app.router.add_get('/health', handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', PORT).start()
    logger.info(f"🌐 HTTP server on port {PORT}")
    logger.info("🚀 QARA Bot starting...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
