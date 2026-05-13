import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ── Config ──
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://tangerine-boba-ff5a75.netlify.app")
ADMIN_ID   = int(os.getenv("ADMIN_ID", "0"))  # твой Telegram ID

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# ── Keyboards ──
def main_keyboard():
    """Main reply keyboard with Open QARA button"""
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
    """Inline keyboard for /start message"""
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
    text = (
        f"👋 Привет, <b>{name}</b>!\n\n"
        f"Добро пожаловать в <b>QARA</b> — твой крипто-кошелёк и виртуальная карта.\n\n"
        f"<b>Что умеет QARA:</b>\n"
        f"💰 Хранение BTC, ETH, USDT, SOL\n"
        f"💳 Виртуальная Visa карта\n"
        f"⚡ Мгновенный обмен крипты\n"
        f"🌍 Apple Pay & Google Pay\n"
        f"📊 Курсы в реальном времени\n\n"
        f"Нажми кнопку ниже чтобы открыть приложение 👇"
    )
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )
    await message.answer(
        "Или открой через кнопку:",
        reply_markup=main_inline()
    )

# ── /help ──
@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "<b>Команды QARA:</b>\n\n"
        "/start — запустить бота\n"
        "/wallet — открыть кошелёк\n"
        "/rates — курсы криптовалют\n"
        "/card — управление картой\n"
        "/referral — реферальная программа\n"
        "/support — техподдержка\n"
        "/help — список команд"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_inline())

# ── /wallet ──
@dp.message(Command("wallet"))
async def cmd_wallet(message: Message):
    await message.answer(
        "💼 <b>QARA Wallet</b>\n\nОткрой приложение чтобы управлять балансом:",
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
    # Статичные курсы (потом подключим CoinGecko API)
    text = (
        "📊 <b>Курсы криптовалют</b>\n"
        "<i>Обновлено только что</i>\n\n"
        "₿ <b>Bitcoin</b>   $67,420.18  <code>+1.82%</code>\n"
        "◆ <b>Ethereum</b>  $3,184.06   <code>+3.47%</code>\n"
        "₮ <b>Tether</b>    $1.0001     <code>+0.01%</code>\n"
        "◎ <b>Solana</b>    $148.92     <code>-2.14%</code>\n"
        "B <b>BNB</b>       $580.40     <code>+4.22%</code>\n\n"
        "📈 Полная аналитика в приложении:"
    )
    await message.answer(
        text,
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
    text = (
        "💳 <b>QARA Virtual Card</b>\n\n"
        "• Visa карта для онлайн и офлайн платежей\n"
        "• Apple Pay & Google Pay\n"
        "• Пополнение через USDT/BTC/ETH\n"
        "• Работает в 150+ странах включая Европу\n\n"
        "Управляй картой в приложении:"
    )
    await message.answer(
        text,
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
    text = (
        f"🎁 <b>Реферальная программа</b>\n\n"
        f"Приглашай друзей и получай <b>$10 USDT</b> за каждого!\n\n"
        f"Твой код: <code>{ref_code}</code>\n"
        f"Твоя ссылка:\n<code>{ref_link}</code>\n\n"
        f"📌 Бонус начисляется после того как друг:\n"
        f"1. Зарегистрировался\n"
        f"2. Прошёл KYC\n"
        f"3. Пополнил карту на $50+"
    )
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔗 Поделиться ссылкой",
                url=f"https://t.me/share/url?url={ref_link}&text=Присоединяйся%20к%20QARA%20Wallet!"
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
    text = (
        "🆘 <b>Поддержка QARA</b>\n\n"
        "Опиши свою проблему и мы ответим в течение 5 минут.\n\n"
        "Или напиши напрямую: @qara_support\n\n"
        "Чат поддержки также доступен прямо в приложении 👇"
    )
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="💬 Открыть чат поддержки",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [InlineKeyboardButton(
                text="📝 Написать в поддержку",
                callback_data="write_support"
            )]
        ])
    )

