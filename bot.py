import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, ReplyKeyboardMarkup, KeyboardButton,
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")
ADMIN_ID   = int(os.getenv("ADMIN_ID", "462231903"))

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# Хранилище: reply_to[admin_msg_id] = user_id
reply_map = {}

# ── Keyboards ──
def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text="💳 Открыть QARA",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]],
        resize_keyboard=True,
        persistent=True
    )

def main_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💳 Открыть QARA Wallet",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [
            InlineKeyboardButton(text="📊 Курсы", callback_data="rates"),
            InlineKeyboardButton(text="ℹ️ О нас", callback_data="about"),
        ],
        [InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")],
    ])

def back_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="‹ Назад", callback_data="back_main")]
    ])

# ── /start ──
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
        f"Нажми кнопку ниже чтобы открыть приложение 👇",
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )
    await message.answer(
        "Выбери действие:",
        reply_markup=main_inline()
    )

# ── /help ──
@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Команды QARA:</b>\n\n"
        "/start — запустить бота\n"
        "/wallet — открыть кошелёк\n"
        "/rates — курсы криптовалют\n"
        "/card — управление картой\n"
        "/referral — реферальная программа\n"
        "/support — техподдержка\n"
        "/help — список команд",
        parse_mode="HTML",
        reply_markup=main_inline()
    )

# ── /wallet ──
@dp.message(Command("wallet"))
async def cmd_wallet(message: Message):
    await message.answer(
        "💼 <b>QARA Wallet</b>\n\nОткрой приложение:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="💳 Открыть кошелёк",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
    )

# ── /rates ──
@dp.message(Command("rates"))
async def cmd_rates(message: Message):
    await message.answer(
        "📊 <b>Курсы криптовалют</b>\n\n"
        "₿ <b>Bitcoin</b>   $67,420  <code>+1.82%</code>\n"
        "◆ <b>Ethereum</b>  $3,184   <code>+3.47%</code>\n"
        "₮ <b>Tether</b>    $1.00    <code>+0.01%</code>\n"
        "◎ <b>Solana</b>    $148.92  <code>-2.14%</code>\n\n"
        "Полная аналитика в приложении:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="📊 Открыть Markets",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
    )

# ── /card ──
@dp.message(Command("card"))
async def cmd_card(message: Message):
    await message.answer(
        "💳 <b>QARA Virtual Card</b>\n\n"
        "• Visa карта для онлайн и офлайн платежей\n"
        "• Apple Pay & Google Pay\n"
        "• Пополнение через USDT/BTC/ETH\n"
        "• Работает в 150+ странах\n\n"
        "Управляй картой в приложении:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="💳 Управление картой",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
    )

# ── /referral ──
@dp.message(Command("referral"))
async def cmd_referral(message: Message):
    user_id = message.from_user.id
    ref_code = f"QARA{str(user_id)[-4:]}"
    ref_link = f"https://t.me/cruptoqara_bot?start=ref_{ref_code}"
    await message.answer(
        f"🎁 <b>Реферальная программа</b>\n\n"
        f"Приглашай друзей и получай <b>$10 USDT</b> за каждого!\n\n"
        f"Твой код: <code>{ref_code}</code>\n"
        f"Твоя ссылка:\n<code>{ref_link}</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔗 Поделиться",
                url=f"https://t.me/share/url?url={ref_link}&text=Присоединяйся к QARA!"
            )],
            [InlineKeyboardButton(
                text="💳 Открыть QARA",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ])
    )

# ── /support ──
@dp.message(Command("support"))
async def cmd_support(message: Message):
    await message.answer(
        "🆘 <b>Поддержка QARA</b>\n\n"
        "Напиши своё сообщение — оператор ответит в течение 5 минут.\n\n"
        "Просто отправь текст прямо сюда 👇",
        parse_mode="HTML"
    )

