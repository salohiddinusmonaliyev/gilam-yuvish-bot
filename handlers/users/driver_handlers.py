from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import DRIVER, ADMINS
from keyboards.default.keyboards import driver_main_menu, yes_no, main_menu, admin_main_menu
from loader import dp, bot, db
from states.main_states import Delivered


@dp.message_handler(text="✅ Buyurtma yetkazib berildi")
async def delivered(message: types.Message):
    await message.answer("Buyurtma raqamini kiriting.")
    await Delivered.id.set()

@dp.message_handler(state=Delivered.id)
async def set_delivered(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            await message.answer(f"Siz kiritdingiz: {message.text}", reply_markup=driver_main_menu)
            order_record = await db.get_order(id=int(message.text))
            global order_id
            order_id = order_record['id']  # Extract the id from the record
            service_id = int(order_record['service_id'])
            service = await db.get_service(service_id)
            user = await db.select_user(id=int(order_record['user_id']))
            global supplier
            supplier = await db.select_user(telegram_id=int(message.from_user.id))
            await message.answer(f"Id: {order_record['id']} \n"
                    f"Manzil: {order_record['address']} \n"
                    f"Buyurtma holati: Topshirildi\n"
                    f"Xizmat turi: {service[0]['name']}\n"
                    f"Buyurtmachi telefon raqami: {order_record['phone_number']}\n"
                                 "\n<b>Buyurtma yetkazib berildi!\n \nMijozga ma'lumot yuborildi.</b>")
            await bot.send_message(int(user['telegram_id']), f"{order_record['id']} raqamli buyurtmangiz yetkazib berildimi?", reply_markup=yes_no)
            await state.finish()
        elif message.text == "🔙 Ortga":
            await state.finish()
            await message.answer("Ortga qaytildi.", reply_markup=driver_main_menu)
    except:
        await message.answer("Bu raqamga tegishli buyurtma yo'q\nTekshirib qaytadan kiriting: ")

@dp.message_handler(text="Ha, yetkazib berildi")
async def yes(message: types.Message):
    await message.answer("Buyurtmangiz uchun rahmat!", reply_markup=main_menu)
    global order_id
    global supplier
    await db.delivered(order_id, supplier['id'])




@dp.message_handler(text="Yo'q, kelmadi")
async def no(message: types.Message):
    await message.answer("Sizning muammoyingiz tez orada hal qilinadi.", reply_markup=main_menu)
    await bot.send_message(chat_id=ADMINS[0], text=f"{order_id} raqamli buyurtma manzilga yetib bormadi lekin yetkazib beruvchi yetkazib berildi deb ma'lumot kiritdi.", reply_markup=admin_main_menu)