# ── Callback handlers ──
@dp.callback_query(F.data == "rates")
async def cb_rates(call: CallbackQuery):
    text = (
        "📊 <b>Актуальные курсы</b>\n\n"
        "₿ BTC    $67,420  <code>+1.82%</code>\n"
        "◆ ETH    $3,184   <code>+3.47%</code>\n"
        "₮ USDT   $1.00    <code>+0.01%</code>\n"
        "◎ SOL    $148.92  <code>-2.14%</code>\n"
        "B BNB    $580.40  <code>+4.22%</code>\n\n"
        "Полная аналитика в приложении ↗"
    )
    await call.message.edit_text(
        text,
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
    text = (
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
        "<b>Лицензия:</b> В процессе получения\n"
        "<b>Партнёры:</b> Wallester, Sumsub, CoinGecko"
    )
    await call.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=back_inline()
    )
    await call.answer()

@dp.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    await call.message.edit_text(
        "🆘 <b>Поддержка</b>\n\nНапиши свой вопрос — мы ответим в течение 5 минут.\n\nИли открой чат в приложении:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="💬 Открыть чат",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [InlineKeyboardButton(text="‹ Назад", callback_data="back_main")]
        ])
    )
    await call.answer()

@dp.callback_query(F.data == "write_support")
async def cb_write_support(call: CallbackQuery):
    await call.message.answer(
        "✍️ Напиши свой вопрос следующим сообщением и мы передадим его оператору:"
    )
    await call.answer()

@dp.callback_query(F.data == "back_main")
async def cb_back(call: CallbackQuery):
    name = call.from_user.first_name or "друг"
    await call.message.edit_text(
        f"👋 Привет, <b>{name}</b>! Выбери действие:",
        parse_mode="HTML",
        reply_markup=main_inline()
    )
    await call.answer()

# ── Referral deep link ──
@dp.message(CommandStart(deep_link=True))
async def cmd_start_ref(message: Message, command):
    ref = command.args or ""
    if ref.startswith("ref_"):
        code = ref.replace("ref_", "")
        await message.answer(
            f"🎁 Ты пришёл по реферальной ссылке!\n"
            f"Код: <code>{code}</code>\n\n"
            f"После регистрации и KYC ты и твой друг получите по <b>$10 USDT</b>!",
            parse_mode="HTML"
        )
    await cmd_start(message)

# ── Forward user messages to admin ──
@dp.message(F.text & ~F.text.startswith("/"))
async def handle_message(message: Message):
    user = message.from_user
    # Forward to admin if set
    if ADMIN_ID:
        try:
            await bot.send_message(
                ADMIN_ID,
                f"💬 <b>Сообщение от пользователя</b>\n\n"
                f"👤 {user.full_name} (@{user.username or 'нет'})\n"
                f"🆔 ID: <code>{user.id}</code>\n\n"
                f"📝 {message.text}",
                parse_mode="HTML"
            )
        except Exception:
            pass

    await message.answer(
        "✅ Сообщение получено! Оператор ответит в течение 5 минут.\n\n"
        "Или открой чат поддержки прямо в приложении:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="💬 Открыть поддержку",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
    )

# ── Web App data handler ──
@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Handle data sent from Mini App to bot"""
    data = message.web_app_data.data
    logger.info(f"WebApp data from {message.from_user.id}: {data}")

    # Parse and respond
    import json
    try:
        payload = json.loads(data)
        action = payload.get("action", "")

        if action == "topup":
            amount = payload.get("amount", 0)
            await message.answer(
                f"✅ <b>Карта пополнена!</b>\n\nСумма: <b>${amount} USDT</b>",
                parse_mode="HTML"
            )
        elif action == "exchange":
            from_coin = payload.get("from", "")
            to_coin = payload.get("to", "")
            amount = payload.get("amount", 0)
            await message.answer(
                f"✅ <b>Обмен выполнен!</b>\n\n"
                f"{amount} {from_coin} → {to_coin}",
                parse_mode="HTML"
            )
        elif action == "kyc_complete":
            await message.answer(
                "🎉 <b>KYC пройден!</b>\n\n"
                "Твоя карта активирована. Теперь ты можешь пополнить её и начать пользоваться!",
                parse_mode="HTML"
            )
        else:
            await message.answer(f"📲 Данные из приложения получены.")

    except json.JSONDecodeError:
        await message.answer(f"📲 {data}")

# ── Main ──
async def main():
    logger.info("🚀 QARA Bot starting...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