# ── Callbacks ──
@dp.callback_query(F.data == "rates")
async def cb_rates(call: CallbackQuery):
    await call.message.edit_text(
        "📊 <b>Актуальные курсы</b>\n\n"
        "₿ BTC    $67,420  <code>+1.82%</code>\n"
        "◆ ETH    $3,184   <code>+3.47%</code>\n"
        "₮ USDT   $1.00    <code>+0.01%</code>\n"
        "◎ SOL    $148.92  <code>-2.14%</code>\n\n"
        "Полная аналитика в приложении ↗",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📊 Открыть Markets",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [InlineKeyboardButton(text="‹ Назад", callback_data="back_main")]
        ])
    )
    await call.answer()

@dp.callback_query(F.data == "about")
async def cb_about(call: CallbackQuery):
    await call.message.edit_text(
        "ℹ️ <b>О QARA</b>\n\n"
        "QARA — финтех платформа нового поколения.\n\n"
        "<b>Возможности:</b>\n"
        "• Мультивалютный крипто-кошелёк\n"
        "• Виртуальная Visa карта\n"
        "• Обмен крипты по лучшему курсу\n"
        "• Apple Pay & Google Pay\n"
        "• KYC верификация через Sumsub\n"
        "• Работает в 150+ странах\n\n"
        "<b>Юрисдикция:</b> Эстония (ЕС)\n"
        "<b>Партнёры:</b> Wallester, Sumsub, CoinGecko",
        parse_mode="HTML",
        reply_markup=back_inline()
    )
    await call.answer()

@dp.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    await call.message.edit_text(
        "🆘 <b>Поддержка</b>\n\n"
        "Напиши своё сообщение — оператор ответит в течение 5 минут.\n\n"
        "Просто отправь текст прямо в этот чат 👇",
        parse_mode="HTML",
        reply_markup=back_inline()
    )
    await call.answer()

@dp.callback_query(F.data == "back_main")
async def cb_back(call: CallbackQuery):
    await call.message.edit_text(
        "Выбери действие:",
        reply_markup=main_inline()
    )
    await call.answer()

# ── Главный обработчик сообщений пользователей ──
@dp.message(F.text & ~F.text.startswith("/"))
async def handle_user_message(message: Message):
    user = message.from_user

    # Если это АДМИН отвечает — пересылаем пользователю
    if user.id == ADMIN_ID and message.reply_to_message:
        original_msg_id = message.reply_to_message.message_id
        target_user_id = reply_map.get(original_msg_id)
        if target_user_id:
            try:
                await bot.send_message(
                    target_user_id,
                    f"💬 <b>Ответ от поддержки QARA:</b>\n\n{message.text}",
                    parse_mode="HTML"
                )
                await message.answer("✅ Ответ отправлен пользователю")
            except Exception as e:
                await message.answer(f"❌ Ошибка: {e}")
            return

    # Обычный пользователь — пересылаем админу
    try:
        sent = await bot.send_message(
            ADMIN_ID,
            f"💬 <b>Сообщение в поддержку</b>\n\n"
            f"👤 {user.full_name}\n"
            f"🔗 @{user.username or '—'}\n"
            f"🆔 <code>{user.id}</code>\n\n"
            f"📝 {message.text}\n\n"
            f"<i>Ответь на это сообщение чтобы написать пользователю</i>",
            parse_mode="HTML"
        )
        # Запоминаем связь: сообщение админу → user_id
        reply_map[sent.message_id] = user.id

    except Exception as e:
        logger.error(f"Failed to forward to admin: {e}")

    await message.answer(
        "✅ Сообщение получено! Оператор ответит в течение 5 минут.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="💳 Открыть QARA",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
    )

# ── Web App data ──
@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    import json
    try:
        payload = json.loads(message.web_app_data.data)
        action = payload.get("action", "")
        if action == "topup":
            await message.answer(f"✅ Карта пополнена на ${payload.get('amount')} USDT", parse_mode="HTML")
        elif action == "exchange":
            await message.answer(f"✅ Обмен выполнен: {payload.get('from')} → {payload.get('to')}", parse_mode="HTML")
        elif action == "kyc_complete":
            await message.answer("🎉 KYC пройден! Карта активирована.", parse_mode="HTML")
    except Exception:
        pass

# ── Main ──
async def main():
    logger.info("🚀 QARA Bot starting...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
