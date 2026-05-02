from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import text, bold

from .db import save_user_and_order
from . import ai as ai_module

class OrderForm(StatesGroup):
    phone = State()
    email = State()
    address = State()
    product = State()
    quantity = State()
    delivery_address = State()


def register_handlers(dp, pool):

    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        # greet and ask for phone (request contact)
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Send phone', request_contact=True))
        await message.answer("Salom! Buyurtma berish uchun telefoningizni yuboring.", reply_markup=kb)
        await OrderForm.phone.set()

    @dp.message_handler(content_types=types.ContentType.CONTACT, state=OrderForm.phone)
    @dp.message_handler(state=OrderForm.phone)
    async def process_phone(message: types.Message, state: FSMContext):
        if message.contact:
            phone = message.contact.phone_number
        else:
            phone = message.text.strip()
        await state.update_data(phone=phone)
        await message.reply("Emailingizni kiriting:", reply_markup=ReplyKeyboardRemove())
        await OrderForm.email.set()

    @dp.message_handler(state=OrderForm.email)
    async def process_email(message: types.Message, state: FSMContext):
        email = message.text.strip()
        await state.update_data(email=email)
        await message.reply("Qayerda yashaysiz? (manzil)")
        await OrderForm.address.set()

    @dp.message_handler(state=OrderForm.address)
    async def process_address(message: types.Message, state: FSMContext):
        address = message.text.strip()
        await state.update_data(address=address)
        await message.reply("Buyurtma qilmoqchi bo'lgan mahsulot nomini yozing:")
        await OrderForm.product.set()

    @dp.message_handler(state=OrderForm.product)
    async def process_product(message: types.Message, state: FSMContext):
        product = message.text.strip()
        await state.update_data(product=product)
        await message.reply("Miqdorini kiriting (raqam):")
        await OrderForm.quantity.set()

    @dp.message_handler(state=OrderForm.quantity)
    async def process_quantity(message: types.Message, state: FSMContext):
        qty_text = message.text.strip()
        try:
            qty = int(qty_text)
        except ValueError:
            await message.reply("Iltimos, butun son kiriting.")
            return
        await state.update_data(quantity=qty)
        await message.reply("Yetkazib berish manzilini kiriting (agar boshqacha bo'lsa, aks holda ENTER):")
        await OrderForm.delivery_address.set()

    @dp.message_handler(state=OrderForm.delivery_address)
    async def process_delivery(message: types.Message, state: FSMContext):
        delivery_address = message.text.strip()
        data = await state.get_data()

        # prepare user dict from telegram info
        telegram_user = {
            'telegram_id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'phone': data.get('phone'),
            'email': data.get('email'),
            'address': data.get('address')
        }
        order = {
            'product': data.get('product'),
            'quantity': data.get('quantity'),
            'delivery_address': delivery_address if delivery_address else data.get('address')
        }

        # save to DB
        try:
            order_id = await save_user_and_order(telegram_user, order)
        except Exception as e:
            await message.reply(f"Xatolik yuz berdi: {e}")
            await state.finish()
            return

        await message.reply(text(bold('Rahmat!'), f"Buyurtma #{order_id} qabul qilindi."))
        await state.finish()

    @dp.message_handler(commands=['ai'])
    async def cmd_ai(message: types.Message):
        # usage: /ai <prompt>
        args = message.get_args() if hasattr(message, 'get_args') else None
        prompt = None
        if args:
            prompt = args.strip()
        else:
            # fallback to splitting the text
            parts = message.text.split(' ', 1)
            if len(parts) > 1:
                prompt = parts[1].strip()

        if not prompt:
            await message.reply("/ai so'rovini quyidagicha ishlating: /ai Qanday yordam kerak?")
            return

        await message.reply("AI ga yuborilmoqda...")
        try:
            resp = await ai_module.generate_response(prompt)
        except Exception as e:
            await message.reply(f"AI xatolik: {e}")
            return
        await message.reply(resp)

    # simple info command
    @dp.message_handler(commands=['help'])
    async def cmd_help(message: types.Message):
        await message.reply("/start — yangi buyurtma\\n/help — yordam\\n/ai <savol> — Gemini bilan suhbat")

