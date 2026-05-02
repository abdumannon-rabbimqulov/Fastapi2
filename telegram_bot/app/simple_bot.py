"""
Oddiy Telegram Bot - User info collection + PostgreSQL + AI Chat
"""
import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import asyncpg
from ai import generate_response

# Konfiguratsiya
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation states
ASKING_NAME, ASKING_PHONE, ASKING_EMAIL, CHATTING_WITH_AI = range(4)

db_pool = None

# ============ Database Functions ============
async def init_db():
    """PostgreSQL database initialize"""
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    
    async with db_pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                username TEXT,
                first_name TEXT,
                phone TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')

async def save_user(telegram_id, username, first_name, phone, email):
    """User ma'lumotlarini PostgreSQL ga suhrafayq"""
    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO users (telegram_id, username, first_name, phone, email)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (telegram_id) DO UPDATE SET
                phone = EXCLUDED.phone,
                email = EXCLUDED.email
        ''', telegram_id, username, first_name, phone, email)

# ============ Bot Handlers ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot start - ma'lumot talab qilishni boshlash"""
    user = update.effective_user
    await update.message.reply_text(
        f"Salom {user.first_name}! 👋\n\n"
        "Iltimos, ismingizni kiriting:"
    )
    return ASKING_NAME

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ismdan keyin telefon talab qilish"""
    context.user_data['first_name'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return ASKING_PHONE

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefondan keyin email talab qilish"""
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Email addressingizni kiriting:")
    return ASKING_EMAIL

async def save_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Email dan keyin DB ga suhafayq va tugatish"""
    context.user_data['email'] = update.message.text
    
    # DB ga suhafayq
    user = update.effective_user
    await save_user(
        user.id,
        user.username,
        context.user_data['first_name'],
        context.user_data['phone'],
        context.user_data['email']
    )
    
    await update.message.reply_text(
        f"✅ Rahmat {context.user_data['first_name']}!\n\n"
        f"Sizning ma'lumotlar saqlandi:\n"
        f"📱 Telefon: {context.user_data['phone']}\n"
        f"✉️ Email: {context.user_data['email']}\n\n"
        "Xayr! /start deb qaytib kelib yangilashingiz mumkin."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chikish"""
    await update.message.reply_text("Xayr! /start deb qaytib kelib boshlashingiz mumkin.")
    return ConversationHandler.END

# ============ AI Chat Handlers ============
async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI chat boshlash"""
    await update.message.reply_text(
        "🤖 AI chat rejimi boshlandi!\n\n"
        "Menga savollar bering, men javob beraman.\n"
        "Chiqish uchun /cancel yozing."
    )
    return CHATTING_WITH_AI

async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI ga xabar yuborish va javob olish"""
    user_message = update.message.text
    
    # Typing ko'rsatish
    await update.message.chat.send_action("typing")
    
    try:
        # AI dan javob olish
        ai_response = await generate_response(user_message)
        await update.message.reply_text(f"🤖 {ai_response}")
    except Exception as e:
        logger.error(f"AI xatolik: {e}")
        await update.message.reply_text("❌ Kechirasiz, AI bilan muammo bor. Keyinroq urinib ko'ring.")
    
    return CHATTING_WITH_AI

async def end_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI chat tugatish"""
    await update.message.reply_text("AI chat tugadi. /chat deb qaytib boshlashingiz mumkin.")
    return ConversationHandler.END

# ============ Bot Ishga Tushirish ============
async def main():
    """Bot ishga tushirish"""
    global db_pool
    
    # Database initialize
    logger.info("Database initialize qilmoqda...")
    await init_db()
    logger.info("✅ Database tayyor!")
    
    # Bot application yaratish
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASKING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASKING_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_and_finish)],
            CHATTING_WITH_AI: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_message)],
        },
        fallbacks=[CommandHandler('cancel', end_chat)],
    )
    
    # AI chat handler
    chat_handler = ConversationHandler(
        entry_points=[CommandHandler('chat', start_chat)],
        states={
            CHATTING_WITH_AI: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_message)],
        },
        fallbacks=[CommandHandler('cancel', end_chat)],
    )
    
    app.add_handler(conv_handler)
    app.add_handler(chat_handler)
    
    # Bot ishga tushirish
    logger.info("🤖 Bot ishga tushirilmoqda...")
    async with app:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        # Bot ishda, Ctrl+C bosing chikishga
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Bot to'xtadi.")
        finally:
            if db_pool:
                await db_pool.close()
            await app.updater.stop()
            await app.stop()
            await app.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
